#!/usr/bin/env python3
"""
Migrate UBB v2 pricing plan subscriptions to v1 Subscriptions.

Requires STRIPE_SECRET_KEY_SANDBOX. Default is dry-run; add --execute to write.
See --help for flags (--map-json, --customer).
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
LIST_PAGE_SIZE = 100
# Meter usage window start (UTC)
USAGE_START = int(datetime(2026, 3, 31, 23, 59, 59, tzinfo=timezone.utc).timestamp())

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

META_MAX = 500


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


def iter_plan_subscriptions(client: StripeClient, pricing_plan_id: str) -> Iterator[dict[str, Any]]:
    """Paginate list; try servicing_status=active, then without if the API errors."""
    page: str | None = None
    seen: set[str] = set()

    def fetch(with_servicing: bool) -> dict[str, Any]:
        p: dict[str, Any] = {
            "pricing_plan": pricing_plan_id,
            "limit": LIST_PAGE_SIZE,
        }
        if with_servicing:
            p["servicing_status"] = "active"
        if page:
            p["page"] = page
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
        for row in body.get("data") or []:
            yield row if isinstance(row, dict) else dict(row)
        nxt = body.get("next_page") or body.get("page")
        if not nxt or (isinstance(nxt, str) and nxt in seen):
            break
        if isinstance(nxt, str):
            seen.add(nxt)
        page = str(nxt)


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


def migrate_one(
    client: StripeClient,
    bpp_id: str,
    price_id: str,
    pp_sub: dict[str, Any],
    t_usage_start: int,
    t_usage_end: int,
    execute: bool,
    customer_only: str | None,
) -> None:
    sub_id = pp_sub.get("id")
    if not sub_id or _servicing_status(pp_sub) == "canceled":
        return

    cadence_id = _ref_id(pp_sub.get("billing_cadence") or pp_sub.get("cadence"))
    if not cadence_id:
        print(f"skip {sub_id}: no cadence")
        return

    cadence = client.deserialize(
        client.raw_request("get", f"/v2/billing/cadences/{cadence_id}"),
        api_mode="V2",
    )
    customer_id = _ref_id(_get(cadence, "payer", "customer"))
    if not customer_id:
        print(f"skip {sub_id}: no customer on cadence")
        return
    if customer_only and customer_id != customer_only:
        return

    print(f"\n--- {sub_id}  customer={customer_id}  plan={bpp_id} → {price_id}")

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
        print("dry-run: would create v1 subscription + deactivate v2 + cancel cadence + expire grants")
        return

    sub_v1 = stripe.Subscription.create(**create)
    print(f"v1 subscription {sub_v1.id}")

    intent = client.deserialize(
        client.raw_request(
            "post",
            "/v2/billing/intents",
            **deactivate_intent_body(currency, sub_id),
        ),
        api_mode="V2",
    )
    iid = intent["id"]
    client.raw_request("post", f"/v2/billing/intents/{iid}/reserve")
    client.raw_request("post", f"/v2/billing/intents/{iid}/commit")
    print(f"billing intent {iid} committed")

    try:
        client.raw_request("post", f"/v2/billing/cadences/{cadence_id}/cancel")
        print("cadence canceled")
    except Exception as e:
        print(f"cadence cancel: {e}")

    for g in stripe.billing.CreditGrant.list(customer=customer_id, limit=100).data or []:
        gid = getattr(g, "id", None)
        if gid:
            try:
                stripe.billing.CreditGrant.expire(gid)
            except Exception as e:
                print(f"expire {gid}: {e}")


def load_map(path: str | None) -> dict[str, str]:
    if not path:
        return dict(DEFAULT_PRICING_PLAN_TO_PRICE)
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, dict):
        sys.exit("--map-json must be a JSON object: bpp_id → price_id")
    return {str(k): str(v) for k, v in raw.items()}


def main() -> None:
    load_dotenv()
    p = argparse.ArgumentParser(
        description=__doc__,
        epilog="Examples: dry-run;  --execute;  --execute --customer cus_XXX",
    )
    p.add_argument("--execute", action="store_true", help="perform writes (default is dry-run)")
    p.add_argument("--map-json", metavar="PATH", help="JSON map bpp_id → price_id")
    p.add_argument("--customer", metavar="CUS_ID", help="only this Stripe customer")
    args = p.parse_args()

    key = os.getenv("STRIPE_SECRET_KEY_SANDBOX")
    if not key:
        sys.exit("Set STRIPE_SECRET_KEY_SANDBOX in .env or the environment")

    if not args.execute:
        print("Dry-run (no writes). Use --execute to apply changes.\n")

    t0 = align_minute(USAGE_START)
    t1 = align_minute(int(time.time()))
    plan_map = load_map(args.map_json)
    client = StripeClient(api_key=key, stripe_version=STRIPE_PREVIEW_VERSION)
    stripe.api_key = key
    stripe.api_version = STRIPE_PREVIEW_VERSION

    for bpp_id, price_id in plan_map.items():
        print(f"\nplan {bpp_id}")
        try:
            for pp_sub in iter_plan_subscriptions(client, bpp_id):
                migrate_one(
                    client,
                    bpp_id,
                    price_id,
                    pp_sub,
                    t0,
                    t1,
                    args.execute,
                    args.customer,
                )
        except Exception as e:
            print(f"list subscriptions for {bpp_id}: {e}")


if __name__ == "__main__":
    main()
