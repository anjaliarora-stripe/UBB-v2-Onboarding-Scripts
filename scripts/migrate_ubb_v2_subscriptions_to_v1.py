#!/usr/bin/env python3
"""
UBB V2 → V1 migration: pricing plan subscriptions → classic Subscriptions.

Reads STRIPE_SECRET_KEY_SANDBOX from the environment (.env). Uses Stripe-Version
2026-03-25.preview for V2 billing HTTP calls.

Discovery: for each pricing plan ID in the bpp→price map, lists
GET /v2/billing/pricing_plan_subscriptions?pricing_plan=... (paginated with ``page``).
``payer`` and ``pricing_plan`` filters are mutually exclusive on that endpoint.

Dry-run (default): performs GET/list calls and logs each step; does **not** create
v1 subscriptions, billing intents, cadence cancel, or credit grant expires.

Live run: pass ``--execute`` to perform mutations. Use ``--customer cus_...`` to
process only that customer (client-side filter after list).

Reference curl shapes (Julius migration) are documented in the repo plan
``.cursor/plans/v2_to_v1_migration_script_720317a8.plan.md`` — key calls:
list by ``pricing_plan``, credit_balance_summary, meter event_summaries,
subscriptions.create with ``billing_cycle_anchor_config``, billing intent
deactivate with ``collect_at: next_billing_date``, POST cadences/{id}/cancel,
credit_grants expire.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Iterator

import stripe
from dotenv import load_dotenv
from stripe import StripeClient

STRIPE_PREVIEW_VERSION = "2026-03-25.preview"

# Default bpp_test → price_ map (override with --map-json).
DEFAULT_PRICING_PLAN_TO_PRICE: dict[str, str] = {
    "bpp_test_61UYWAYT44e1WMi9J16UYVtU9jSQKkalVhfJ3aEEaC9Y": "price_1TP8o9GKcSbvc1hc91iNWp8a",
    "bpp_test_61UYWZ50LO6c2eNQw16UYVtU9jSQKkalVhfJ3aEEaMaO": "price_1TP8pbGKcSbvc1hcZSX2Qgv9",
    "bpp_test_61UYWJLRB3d8RSS9j16UYVtU9jSQKkalVhfJ3aEEa9t2": "price_1TP8rSGKcSbvc1hcBlWGj7on",
    "bpp_test_61UYWfrCT7L7aqFvz16UYVtU9jSQKkalVhfJ3aEEaRA8": "price_1TP8rSGKcSbvc1hc3zPKroWZ",
    "bpp_test_61UYWOsMfd6iwTMXv16UYVtU9jSQKkalVhfJ3aEEaN8y": "price_1TP8rSGKcSbvc1hcJWtR84xj",
    "bpp_test_61UYWe55Md9RuX0iV16UYVtU9jSQKkalVhfJ3aEEaGRc": "price_1TP8rSGKcSbvc1hcTvgWbx1P",
    "bpp_test_61UYWTpTFF04ciYtk16UYVtU9jSQKkalVhfJ3aEEa2Vs": "price_1TP8sBGKcSbvc1hcWRLXTySf",
    "bpp_test_61UYWiNl0nAgxOj8J16UYVtU9jSQKkalVhfJ3aEEaLcO": "price_1TP8sBGKcSbvc1hcwlBmLxMq",
}

STRIPE_METADATA_VALUE_MAX = 500


def _log(msg: str, *, verbose: bool = True) -> None:
    if verbose:
        print(msg, flush=True)


def _get_nested(obj: Any, *keys: str, default: Any = None) -> Any:
    cur = obj
    for k in keys:
        if cur is None:
            return default
        if isinstance(cur, dict):
            cur = cur.get(k)
        else:
            cur = getattr(cur, k, None)
    return cur if cur is not None else default


def _servicing_status_str(sub: dict[str, Any]) -> str | None:
    ss = sub.get("servicing_status")
    if isinstance(ss, dict):
        return ss.get("status")
    return ss if isinstance(ss, str) else None


def _ref_id(ref: Any) -> str | None:
    if ref is None:
        return None
    if isinstance(ref, dict):
        return ref.get("id")
    if isinstance(ref, str):
        return ref
    return getattr(ref, "id", None)


def align_to_minute_boundary(ts: int) -> int:
    return ts - (ts % 60)


def cadence_to_billing_cycle_anchor_config(cadence: dict[str, Any]) -> dict[str, Any] | None:
    """Map v2 cadence.billing_cycle to SubscriptionCreate billing_cycle_anchor_config."""
    bc = cadence.get("billing_cycle") or {}
    btype = bc.get("type")
    if btype == "month":
        m = bc.get("month") or {}
        tm = m.get("time") or {}
        return {
            "day_of_month": int(m.get("day_of_month") or 1),
            "hour": int(tm.get("hour") or 0),
            "minute": int(tm.get("minute") or 0),
            "second": int(tm.get("second") or 0),
        }
    if btype == "year":
        y = bc.get("year") or {}
        tm = y.get("time") or {}
        cfg: dict[str, Any] = {
            "day_of_month": int(y.get("day_of_month") or 1),
            "hour": int(tm.get("hour") or 0),
            "minute": int(tm.get("minute") or 0),
            "second": int(tm.get("second") or 0),
        }
        moy = y.get("month_of_year")
        if moy is not None:
            cfg["month"] = int(moy)
        return cfg
    return None


def next_billing_timestamp(cadence: dict[str, Any]) -> int | None:
    """Parse cadence.next_billing_date if present (unix or ISO)."""
    nb = cadence.get("next_billing_date")
    if nb is None:
        return None
    if isinstance(nb, (int, float)):
        return int(nb)
    if isinstance(nb, str):
        s = nb.strip()
        if s.isdigit():
            return int(s)
        # ISO8601
        from datetime import datetime

        try:
            if s.endswith("Z"):
                s2 = s[:-1] + "+00:00"
            else:
                s2 = s
            dt = datetime.fromisoformat(s2)
            if dt.tzinfo is None:
                from datetime import timezone

                dt = dt.replace(tzinfo=timezone.utc)
            return int(dt.timestamp())
        except ValueError:
            return None
    return None


def truncate_metadata_value(s: str, max_len: int = STRIPE_METADATA_VALUE_MAX) -> str:
    if len(s) <= max_len:
        return s
    return s[: max_len - 3] + "..."


def collect_meter_ids_from_plan(client: StripeClient, pricing_plan_id: str) -> list[str]:
    """Resolve v1 billing meter IDs (mtr_*) from plan rate cards."""
    resp = client.raw_request(
        "get", f"/v2/billing/pricing_plans/{pricing_plan_id}/components"
    )
    body = client.deserialize(resp, api_mode="V2")
    meter_ids: list[str] = []
    seen: set[str] = set()
    for comp in body.get("data") or []:
        if comp.get("type") != "rate_card":
            continue
        rc_ref = comp.get("rate_card") or {}
        rc_id = _ref_id(rc_ref)
        if not rc_id:
            continue
        rates_resp = client.raw_request("get", f"/v2/billing/rate_cards/{rc_id}/rates")
        rates_body = client.deserialize(rates_resp, api_mode="V2")
        for rate in rates_body.get("data") or []:
            mi_ref = rate.get("metered_item")
            mi_id = _ref_id(mi_ref)
            if not mi_id:
                continue
            mi_resp = client.raw_request("get", f"/v2/billing/metered_items/{mi_id}")
            mi = client.deserialize(mi_resp, api_mode="V2")
            meter = _ref_id(mi.get("meter"))
            if meter and meter not in seen:
                seen.add(meter)
                meter_ids.append(meter)
    return meter_ids


def credit_balance_available_minor(summary: Any) -> int | None:
    """Return available monetary minor units from credit_balance_summary, best-effort."""
    balances = getattr(summary, "balances", None) if summary is not None else None
    if balances is None and isinstance(summary, dict):
        balances = summary.get("balances")
    if not balances:
        return None
    b0 = balances[0]
    ab = getattr(b0, "available_balance", None) or (
        b0.get("available_balance") if isinstance(b0, dict) else None
    )
    mon_a = getattr(ab, "monetary", None) if ab is not None else None
    if isinstance(ab, dict):
        mon_a = ab.get("monetary") or ab
    if isinstance(mon_a, dict) and "value" in mon_a:
        return int(mon_a["value"])
    if mon_a is not None and getattr(mon_a, "value", None) is not None:
        return int(mon_a.value)
    return None


def meter_usage_total(
    meter_id: str,
    customer_id: str,
    start_time: int,
    end_time: int,
) -> float:
    total = 0.0
    page = stripe.billing.Meter.list_event_summaries(
        meter_id,
        customer=customer_id,
        start_time=start_time,
        end_time=end_time,
    )
    for row in page.data or []:
        v = getattr(row, "aggregated_value", None)
        if v is None and isinstance(row, dict):
            v = row.get("aggregated_value")
        if v is not None:
            total += float(v)
    return total


def list_pricing_plan_subscriptions_for_plan(
    client: StripeClient,
    *,
    pricing_plan_id: str,
    servicing_status: str | None,
    limit: int,
    include_component_details: bool,
) -> Iterator[dict[str, Any]]:
    page_cursor: str | None = None
    seen_cursors: set[str] = set()
    while True:
        params: dict[str, Any] = {
            "pricing_plan": pricing_plan_id,
            "limit": limit,
        }
        if servicing_status:
            params["servicing_status"] = servicing_status
        if page_cursor:
            params["page"] = page_cursor
        if include_component_details:
            params["include"] = ["pricing_plan_component_details"]
        resp = client.raw_request(
            "get",
            "/v2/billing/pricing_plan_subscriptions",
            **params,
        )
        body = client.deserialize(resp, api_mode="V2")
        for item in body.get("data") or []:
            if isinstance(item, dict):
                yield item
            else:
                yield dict(item)
        next_cursor = body.get("next_page") or body.get("page")
        if not next_cursor or (isinstance(next_cursor, str) and next_cursor in seen_cursors):
            break
        if isinstance(next_cursor, str):
            seen_cursors.add(next_cursor)
        page_cursor = next_cursor if isinstance(next_cursor, str) else str(next_cursor)


def build_deactivate_intent_body(
    *,
    currency: str,
    pricing_plan_subscription_id: str,
) -> dict[str, Any]:
    return {
        "currency": currency,
        "actions": [
            {
                "type": "deactivate",
                "deactivate": {
                    "type": "pricing_plan_subscription_details",
                    "collect_at": "next_billing_date",
                    "pricing_plan_subscription_details": {
                        "pricing_plan_subscription": pricing_plan_subscription_id,
                        "overrides": {
                            "partial_period_behaviors": [
                                {
                                    "type": "license_fee",
                                    "license_fee": {
                                        "credit_proration_behavior": "none",
                                    },
                                }
                            ]
                        },
                    },
                },
            }
        ],
    }


def migrate_one_subscription(
    client: StripeClient,
    *,
    bpp_id: str,
    v1_price_id: str,
    pp_sub: dict[str, Any],
    usage_start: int,
    usage_end: int,
    execute: bool,
    skip_if_metadata: bool,
    servicing_status_filter: str | None,
    verbose: bool,
) -> bool:
    sub_id = pp_sub.get("id")
    if not sub_id:
        _log("  skip: missing subscription id", verbose=verbose)
        return False

    ss = _servicing_status_str(pp_sub)
    if servicing_status_filter and ss != servicing_status_filter:
        _log(f"  skip {sub_id}: servicing_status={ss!r} != filter", verbose=verbose)
        return False
    if ss == "canceled":
        _log(f"  skip {sub_id}: already canceled", verbose=verbose)
        return False

    _log(f"\n{'='*80}\nPricing plan subscription: {sub_id}\nPlan: {bpp_id} → price {v1_price_id}\n{'='*80}", verbose=verbose)

    # --- Retrieve cadence ---
    cadence_ref = pp_sub.get("billing_cadence") or pp_sub.get("cadence")
    cadence_id = _ref_id(cadence_ref)
    if not cadence_id:
        _log("  ❌ No billing cadence on subscription", verbose=verbose)
        return False
    _log(f"[1] GET cadence {cadence_id}", verbose=verbose)
    cadence = client.deserialize(
        client.raw_request("get", f"/v2/billing/cadences/{cadence_id}"),
        api_mode="V2",
    )
    customer_id = _ref_id(_get_nested(cadence, "payer", "customer"))
    billing_profile_id = _ref_id(_get_nested(cadence, "payer", "billing_profile"))
    if not customer_id:
        _log("  ❌ Could not resolve customer from cadence", verbose=verbose)
        return False

    # --- Billing profile → default payment method ---
    default_pm: str | None = None
    if billing_profile_id:
        _log(f"[2] GET billing profile {billing_profile_id}", verbose=verbose)
        profile = client.deserialize(
            client.raw_request("get", f"/v2/billing/profiles/{billing_profile_id}"),
            api_mode="V2",
        )
        default_pm = profile.get("default_payment_method") or profile.get(
            "default_payment_method_id"
        )
        if isinstance(default_pm, dict):
            default_pm = default_pm.get("id")
    if not default_pm:
        _log("  ⚠ No default_payment_method on billing profile; subscription create may fail", verbose=verbose)

    # --- Plan currency ---
    _log(f"[3] GET pricing plan {bpp_id}", verbose=verbose)
    plan_obj = client.deserialize(
        client.raw_request("get", f"/v2/billing/pricing_plans/{bpp_id}"),
        api_mode="V2",
    )
    currency = (plan_obj.get("currency") or "usd").lower()

    # --- Credit balance summary ---
    _log(f"[4] GET credit_balance_summary customer={customer_id}", verbose=verbose)
    avail_cents: int | None = None
    try:
        cbs = stripe.billing.CreditBalanceSummary.retrieve(
            customer=customer_id,
            filter={
                "type": "applicability_scope",
                "applicability_scope": {"price_type": "metered"},
            },
        )
        avail_cents = credit_balance_available_minor(cbs)
        _log(f"    available_credit_balance={avail_cents!r}", verbose=verbose)
    except Exception as e:
        _log(f"    ⚠ credit_balance_summary: {e}", verbose=verbose)

    # --- Meter usage ---
    _log(f"[5] Resolve meters + event_summaries [{usage_start}..{usage_end}]", verbose=verbose)
    meter_ids = collect_meter_ids_from_plan(client, bpp_id)
    usage_total = 0.0
    for mtr in meter_ids:
        try:
            part = meter_usage_total(mtr, customer_id, usage_start, usage_end)
            usage_total += part
            _log(f"    meter {mtr}: aggregated {part}", verbose=verbose)
        except Exception as e:
            _log(f"    ⚠ meter {mtr}: {e}", verbose=verbose)

    anchor_cfg = cadence_to_billing_cycle_anchor_config(cadence)
    if anchor_cfg is None:
        nb_ts = next_billing_timestamp(cadence)
        _log(
            f"  ⚠ Unsupported cadence billing_cycle.type for anchor_config; "
            f"next_billing_date ts={nb_ts!r} — set billing_cycle_anchor manually if needed",
            verbose=verbose,
        )

    meta_ubb = sub_id
    meta_avail = str(avail_cents if avail_cents is not None else "")
    meta_meter = str(int(usage_total)) if usage_total == int(usage_total) else str(usage_total)
    meta_meter = truncate_metadata_value(meta_meter)

    _log("[6] Would create v1 subscription (dry-run)" if not execute else "[6] POST /v1/subscriptions", verbose=verbose)
    create_kwargs: dict[str, Any] = {
        "customer": customer_id,
        "items": [{"price": v1_price_id, "quantity": 1}],
        "proration_behavior": "none",
        "metadata": {
            "ubb_subscription_id": truncate_metadata_value(meta_ubb),
            "available_credit_balance": truncate_metadata_value(meta_avail),
            "meter_usage": meta_meter,
        },
    }
    if default_pm:
        create_kwargs["default_payment_method"] = default_pm
    if anchor_cfg:
        create_kwargs["billing_cycle_anchor_config"] = anchor_cfg
    else:
        nb_ts = next_billing_timestamp(cadence)
        if nb_ts:
            create_kwargs["billing_cycle_anchor"] = nb_ts

    v1_sub_id: str | None = None
    if execute:
        if skip_if_metadata:
            existing = stripe.Subscription.list(
                customer=customer_id, status="all", limit=20
            )
            for s in existing.data or []:
                md = getattr(s, "metadata", None) or {}
                if md.get("ubb_subscription_id") == sub_id:
                    _log(f"  skip (--skip-if-metadata): found sub {s.id}", verbose=verbose)
                    return True
        sub = stripe.Subscription.create(**create_kwargs)
        v1_sub_id = sub.id
        _log(f"    ✓ Created subscription {v1_sub_id}", verbose=verbose)
    else:
        _log(f"    payload: {json.dumps(create_kwargs, default=str)[:2000]}", verbose=verbose)

    # --- Deactivate v2 subscription ---
    _log(
        "[7] Would POST billing intent deactivate (dry-run)"
        if not execute
        else "[7] POST /v2/billing/intents deactivate + reserve + commit",
        verbose=verbose,
    )
    if execute:
        body = build_deactivate_intent_body(
            currency=currency,
            pricing_plan_subscription_id=sub_id,
        )
        intent_resp = client.raw_request("post", "/v2/billing/intents", **body)
        intent = client.deserialize(intent_resp, api_mode="V2")
        intent_id = intent.get("id")
        client.raw_request("post", f"/v2/billing/intents/{intent_id}/reserve")
        client.raw_request("post", f"/v2/billing/intents/{intent_id}/commit")
        _log(f"    ✓ Billing intent {intent_id} committed", verbose=verbose)

    # --- Cancel cadence ---
    _log(
        "[8] Would POST cadence cancel (dry-run)"
        if not execute
        else f"[8] POST /v2/billing/cadences/{cadence_id}/cancel",
        verbose=verbose,
    )
    if execute:
        try:
            client.raw_request("post", f"/v2/billing/cadences/{cadence_id}/cancel")
            _log("    ✓ Cadence canceled", verbose=verbose)
        except Exception as e:
            _log(
                f"    ⚠ Cadence cancel skipped or failed (often expected when deactivate "
                f"uses collect_at=next_billing_date — cadence still has an active/unbilled sub "
                f"until that date): {e}",
                verbose=verbose,
            )

    # --- Expire credit grants ---
    _log(
        "[9] Would expire credit grants (dry-run)"
        if not execute
        else "[9] Expire credit grants",
        verbose=verbose,
    )
    if execute:
        grants = stripe.billing.CreditGrant.list(customer=customer_id, limit=100)
        for g in grants.data or []:
            gid = getattr(g, "id", None)
            if not gid:
                continue
            try:
                stripe.billing.CreditGrant.expire(gid)
                _log(f"    expired {gid}", verbose=verbose)
            except Exception as e:
                _log(f"    ⚠ expire {gid}: {e}", verbose=verbose)

    _log(f"Done {sub_id} → v1 {v1_sub_id or '(not created — dry-run)'}", verbose=verbose)
    return True


def load_map(path: str | None) -> dict[str, str]:
    if not path:
        return dict(DEFAULT_PRICING_PLAN_TO_PRICE)
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, dict):
        sys.exit("--map-json must contain a JSON object of bpp_id → price_id")
    out: dict[str, str] = {}
    for k, v in raw.items():
        out[str(k)] = str(v)
    return out


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Perform writes (default: dry-run — log only, still runs read APIs)",
    )
    parser.add_argument(
        "--map-json",
        metavar="PATH",
        help="JSON object: pricing_plan_id → v1 price_id (default: built-in map)",
    )
    parser.add_argument(
        "--customer",
        metavar="CUS_ID",
        help="Process only this customer id (after list results)",
    )
    parser.add_argument(
        "--usage-start",
        type=int,
        metavar="UNIX",
        help="Meter event_summaries start_time (default: 2026-03-31 23:59:59 UTC)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Page size for listing pricing plan subscriptions (default 100)",
    )
    parser.add_argument(
        "--servicing-status",
        default="active",
        metavar="ENUM",
        help="List filter servicing_status (default: active). Use empty string to omit.",
    )
    parser.add_argument(
        "--no-include-components",
        action="store_true",
        help="Do not pass include[]=pricing_plan_component_details on list",
    )
    parser.add_argument(
        "--skip-if-metadata",
        action="store_true",
        help="Skip migrate if customer already has a v1 sub with metadata ubb_subscription_id",
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Less logging")
    args = parser.parse_args()
    verbose = not args.quiet

    api_key = os.getenv("STRIPE_SECRET_KEY_SANDBOX")
    if not api_key:
        sys.exit("STRIPE_SECRET_KEY_SANDBOX is not set (.env or environment)")

    execute = bool(args.execute)
    if not execute:
        _log(
            "\n*** DRY-RUN (no writes). Pass --execute to create v1 subs and wind down v2. ***\n",
            verbose=verbose,
        )

    default_start = int(
        datetime(2026, 3, 31, 23, 59, 59, tzinfo=timezone.utc).timestamp()
    )
    usage_start = align_to_minute_boundary(
        int(args.usage_start) if args.usage_start is not None else default_start
    )
    usage_end = align_to_minute_boundary(int(time.time()))

    plan_map = load_map(args.map_json)
    client = StripeClient(api_key=api_key, stripe_version=STRIPE_PREVIEW_VERSION)
    stripe.api_key = api_key
    stripe.api_version = STRIPE_PREVIEW_VERSION

    servicing = args.servicing_status.strip() or None

    for bpp_id, price_id in plan_map.items():
        _log(f"\n### Plan {bpp_id} → {price_id}", verbose=verbose)
        try:
            iterator = list_pricing_plan_subscriptions_for_plan(
                client,
                pricing_plan_id=bpp_id,
                servicing_status=servicing,
                limit=max(1, min(args.limit, 100)),
                include_component_details=not args.no_include_components,
            )
        except Exception as e:
            _log(f"  ⚠ list failed for {bpp_id}: {e}", verbose=verbose)
            if not servicing:
                continue
            _log("  retrying list without servicing_status filter…", verbose=verbose)
            try:
                iterator = list_pricing_plan_subscriptions_for_plan(
                    client,
                    pricing_plan_id=bpp_id,
                    servicing_status=None,
                    limit=max(1, min(args.limit, 100)),
                    include_component_details=not args.no_include_components,
                )
            except Exception as e2:
                _log(f"  ❌ retry failed: {e2}", verbose=verbose)
                continue

        for pp_sub in iterator:
            cadence_ref = pp_sub.get("billing_cadence") or pp_sub.get("cadence")
            cadence_id = _ref_id(cadence_ref)
            if not cadence_id:
                continue
            try:
                cadence = client.deserialize(
                    client.raw_request("get", f"/v2/billing/cadences/{cadence_id}"),
                    api_mode="V2",
                )
            except Exception:
                continue
            cust = _ref_id(_get_nested(cadence, "payer", "customer"))
            if args.customer and cust != args.customer:
                continue
            migrate_one_subscription(
                client,
                bpp_id=bpp_id,
                v1_price_id=price_id,
                pp_sub=pp_sub,
                usage_start=usage_start,
                usage_end=usage_end,
                execute=execute,
                skip_if_metadata=args.skip_if_metadata,
                servicing_status_filter=servicing,
                verbose=verbose,
            )


if __name__ == "__main__":
    main()
