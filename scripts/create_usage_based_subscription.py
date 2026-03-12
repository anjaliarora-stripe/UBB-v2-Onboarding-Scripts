#!/usr/bin/env python3
"""
Usage-Based Subscription (Products & Prices) — Annual Scale Plan

Creates a Stripe subscription using Products and Prices with:
- Scale Credits: $12,000/year (fixed, quantity 1)
- Proxy Usage • Proxy Usage (10% discount) Annual: $0.009 per unit (metered, annual)
- Browser Minute Usage • Browser Hour Usage (10% discount) Annual: $0.0015 per unit (metered, annual)

Run once to create the products, prices, meters, and subscription(s). Report usage by
sending meter events (event_name matches each meter); Stripe aggregates and bills at period end.
"""

import os
import sys
import argparse
import time
import json
from dotenv import load_dotenv
import stripe

load_dotenv()

STRIPE_SECRET_KEY_SANDBOX = os.getenv("STRIPE_SECRET_KEY_SANDBOX")
if not STRIPE_SECRET_KEY_SANDBOX:
    raise ValueError(
        "STRIPE_SECRET_KEY_SANDBOX environment variable not set. "
        "Please set it in your environment or create a .env file."
    )
stripe.api_key = STRIPE_SECRET_KEY_SANDBOX

# Product names (exact as in UI)
NAME_SCALE_CREDITS = "Scale Credits"
NAME_PROXY_USAGE = "Proxy Usage • Proxy Usage (10% discount) Annual"
NAME_BROWSER_USAGE = "Browser Minute Usage • Browser Hour Usage (10% discount) Annual"

# Pricing — annual
SCALE_CREDITS_CENTS = 1200000   # $12,000/year
PROXY_UNIT_CENTS = 0.9            # $0.009/unit → 1 cent (smallest unit; exact $0.009 not representable)
BROWSER_UNIT_CENTS = 0.15          # $0.0015/unit → 1 cent (smallest unit)

# Shared with create_credit_burndown.py so meter event names stay unique across runs
COUNTER_FILE = "meter_counter.json"


def get_next_meter_number():
    """Get the next meter number from the counter file (shared with credit burndown script)."""
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, "r") as f:
                data = json.load(f)
                current = data.get("meter_count", 0)
        except (json.JSONDecodeError, KeyError):
            current = 0
    else:
        current = 0
    next_number = current + 1
    with open(COUNTER_FILE, "w") as f:
        json.dump({"meter_count": next_number}, f, indent=2)
    return next_number


parser = argparse.ArgumentParser(
    description="Create Annual Scale Plan subscriptions (Scale Credits + Proxy + Browser usage)"
)
parser.add_argument(
    "num_subscriptions",
    type=int,
    nargs="?",
    default=1,
    help="Number of subscriptions to create (default: 1)",
)
args = parser.parse_args()
num_subscriptions = args.num_subscriptions

if num_subscriptions < 1:
    print("Error: Number of subscriptions must be at least 1")
    sys.exit(1)

all_resources = []


def create_product_and_prices():
    """Create two meters, three products, and three prices (Scale Credits + 2 metered). Returns dict of ids."""
    num1 = get_next_meter_number()
    num2 = get_next_meter_number()
    proxy_event_name = f"proxy_usage_{num1}"
    browser_event_name = f"browser_usage_{num2}"

    print("\n[1/6] Creating Meters (for metered prices)...")
    meter_proxy = stripe.billing.Meter.create(
        display_name=f"Proxy Usage {num1}",
        event_name=proxy_event_name,
        default_aggregation={"formula": "sum"},
        value_settings={"event_payload_key": "quantity"},
        customer_mapping={
            "type": "by_id",
            "event_payload_key": "stripe_customer_id",
        },
    )
    print(f"  ✓ Meter (Proxy): {meter_proxy.id} - event_name '{proxy_event_name}'")

    meter_browser = stripe.billing.Meter.create(
        display_name=f"Browser Usage {num2}",
        event_name=browser_event_name,
        default_aggregation={"formula": "sum"},
        value_settings={"event_payload_key": "quantity"},
        customer_mapping={
            "type": "by_id",
            "event_payload_key": "stripe_customer_id",
        },
    )
    print(f"  ✓ Meter (Browser): {meter_browser.id} - event_name '{browser_event_name}'")

    print("\n[2/6] Creating Product: Scale Credits...")
    product_scale = stripe.Product.create(
        name=NAME_SCALE_CREDITS,
        description="Annual Scale Plan - Scale Credits",
    )
    print(f"  ✓ Product: {product_scale.id} - {product_scale.name}")

    print("\n[3/6] Creating Product: Proxy Usage...")
    product_proxy = stripe.Product.create(
        name=NAME_PROXY_USAGE,
        description="Proxy usage, billed annually per unit",
    )
    print(f"  ✓ Product: {product_proxy.id} - {product_proxy.name}")

    print("\n[4/6] Creating Product: Browser Minute Usage...")
    product_browser = stripe.Product.create(
        name=NAME_BROWSER_USAGE,
        description="Browser minute/hour usage, billed annually per unit",
    )
    print(f"  ✓ Product: {product_browser.id} - {product_browser.name}")

    print("\n[5/6] Creating Prices...")
    price_scale = stripe.Price.create(
        product=product_scale.id,
        currency="usd",
        unit_amount=SCALE_CREDITS_CENTS,
        recurring={"interval": "year"},
    )
    print(f"  ✓ Scale Credits: {price_scale.id} - $12,000.00/year")

    price_proxy = stripe.Price.create(
        product=product_proxy.id,
        currency="usd",
        unit_amount_decimal=PROXY_UNIT_CENTS,
        recurring={
            "interval": "year",
            "usage_type": "metered",
            "meter": meter_proxy.id,
        },
    )
    print(f"  ✓ Proxy Usage: {price_proxy.id} - $0.009 per unit/year (metered)")

    price_browser = stripe.Price.create(
        product=product_browser.id,
        currency="usd",
        unit_amount_decimal=BROWSER_UNIT_CENTS,
        recurring={
            "interval": "year",
            "usage_type": "metered",
            "meter": meter_browser.id,
        },
    )
    print(f"  ✓ Browser Usage: {price_browser.id} - $0.0015 per unit/year (metered)")

    return {
        "meter_proxy_id": meter_proxy.id,
        "meter_browser_id": meter_browser.id,
        "meter_proxy_event_name": proxy_event_name,
        "meter_browser_event_name": browser_event_name,
        "meter_number": num1,
        "product_scale_id": product_scale.id,
        "product_proxy_id": product_proxy.id,
        "product_browser_id": product_browser.id,
        "price_scale_id": price_scale.id,
        "price_proxy_id": price_proxy.id,
        "price_browser_id": price_browser.id,
    }


def create_customer_and_subscription(plan_number, ids):
    """Create a customer and subscription with Scale Credits + Proxy + Browser items. Returns dict or None."""
    try:
        print("\n" + "=" * 80)
        print(f"CREATING SUBSCRIPTION {plan_number} OF {num_subscriptions}")
        print("=" * 80)

        meter_number = ids.get("meter_number", plan_number)
        if num_subscriptions == 1:
            email = f"scale-user{meter_number}@example.com"
            name = f"Scale Plan User {meter_number}"
        else:
            email = f"scale-user{meter_number}-{plan_number}@example.com"
            name = f"Scale Plan User {meter_number}-{plan_number}"

        print("\n[6/6] Creating Customer...")
        customer = stripe.Customer.create(
            email=email,
            name=name,
            description="Annual - Scale Plan 1",
        )
        print(f"  ✓ Customer: {customer.id} - {email}")

        print("     Creating Subscription (Scale Credits + Proxy + Browser)...")
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[
                {"price": ids["price_scale_id"], "quantity": 1},
                {"price": ids["price_proxy_id"]},
                {"price": ids["price_browser_id"]},
            ],
            collection_method="send_invoice",
            days_until_due=30,
            description="Annual - Scale Plan 1",
        )

        proxy_item_id = None
        browser_item_id = None
        for item in subscription["items"]["data"]:
            if item["price"]["id"] == ids["price_proxy_id"]:
                proxy_item_id = item["id"]
            elif item["price"]["id"] == ids["price_browser_id"]:
                browser_item_id = item["id"]

        print(f"  ✓ Subscription: {subscription.id} (status: {subscription.status})")
        print(f"  ✓ Proxy metered item: {proxy_item_id}  |  Browser metered item: {browser_item_id}")

        return {
            "customer_id": customer.id,
            "subscription_id": subscription.id,
            "proxy_subscription_item_id": proxy_item_id,
            "browser_subscription_item_id": browser_item_id,
        }
    except stripe.StripeError as e:
        print(f"\n❌ Error: {e}")
        return None


def main():
    print("=" * 80)
    print("USAGE-BASED SUBSCRIPTION - ANNUAL SCALE PLAN 1")
    print("=" * 80)
    print(f"  Scale Credits: $12,000/year  |  Proxy: $0.009/unit  |  Browser: $0.0015/unit (annual)")
    print(f"\n🔢 Creating {num_subscriptions} subscription(s)...")

    ids = create_product_and_prices()
    success_count = 0
    failed_count = 0

    for i in range(1, num_subscriptions + 1):
        result = create_customer_and_subscription(i, ids)
        if result:
            all_resources.append(result)
            success_count += 1
        else:
            failed_count += 1
        if i < num_subscriptions:
            print("\n⏳ Waiting 2 seconds before next subscription...")
            time.sleep(2)

    print("\n" + "=" * 80)
    print("SETUP COMPLETE")
    print("=" * 80)
    print(f"\n📊 Summary:")
    print(f"   • Total requested: {num_subscriptions}")
    print(f"   • Successfully created: {success_count}")
    print(f"   • Failed: {failed_count}")

    if all_resources:
        print(f"\n📋 Resources:")
        print(f"   • Scale Credits product:  {ids['product_scale_id']}")
        print(f"   • Scale Credits price:   {ids['price_scale_id']} ($12,000/year)")
        print(f"   • Proxy product:         {ids['product_proxy_id']}")
        print(f"   • Proxy price:           {ids['price_proxy_id']} (metered)")
        print(f"   • Proxy meter:           {ids['meter_proxy_id']} (event_name: {ids['meter_proxy_event_name']})")
        print(f"   • Browser product:      {ids['product_browser_id']}")
        print(f"   • Browser price:        {ids['price_browser_id']} (metered)")
        print(f"   • Browser meter:        {ids['meter_browser_id']} (event_name: {ids['meter_browser_event_name']})")
        for i, r in enumerate(all_resources, 1):
            print(f"\n   Subscription {i}:")
            print(f"      • Customer:    {r['customer_id']}")
            print(f"      • Subscription: {r['subscription_id']}")

        print("\n📊 Report usage via meter events:")
        print(f"""
# Proxy usage
stripe.billing.MeterEvent.create(
    event_name="{ids['meter_proxy_event_name']}",
    payload={{"stripe_customer_id": "<customer_id>", "quantity": 1}}
)

# Browser usage
stripe.billing.MeterEvent.create(
    event_name="{ids['meter_browser_event_name']}",
    payload={{"stripe_customer_id": "<customer_id>", "quantity": 1}}
)
""")
    print("=" * 80)


if __name__ == "__main__":
    main()
