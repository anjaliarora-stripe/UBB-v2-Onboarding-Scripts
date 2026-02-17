#!/usr/bin/env python3
"""
Update Pricing Plan Service Action and Resubscribe Customer
Increases service action credit grant by $10 and migrates customer to new version
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

def update_pricing_plan_and_resubscribe(pricing_plan_id: str, customer_id: str, increase_amount: int = 1000):
    """
    Creates a new version of pricing plan with increased service action credit grant
    and migrates customer subscription to new version.
    
    Args:
        pricing_plan_id: The pricing plan ID to update
        customer_id: The customer ID to migrate
        increase_amount: Amount to increase in cents (default: 1000 = $10)
    """
    
    print(f"\n{'='*80}")
    print(f"UPDATE PRICING PLAN SERVICE ACTION")
    print(f"{'='*80}")
    print(f"Pricing Plan: {pricing_plan_id}")
    print(f"Customer: {customer_id}")
    print(f"Increase: ${increase_amount/100:.2f}")
    print(f"{'='*80}\n")
    
    # Step 1: Get existing pricing plan and components
    print(f"[1/9] Retrieving pricing plan {pricing_plan_id}...")
    plan_response = client.raw_request("get", f"/v2/billing/pricing_plans/{pricing_plan_id}")
    plan = client.deserialize(plan_response, api_mode='V2')
    print(f"  ✓ Plan: {plan['display_name']}")
    print(f"    Current live version: {plan.get('live_version')}")
    
    # Get components
    print(f"  • Fetching components...")
    components_response = client.raw_request("get", f"/v2/billing/pricing_plans/{pricing_plan_id}/components")
    components = client.deserialize(components_response, api_mode='V2')['data']
    print(f"  ✓ Found {len(components)} component(s)")
    
    # Find service action component
    service_action_component = None
    for component in components:
        if component['type'] == 'service_action':
            service_action_component = component
            print(f"    → Service action component found: {component['id']}")
            break
    
    if not service_action_component:
        print("\n❌ Error: No service action found in pricing plan")
        return False
    
    # Step 2: Get existing service action details
    print(f"\n[2/9] Retrieving existing service action...")
    old_service_action_id = service_action_component['service_action']['id']
    sa_response = client.raw_request("get", f"/v2/billing/service_actions/{old_service_action_id}")
    old_service_action = client.deserialize(sa_response, api_mode='V2')
    
    old_amount = old_service_action['credit_grant']['amount']['monetary']['value']
    new_amount = old_amount + increase_amount
    
    print(f"  ✓ Current service action: {old_service_action_id}")
    print(f"    Type: {old_service_action['type']}")
    print(f"    Current credit grant: ${old_amount/100:.2f}")
    print(f"    New credit grant: ${new_amount/100:.2f}")
    print(f"    Increase: ${increase_amount/100:.2f}")
    
    # Step 3: Delete old service action component
    print(f"\n[3/9] Removing old service action component...")
    component_id = service_action_component['id']
    delete_response = client.raw_request(
        "delete",
        f"/v2/billing/pricing_plans/{pricing_plan_id}/components/{component_id}"
    )
    print(f"  ✓ Old service action component removed: {component_id}")
    print(f"    This creates a new pricing plan version")
    
    # Step 4: Create new service action with increased credit grant
    print(f"\n[4/9] Creating new service action...")
    new_sa_response = client.raw_request(
        "post",
        "/v2/billing/service_actions",
        service_interval=old_service_action['service_interval'],
        service_interval_count=old_service_action['service_interval_count'],
        type=old_service_action['type'],
        credit_grant={
            "amount": {
                "type": "monetary",
                "monetary": {
                    "currency": old_service_action['credit_grant']['amount']['monetary']['currency'],
                    "value": new_amount
                }
            },
            "applicability_config": old_service_action['credit_grant']['applicability_config'],
            "expiry_config": old_service_action['credit_grant']['expiry_config'],
            "name": old_service_action['credit_grant']['name']
        }
    )
    new_service_action = client.deserialize(new_sa_response, api_mode='V2')
    print(f"  ✓ New service action created: {new_service_action.id}")
    print(f"    Credit grant: ${new_amount/100:.2f}")
    
    # Step 5: Attach new service action to pricing plan (creates new version)
    print(f"\n[5/9] Attaching new service action to pricing plan...")
    attach_response = client.raw_request(
        "post",
        f"/v2/billing/pricing_plans/{pricing_plan_id}/components",
        type="service_action",
        service_action={
            "id": new_service_action.id
        }
    )
    print(f"  ✓ New service action attached to pricing plan")
    print(f"    This creates another new pricing plan version")
    
    # Step 6: Activate the new version
    print(f"\n[6/9] Activating new pricing plan version...")
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
    
    # Step 7: Find customer's subscription
    print(f"\n[7/9] Finding customer's subscription...")
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
    
    # Step 8: Create billing intent to migrate to new version
    print(f"\n[8/9] Creating billing intent to migrate subscription...")
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
    
    # Step 9: Verify the change
    print(f"\n[9/9] Verifying subscription update...")
    verify_response = client.raw_request("get", f"/v2/billing/pricing_plan_subscriptions/{customer_subscription['id']}")
    updated_sub = client.deserialize(verify_response, api_mode='V2')
    
    print(f"\n{'='*80}")
    print(f"MIGRATION COMPLETE ✓")
    print(f"{'='*80}")
    print(f"\n📋 Pricing Plan Update:")
    print(f"  Plan ID: {pricing_plan_id}")
    print(f"  Old version: {plan.get('live_version')}")
    print(f"  New version: {new_version}")
    print(f"\n💰 Service Action (Credit Grant) Update:")
    print(f"  Old service action: {old_service_action_id} (${old_amount/100:.2f} credits)")
    print(f"  New service action: {new_service_action.id} (${new_amount/100:.2f} credits)")
    print(f"  Credit increase: ${increase_amount/100:.2f}")
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
        print("python update_pricing_plan_license_fee.py <pricing_plan_id> <customer_id> [increase_amount]")
        print("\nArguments:")
        print("  pricing_plan_id  - Pricing plan ID (e.g., bpp_xxxxx)")
        print("  customer_id      - Customer ID (e.g., cus_xxxxx)")
        print("  increase_amount  - Optional: Credit amount to increase in cents (default: 1000 = $10)")
        print("\nWhat it does:")
        print("  Updates the service action (credit grant) amount in the pricing plan")
        print("  and migrates the customer to the new version.")
        print("\nExamples:")
        print("  # Increase credit grant by $10 (default)")
        print("  python update_pricing_plan_license_fee.py bpp_test_xxxxx cus_xxxxx")
        print("\n  # Increase credit grant by $25")
        print("  python update_pricing_plan_license_fee.py bpp_test_xxxxx cus_xxxxx 2500")
        print("="*80 + "\n")
        sys.exit(1)
    
    pricing_plan_id = sys.argv[1]
    customer_id = sys.argv[2]
    increase_amount = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    
    try:
        success = update_pricing_plan_and_resubscribe(pricing_plan_id, customer_id, increase_amount)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
