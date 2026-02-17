#!/usr/bin/env python3
"""
Update Pricing Plan Rate Card Rates and Resubscribe Customer
Increases each rate in the rate card by $0.01 and migrates customer to new version
"""

from stripe import StripeClient
import stripe
import sys
import os
from dotenv import load_dotenv
load_dotenv()
# Load environment variables
#STRIPE_SECRET_KEY_TEST_MODE = os.getenv('STRIPE_SECRET_KEY_TEST_MODE')
STRIPE_SECRET_KEY_SANDBOX = os.getenv('STRIPE_SECRET_KEY_SANDBOX')

if not STRIPE_SECRET_KEY_SANDBOX:
    raise ValueError(
        "STRIPE_SECRET_KEY_SANDBOX environment variable not set. "
        "Please set it in your environment or create a .env file."
    )

# Initialize clients
client = StripeClient(
    api_key=STRIPE_SECRET_KEY_SANDBOX,
    stripe_version="2026-01-28.preview"
)
stripe.api_key = STRIPE_SECRET_KEY_SANDBOX

def update_rate_card_and_resubscribe(pricing_plan_id: str, customer_id: str, increase_amount: int = 1):
    """
    Creates a new version of rate card with rates increased by specified amount
    and migrates customer subscription to new pricing plan version.

    Args:
        pricing_plan_id: The pricing plan ID to update
        customer_id: The customer ID to migrate
        increase_amount: Amount to increase each rate in cents (default: 1 = $0.01)
    """

    print(f"\n{'='*80}")
    print(f"UPDATE PRICING PLAN RATE CARD RATES")
    print(f"{'='*80}")
    print(f"Pricing Plan: {pricing_plan_id}")
    print(f"Customer: {customer_id}")
    print(f"Increase per rate: ${increase_amount/100:.2f}")
    print(f"{'='*80}\n")

    # Step 1: Get existing pricing plan and components
    print(f"[1/10] Retrieving pricing plan {pricing_plan_id}...")
    plan_response = client.raw_request("get", f"/v2/billing/pricing_plans/{pricing_plan_id}")
    plan = client.deserialize(plan_response, api_mode='V2')
    print(f"  ✓ Plan: {plan['display_name']}")
    print(f"    Current live version: {plan.get('live_version')}")

    # Get components
    print(f"  • Fetching components...")
    components_response = client.raw_request("get", f"/v2/billing/pricing_plans/{pricing_plan_id}/components")
    components = client.deserialize(components_response, api_mode='V2')['data']
    print(f"  ✓ Found {len(components)} component(s)")

    # Find rate card component
    rate_card_component = None
    for component in components:
        if component['type'] == 'rate_card':
            rate_card_component = component
            print(f"    → Rate card component found: {component['id']}")
            break

    if not rate_card_component:
        print("\n❌ Error: No rate card found in pricing plan")
        return False

    # Step 2: Get existing rate card details
    print(f"\n[2/10] Retrieving existing rate card...")
    old_rate_card_id = rate_card_component['rate_card']['id']
    old_rate_card_version = rate_card_component['rate_card'].get('version')

    rc_response = client.raw_request("get", f"/v2/billing/rate_cards/{old_rate_card_id}")
    old_rate_card = client.deserialize(rc_response, api_mode='V2')

    print(f"  ✓ Current rate card: {old_rate_card_id}")
    print(f"    Version: {old_rate_card_version}")
    print(f"    Display name: {old_rate_card['display_name']}")
    print(f"    Service interval: {old_rate_card['service_interval']}")

    # Step 3: Get all rates from the rate card
    print(f"\n[3/10] Retrieving rates from rate card...")
    rates_response = client.raw_request("get", f"/v2/billing/rate_cards/{old_rate_card_id}/rates")
    rates_data = client.deserialize(rates_response, api_mode='V2')
    old_rates = rates_data['data']

    if not old_rates:
        print("\n❌ Error: No rates found in rate card")
        print("\n💡 This rate card has no rates. This usually means:")
        print("   1. The rate card was created but rates were never added")
        print("   2. There was an error during the pricing plan creation")
        print("\n   To fix this, you can:")
        print("   - Create a new pricing plan with rates using create_credit_burndown.py")
        print("   - Or manually add rates to this rate card in the Stripe Dashboard")
        print(f"\n   Rate Card ID: {old_rate_card_id}")
        print(f"   Rate Card Dashboard: https://dashboard.stripe.com/test/billing/rate-cards/{old_rate_card_id}")
        return False

    print(f"  ✓ Found {len(old_rates)} rate(s):")
    for idx, rate in enumerate(old_rates, 1):
        old_amount = rate.get('unit_amount', '0')
        metered_item_ref = rate.get('metered_item', {})
        metered_item_id = metered_item_ref.get('id') if isinstance(metered_item_ref, dict) else metered_item_ref
        print(f"    {idx}. Rate ID: {rate['id']}")
        print(f"       Current amount: ${float(old_amount)/100:.2f}")
        print(f"       Metered item: {metered_item_id}")

    # Step 4: Create new rate card with same configuration
    print(f"\n[4/10] Creating new rate card...")
    new_rc_response = client.raw_request(
        "post",
        "/v2/billing/rate_cards",
        display_name=old_rate_card['display_name'],
        service_interval=old_rate_card['service_interval'],
        service_interval_count=old_rate_card['service_interval_count'],
        currency=old_rate_card['currency'],
        tax_behavior=old_rate_card['tax_behavior']
    )
    new_rate_card = client.deserialize(new_rc_response, api_mode='V2')
    print(f"  ✓ New rate card created: {new_rate_card.id}")

    # Step 5: Add updated rates to new rate card
    print(f"\n[5/10] Adding updated rates to new rate card...")
    new_rate_card_version = None

    for idx, old_rate in enumerate(old_rates, 1):
        old_amount = int(float(old_rate.get('unit_amount', '0')))
        new_amount = old_amount + increase_amount

        # Get metered item ID
        metered_item_ref = old_rate.get('metered_item', {})
        metered_item_id = metered_item_ref.get('id') if isinstance(metered_item_ref, dict) else metered_item_ref

        # Create rate parameters
        rate_params = {
            "metered_item": metered_item_id,
            "unit_amount": str(new_amount)
        }

        # Add tiered pricing if present
        if old_rate.get('type') == 'tiered':
            rate_params['type'] = 'tiered'
            if old_rate.get('tiers'):
                rate_params['tiers'] = old_rate['tiers']

        # Create new rate
        new_rate_response = client.raw_request(
            "post",
            f"/v2/billing/rate_cards/{new_rate_card.id}/rates",
            **rate_params
        )
        new_rate = client.deserialize(new_rate_response, api_mode='V2')
        new_rate_card_version = new_rate.get('version')

        print(f"  ✓ Rate {idx} added:")
        print(f"    Old amount: ${old_amount/100:.2f}")
        print(f"    New amount: ${new_amount/100:.2f}")
        print(f"    Increase: ${increase_amount/100:.2f}")

    print(f"  • New rate card version: {new_rate_card_version}")

    # Step 6: Remove old rate card component from pricing plan
    print(f"\n[6/10] Removing old rate card component from pricing plan...")
    component_id = rate_card_component['id']
    delete_response = client.raw_request(
        "delete",
        f"/v2/billing/pricing_plans/{pricing_plan_id}/components/{component_id}"
    )
    print(f"  ✓ Old rate card component removed: {component_id}")
    print(f"    This creates a new pricing plan version")

    # Step 7: Attach new rate card to pricing plan
    print(f"\n[7/10] Attaching new rate card to pricing plan...")
    attach_response = client.raw_request(
        "post",
        f"/v2/billing/pricing_plans/{pricing_plan_id}/components",
        type="rate_card",
        rate_card={
            "id": new_rate_card.id,
            "version": new_rate_card_version
        }
    )
    print(f"  ✓ New rate card attached to pricing plan")
    print(f"    This creates another new pricing plan version")

    # Step 8: Activate the new version
    print(f"\n[8/10] Activating new pricing plan version...")
    activate_response = client.raw_request(
        "post",
        f"/v2/billing/pricing_plans/{pricing_plan_id}",
        live_version="latest"
    )
    activated_plan = client.deserialize(activate_response, api_mode='V2')
    new_version = activated_plan['live_version']
    print(f"  ✓ New version activated: {new_version}")
    print(f"    Old version: {plan.get('live_version')}")
    print(f"    New version: {new_version}")

    # Step 9: Find customer's subscription
    print(f"\n[9/10] Finding customer's subscription...")
    subs_response = client.raw_request(
        "get",
        "/v2/billing/pricing_plan_subscriptions",
        limit=100
    )
    subs_list = client.deserialize(subs_response, api_mode='V2')

    customer_subscription = None
    billing_cadence_id = None

    for sub in subs_list['data']:
        # Get cadence to check customer
        cadence_ref = sub.get('billing_cadence') or sub.get('cadence')
        if isinstance(cadence_ref, dict):
            cadence_id = cadence_ref['id']
        else:
            cadence_id = cadence_ref

        try:
            cadence_response = client.raw_request("get", f"/v2/billing/cadences/{cadence_id}")
            cadence = client.deserialize(cadence_response, api_mode='V2')

            sub_customer_ref = cadence['payer']['customer']
            if isinstance(sub_customer_ref, dict):
                sub_customer_id = sub_customer_ref['id']
            else:
                sub_customer_id = sub_customer_ref

            # Get pricing plan from subscription
            sub_plan_ref = sub['pricing_plan']
            if isinstance(sub_plan_ref, dict):
                sub_plan_id = sub_plan_ref['id']
            else:
                sub_plan_id = sub_plan_ref

            if sub_customer_id == customer_id and sub_plan_id == pricing_plan_id:
                customer_subscription = sub
                billing_cadence_id = cadence_id
                break
        except Exception as e:
            continue

    if not customer_subscription:
        print(f"\n❌ Error: No subscription found for customer {customer_id} on plan {pricing_plan_id}")
        return False

    print(f"  ✓ Found subscription: {customer_subscription['id']}")
    print(f"    Current version: {customer_subscription.get('pricing_plan_version')}")
    print(f"    Status: {customer_subscription.get('status')}")
    print(f"    Billing cadence: {billing_cadence_id}")

    # Step 10: Create billing intent to migrate to new version
    print(f"\n[10/10] Creating billing intent to migrate subscription...")
    intent_response = client.raw_request(
        "post",
        "/v2/billing/intents",
        cadence=billing_cadence_id,
        currency=plan['currency'],
        actions=[{
            "type": "modify",
            "modify": {
                "type": "pricing_plan_subscription_details",
                "pricing_plan_subscription_details": {
                    "pricing_plan_subscription": customer_subscription['id'],
                    "new_pricing_plan": pricing_plan_id,
                    "new_pricing_plan_version": new_version,
                    "component_configurations": []
                }
            }
        }]
    )
    intent = client.deserialize(intent_response, api_mode='V2')
    print(f"  ✓ Billing intent created: {intent.id}")

    # Reserve the intent
    print(f"  • Reserving billing intent...")
    reserve_response = client.raw_request("post", f"/v2/billing/intents/{intent.id}/reserve")
    print(f"  ✓ Billing intent reserved")

    # Commit the intent
    print(f"  • Committing billing intent...")
    commit_response = client.raw_request("post", f"/v2/billing/intents/{intent.id}/commit")
    print(f"  ✓ Billing intent committed")

    # Verify the change
    print(f"\n  Verifying subscription update...")
    verify_response = client.raw_request("get", f"/v2/billing/pricing_plan_subscriptions/{customer_subscription['id']}")
    updated_sub = client.deserialize(verify_response, api_mode='V2')

    print(f"\n{'='*80}")
    print(f"MIGRATION COMPLETE ✓")
    print(f"{'='*80}")
    print(f"\n📋 Pricing Plan Update:")
    print(f"  Plan ID: {pricing_plan_id}")
    print(f"  Old version: {plan.get('live_version')}")
    print(f"  New version: {new_version}")
    print(f"\n💰 Rate Card Update:")
    print(f"  Old rate card: {old_rate_card_id} (v{old_rate_card_version})")
    print(f"  New rate card: {new_rate_card.id} (v{new_rate_card_version})")
    print(f"  Number of rates updated: {len(old_rates)}")
    print(f"  Rate increase: ${increase_amount/100:.2f} per rate")
    print(f"\n  Rate changes:")
    for idx, old_rate in enumerate(old_rates, 1):
        old_amount = int(float(old_rate.get('unit_amount', '0')))
        new_amount = old_amount + increase_amount
        print(f"    Rate {idx}: ${old_amount/100:.2f} → ${new_amount/100:.2f}")
    print(f"\n👤 Customer Subscription:")
    print(f"  Customer: {customer_id}")
    print(f"  Subscription: {customer_subscription['id']}")
    print(f"  Old version: {customer_subscription.get('pricing_plan_version')}")
    print(f"  New version: {updated_sub.get('pricing_plan_version')}")
    print(f"  Status: {updated_sub.get('status')}")
    print(f"\n{'='*80}\n")

    return True


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("\n" + "="*80)
        print("USAGE")
        print("="*80)
        print("python update_pricing_plan_rate_card.py <pricing_plan_id> <customer_id> [increase_amount]")
        print("\nArguments:")
        print("  pricing_plan_id  - Pricing plan ID (e.g., bpp_xxxxx)")
        print("  customer_id      - Customer ID (e.g., cus_xxxxx)")
        print("  increase_amount  - Optional: Amount to increase each rate in cents (default: 1 = $0.01)")
        print("\nWhat it does:")
        print("  1. Retrieves the pricing plan and its rate card component")
        print("  2. Gets all rates from the rate card")
        print("  3. Creates a new rate card with all rates increased by specified amount")
        print("  4. Updates the pricing plan with the new rate card (creates new version)")
        print("  5. Migrates the customer's subscription to the new pricing plan version")
        print("\nExamples:")
        print("  # Increase all rates by $0.01 (default)")
        print("  python update_pricing_plan_rate_card.py bpp_test_xxxxx cus_xxxxx")
        print("\n  # Increase all rates by $0.05")
        print("  python update_pricing_plan_rate_card.py bpp_test_xxxxx cus_xxxxx 5")
        print("\n  # Increase all rates by $1.00")
        print("  python update_pricing_plan_rate_card.py bpp_test_xxxxx cus_xxxxx 100")
        print("="*80 + "\n")
        sys.exit(1)

    pricing_plan_id = sys.argv[1]
    customer_id = sys.argv[2]
    increase_amount = int(sys.argv[3]) if len(sys.argv) > 3 else 1

    try:
        success = update_rate_card_and_resubscribe(pricing_plan_id, customer_id, increase_amount)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
