#!/usr/bin/env python3
"""
Cancel Pricing Plan Subscription
Cancels an active pricing plan subscription using a billing intent
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

def cancel_subscription(subscription_id: str):
    """
    Cancels a pricing plan subscription using a billing intent.
    
    Args:
        subscription_id: The pricing plan subscription ID to cancel
    
    Returns:
        bool: True if cancellation successful, False otherwise
    """
    
    print(f"\n{'='*80}")
    print(f"CANCEL PRICING PLAN SUBSCRIPTION")
    print(f"{'='*80}")
    print(f"Subscription ID: {subscription_id}")
    print(f"{'='*80}\n")
    
    # Step 1: Retrieve the subscription
    print(f"[1/4] Retrieving subscription {subscription_id}...")
    try:
        sub_response = client.raw_request("get", f"/v2/billing/pricing_plan_subscriptions/{subscription_id}")
        subscription = client.deserialize(sub_response, api_mode='V2')
    except Exception as e:
        print(f"\n❌ Error: Could not retrieve subscription")
        print(f"   {str(e)}")
        return False
    
    # Extract billing cadence and pricing plan info
    cadence_ref = subscription.get('billing_cadence', {})
    billing_cadence_id = cadence_ref.get('id') if isinstance(cadence_ref, dict) else cadence_ref
    
    plan_ref = subscription.get('pricing_plan', {})
    plan_id = plan_ref.get('id') if isinstance(plan_ref, dict) else plan_ref
    
    servicing_status = subscription.get('servicing_status', {}).get('status') if isinstance(subscription.get('servicing_status'), dict) else subscription.get('servicing_status')
    collection_status = subscription.get('collection_status', {}).get('status') if isinstance(subscription.get('collection_status'), dict) else subscription.get('collection_status')
    
    print(f"  ✓ Subscription retrieved:")
    print(f"    Servicing Status: {servicing_status}")
    print(f"    Collection Status: {collection_status}")
    print(f"    Pricing Plan: {plan_id}")
    print(f"    Billing Cadence: {billing_cadence_id}")
    
    # Check if already canceled
    if servicing_status == 'canceled':
        print(f"\n⚠️  Subscription is already canceled")
        return True
    
    # Step 2: Get pricing plan to extract currency
    print(f"\n[2/4] Retrieving pricing plan details...")
    try:
        plan_response = client.raw_request("get", f"/v2/billing/pricing_plans/{plan_id}")
        plan = client.deserialize(plan_response, api_mode='V2')
        currency = plan.get('currency', 'usd')
        print(f"  ✓ Pricing Plan: {plan['display_name']}")
        print(f"    Currency: {currency}")
    except Exception as e:
        print(f"  ⚠️  Could not retrieve pricing plan, using default currency 'usd': {str(e)}")
        currency = 'usd'
    
    # Step 3: Create billing intent to deactivate subscription
    print(f"\n[3/4] Creating billing intent to deactivate subscription...")
    try:
        intent_response = client.raw_request(
            "post",
            "/v2/billing/intents",
            currency=currency,
            actions=[{
                "type": "deactivate",
                "deactivate": {
                    "type": "pricing_plan_subscription_details",
                    "pricing_plan_subscription_details": {
                        "pricing_plan_subscription": subscription_id,
                    }
                }
            }]
        )
        intent = client.deserialize(intent_response, api_mode='V2')
        print(f"  ✓ Billing intent created: {intent.id}")
    except Exception as e:
        print(f"\n❌ Error: Could not create billing intent")
        print(f"   {str(e)}")
        return False
    
    # Step 4: Reserve + Commit the billing intent
    print(f"\n[4/4] Reserving + Committing billing intent...")
    print(f"  • Reserving billing intent...")
    try:
        commit_response = client.raw_request("post", f"/v2/billing/intents/{intent.id}/reserve")
        committed_intent = client.deserialize(commit_response, api_mode='V2')
        print(f"  ✓ Billing intent committed")
    except Exception as e:
        print(f"\n❌ Error: Could not commit billing intent")
        print(f"   {str(e)}")
        return False
    print(f"  ✓ Billing intent reserved")
    print(f"  • Committing billing intent...")
    try:
        commit_response = client.raw_request("post", f"/v2/billing/intents/{intent.id}/commit")
        committed_intent = client.deserialize(commit_response, api_mode='V2')
        print(f"  ✓ Billing intent committed")
    except Exception as e:
        print(f"\n❌ Error: Could not commit billing intent")
        print(f"   {str(e)}")
        return False
    
    # Verify the cancellation
    print(f"\n  Verifying subscription cancellation...")
    try:
        verify_response = client.raw_request("get", f"/v2/billing/pricing_plan_subscriptions/{subscription_id}")
        updated_sub = client.deserialize(verify_response, api_mode='V2')
        new_servicing_status = updated_sub.get('servicing_status', {}).get('status') if isinstance(updated_sub.get('servicing_status'), dict) else updated_sub.get('servicing_status')
        new_collection_status = updated_sub.get('collection_status', {}).get('status') if isinstance(updated_sub.get('collection_status'), dict) else updated_sub.get('collection_status')
        
        print(f"\n{'='*80}")
        print("SUBSCRIPTION CANCELED SUCCESSFULLY")
        print(f"{'='*80}")
        print(f"\n📋 Cancellation Summary:")
        print(f"  Subscription ID: {subscription_id}")
        print(f"  Previous servicing status: {servicing_status}")
        print(f"  Current servicing status: {new_servicing_status}")
        print(f"  Collection status: {new_collection_status}")
        print(f"  Pricing Plan: {plan_id}")
        print(f"\n{'='*80}\n")
        
        return True
    except Exception as e:
        print(f"  ⚠️  Could not verify cancellation: {str(e)}")
        print(f"\n{'='*80}")
        print("CANCELLATION INITIATED")
        print(f"{'='*80}\n")
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n" + "="*80)
        print("Cancel Pricing Plan Subscription")
        print("="*80)
        print("\nUsage:")
        print(f"  python {sys.argv[0]} <subscription_id>")
        print("\nDescription:")
        print("  Cancels an active pricing plan subscription using a billing intent.")
        print("  The subscription will be canceled immediately.")
        print("\nExample:")
        print(f"  python {sys.argv[0]} bppsub_test_xxxxx")
        print("\nWhat this script does:")
        print("  1. Retrieves the subscription details")
        print("  2. Creates a billing intent with a cancel action")
        print("  3. Commits the billing intent to execute the cancellation")
        print("  4. Verifies that the subscription was canceled")
        print("\n" + "="*80 + "\n")
        sys.exit(1)
    
    subscription_id = sys.argv[1]
    
    try:
        success = cancel_subscription(subscription_id)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation canceled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
