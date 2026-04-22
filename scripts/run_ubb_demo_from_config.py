#!/usr/bin/env python3
"""Create a v2 pricing plan from JSON config, subscribe N customers, send configured meter usage."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any

import stripe
from dotenv import load_dotenv
from stripe import StripeClient

from stripe_v2_billing_helpers import (
    STRIPE_PREVIEW_VERSION,
    billing_intent_reserve_and_commit,
    find_license_plan_component_id,
    meter_value_payload_key,
    resolve_license_fee_version,
    resolve_rate_card_version,
    send_meter_event,
    tok_visa_payment_method_for_customer,
)

REQUIRED_TOP = (
    "pricing_plan",
    "meter",
    "rate_card",
    "license",
    "service_action",
    "billing",
    "customers",
)


def _tpl(s: str, ts: int) -> str:
    return (s or "").replace("{timestamp}", str(ts))


def load_config(path: str) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _normalized_rates(cfg: dict[str, Any], path: str) -> list[dict[str, Any]]:
    if cfg.get("rates") is not None:
        rates = cfg["rates"]
        if not isinstance(rates, list) or len(rates) < 1:
            sys.exit(f"Invalid config {path!r}: rates must be a non-empty array")
        out: list[dict[str, Any]] = []
        for i, r in enumerate(rates):
            if not isinstance(r, dict):
                sys.exit(f"Invalid config {path!r}: rates[{i}] must be an object")
            if not r.get("metered_item_display_name"):
                sys.exit(
                    f"Invalid config {path!r}: rates[{i}].metered_item_display_name is required"
                )
            if r.get("unit_amount_cents") in (None, ""):
                sys.exit(
                    f"Invalid config {path!r}: rates[{i}].unit_amount_cents is required"
                )
            conds = r.get("meter_segment_conditions")
            if conds is not None and not isinstance(conds, list):
                sys.exit(
                    f"Invalid config {path!r}: rates[{i}].meter_segment_conditions "
                    "must be an array"
                )
            out.append(
                {
                    "metered_item_display_name": str(r["metered_item_display_name"]),
                    "unit_amount_cents": str(r["unit_amount_cents"]),
                    "meter_segment_conditions": list(conds or []),
                }
            )
        return out
    if "metered_item" not in cfg or "rate" not in cfg:
        sys.exit(
            f"Invalid config {path!r}: provide either non-empty rates[] or "
            "both metered_item and rate (legacy)"
        )
    if not cfg["rate"].get("unit_amount_cents"):
        sys.exit(f"Invalid config {path!r}: rate.unit_amount_cents is required")
    return [
        {
            "metered_item_display_name": str(cfg["metered_item"]["display_name"]),
            "unit_amount_cents": str(cfg["rate"]["unit_amount_cents"]),
            "meter_segment_conditions": [],
        }
    ]


def _dimension_keys_from_rates(rates: list[dict[str, Any]]) -> list[str]:
    keys: list[str] = []
    for r in rates:
        for c in r.get("meter_segment_conditions") or []:
            if not isinstance(c, dict):
                continue
            d = c.get("dimension")
            if d and str(d) not in keys:
                keys.append(str(d))
    return keys


def _plan_dimension_keys(
    cfg: dict[str, Any],
    path: str,
    rates: list[dict[str, Any]] | None = None,
) -> list[str] | None:
    if rates is None:
        rates = _normalized_rates(cfg, path)
    explicit = cfg["meter"].get("dimension_payload_keys")
    if explicit is not None:
        return [str(x) for x in explicit]
    inferred = _dimension_keys_from_rates(rates)
    return inferred if inferred else None


def validate_config(cfg: dict[str, Any], path: str) -> None:
    for k in REQUIRED_TOP:
        if k not in cfg:
            sys.exit(f"Invalid config {path!r}: missing top-level key {k!r}")
    rates = _normalized_rates(cfg, path)
    flat_count = sum(1 for r in rates if not r.get("meter_segment_conditions"))
    if len(rates) > 1 and flat_count > 1:
        sys.exit(
            f"Invalid config {path!r}: multiple undimensioned rates are not supported; "
            "use meter_segment_conditions on all but at most one rate"
        )
    if flat_count > 1:
        sys.exit(f"Invalid config {path!r}: at most one rate may omit meter_segment_conditions")

    has_dim = any(r.get("meter_segment_conditions") for r in rates)
    m = cfg["meter"]
    explicit_dims = m.get("dimension_payload_keys")
    if explicit_dims is not None:
        if not isinstance(explicit_dims, list) or not explicit_dims:
            sys.exit(
                f"Invalid config {path!r}: meter.dimension_payload_keys must be a non-empty array"
            )
    elif has_dim and not _dimension_keys_from_rates(rates):
        sys.exit(
            f"Invalid config {path!r}: dimensioned rates require meter_segment_conditions "
            "with dimension, or set meter.dimension_payload_keys"
        )

    if explicit_dims is not None:
        used_explicit = False
        allowed = {str(x) for x in explicit_dims}
        for r in rates:
            for c in r.get("meter_segment_conditions") or []:
                d = c.get("dimension")
                if d is not None and str(d) not in allowed:
                    sys.exit(
                        f"Invalid config {path!r}: meter_segment_conditions references "
                        f"unknown dimension {d!r} (not in meter.dimension_payload_keys)"
                    )
                if d is not None and str(d) in allowed:
                    used_explicit = True
        if not used_explicit:
            sys.exit(
                f"Invalid config {path!r}: meter.dimension_payload_keys requires at least "
                "one rate with meter_segment_conditions using those dimensions"
            )

    plan_dims = _plan_dimension_keys(cfg, path, rates)

    customers = cfg["customers"]
    if not isinstance(customers, list) or len(customers) < 1:
        sys.exit(f"Invalid config {path!r}: customers must be a non-empty array")
    for i, c in enumerate(customers):
        if not isinstance(c, dict):
            sys.exit(f"Invalid config {path!r}: customers[{i}] must be an object")
        if not c.get("email"):
            sys.exit(f"Invalid config {path!r}: customers[{i}].email is required")
        usage = c.get("usage") or {}
        if usage.get("units") is not None and usage.get("events") is not None:
            sys.exit(
                f"Invalid config {path!r}: customers[{i}] cannot set both usage.units "
                "and usage.events"
            )
        if usage.get("units") is not None and int(usage["units"]) < 0:
            sys.exit(f"Invalid config {path!r}: customers[{i}].usage.units must be >= 0")
        if usage.get("events") is not None:
            if not isinstance(usage["events"], list):
                sys.exit(f"Invalid config {path!r}: customers[{i}].usage.events must be an array")
            for j, ev in enumerate(usage["events"]):
                if not isinstance(ev, dict):
                    sys.exit(
                        f"Invalid config {path!r}: customers[{i}].usage.events[{j}] must be object"
                    )
                if int(ev.get("units", 0) or 0) < 0:
                    sys.exit(
                        f"Invalid config {path!r}: customers[{i}].usage.events[{j}].units "
                        "must be >= 0"
                    )
                if plan_dims and int(ev.get("units", 0) or 0) > 0:
                    dims = ev.get("dimensions") or {}
                    if not isinstance(dims, dict):
                        sys.exit(
                            f"Invalid config {path!r}: customers[{i}].usage.events[{j}].dimensions "
                            "must be an object"
                        )
                    for dk in plan_dims:
                        if dk not in dims:
                            sys.exit(
                                f"Invalid config {path!r}: customers[{i}].usage.events[{j}] "
                                f"missing dimension {dk!r}"
                            )
    if plan_dims:
        for i, c in enumerate(customers):
            u = c.get("usage") or {}
            if u.get("events") is None:
                sys.exit(
                    f"Invalid config {path!r}: customers[{i}] must set usage.events when "
                    "using dimensioned rates (or meter.dimension_payload_keys)"
                )
    if not m.get("event_name"):
        sys.exit(f"Invalid config {path!r}: meter.event_name is required")
    if not cfg["license"].get("unit_amount_cents"):
        sys.exit(f"Invalid config {path!r}: license.unit_amount_cents is required")
    coll = cfg["billing"].get("collection_method")
    if coll not in ("automatic", "send_invoice"):
        sys.exit(
            f"Invalid config {path!r}: billing.collection_method must be "
            f"'automatic' or 'send_invoice'"
        )
    if coll == "automatic" and not cfg["billing"].get("attach_tok_visa", True):
        sys.exit(
            f"Invalid config {path!r}: attach_tok_visa must be true when "
            f"collection_method is automatic"
        )


def _get_or_create_meter(
    client: StripeClient,
    cfg: dict[str, Any],
    ts: int,
    event_name: str,
    dimension_payload_keys: list[str] | None,
) -> tuple[Any, bool, str]:
    """Returns (meter, reused, effective_event_name)."""
    mcfg = cfg["meter"]
    reuse = bool(mcfg.get("reuse_if_exists", True))
    if reuse:
        for meter in stripe.billing.Meter.list(limit=100).auto_paging_iter():
            if getattr(meter, "event_name", None) == event_name:
                return meter, True, event_name
    else:
        event_name = f"{event_name}_{ts}"
    body: dict[str, Any] = {
        "display_name": _tpl(str(mcfg.get("display_name") or "Meter"), ts),
        "event_name": event_name,
        "default_aggregation": mcfg.get("default_aggregation") or {"formula": "sum"},
    }
    if dimension_payload_keys:
        body["dimension_payload_keys"] = dimension_payload_keys
    if mcfg.get("value_settings"):
        body["value_settings"] = mcfg["value_settings"]
    meter = client.billing.meters.create(body)
    return meter, False, event_name


def build_pricing_plan(
    client: StripeClient, cfg: dict[str, Any], ts: int, cfg_path: str
) -> dict[str, Any]:
    rates = _normalized_rates(cfg, cfg_path)
    dim_keys = _plan_dimension_keys(cfg, cfg_path, rates)

    ppc = cfg["pricing_plan"]
    pp = client.deserialize(
        client.raw_request(
            "post",
            "/v2/billing/pricing_plans",
            display_name=_tpl(str(ppc["display_name"]), ts),
            currency=ppc["currency"],
            tax_behavior=ppc["tax_behavior"],
        ),
        api_mode="V2",
    )

    base_event = str(cfg["meter"]["event_name"])
    meter, meter_reused, meter_event_name = _get_or_create_meter(
        client, cfg, ts, base_event, dim_keys
    )
    value_payload_key = meter_value_payload_key(meter)

    metered_items_out: list[dict[str, Any]] = []
    for r in rates:
        mi_kwargs: dict[str, Any] = {
            "display_name": str(r["metered_item_display_name"]),
            "meter": meter.id,
        }
        conds = r.get("meter_segment_conditions") or []
        if conds:
            mi_kwargs["meter_segment_conditions"] = conds
        mi = client.deserialize(
            client.raw_request(
                "post",
                "/v2/billing/metered_items",
                **mi_kwargs,
            ),
            api_mode="V2",
        )
        metered_items_out.append(
            {
                "id": mi.id,
                "display_name": r["metered_item_display_name"],
                "unit_amount_cents": r["unit_amount_cents"],
                "meter_segment_conditions": conds,
            }
        )

    rcc = cfg["rate_card"]
    rc = client.deserialize(
        client.raw_request(
            "post",
            "/v2/billing/rate_cards",
            display_name=rcc["display_name"],
            service_interval=rcc["service_interval"],
            service_interval_count=rcc["service_interval_count"],
            currency=rcc["currency"],
            tax_behavior=rcc["tax_behavior"],
        ),
        api_mode="V2",
    )
    last_rate: Any = None
    for mi_entry in metered_items_out:
        last_rate = client.deserialize(
            client.raw_request(
                "post",
                f"/v2/billing/rate_cards/{rc.id}/rates",
                metered_item=mi_entry["id"],
                unit_amount=str(mi_entry["unit_amount_cents"]),
            ),
            api_mode="V2",
        )
    rc_ver = resolve_rate_card_version(client, rc.id, last_rate)

    lic = cfg["license"]
    lic_item = client.deserialize(
        client.raw_request(
            "post",
            "/v2/billing/licensed_items",
            display_name=lic["licensed_item_display_name"],
        ),
        api_mode="V2",
    )
    lf = client.deserialize(
        client.raw_request(
            "post",
            "/v2/billing/license_fees",
            display_name=lic["fee_display_name"],
            currency=lic["currency"],
            service_interval=lic["service_interval"],
            service_interval_count=lic["service_interval_count"],
            tax_behavior=lic["tax_behavior"],
            unit_amount=str(lic["unit_amount_cents"]),
            licensed_item=lic_item.id,
        ),
        api_mode="V2",
    )
    lf_ver = resolve_license_fee_version(client, lf)

    sa_cfg = cfg["service_action"]
    sa = client.deserialize(
        client.raw_request(
            "post",
            "/v2/billing/service_actions",
            service_interval=sa_cfg["service_interval"],
            service_interval_count=sa_cfg["service_interval_count"],
            type="credit_grant",
            credit_grant={
                "amount": {
                    "type": "monetary",
                    "monetary": {
                        "currency": sa_cfg["credit_grant_currency"],
                        "value": int(sa_cfg["credit_grant_cents"]),
                    },
                },
                "applicability_config": {"scope": {"price_type": "metered"}},
                "expiry_config": {"type": "end_of_service_period"},
                "name": sa_cfg["credit_grant_name"],
            },
        ),
        api_mode="V2",
    )

    client.raw_request(
        "post",
        f"/v2/billing/pricing_plans/{pp.id}/components",
        type="rate_card",
        rate_card={"id": rc.id, "version": rc_ver},
    )
    client.raw_request(
        "post",
        f"/v2/billing/pricing_plans/{pp.id}/components",
        type="license_fee",
        license_fee={"id": lf.id, "version": lf_ver},
    )
    client.raw_request(
        "post",
        f"/v2/billing/pricing_plans/{pp.id}/components",
        type="service_action",
        service_action={"id": sa.id},
    )

    activated = client.deserialize(
        client.raw_request(
            "post",
            f"/v2/billing/pricing_plans/{pp.id}",
            live_version="latest",
        ),
        api_mode="V2",
    )
    pp_ver = activated.get("live_version")
    lic_comp = find_license_plan_component_id(client, pp.id)

    return {
        "pricing_plan_id": pp.id,
        "pricing_plan_version": pp_ver,
        "license_pricing_plan_component_id": lic_comp,
        "meter_id": meter.id,
        "meter_reused": meter_reused,
        "meter_event_name": meter_event_name,
        "meter_value_payload_key": value_payload_key,
        "dimension_payload_keys": dim_keys,
        "metered_items": metered_items_out,
        "subscribe_quantity": int(lic.get("subscribe_quantity", 1)),
    }


def main() -> None:
    load_dotenv()
    default_cfg = os.path.join(os.path.dirname(__file__), "ubb_demo.config.json")
    ap = argparse.ArgumentParser(
        description="Create v2 pricing plan from config and subscribe customers."
    )
    ap.add_argument(
        "--config",
        default=default_cfg,
        help=f"Path to JSON config (default: {default_cfg})",
    )
    args = ap.parse_args()
    cfg_path = os.path.abspath(args.config)
    cfg = load_config(cfg_path)
    validate_config(cfg, cfg_path)

    key = os.getenv("STRIPE_SECRET_KEY_SANDBOX")
    if not key:
        sys.exit("STRIPE_SECRET_KEY_SANDBOX not set.")

    client = StripeClient(api_key=key, stripe_version=STRIPE_PREVIEW_VERSION)
    stripe.api_key = key

    ts = int(time.time())
    billing = cfg["billing"]
    collection_method = billing["collection_method"]
    bi_currency = billing["billing_intent_currency"]
    offset = int(billing.get("test_clock_offset_seconds", 86400))
    shared_clock = bool(billing.get("shared_test_clock", True))
    attach_pm = bool(billing.get("attach_tok_visa", True))

    plan_out = build_pricing_plan(client, cfg, ts, cfg_path)
    pp_id = plan_out["pricing_plan_id"]
    pp_ver = plan_out["pricing_plan_version"]
    lic_comp = plan_out["license_pricing_plan_component_id"]
    meter_event_name = plan_out["meter_event_name"]
    value_payload_key = plan_out["meter_value_payload_key"]
    lic_qty = plan_out["subscribe_quantity"]

    cs = client.deserialize(
        client.raw_request(
            "post",
            "/v2/billing/collection_settings",
            collection_method=collection_method,
            display_name=billing["collection_display_name"],
        ),
        api_mode="V2",
    )

    tc_id: str | None = None
    if shared_clock:
        tc = client.v1.test_helpers.test_clocks.create(
            {"frozen_time": int(time.time()) + offset}
        )
        tc_id = tc.id

    customers_out: list[dict[str, Any]] = []
    meter_events_out: list[dict[str, Any]] = []

    for idx, cust_spec in enumerate(cfg["customers"], start=1):
        email = _tpl(str(cust_spec["email"]), ts)
        name = _tpl(str(cust_spec.get("name") or ""), ts) or f"Customer {idx}"
        desc = _tpl(str(cust_spec.get("description") or ""), ts)

        cust_kwargs: dict[str, Any] = {
            "email": email,
            "name": name,
            "description": desc,
        }
        if tc_id:
            cust_kwargs["test_clock"] = tc_id
        elif not shared_clock:
            tc2 = client.v1.test_helpers.test_clocks.create(
                {"frozen_time": int(time.time()) + offset}
            )
            cust_kwargs["test_clock"] = tc2.id

        cust = client.v1.customers.create(cust_kwargs)

        pm_id: str | None = None
        if attach_pm:
            pm_id = tok_visa_payment_method_for_customer(cust.id)

        bp_kwargs: dict[str, Any] = {
            "customer": cust.id,
            "display_name": billing["billing_profile_display_name"],
        }
        if pm_id:
            bp_kwargs["default_payment_method"] = pm_id

        bp = client.deserialize(
            client.raw_request("post", "/v2/billing/profiles", **bp_kwargs),
            api_mode="V2",
        )

        cad_cfg = billing["cadence"]
        cad = client.deserialize(
            client.raw_request(
                "post",
                "/v2/billing/cadences",
                payer={"billing_profile": bp.id},
                billing_cycle={
                    "type": cad_cfg["billing_cycle_type"],
                    "interval_count": cad_cfg["billing_cycle_interval_count"],
                },
                settings={"collection": {"id": cs.id}},
            ),
            api_mode="V2",
        )

        sub: dict[str, Any] = {"pricing_plan": pp_id, "pricing_plan_version": pp_ver}
        if lic_comp:
            sub["component_configurations"] = [
                {"pricing_plan_component": lic_comp, "quantity": lic_qty}
            ]

        bi = client.deserialize(
            client.raw_request(
                "post",
                "/v2/billing/intents",
                currency=bi_currency,
                cadence=cad.id,
                actions=[
                    {
                        "type": "subscribe",
                        "subscribe": {
                            "type": "pricing_plan_subscription_details",
                            "pricing_plan_subscription_details": sub,
                        },
                    }
                ],
            ),
            api_mode="V2",
        )

        commit_pi = billing_intent_reserve_and_commit(
            client,
            bi.id,
            cust.id,
            pm_id,
            bi_currency,
            collection_method,
        )

        usage = cust_spec.get("usage") or {}
        if usage.get("events") is not None:
            usage_units = sum(int(e.get("units", 0) or 0) for e in usage["events"])
        else:
            usage_units = int(usage.get("units", 0) or 0)

        row: dict[str, Any] = {
            "index": idx,
            "customer_id": cust.id,
            "email": email,
            "billing_profile_id": bp.id,
            "billing_intent_id": bi.id,
            "usage_units": usage_units,
        }
        if pm_id:
            row["default_payment_method"] = pm_id
        if commit_pi is not None:
            row["commit_payment_intent_id"] = commit_pi
        customers_out.append(row)

    plan_dims = plan_out.get("dimension_payload_keys") or []

    for row, cust_spec in zip(customers_out, cfg["customers"], strict=True):
        usage = cust_spec.get("usage") or {}
        sent_records: list[dict[str, Any]] = []
        if usage.get("events") is not None:
            for ev in usage["events"]:
                u = int(ev.get("units", 0) or 0)
                if u <= 0:
                    continue
                dims_raw = ev.get("dimensions") or {}
                if not isinstance(dims_raw, dict):
                    sys.exit(
                        f"Invalid usage: customer {row['email']} has non-object dimensions in an event"
                    )
                dims = {str(k): str(v) for k, v in dims_raw.items()}
                for dk in plan_dims:
                    if dk not in dims:
                        sys.exit(
                            f"Missing dimension {dk!r} in meter event for customer {row['email']}"
                        )
                send_meter_event(
                    row["customer_id"],
                    u,
                    meter_event_name,
                    value_payload_key,
                    dims if dims else None,
                )
                sent_records.append({"units": u, "dimensions": dims})
        else:
            u = int(usage.get("units", 0) or 0)
            if u > 0:
                if plan_dims:
                    sys.exit(
                        f"Customer {row['email']}: usage.units not allowed when plan has "
                        "dimensions; use usage.events"
                    )
                send_meter_event(
                    row["customer_id"],
                    u,
                    meter_event_name,
                    value_payload_key,
                    None,
                )
                sent_records.append({"units": u, "dimensions": {}})
        meter_events_out.append(
            {"customer_index": row["index"], "sent": sent_records}
        )

    summary: dict[str, Any] = {
        "config_path": cfg_path,
        "meter_event_name": meter_event_name,
        "pricing_plan_id": pp_id,
        "meter_id": plan_out["meter_id"],
        "meter_reused": plan_out["meter_reused"],
        "meter_value_payload_key": value_payload_key,
        "dimension_payload_keys": plan_out.get("dimension_payload_keys"),
        "metered_items": plan_out.get("metered_items"),
        "pricing_plan_version": pp_ver,
        "license_pricing_plan_component_id": lic_comp,
        "test_clock_id": tc_id,
        "collection_method": collection_method,
        "customers": customers_out,
        "meter_events": meter_events_out,
    }

    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
