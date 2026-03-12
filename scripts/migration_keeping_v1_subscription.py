#!/usr/bin/env python3
"""
Migration: Keeping v1 Subscription + Migrating Metered to v2 Pricing Plan

Takes an existing v1 subscription ID and:
1. Retrieves the subscription and its customer
2. Extracts metered (usage-based) prices from the v1 subscription
3. Creates a billing profile and billing cadence; the cadence is yearly and aligned to the v1
   subscription's billing_cycle_anchor (same month, day, and time) so the billing period is not reset.
4. Attaches the cadence to the v1 subscription (keeps licensed/fixed fees on v1)
5. Creates a v2 pricing plan with only the metered pricing (reusing the same meter)
6. Subscribes the customer to that v2 plan on the same cadence (one invoice for both)
7. Removes the old metered subscription items from the v1 subscription (the meter is kept).

Result: v1 subscription (licensed fees only) + v2 pricing plan subscription (metered usage)
on the same billing cadence; meter is shared and unchanged.

Run: python scripts/migration_keeping_v1_subscription.py <subscription_id>
"""

import os
import argparse
import datetime
from dotenv import load_dotenv
from stripe import StripeClient
import stripe

load_dotenv()

STRIPE_SECRET_KEY_SANDBOX = os.getenv("STRIPE_SECRET_KEY_SANDBOX")
if not STRIPE_SECRET_KEY_SANDBOX:
    raise ValueError(
        "STRIPE_SECRET_KEY_SANDBOX environment variable not set. "
        "Set it in your environment or .env file."
    )

client = StripeClient(
    api_key=STRIPE_SECRET_KEY_SANDBOX,
    stripe_version="2026-02-25.preview",
)
stripe.api_key = STRIPE_SECRET_KEY_SANDBOX

parser = argparse.ArgumentParser(
    description="Migrate metered pricing to v2 pricing plan; keep v1 for licensed fees; same cadence"
)
parser.add_argument(
    "subscription_id",
    help="Stripe v1 subscription ID (e.g. sub_xxxxx)",
)
args = parser.parse_args()


def _get(obj, *keys, default=None):
    """Get nested key from dict or StripeObject."""
    for key in keys:
        if obj is None:
            return default
        obj = obj.get(key) if hasattr(obj, "get") and callable(getattr(obj, "get")) else getattr(obj, key, None)
    return obj


def extract_metered_prices_from_subscription(subscription):
    """
    From a v1 subscription, return a list of metered price info (one per metered subscription item):
    [{"meter_id": "...", "unit_amount": ..., "currency": "usd", "subscription_item_id": "si_xxx", "display_name": "Product Name"}, ...]
    Use unique by meter_id for v2 plan creation; use full list (subscription_item_id) for deleting v1 items.
    """
    metered = []
    items = _get(subscription, "items")
    items_data = _get(items, "data") if items is not None else []
    if not items_data and hasattr(subscription, "items"):
        items_data = getattr(getattr(subscription, "items", None), "data", []) or []
    for item in items_data:
        price = _get(item, "price") or _get(item, "plan")
        if not price:
            continue
        recurring = _get(price, "recurring") or {}
        usage_type = recurring.get("usage_type") if isinstance(recurring, dict) else getattr(recurring, "usage_type", None)
        meter_id = recurring.get("meter") if isinstance(recurring, dict) else getattr(recurring, "meter", None)
        if usage_type != "metered" and not meter_id:
            continue
        meter_id = meter_id or _get(price, "recurring", "meter")
        if not meter_id:
            continue
        item_id = _get(item, "id") or getattr(item, "id", None)
        if not item_id:
            continue
        # Prefer unit_amount_decimal (decimal string in minor units) for exact rates (e.g. $0.009, $0.0015)
        unit_amount_decimal = _get(price, "unit_amount_decimal")
        if unit_amount_decimal is not None and str(unit_amount_decimal).strip() != "":
            unit_amount = str(unit_amount_decimal).strip()
        else:
            unit_amount_raw = _get(price, "unit_amount")
            unit_amount = str(unit_amount_raw) if unit_amount_raw is not None else "0"
        currency = _get(price, "currency") or "usd"
        # Original product name for v2 metered item display_name
        product = _get(price, "product")
        display_name = _get(product, "name") if product else None
        if display_name is None and hasattr(product, "name"):
            display_name = getattr(product, "name", None)
        metered.append({
            "meter_id": meter_id,
            "unit_amount": unit_amount,
            "currency": currency,
            "subscription_item_id": item_id,
            "display_name": display_name,
        })
    return metered


def main():
    subscription_id = args.subscription_id.strip()

    print("=" * 80)
    print("MIGRATION - v1 Subscription + v2 Pricing Plan (metered) on same cadence")
    print("=" * 80)

    # 1. Retrieve subscription and get customer (expand price.product so we get original product names)
    print("\n[1/9] Retrieving v1 subscription...")
    subscription = stripe.Subscription.retrieve(
        subscription_id,
        expand=["items.data.price.product"],
    )
    customer_id = subscription.customer if isinstance(subscription.customer, str) else subscription.customer.id
    print(f"  ✓ Subscription: {subscription.id} (status: {subscription.status})")
    print(f"  ✓ Customer: {customer_id}")

    # Billing period anchor from v1 subscription (so cadence aligns, no period reset)
    anchor_ts = getattr(subscription, "billing_cycle_anchor", None) or _get(subscription, "billing_cycle_anchor")
    if not anchor_ts and hasattr(subscription, "items") and subscription.items and getattr(subscription.items, "data", None):
        first_item = subscription.items.data[0] if subscription.items.data else None
        if first_item:
            anchor_ts = getattr(first_item, "current_period_start", None) or _get(first_item, "current_period_start")
    if anchor_ts:
        anchor_dt = datetime.datetime.utcfromtimestamp(int(anchor_ts))
        billing_day = anchor_dt.day
        billing_month = anchor_dt.month
        billing_hour = anchor_dt.hour
        billing_minute = anchor_dt.minute
        billing_second = anchor_dt.second
    else:
        billing_day = 1
        billing_month = 1
        billing_hour = 0
        billing_minute = 0
        billing_second = 0
    print(f"  ✓ Billing anchor (from v1): month={billing_month}, day={billing_day}, time={billing_hour:02d}:{billing_minute:02d}:{billing_second:02d} UTC")

    # 2. Extract metered prices from v1 subscription
    print("\n[2/9] Extracting metered (usage-based) prices from v1 subscription...")
    metered_prices = extract_metered_prices_from_subscription(subscription)
    if not metered_prices:
        print("  ⚠ No metered prices found on this subscription. Skipping v2 pricing plan creation.")
        print("  Will still create billing profile, cadence, and attach cadence to v1.")
        create_v2_plan = False
    else:
        create_v2_plan = True
        # Unique by meter for v2 plan (one metered item per meter); full list used later to delete v1 items
        unique_metered_for_plan = {}
        for mp in metered_prices:
            if mp["meter_id"] not in unique_metered_for_plan:
                unique_metered_for_plan[mp["meter_id"]] = mp
        for i, mp in enumerate(unique_metered_for_plan.values(), 1):
            name_info = f" — {mp['display_name']!r}" if mp.get("display_name") else ""
            print(f"  ✓ Metered price {i}: meter={mp['meter_id']}, unit_amount={mp['unit_amount']} {mp['currency']}{name_info}")

    # 3. Create collection setting
    print("\n[3/9] Creating Collection Setting...")
    collection_response = client.raw_request(
        "post",
        "/v2/billing/collection_settings",
        collection_method="send_invoice",
        display_name="Migration collection (send invoice)",
    )
    collection_setting = client.deserialize(collection_response, api_mode="V2")
    collection_setting_id = collection_setting.id
    print(f"  ✓ Collection Setting: {collection_setting_id} (send_invoice)")

    # 4. Create billing profile
    print("\n[4/9] Creating Billing Profile...")
    profile_response = client.raw_request(
        "post",
        "/v2/billing/profiles",
        customer=customer_id,
        display_name="Migration Billing Profile",
    )
    billing_profile = client.deserialize(profile_response, api_mode="V2")
    billing_profile_id = billing_profile.id
    print(f"  ✓ Billing Profile: {billing_profile_id}")

    # 5. Create billing cadence (yearly; same day and month as v1 subscription anchor)
    print(f"\n[5/9] Creating Billing Cadence (yearly, month {billing_month} day {billing_day} at {billing_hour:02d}:{billing_minute:02d}:{billing_second:02d} UTC — aligned to v1)...")
    cadence_response = client.raw_request(
        "post",
        "/v2/billing/cadences",
        payer={"billing_profile": billing_profile_id},
        billing_cycle={
            "type": "year",
            "interval_count": 1,
            "year": {
                "month_of_year": billing_month,
                "day_of_month": billing_day,
                "time": {
                    "hour": billing_hour,
                    "minute": billing_minute,
                    "second": billing_second,
                },
            },
        },
        settings={"collection": {"id": collection_setting_id}},
    )
    billing_cadence = client.deserialize(cadence_response, api_mode="V2")
    billing_cadence_id = billing_cadence.id
    print(f"  ✓ Billing Cadence: {billing_cadence_id}")
    print(f"    Interval: Yearly, month={billing_month}, day={billing_day}, time: {billing_hour:02d}:{billing_minute:02d}:{billing_second:02d} UTC (aligned to v1)")

    # 6. Attach billing cadence to v1 subscription
    print("\n[6/9] Attaching Billing Cadence to v1 subscription...")
    attach_response = client.raw_request(
        "post",
        f"/v1/subscriptions/{subscription_id}/attach_cadence",
        billing_cadence=billing_cadence_id,
    )
    client.deserialize(attach_response, api_mode="V1")
    print(f"  ✓ Billing Cadence attached to v1 subscription {subscription_id}")

    pricing_plan_id = None
    pricing_plan_version = None
    v2_subscription_id = None

    if create_v2_plan:
        # 7. Create v2 pricing plan (metered only), rate card, activate
        print("\n[7/9] Creating v2 Pricing Plan (metered only)...")
        plan_response = client.raw_request(
            "post",
            "/v2/billing/pricing_plans",
            display_name="Migration metered plan",
            currency="usd",
            tax_behavior="exclusive",
        )
        pricing_plan = client.deserialize(plan_response, api_mode="V2")
        pricing_plan_id = pricing_plan.id
        print(f"  ✓ Pricing Plan: {pricing_plan_id}")

        metered_items = []
        for i, mp in enumerate(unique_metered_for_plan.values(), 1):
            display_name = mp.get("display_name") or f"Metered usage (migrated) {i}"
            mi_response = client.raw_request(
                "post",
                "/v2/billing/metered_items",
                display_name=display_name,
                meter=mp["meter_id"],
            )
            mi = client.deserialize(mi_response, api_mode="V2")
            metered_items.append({"id": mi.id, "unit_amount": mp["unit_amount"]})
            print(f"  ✓ Metered Item {i}: {mi.id} — {display_name!r} (meter {mp['meter_id']})")

        print("  Creating Rate Card...")
        rate_card_response = client.raw_request(
            "post",
            "/v2/billing/rate_cards",
            display_name="Migration rate card",
            service_interval="year",
            service_interval_count=1,
            currency="usd",
            tax_behavior="exclusive",
        )
        rate_card = client.deserialize(rate_card_response, api_mode="V2")
        rate_card_version = None
        for mi in metered_items:
            rate_resp = client.raw_request(
                "post",
                f"/v2/billing/rate_cards/{rate_card.id}/rates",
                metered_item=mi["id"],
                unit_amount=mi["unit_amount"],
            )
            rate = client.deserialize(rate_resp, api_mode="V2")
            rate_card_version = rate.get("version")
        print(f"  ✓ Rate Card: {rate_card.id}")

        comp_response = client.raw_request(
            "post",
            f"/v2/billing/pricing_plans/{pricing_plan_id}/components",
            type="rate_card",
            rate_card={"id": rate_card.id, "version": rate_card_version},
        )
        client.deserialize(comp_response, api_mode="V2")
        print(f"  ✓ Rate Card attached to Pricing Plan")

        activate_response = client.raw_request(
            "post",
            f"/v2/billing/pricing_plans/{pricing_plan_id}",
            live_version="latest",
        )
        activated = client.deserialize(activate_response, api_mode="V2")
        pricing_plan_version = activated.get("live_version")
        print(f"  ✓ Pricing Plan activated, version: {pricing_plan_version}")

        # 8. Create billing intent to subscribe to v2 plan on same cadence, reserve, commit
        print("\n[8/9] Subscribing customer to v2 Pricing Plan (same cadence)...")
        intent_response = client.raw_request(
            "post",
            "/v2/billing/intents",
            currency="usd",
            cadence=billing_cadence_id,
            actions=[{
                "type": "subscribe",
                "subscribe": {
                    "type": "pricing_plan_subscription_details",
                    "pricing_plan_subscription_details": {
                        "pricing_plan": pricing_plan_id,
                        "pricing_plan_version": pricing_plan_version,
                        "component_configurations": [],
                    },
                },
            }],
        )
        billing_intent = client.deserialize(intent_response, api_mode="V2")
        print(f"  ✓ Billing Intent: {billing_intent.id}")

        reserve_response = client.raw_request(
            "post",
            f"/v2/billing/intents/{billing_intent.id}/reserve",
        )
        client.deserialize(reserve_response, api_mode="V2")
        print(f"  ✓ Billing Intent reserved")

        commit_response = client.raw_request(
            "post",
            f"/v2/billing/intents/{billing_intent.id}/commit",
        )
        committed = client.deserialize(commit_response, api_mode="V2")
        v2_subscription_id = None
        if hasattr(committed, "subscriptions") and committed.subscriptions:
            sub_list = committed.subscriptions
            if isinstance(sub_list, list) and len(sub_list) > 0:
                first = sub_list[0]
                v2_subscription_id = first.get("id") if hasattr(first, "get") else getattr(first, "id", None)
        elif isinstance(committed, dict) and committed.get("subscriptions"):
            subs = committed["subscriptions"]
            if isinstance(subs, list) and len(subs) > 0:
                v2_subscription_id = subs[0].get("id") if isinstance(subs[0], dict) else getattr(subs[0], "id", None)
        print(f"  ✓ Billing Intent committed — v2 subscription active")

        # 9. Remove metered items from v1 subscription (meter is kept; v2 plan uses it)
        print("\n[9/9] Removing metered items from v1 subscription (keeping meter)...")
        for mp in metered_prices:
            si_id = mp.get("subscription_item_id")
            if si_id:
                stripe.SubscriptionItem.delete(si_id)
                print(f"  ✓ Deleted v1 subscription item: {si_id}")
    else:
        print("\n[7/9] Skipping v2 pricing plan (no metered prices).")
        print("[8/9] Skipped.")

    print("\n" + "=" * 80)
    print("DONE")
    print("=" * 80)
    print("\n📋 Summary:")
    print(f"   • v1 Subscription:   {subscription_id} (licensed fees only; metered items removed; cadence attached)")
    print(f"   • Customer:         {customer_id}")
    print(f"   • Collection Setting: {collection_setting_id}")
    print(f"   • Billing Profile:  {billing_profile_id}")
    print(f"   • Billing Cadence:  {billing_cadence_id} (yearly, month {billing_month} day {billing_day} at {billing_hour:02d}:{billing_minute:02d}:{billing_second:02d} UTC — aligned to v1)")
    if create_v2_plan and pricing_plan_id:
        print(f"   • v2 Pricing Plan:   {pricing_plan_id} (v{pricing_plan_version}) — metered only")
        if v2_subscription_id:
            print(f"   • v2 Subscription:   {v2_subscription_id} (on same cadence)")
    print()


if __name__ == "__main__":
    main()
