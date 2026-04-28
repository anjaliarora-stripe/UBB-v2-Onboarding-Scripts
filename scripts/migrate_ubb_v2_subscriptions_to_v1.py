#!/usr/bin/env python3
"""
Migrate UBB v2 pricing plan subscriptions to v1 Subscriptions.

Requires STRIPE_SECRET_KEY_SANDBOX. Default is dry-run; add --execute to write.
Skips canceled subs and subs with servicing_status_transitions.will_cancel_at set.

Optional --cancel-map-json lists additional v2 pricing plan ids (bpp_*). After a
successful migrate (finalize_v2_teardown on the source plan), for each customer
we run billing-intent deactivate + cadence cancel on their active subscriptions
to those plans (no second credit-grant sweep).

Optional --customer and/or --customers-json restrict processing to those Stripe
customer ids (union). See --help for flags.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Iterator
from urllib.parse import parse_qs, urlparse

import stripe
from dotenv import load_dotenv
from stripe import StripeClient

STRIPE_PREVIEW_VERSION = "2026-03-25.preview"
LIST_PAGE_SIZE = 100
# Only migrate when cadence next_billing_date is in (now, now + this]; others are skipped.
NEXT_BILLING_WITHIN_SEC = 7 * 86400
# Meter usage window start (UTC)
USAGE_START = int(datetime(2026, 3, 31, 23, 59, 59, tzinfo=timezone.utc).timestamp())

# Optional default cancel-only plan ids (bpp_*); usually pass --cancel-map-json instead.
DEFAULT_CANCEL_ONLY_PLAN_IDS: frozenset[str] = frozenset(
    {
        "bpp_61UHSINKo8hiFtTQI16PFftvK2SQcbvDYYWHjkNkG6Qi",
    }
)

DEFAULT_PRICING_PLAN_TO_PRICE: dict[str, str] = {
    "bpp_61UHSLI1OVlebhmxU16PFftvK2SQcbvDYYWHjkNkGL1E": "price_1OelH9CLWA6kvkpErdG01ENb",
    "bpp_61UHSDpWjlhtrNS5k16PFftvK2SQcbvDYYWHjkNkGFqy": "price_1OelKECLWA6kvkpEJMU34MzC",
    "bpp_61ULsGyqodIYGnMY516PFftvK2SQcbvDYYWHjkNkGEPw": "price_1OelMhCLWA6kvkpEqt7yTpJx",
    "bpp_61ULsJ2ICr8tyX0LT16PFftvK2SQcbvDYYWHjkNkGQDg": "price_1OelNVCLWA6kvkpECQArVJkR",
    "bpp_61UHSNcxCHxoyGmgd16PFftvK2SQcbvDYYWHjkNkGVMG": "price_1TP6qSCLWA6kvkpEsvYKeooz",
    "bpp_61UHSAI4WduIoxK5k16PFftvK2SQcbvDYYWHjkNkGVou": "price_1TP6rlCLWA6kvkpE2fxLnQU2",
    "bpp_61UHSPFs97T8xa8PY16PFftvK2SQcbvDYYWHjkNkGPXU": "price_1SGTuaCLWA6kvkpE980JLqhq",
    "bpp_61UHRoy4oYtvt7fRm16PFftvK2SQcbvDYYWHjkNkGVqi": "price_1SGTuiCLWA6kvkpEmweD1H6N",
}

META_MAX = 500


def _progress_prefix(progress: tuple[int, int] | None) -> str:
    if progress is None:
        return ""
    i, n = progress
    return f"[{i}/{n}] "


def _get(obj: Any, *keys: str, default: Any = None) -> Any:
    for k in keys:
        if obj is None:
            return default
        obj = obj.get(k) if isinstance(obj, dict) else getattr(obj, k, None)
    return default if obj is None else obj


def _ref_id(ref: Any) -> str | None:
    if ref is None:
        return None
    if isinstance(ref, dict):
        return ref.get("id")
    if isinstance(ref, str):
        return ref
    return getattr(ref, "id", None)


def _servicing_status(sub: dict[str, Any]) -> str | None:
    ss = sub.get("servicing_status")
    if isinstance(ss, dict):
        return ss.get("status")
    return ss if isinstance(ss, str) else None


def _will_cancel_at(sub: dict[str, Any]) -> str | None:
    """ISO timestamp when servicing is scheduled to cancel, or None."""
    t = sub.get("servicing_status_transitions")
    if not t:
        return None
    if isinstance(t, dict):
        v = t.get("will_cancel_at")
    else:
        v = getattr(t, "will_cancel_at", None)
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def align_minute(ts: int) -> int:
    return ts - (ts % 60)


def cadence_to_anchor_config(cadence: dict[str, Any]) -> dict[str, Any] | None:
    bc = cadence.get("billing_cycle") or {}
    t = bc.get("type")
    if t == "month":
        m = bc.get("month") or {}
        tm = m.get("time") or {}
        return {
            "day_of_month": int(m.get("day_of_month") or 1),
            "hour": int(tm.get("hour") or 0),
            "minute": int(tm.get("minute") or 0),
            "second": int(tm.get("second") or 0),
        }
    if t == "year":
        y = bc.get("year") or {}
        tm = y.get("time") or {}
        cfg: dict[str, Any] = {
            "day_of_month": int(y.get("day_of_month") or 1),
            "hour": int(tm.get("hour") or 0),
            "minute": int(tm.get("minute") or 0),
            "second": int(tm.get("second") or 0),
        }
        if y.get("month_of_year") is not None:
            cfg["month"] = int(y["month_of_year"])
        return cfg
    return None


def next_billing_ts(cadence: dict[str, Any]) -> int | None:
    nb = cadence.get("next_billing_date")
    if nb is None:
        return None
    if isinstance(nb, (int, float)):
        return int(nb)
    if isinstance(nb, str):
        s = nb.strip()
        if s.isdigit():
            return int(s)
        try:
            s2 = s[:-1] + "+00:00" if s.endswith("Z") else s
            dt = datetime.fromisoformat(s2)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return int(dt.timestamp())
        except ValueError:
            return None
    return None


def fmt_next_billing(nb: int | None) -> str:
    if nb is None:
        return "(unparsed)"
    return datetime.fromtimestamp(nb, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def trunc(s: str, n: int = META_MAX) -> str:
    return s if len(s) <= n else s[: n - 3] + "..."


def meter_ids_for_plan(client: StripeClient, pricing_plan_id: str) -> list[str]:
    body = client.deserialize(
        client.raw_request("get", f"/v2/billing/pricing_plans/{pricing_plan_id}/components"),
        api_mode="V2",
    )
    out: list[str] = []
    seen: set[str] = set()
    for comp in body.get("data") or []:
        if comp.get("type") != "rate_card":
            continue
        rc_id = _ref_id(comp.get("rate_card"))
        if not rc_id:
            continue
        rates = client.deserialize(
            client.raw_request("get", f"/v2/billing/rate_cards/{rc_id}/rates"),
            api_mode="V2",
        )
        for rate in rates.get("data") or []:
            mi_id = _ref_id(rate.get("metered_item"))
            if not mi_id:
                continue
            mi = client.deserialize(
                client.raw_request("get", f"/v2/billing/metered_items/{mi_id}"),
                api_mode="V2",
            )
            mid = _ref_id(mi.get("meter"))
            if mid and mid not in seen:
                seen.add(mid)
                out.append(mid)
    return out


def credit_available_minor(summary: Any) -> int | None:
    bal = getattr(summary, "balances", None) or (
        summary.get("balances") if isinstance(summary, dict) else None
    )
    if not bal:
        return None
    b0 = bal[0]
    ab = getattr(b0, "available_balance", None) or (
        b0.get("available_balance") if isinstance(b0, dict) else None
    )
    mon = getattr(ab, "monetary", None) if ab else None
    if isinstance(ab, dict):
        mon = ab.get("monetary") or ab
    if isinstance(mon, dict) and "value" in mon:
        return int(mon["value"])
    if mon is not None and getattr(mon, "value", None) is not None:
        return int(mon.value)
    return None


def meter_usage_sum(meter_id: str, customer_id: str, t0: int, t1: int) -> float:
    page = stripe.billing.Meter.list_event_summaries(
        meter_id, customer=customer_id, start_time=t0, end_time=t1
    )
    s = 0.0
    for row in page.data or []:
        v = getattr(row, "aggregated_value", None)
        if v is not None:
            s += float(v)
    return s


def _next_page_cursor(body: dict[str, Any]) -> str | None:
    """Cursor for the next list page (up to ``LIST_PAGE_SIZE`` rows per request)."""
    nxt = body.get("next_page") or body.get("page")
    if nxt:
        return str(nxt)
    url = body.get("next_page_url")
    if isinstance(url, str) and url:
        try:
            q = parse_qs(urlparse(url).query).get("page", [None])[0]
            return str(q) if q else None
        except Exception:
            return None
    return None


def iter_plan_subscriptions(client: StripeClient, pricing_plan_id: str) -> Iterator[dict[str, Any]]:
    """Paginate list in chunks of ``LIST_PAGE_SIZE``; try servicing_status=active, then without if the API errors."""
    page_cursor: str | None = None
    seen: set[str] = set()

    def fetch(with_servicing: bool) -> dict[str, Any]:
        p: dict[str, Any] = {
            "pricing_plan": pricing_plan_id,
            "limit": LIST_PAGE_SIZE,
        }
        if with_servicing:
            p["servicing_status"] = "active"
        if page_cursor:
            p["page"] = page_cursor
        r = client.raw_request("get", "/v2/billing/pricing_plan_subscriptions", **p)
        return client.deserialize(r, api_mode="V2")

    use_servicing = True
    while True:
        try:
            body = fetch(use_servicing)
        except Exception:
            if use_servicing:
                use_servicing = False
                continue
            raise
        rows = body.get("data") or []
        for row in rows:
            yield row if isinstance(row, dict) else dict(row)
        nxt = _next_page_cursor(body)
        if not nxt or nxt in seen:
            break
        seen.add(nxt)
        page_cursor = nxt


def iter_subscriptions_for_customer(
    client: StripeClient, customer_id: str
) -> Iterator[dict[str, Any]]:
    """Paginate GET /v2/billing/pricing_plan_subscriptions with payer=customer."""
    page_cursor: str | None = None
    seen: set[str] = set()

    def fetch(with_servicing: bool) -> dict[str, Any]:
        params: dict[str, Any] = {
            "limit": LIST_PAGE_SIZE,
            "payer": {"type": "customer", "customer": customer_id},
        }
        if with_servicing:
            params["servicing_status"] = "active"
        if page_cursor:
            params["page"] = page_cursor
        r = client.raw_request("get", "/v2/billing/pricing_plan_subscriptions", **params)
        return client.deserialize(r, api_mode="V2")

    use_servicing = True
    while True:
        try:
            body = fetch(use_servicing)
        except Exception:
            if use_servicing:
                use_servicing = False
                continue
            raise
        rows = body.get("data") or []
        for row in rows:
            yield row if isinstance(row, dict) else dict(row)
        nxt = _next_page_cursor(body)
        if not nxt or (isinstance(nxt, str) and nxt in seen):
            break
        seen.add(str(nxt))
        page_cursor = str(nxt)


def _pp_sub_pricing_plan_id(sub: dict[str, Any]) -> str | None:
    pplan = _ref_id(sub.get("pricing_plan")) or sub.get("pricing_plan")
    if isinstance(pplan, dict):
        return pplan.get("id")
    return pplan


def deactivate_intent_body(currency: str, bppsub_id: str) -> dict[str, Any]:
    return {
        "currency": currency,
        "actions": [
            {
                "type": "deactivate",
                "deactivate": {
                    "type": "pricing_plan_subscription_details",
                    "collect_at": "next_billing_date",
                    "pricing_plan_subscription_details": {
                        "pricing_plan_subscription": bppsub_id,
                        "overrides": {
                            "partial_period_behaviors": [
                                {
                                    "type": "license_fee",
                                    "license_fee": {"credit_proration_behavior": "none"},
                                }
                            ]
                        },
                    },
                },
            }
        ],
    }


def _commit_deactivate_billing_intent(
    client: StripeClient, currency: str, bppsub_id: str, pf: str
) -> None:
    intent = client.deserialize(
        client.raw_request(
            "post",
            "/v2/billing/intents",
            **deactivate_intent_body(currency, bppsub_id),
        ),
        api_mode="V2",
    )
    iid = intent["id"]
    client.raw_request("post", f"/v2/billing/intents/{iid}/reserve")
    client.raw_request("post", f"/v2/billing/intents/{iid}/commit")
    print(f"{pf}billing intent {iid} committed")


def _cancel_cadence(client: StripeClient, cadence_id: str, pf: str) -> None:
    try:
        client.raw_request("post", f"/v2/billing/cadences/{cadence_id}/cancel")
        print(f"{pf}cadence canceled")
    except Exception as e:
        print(f"{pf}cadence cancel: {e}")


def deactivate_pp_subscription_and_cadence(
    client: StripeClient,
    currency: str,
    bppsub_id: str,
    cadence_id: str,
    pf: str,
) -> None:
    """V2 billing intent deactivate + cadence cancel (no credit grants)."""
    _commit_deactivate_billing_intent(client, currency, bppsub_id, pf)
    _cancel_cadence(client, cadence_id, pf)


def finalize_v2_teardown(
    client: StripeClient,
    currency: str,
    bppsub_id: str,
    cadence_id: str,
    customer_id: str,
    pf: str = "",
) -> None:
    """Billing intent deactivate PP sub, cancel cadence, expire credit grants."""
    deactivate_pp_subscription_and_cadence(client, currency, bppsub_id, cadence_id, pf)

    for g in stripe.billing.CreditGrant.list(customer=customer_id, limit=100).data or []:
        gid = getattr(g, "id", None)
        if gid:
            try:
                stripe.billing.CreditGrant.expire(gid)
            except Exception as e:
                print(f"{pf}expire {gid}: {e}")


def _run_cancel_only_plans_teardown(
    client: StripeClient,
    customer_id: str,
    cancel_plan_ids: set[str],
    execute: bool,
    pf: str,
) -> None:
    """Deactivate + cancel cadence for this customer's active subs on cancel-only plans."""
    if not cancel_plan_ids:
        return

    for sub in iter_subscriptions_for_customer(client, customer_id):
        sid = sub.get("id")
        if not sid or not isinstance(sid, str):
            continue
        plan_id = _pp_sub_pricing_plan_id(sub)
        if not plan_id or plan_id not in cancel_plan_ids:
            continue
        if _servicing_status(sub) == "canceled":
            continue
        wca = _will_cancel_at(sub)
        if wca:
            print(f"{pf}cancel-only skip {sid} (plan={plan_id}): will_cancel_at={wca}")
            continue
        cadence_id = _ref_id(sub.get("billing_cadence") or sub.get("cadence"))
        if not cadence_id:
            print(f"{pf}cancel-only skip {sid} (plan={plan_id}): no cadence")
            continue
        cadence = client.deserialize(
            client.raw_request("get", f"/v2/billing/cadences/{cadence_id}"),
            api_mode="V2",
        )
        cad_cust = _ref_id(_get(cadence, "payer", "customer"))
        if cad_cust != customer_id:
            print(
                f"{pf}cancel-only skip {sid}: cadence payer {cad_cust!r} != customer {customer_id!r}"
            )
            continue

        plan = client.deserialize(
            client.raw_request("get", f"/v2/billing/pricing_plans/{plan_id}"),
            api_mode="V2",
        )
        currency = (plan.get("currency") or "usd").lower()

        if not execute:
            print(
                f"{pf}dry-run: would deactivate cancel-only sub {sid} "
                f"(plan={plan_id}, cadence={cadence_id}, currency={currency})"
            )
            continue

        print(f"{pf}cancel-only teardown {sid} (plan={plan_id})")
        try:
            deactivate_pp_subscription_and_cadence(
                client, currency, sid, cadence_id, pf=pf
            )
        except Exception as e:
            print(f"{pf}cancel-only teardown {sid} failed: {e}")


def migrate_one(
    client: StripeClient,
    bpp_id: str,
    price_id: str,
    pp_sub: dict[str, Any],
    t_usage_start: int,
    t_usage_end: int,
    execute: bool,
    customer_allowlist: set[str] | None,
    cancel_plan_ids: set[str],
    cancel_hook_done: set[str],
    progress: tuple[int, int] | None = None,
) -> None:
    pf = _progress_prefix(progress)
    sub_id = pp_sub.get("id")
    if not sub_id or _servicing_status(pp_sub) == "canceled":
        return

    wca = _will_cancel_at(pp_sub)
    if wca:
        print(f"{pf}skip {sub_id}: servicing scheduled to cancel (will_cancel_at={wca})")
        return

    cadence_id = _ref_id(pp_sub.get("billing_cadence") or pp_sub.get("cadence"))
    if not cadence_id:
        print(f"{pf}skip {sub_id}: no cadence")
        return

    cadence = client.deserialize(
        client.raw_request("get", f"/v2/billing/cadences/{cadence_id}"),
        api_mode="V2",
    )
    customer_id = _ref_id(_get(cadence, "payer", "customer"))
    if not customer_id:
        print(f"{pf}skip {sub_id}: no customer on cadence")
        return
    if customer_allowlist is not None and customer_id not in customer_allowlist:
        return

    raw_nb = cadence.get("next_billing_date")
    nb = next_billing_ts(cadence)
    now_ts = int(time.time())
    horizon = now_ts + NEXT_BILLING_WITHIN_SEC
    if nb is None or not (now_ts < nb <= horizon):
        print(
            f"skip {sub_id} customer={customer_id}: "
            f"next_billing_date not within next {NEXT_BILLING_WITHIN_SEC // 86400} days "
            f"(parsed={fmt_next_billing(nb)} unix={nb!r} api_value={raw_nb!r})"
        )
        return

    print(
        f"\n--- {pf}{sub_id}  customer={customer_id}  plan={bpp_id} → {price_id}  "
        f"next_billing_date={fmt_next_billing(nb)} (unix={nb})"
    )

    profile_id = _ref_id(_get(cadence, "payer", "billing_profile"))
    default_pm: str | None = None
    if profile_id:
        prof = client.deserialize(
            client.raw_request("get", f"/v2/billing/profiles/{profile_id}"),
            api_mode="V2",
        )
        default_pm = prof.get("default_payment_method") or prof.get("default_payment_method_id")
        if isinstance(default_pm, dict):
            default_pm = default_pm.get("id")

    if not default_pm:
        cust = stripe.Customer.retrieve(
            customer_id,
            expand=["invoice_settings.default_payment_method"],
        )
        pm = _get(cust, "invoice_settings", "default_payment_method")
        default_pm = _ref_id(pm) if pm else None

    plan = client.deserialize(
        client.raw_request("get", f"/v2/billing/pricing_plans/{bpp_id}"),
        api_mode="V2",
    )
    currency = (plan.get("currency") or "usd").lower()

    avail: int | None = None
    try:
        cbs = stripe.billing.CreditBalanceSummary.retrieve(
            customer=customer_id,
            filter={
                "type": "applicability_scope",
                "applicability_scope": {"price_type": "metered"},
            },
        )
        avail = credit_available_minor(cbs)
    except Exception as e:
        print(f"credit_balance_summary: {e}")

    usage_total = 0.0
    for mtr in meter_ids_for_plan(client, bpp_id):
        try:
            usage_total += meter_usage_sum(mtr, customer_id, t_usage_start, t_usage_end)
        except Exception as e:
            print(f"meter {mtr}: {e}")

    anchor = cadence_to_anchor_config(cadence)
    meta_meter = str(int(usage_total)) if usage_total == int(usage_total) else str(usage_total)
    create: dict[str, Any] = {
        "customer": customer_id,
        "items": [{"price": price_id, "quantity": 1}],
        "proration_behavior": "none",
        "metadata": {
            "ubb_subscription_id": trunc(str(sub_id)),
            "available_credit_balance": trunc("" if avail is None else str(avail)),
            "meter_usage": trunc(meta_meter),
        },
    }
    if default_pm:
        create["default_payment_method"] = default_pm
    if anchor:
        create["billing_cycle_anchor_config"] = anchor
    else:
        nb = next_billing_ts(cadence)
        if nb:
            create["billing_cycle_anchor"] = nb

    if not execute:
        print(
            f"{pf}dry-run: would create v1 subscription + deactivate v2 + "
            "cancel cadence + expire grants"
        )
        if cancel_plan_ids and customer_id not in cancel_hook_done:
            cancel_hook_done.add(customer_id)
            _run_cancel_only_plans_teardown(
                client, customer_id, cancel_plan_ids, execute=False, pf=pf
            )
        return

    sub_v1 = stripe.Subscription.create(**create)
    print(f"{pf}v1 subscription {sub_v1.id}")

    finalize_v2_teardown(client, currency, sub_id, cadence_id, customer_id, pf=pf)

    if cancel_plan_ids and customer_id not in cancel_hook_done:
        cancel_hook_done.add(customer_id)
        _run_cancel_only_plans_teardown(
            client, customer_id, cancel_plan_ids, execute=True, pf=pf
        )


def load_map(path: str | None) -> dict[str, str]:
    if not path:
        return dict(DEFAULT_PRICING_PLAN_TO_PRICE)
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, dict):
        sys.exit("--map-json must be a JSON object: bpp_id → price_id")
    return {str(k): str(v) for k, v in raw.items()}


def load_cancel_only_plan_ids(path: str | None) -> set[str]:
    if not path:
        return set(DEFAULT_CANCEL_ONLY_PLAN_IDS)
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    if isinstance(raw, list):
        return {str(x) for x in raw}
    if isinstance(raw, dict):
        return {str(k) for k in raw}
    sys.exit("--cancel-map-json must be a JSON array of bpp ids or an object whose keys are bpp ids")


def load_customer_ids_json(path: str) -> set[str]:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, list):
        sys.exit("--customers-json must be a JSON array of customer id strings")
    out = {str(x).strip() for x in raw}
    out.discard("")
    if not out:
        sys.exit("--customers-json must contain at least one non-empty customer id")
    return out


def main() -> None:
    load_dotenv()
    p = argparse.ArgumentParser(
        description=__doc__,
        epilog=(
            "Examples: dry-run;  --execute;  --execute --customer cus_XXX;  "
            "--customers-json scripts/customers_allowlist.sample.json;  "
            "--cancel-map-json cancel_plans.json"
        ),
    )
    p.add_argument("--execute", action="store_true", help="perform writes (default is dry-run)")
    p.add_argument("--map-json", metavar="PATH", help="JSON map bpp_id → price_id")
    p.add_argument(
        "--cancel-map-json",
        metavar="PATH",
        help="JSON array of bpp ids (or object with bpp keys) to deactivate per customer after migrate",
    )
    p.add_argument("--customer", metavar="CUS_ID", help="only this Stripe customer")
    p.add_argument(
        "--customers-json",
        metavar="PATH",
        help="JSON array of Stripe customer ids (cus_...); union with --customer if both set",
    )
    args = p.parse_args()

    key = os.getenv("STRIPE_SECRET_KEY_SANDBOX")
    if not key:
        sys.exit("Set STRIPE_SECRET_KEY_SANDBOX in .env or the environment")

    if not args.execute:
        print("Dry-run (no writes). Use --execute to apply changes.\n")

    t0 = align_minute(USAGE_START)
    t1 = align_minute(int(time.time()))
    plan_map = load_map(args.map_json)
    cancel_plan_ids = load_cancel_only_plan_ids(args.cancel_map_json)
    overlap = cancel_plan_ids.intersection(plan_map.keys())
    if overlap:
        print(
            "warning: these bpp ids appear in both --map-json and --cancel-map-json "
            f"(migrate path runs first): {sorted(overlap)}",
            file=sys.stderr,
        )
    client = StripeClient(api_key=key, stripe_version=STRIPE_PREVIEW_VERSION)
    stripe.api_key = key
    stripe.api_version = STRIPE_PREVIEW_VERSION

    cancel_hook_done: set[str] = set()

    customer_allowlist: set[str] | None = None
    allow_ids: set[str] = set()
    if args.customer and str(args.customer).strip():
        allow_ids.add(str(args.customer).strip())
    if args.customers_json:
        allow_ids |= load_customer_ids_json(args.customers_json)
    if allow_ids:
        customer_allowlist = allow_ids

    for bpp_id, price_id in plan_map.items():
        print(f"\nplan {bpp_id}")
        try:
            pp_rows = list(iter_plan_subscriptions(client, bpp_id))
            n_subs = len(pp_rows)
            print(f"pricing_plan_subscriptions listed for this plan: {n_subs}")
            for idx, pp_sub in enumerate(pp_rows, start=1):
                migrate_one(
                    client,
                    bpp_id,
                    price_id,
                    pp_sub,
                    t0,
                    t1,
                    args.execute,
                    customer_allowlist,
                    cancel_plan_ids,
                    cancel_hook_done,
                    progress=(idx, n_subs),
                )
        except Exception as e:
            print(f"list subscriptions for {bpp_id}: {e}")


if __name__ == "__main__":
    main()
