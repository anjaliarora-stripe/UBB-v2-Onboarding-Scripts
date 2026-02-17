#!/usr/bin/env python3

"""
Credit Burndown Model - Complete Implementation
Creates a pricing plan subscription with credit-based billing where:
- Customers receive credits upfront
- Credits burn down as they use the service
- Alerts trigger when credits run low
- Customers can top up to continue service

Subscription Flow: Uses Billing Intents (not Checkout Sessions)
- Creates billing profile and billing cadence
- Subscribes customer via billing intent
- Activates subscription by committing the billing intent
"""

from stripe import StripeClient
import stripe
import time
import json
import sys
import os
import argparse
from config import METER_CONFIG
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

# Get number of plans to create from command line argument
parser = argparse.ArgumentParser(description='Create Credit Burndown pricing plans')
parser.add_argument('num_plans', type=int, nargs='?', default=1, 
                    help='Number of pricing plans to create (default: 1)')
parser.add_argument('--checkout', action='store_true', 
                    help='Use Checkout Session instead of Billing Intent')
args = parser.parse_args()

num_plans = args.num_plans
use_checkout = args.checkout

if num_plans < 1:
    print("Error: Number of plans must be at least 1")
    sys.exit(1)

print("=" * 80)
print("CREDIT BURNDOWN MODEL - COMPLETE SETUP")
print("=" * 80)
print(f"Mode: {'Checkout Session' if use_checkout else 'Billing Intent (Programmatic)'}")
print(f"\n🔢 Creating {num_plans} pricing plan(s) and subscription(s)...")

# Store IDs for all created resources
all_resources = []

# Track meter counter across runs
COUNTER_FILE = 'meter_counter.json'

def get_next_meter_number():
    """Get the next meter number from the counter file."""
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, 'r') as f:
                data = json.load(f)
                current = data.get('meter_count', 0)
        except (json.JSONDecodeError, KeyError):
            current = 0
    else:
        current = 0
    
    # Increment for next use
    next_number = current + 1
    
    # Save the new count
    with open(COUNTER_FILE, 'w') as f:
        json.dump({'meter_count': next_number}, f, indent=2)
    
    return next_number

def create_checkout_session_for_pricing_plan(customer_id, pricing_plan_id, pricing_plan_version, customer_email):
    """
    Create a checkout session for pricing plan subscription.
    Uses the checkout_product_catalog_preview to support pricing plans.
    """
    print("\n[10/11] Creating Checkout Session...")
    
    # Create a temporary client with checkout preview version
    import requests
    
    response = requests.post(
        'https://api.stripe.com/v1/checkout/sessions',
        auth=(STRIPE_SECRET_KEY_SANDBOX, ''),
        headers={
            'Stripe-Version': '2026-01-28.preview;checkout_product_catalog_preview=v1'
        },
        data={
            'checkout_items[0][type]': 'pricing_plan_subscription_item',
            'checkout_items[0][pricing_plan_subscription_item][pricing_plan]': pricing_plan_id,
            'checkout_items[0][pricing_plan_subscription_item][pricing_plan_version]': pricing_plan_version,
            'success_url': 'https://example.com/success?session_id={CHECKOUT_SESSION_ID}',
            'cancel_url': 'https://example.com/cancel',
            'customer': customer_id,
            'payment_method_data[allow_redisplay]': 'always'
        }
    )
    
    if response.status_code != 200:
        raise Exception(f"Failed to create checkout session: {response.text}")
    
    return response.json()

def create_pricing_plan_and_subscription(plan_number):
    """Create a complete pricing plan and subscription."""
    
    print(f"\n{'=' * 80}")
    print(f"CREATING PLAN {plan_number} OF {num_plans}")
    print(f"{'=' * 80}")
    
    # Store IDs for this specific plan
    ids = {}
    
    try:
        # Get the meter number for this run
        meter_number = get_next_meter_number()
        print(f"\n🔢 Using Meter Number: {meter_number}")
    
        # ============================================================================
        # STEP 1: Create Pricing Plan
        # ============================================================================
        print("\n[1/11] Creating Pricing Plan...")
    
        plan_name = f"Credit Burndown Plan {meter_number}" if meter_number > 1 else "Credit Burndown Plan"
        pricing_plan_response = client.raw_request(
            "post",
            "/v2/billing/pricing_plans",
            display_name=plan_name,
            currency="usd",
            tax_behavior="exclusive"
        )
        pricing_plan = client.deserialize(pricing_plan_response, api_mode='V2')
        ids['pricing_plan_id'] = pricing_plan.id
        print(f"  ✓ Pricing Plan Created: {pricing_plan.id} - '{plan_name}'")

        # ============================================================================
        # STEP 2: Create Meter (tracks usage)
        # ============================================================================
        print("\n[2/11] Creating Meter...")
        
        # Use the v1 billing meters API via StripeClient
        meter_name = f"Meter {meter_number}" if meter_number > 1 else "Meter"
        
        # Get dimension configuration from config
        dimension_payload_keys = METER_CONFIG.get('dimension_payload_keys', [])
        
        meter = client.billing.meters.create({
            "display_name": meter_name,
            "event_name": f"token_usage_{meter_number}",
            "default_aggregation": {"formula": "sum"},
            "value_settings": {"event_payload_key": "tokens_used"},
            "dimension_payload_keys": dimension_payload_keys
        })
        ids['meter_id'] = meter.id
        ids['meter_number'] = meter_number
        print(f"  ✓ Meter Created: {meter.id} - '{meter_name}'")
        if dimension_payload_keys:
            print(f"    Dimensions: {', '.join(dimension_payload_keys)}")

        # ============================================================================
        # STEP 3: Create Metered Items (billable items)
        # ============================================================================
        print("\n[3/11] Creating Metered Items...")
        
        # Get dimension values from config
        dimension_values_map = METER_CONFIG.get('dimension_values', {})
        
        # Store metered item IDs
        metered_items = []
        
        # Create one metered item per dimension value
        if dimension_payload_keys and dimension_values_map:
            dimension_key = dimension_payload_keys[0]  # Support first dimension
            dimension_values = dimension_values_map.get(dimension_key, [])
            
            for idx, dimension_value in enumerate(dimension_values, 1):
                display_name = f"{dimension_value.capitalize()} Model Tokens"
                
                metered_item_response = client.raw_request(
                    "post",
                    "/v2/billing/metered_items",
                    display_name=display_name,
                    meter=meter.id,
                    meter_segment_conditions=[
                        {
                            "dimension": dimension_key,
                            "value": dimension_value
                        }
                    ]
                )
                metered_item = client.deserialize(metered_item_response, api_mode='V2')
                metered_items.append({
                    'id': metered_item.id,
                    'dimension_value': dimension_value,
                    'display_name': display_name
                })
                ids[f'metered_item_{idx}_id'] = metered_item.id
                print(f"  ✓ Metered Item {idx} ({dimension_value.capitalize()}): {metered_item.id}")
        else:
            # No dimensions - create single metered item
            metered_item_response = client.raw_request(
                "post",
                "/v2/billing/metered_items",
                display_name="Token Usage",
                meter=meter.id
            )
            metered_item = client.deserialize(metered_item_response, api_mode='V2')
            metered_items.append({
                'id': metered_item.id,
                'dimension_value': None,
                'display_name': 'Token Usage'
            })
            ids['metered_item_1_id'] = metered_item.id
            print(f"  ✓ Metered Item: {metered_item.id}")

        # ============================================================================
        # STEP 4: Create Rate Card
        # ============================================================================
        print("\n[4/11] Creating Rate Card...")
        
        rate_card_response = client.raw_request(
            "post",
            "/v2/billing/rate_cards",
            display_name="Token Rate Card",
            service_interval="month",
            service_interval_count=1,
            currency="usd",
            tax_behavior="exclusive"
        )
        rate_card = client.deserialize(rate_card_response, api_mode='V2')
        ids['rate_card_id'] = rate_card.id
        print(f"  ✓ Rate Card Created: {rate_card.id}")

        # ============================================================================
        # STEP 5: Add Rates to Rate Card
        # ============================================================================
        print("\n[5/11] Adding Rates to Rate Card...")
        
        # Define pricing per dimension value (cents)
        pricing_map = {
            'basic': '5',     # $0.05 per token
            'premium': '10'   # $0.10 per token
        }
        
        # Add one rate per metered item
        rate_card_version = None
        for idx, metered_item_info in enumerate(metered_items, 1):
            dimension_value = metered_item_info['dimension_value']
            metered_item_id = metered_item_info['id']
            
            # Get pricing for this dimension value
            unit_amount = pricing_map.get(dimension_value, '5') if dimension_value else '5'
            
            rate_response = client.raw_request(
                "post",
                f"/v2/billing/rate_cards/{rate_card.id}/rates",
                metered_item=metered_item_id,
                unit_amount=unit_amount
            )
            rate = client.deserialize(rate_response, api_mode='V2')
            rate_card_version = rate.get('version')
            
            price_display = f"${int(unit_amount)/100:.2f}"
            dimension_display = f" per {dimension_value} token" if dimension_value else " per token"
            print(f"  ✓ Rate {idx} Added: {price_display}{dimension_display}")
        
        ids['rate_card_version'] = rate_card_version

        # ============================================================================
        # STEP 6: Attach Rate Card to Pricing Plan
        # ============================================================================
        print("\n[6/11] Attaching Rate Card to Pricing Plan...")
        
        component_response = client.raw_request(
            "post",
            f"/v2/billing/pricing_plans/{pricing_plan.id}/components",
            type="rate_card",
            rate_card={
                "id": rate_card.id,
                "version": ids['rate_card_version']
            }
        )
        print(f"  ✓ Rate Card Attached to Pricing Plan")

        # ============================================================================
        # STEP 7: Activate Pricing Plan
        # ============================================================================
        print("\n[7/11] Activating Pricing Plan...")
        
        activate_response = client.raw_request(
            "post",
            f"/v2/billing/pricing_plans/{pricing_plan.id}",
            live_version="latest"
        )
        activated_plan = client.deserialize(activate_response, api_mode='V2')
        pricing_plan_version = activated_plan.get('live_version')
        ids['pricing_plan_version'] = pricing_plan_version
        print(f"  ✓ Pricing Plan Activated")
        print(f"  Live Version: {pricing_plan_version}")

        # ============================================================================
        # STEP 8: Create Test Clock + Customer
        # ============================================================================
        print("\n[8/11] Creating Test Clock...")
        
        test_clock = client.test_helpers.test_clocks.create({
            #add a time offset of 1 day
            "frozen_time": int(time.time()) + 86400
        })
        ids['test_clock_id'] = test_clock.id
        print(f"  ✓ Test Clock Created: {test_clock.id}")
        
        print("\n[8/11] Creating Customer...")
        
        customer_email = f"testuser{meter_number}@example.com" if meter_number > 1 else "testuser@example.com"
        customer = client.customers.create({
            "email": customer_email,
            "name": f"Test User {meter_number}" if meter_number > 1 else "Test User",
            "description": "Credit burndown test customer",
            "test_clock": test_clock.id
        })
        ids['customer_id'] = customer.id
        print(f"  ✓ Customer Created: {customer.id} - {customer_email}")

        # ============================================================================
        # CONDITIONAL: Checkout Session OR Billing Intent Flow
        # ============================================================================
        
        if use_checkout:
            # ========================================================================
            # CHECKOUT SESSION FLOW
            # ========================================================================
            checkout_session = create_checkout_session_for_pricing_plan(
                customer_id=customer.id,
                pricing_plan_id=pricing_plan.id,
                pricing_plan_version=pricing_plan_version,
                customer_email=customer_email
            )
            
            ids['checkout_session_id'] = checkout_session['id']
            ids['checkout_session_url'] = checkout_session['url']
            
            print(f"  ✓ Checkout Session Created: {checkout_session['id']}")
            print(f"\n  {'='*76}")
            print(f"  🔗 CHECKOUT URL:")
            print(f"  {checkout_session['url']}")
            print(f"  {'='*76}")
            print(f"  📋 Copy the URL above and open it in your browser to complete subscription")
            print(f"  {'='*76}\n")
            
        else:
            # ========================================================================
            # BILLING INTENT FLOW (Programmatic)
            # ========================================================================

            # STEP 9: Create Billing Profile
            print("\n[9/13] Creating Billing Profile...")
            
            billing_profile_response = client.raw_request(
                "post",
                "/v2/billing/profiles",
                customer=customer.id,
                display_name="Primary Billing Profile"
            )
            billing_profile = client.deserialize(billing_profile_response, api_mode='V2')
            ids['billing_profile_id'] = billing_profile.id
            print(f"  ✓ Billing Profile Created: {billing_profile.id}")

            # STEP 10: Create Billing Cadence (Monthly)
            print("\n[10/13] Creating Billing Cadence...")
            
            billing_cadence_response = client.raw_request(
                "post",
                "/v2/billing/cadences",
                payer={
                    "billing_profile": billing_profile.id
                },
                billing_cycle={
                    "type": "month",
                    "interval_count": 1
                }
            )
            billing_cadence = client.deserialize(billing_cadence_response, api_mode='V2')
            ids['billing_cadence_id'] = billing_cadence.id
            print(f"  ✓ Billing Cadence Created: {billing_cadence.id}")
            print(f"  Interval: Monthly")

            # STEP 11: Create Billing Intent
            print("\n[11/13] Creating Billing Intent...")
            
            billing_intent_response = client.raw_request(
                "post",
                "/v2/billing/intents",
                currency="usd",
                cadence=billing_cadence.id,
                actions=[{
                    "type": "subscribe",
                    "subscribe": {
                        "type": "pricing_plan_subscription_details",
                        "pricing_plan_subscription_details": {
                            "pricing_plan": pricing_plan.id,
                            "pricing_plan_version": pricing_plan_version
                        }
                    }
                }]
            )
            billing_intent = client.deserialize(billing_intent_response, api_mode='V2')
            ids['billing_intent_id'] = billing_intent.id
            print(f"  ✓ Billing Intent Created: {billing_intent.id}")

            # STEP 12: Commit Billing Intent (Activate Subscription)
            print("\n[12/13] Reserving Billing Intent (Activating Subscription)...")
            
            commit_response = client.raw_request(
                "post",
                f"/v2/billing/intents/{billing_intent.id}/reserve"
            )
            committed_intent = client.deserialize(commit_response, api_mode='V2')
            print(f"  ✓ Billing Intent Reserved")


            print("\n[12/13] Committing Billing Intent (Activating Subscription)...")
            
            commit_response = client.raw_request(
                "post",
                f"/v2/billing/intents/{billing_intent.id}/commit"
            )
            committed_intent = client.deserialize(commit_response, api_mode='V2')
            print(f"  ✓ Billing Intent Committed")
            print(f"  ✓ Subscription Activated!")

        # ============================================================================
        # STEP 13: Grant Initial Credits
        # ============================================================================
        print("\n[13/13] Granting Initial Credits to Customer...")
        
        credit_grant = client.billing.credit_grants.create({
            "amount": {
                "type": "monetary",
                "monetary": {
                    "currency": "usd",
                    "value": 1000  # $10.00 worth of credits
                }
            },
            "applicability_config": {"scope": {"price_type": "metered"}},
            "category": "paid",
            "customer": customer.id,
            "name": "Initial Welcome Credits"
        })
        ids['credit_grant_id'] = credit_grant.id
        print(f"  ✓ Credit Grant Created: {credit_grant.id}")
        print(f"  ✓ Granted $10.00 worth of credits")

        # ============================================================================
        # STEP 14: Set Up Low Balance Alert
        # ============================================================================
        print("\n[14/14] Setting Up Low Balance Alert...")
        
        alert = stripe.billing.Alert.create(
            alert_type="credit_balance_threshold",
            title="Credit Balance Low Alert",
            credit_balance_threshold={
                "lte": {
                    "balance_type": "monetary",
                    "monetary": {
                        "value": 100,  # Alert when balance drops to $1.00
                        "currency": "usd"
                    }
                }
            },
        )
        ids['alert_id'] = alert.id
        print(f"  ✓ Alert Created: {alert.id}")
        print(f"  ✓ Will trigger when balance drops below $1.00")

        # ============================================================================
        # SUMMARY
        # ============================================================================
        print("\n" + "=" * 80)
        print("SETUP COMPLETE - CREDIT BURNDOWN MODEL READY")
        print("=" * 80)
        
        print("\n📋 Created Resources:")
        print(f"  • Pricing Plan:    {ids['pricing_plan_id']} (v{ids['pricing_plan_version']})")
        meter_display = f"Meter {ids['meter_number']}" if ids['meter_number'] > 1 else "Meter"
        print(f"  • Meter:           {ids['meter_id']} - '{meter_display}'")
        print(f"  • Metered Item 1:  {ids['metered_item_1_id']}")
        print(f"  • Metered Item 2:  {ids['metered_item_2_id']}")
        print(f"  • Rate Card:       {ids['rate_card_id']}")
        print(f"  • Customer:        {ids['customer_id']}")
        
        # Conditional: Only show these if using billing intent flow
        if use_checkout:
            print(f"  • Checkout Session: {ids['checkout_session_id']}")
            print(f"  • Checkout URL:     {ids['checkout_session_url']}")
        else:
            print(f"  • Billing Profile: {ids['billing_profile_id']}")
            print(f"  • Billing Cadence: {ids['billing_cadence_id']}")
            print(f"  • Billing Intent:  {ids['billing_intent_id']}")
        
        print(f"  • Credit Grant:    {ids['credit_grant_id']}")
        print(f"  • Alert:           {ids['alert_id']}")
        
        print("\n💰 Pricing Structure:")
        print("  • Basic Model:    $0.05 per token")
        print("  • Premium Model:  $0.10 per token")
        print("  • Initial Credits: $10.00")
        print("  • Alert Threshold: $1.00")
        
        print("\n📊 Next Steps - Report Usage:")
        print(f"""
# Example: Report basic model usage (100 tokens)
stripe.billing.MeterEvent.create(
        event_name="token_usage_{ids['meter_number']}",
        payload={{
            "stripe_customer_id": "{ids['customer_id']}",
            "model": "basic",
            "tokens_used": 100
        }}
)

# Example: Report premium model usage (50 tokens)
stripe.billing.MeterEvent.create(
        event_name="token_usage_{ids['meter_number']}",
        payload={{
            "stripe_customer_id": "{ids['customer_id']}",
            "model": "premium",
            "tokens_used": 50
        }}
)
        """)
        
        print("\n🔔 Webhook Events to Monitor:")
        print("  • billing.alert.triggered - When credits drop below threshold")
        print("  • billing.alert.recovered - When credits go back above threshold")
        print("  • v2.billing.pricing_plan_subscription.servicing_activated")
        print("  • v2.billing.pricing_plan_subscription.servicing_canceled")
    
    except Exception as e:
        print(f"\n❌ Error creating plan {plan_number}: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return None

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print(f"\nStarting creation of {num_plans} pricing plan(s)...\n")
    
    success_count = 0
    failed_count = 0
    
    for i in range(1, num_plans + 1):
        result = create_pricing_plan_and_subscription(i)
        
        if result:
            all_resources.append(result)
            success_count += 1
        else:
            failed_count += 1
        
        # Add a small delay between creations to avoid rate limiting
        if i < num_plans:
            print(f"\n⏳ Waiting 2 seconds before creating next plan...")
            time.sleep(2)
    
    # Final Summary
    print("\n" + "=" * 80)
    print("ALL PLANS CREATION COMPLETE")
    print("=" * 80)
    print(f"\n📊 Summary:")
    print(f"   • Total plans requested: {num_plans}")
    print(f"   • Successfully created: {success_count}")
    print(f"   • Failed: {failed_count}")
    
    if all_resources:
        print(f"\n📋 Created Resources:")
        for i, resource in enumerate(all_resources, 1):
            print(f"\n   Plan {i}:")
            print(f"      • Pricing Plan: {resource.get('pricing_plan_id')}")
            print(f"      • Customer: {resource.get('customer_id')}")
            print(f"      • Meter: {resource.get('meter_id')}")
            print(f"      • Subscription: Active")
        
        # Save all resources summary
        '''with open('all_credit_burndown_plans.json', 'w') as f:
            json.dump(all_resources, f, indent=2)
        print(f"\n💾 All resources summary saved to: all_credit_burndown_plans.json")'''
    
    print("\n" + "=" * 80)
