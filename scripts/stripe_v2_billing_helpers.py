"""Shared Stripe v2 billing helpers (meters, license fees, billing intents, meter events)."""

from __future__ import annotations

import json
import os
from typing import Any

import stripe
from stripe import StripeClient

STRIPE_PREVIEW_VERSION = "2026-01-28.preview"


def advance_test_clock(client: StripeClient, clock_id: str, delta_seconds: int) -> int:
    """Advance a test clock by ``delta_seconds``; return new ``frozen_time`` (unix)."""
    c = client.v1.test_helpers.test_clocks.retrieve(clock_id)
    ft = getattr(c, "frozen_time", None)
    if ft is None and isinstance(c, dict):
        ft = c.get("frozen_time")
    cur = int(ft) if ft is not None else 0
    new_t = cur + int(delta_seconds)
    client.v1.test_helpers.test_clocks.advance(clock_id, frozen_time=new_t)
    return new_t


def get_next_meter_number(counter_path: str | None = None) -> int:
    """Increment and persist meter counter (default: ``meter_counter.json`` in cwd)."""
    path = counter_path or os.path.join(os.getcwd(), "meter_counter.json")
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                current = json.load(f).get("meter_count", 0)
        except (json.JSONDecodeError, OSError, KeyError):
            current = 0
    else:
        current = 0
    nxt = current + 1
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"meter_count": nxt}, f, indent=2)
    return nxt


def find_license_plan_component_id(client: StripeClient, pricing_plan_id: str) -> str | None:
    resp = client.raw_request(
        "get", f"/v2/billing/pricing_plans/{pricing_plan_id}/components"
    )
    body = client.deserialize(resp, api_mode="V2")
    for c in body.get("data", []):
        if c.get("type") == "license_fee":
            return c.get("id")
    return None


def license_fee_attach_version(lf: Any) -> str | None:
    v = getattr(lf, "live_version", None)
    if v:
        return v
    if isinstance(lf, dict):
        return lf.get("live_version")
    return None


def resolve_license_fee_version(client: StripeClient, lf: Any) -> str:
    v = license_fee_attach_version(lf)
    if v:
        return v
    lf_get = client.deserialize(
        client.raw_request("get", f"/v2/billing/license_fees/{lf.id}"),
        api_mode="V2",
    )
    v = lf_get.get("live_version") or lf_get.get("latest_version")
    if not v:
        raise SystemExit("Could not resolve license_fee version for attach.")
    return v


def meter_value_payload_key(meter: Any) -> str:
    vs = getattr(meter, "value_settings", None)
    if vs is None and isinstance(meter, dict):
        vs = meter.get("value_settings")
    if not vs:
        return "value"
    key = getattr(vs, "event_payload_key", None)
    if key:
        return str(key)
    if isinstance(vs, dict):
        return str(vs.get("event_payload_key") or "value")
    return "value"


def tok_visa_payment_method_for_customer(customer_id: str) -> str:
    pm = stripe.PaymentMethod.create(type="card", card={"token": "tok_visa"})
    stripe.PaymentMethod.attach(pm.id, customer=customer_id)
    return pm.id


def _amount_details_total(reserved: Any) -> int:
    ad = getattr(reserved, "amount_details", None)
    if ad is None and isinstance(reserved, dict):
        ad = reserved.get("amount_details")
    if ad is None:
        return 0
    if isinstance(ad, dict):
        return int(ad.get("total", 0) or 0)
    return int(getattr(ad, "total", 0) or 0)


def _payment_intent_id_from_billing_intent(obj: Any) -> str | None:
    for key in ("payment_intent", "latest_payment_intent"):
        val = getattr(obj, key, None)
        if val is None and isinstance(obj, dict):
            val = obj.get(key)
        if isinstance(val, str) and val.startswith("pi_"):
            return val
        if val is not None and getattr(val, "id", None):
            rid = val.id
            if isinstance(rid, str) and rid.startswith("pi_"):
                return rid
    return None


def _ensure_payment_intent_succeeded(pi_id: str, pm_id: str) -> None:
    pi = stripe.PaymentIntent.retrieve(pi_id)
    if pi.status == "succeeded":
        return
    if pi.status in ("requires_confirmation", "requires_payment_method"):
        stripe.PaymentIntent.confirm(pi_id, payment_method=pm_id, off_session=True)


def billing_intent_reserve_and_commit(
    client: StripeClient,
    bi_id: str,
    customer_id: str,
    pm_id: str | None,
    currency: str,
    collection_method: str,
) -> str | None:
    """Reserve + commit billing intent. Returns PaymentIntent id for ``automatic`` when used."""
    if collection_method != "automatic":
        client.raw_request("post", f"/v2/billing/intents/{bi_id}/reserve")
        client.raw_request("post", f"/v2/billing/intents/{bi_id}/commit")
        return None
    if not pm_id:
        raise SystemExit("payment method required for automatic collection")
    reserve_resp = client.raw_request("post", f"/v2/billing/intents/{bi_id}/reserve")
    reserved = client.deserialize(reserve_resp, api_mode="V2")
    pi_id = _payment_intent_id_from_billing_intent(reserved)
    total = _amount_details_total(reserved)
    if not pi_id and total > 0:
        pi = stripe.PaymentIntent.create(
            amount=total,
            currency=currency,
            customer=customer_id,
            payment_method=pm_id,
            confirm=True,
            off_session=True,
        )
        pi_id = pi.id
    elif pi_id:
        _ensure_payment_intent_succeeded(pi_id, pm_id)
    if pi_id:
        client.raw_request(
            "post", f"/v2/billing/intents/{bi_id}/commit", payment_intent=pi_id
        )
    else:
        client.raw_request("post", f"/v2/billing/intents/{bi_id}/commit")
    return pi_id


def send_meter_event(
    customer_id: str,
    units: int,
    event_name: str,
    value_payload_key: str,
    dimensions: dict[str, str] | None = None,
) -> Any:
    pl: dict[str, str] = {
        "stripe_customer_id": customer_id,
        value_payload_key: str(units),
    }
    if dimensions:
        for k, v in dimensions.items():
            pl[str(k)] = str(v)
    return stripe.billing.MeterEvent.create(event_name=event_name, payload=pl)


def resolve_rate_card_version(
    client: StripeClient, rc_id: str, last_rate: Any | None = None
) -> str:
    v = None
    if last_rate is not None:
        v = (
            last_rate.get("version")
            if isinstance(last_rate, dict)
            else getattr(last_rate, "version", None)
        )
    if v:
        return v
    rc_fetch = client.deserialize(
        client.raw_request("get", f"/v2/billing/rate_cards/{rc_id}"),
        api_mode="V2",
    )
    out = rc_fetch.get("live_version") or rc_fetch.get("latest_version")
    if not out:
        raise SystemExit("No rate card version returned from Stripe after adding rates")
    return out
