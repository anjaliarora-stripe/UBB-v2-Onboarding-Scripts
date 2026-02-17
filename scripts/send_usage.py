from stripe import StripeClient
import stripe
import sys
import os
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

def send_usage_to_pricing_plan(customer_id: str, pricing_plan_id: str, usage_value: int = 10):
    """
    Send usage events to all meters in a pricing plan's rate cards.
    
    Args:
        customer_id: Stripe customer ID
        pricing_plan_id: Stripe pricing plan ID
        usage_value: Value to send for each meter event (default: 10)
    """
    
    print(f"\n{'='*80}")
    print(f"SENDING USAGE TO PRICING PLAN")
    print(f"{'='*80}")
    print(f"Customer ID: {customer_id}")
    print(f"Pricing Plan ID: {pricing_plan_id}")
    print(f"Usage Value: {usage_value}")
    print(f"{'='*80}\n")
    
    # Step 1: Get pricing plan components
    print(f"[1/5] Fetching pricing plan components...")
    try:
        components_response = client.raw_request(
            "get", 
            f"/v2/billing/pricing_plans/{pricing_plan_id}/components"
        )
        components = client.deserialize(components_response, api_mode='V2')['data']
        print(f"  ✓ Found {len(components)} component(s)")
    except Exception as e:
        print(f"  ✗ Error fetching pricing plan: {str(e)}")
        return
    
    # Step 2: Filter for rate card components
    rate_card_components = [c for c in components if c['type'] == 'rate_card']
    print(f"\n[2/5] Filtering rate cards...")
    print(f"  ✓ Found {len(rate_card_components)} rate card(s)")
    
    if not rate_card_components:
        print("\n⚠ No rate cards found in pricing plan. Nothing to do.")
        return
    
    meters_to_send = {}  # {meter_id: {event_name, display_name}}
    
    # Step 3: For each rate card, get its rates
    print(f"\n[3/5] Processing rate cards and rates...")
    for component in rate_card_components:
        rate_card_id = component['rate_card']['id']
        print(f"\n  Rate Card: {rate_card_id}")
        
        try:
            # Get rates for this rate card
            rates_response = client.raw_request(
                "get",
                f"/v2/billing/rate_cards/{rate_card_id}/rates"
            )
            rates = client.deserialize(rates_response, api_mode='V2')['data']
            print(f"    • Found {len(rates)} rate(s)")
            
            # Step 4: For each rate, get the metered item and meter
            for rate in rates:
                metered_item_id = rate['metered_item']
                if isinstance(metered_item_id, dict):
                    metered_item_id = metered_item_id['id']
                
                # Get metered item to find the meter
                mi_response = client.raw_request(
                    "get",
                    f"/v2/billing/metered_items/{metered_item_id}"
                )
                metered_item = client.deserialize(mi_response, api_mode='V2')
                
                meter_id = metered_item['meter']
                if isinstance(meter_id, dict):
                    meter_id = meter_id['id']
                
                # Get meter to find event_name
                stripe.api_key = STRIPE_SECRET_KEY_SANDBOX
                meter = stripe.billing.Meter.retrieve(meter_id)
                
                meters_to_send[meter_id] = {
                    'event_name': meter['event_name'],
                    'display_name': meter['display_name']
                }
                print(f"      → Rate: {rate.get('display_name', 'Unnamed')} -> Meter: {meter['display_name']}")
        
        except Exception as e:
            print(f"    ✗ Error processing rate card: {str(e)}")
            continue
    
    # Step 5: Send meter events for each unique meter
    print(f"\n[4/5] Preparing to send usage events...")
    print(f"  ✓ {len(meters_to_send)} unique meter(s) identified")
    
    print(f"\n[5/5] Sending meter events...")
    print(f"{'='*80}\n")
    
    success_count = 0
    error_count = 0
    
    for meter_id, meter_info in meters_to_send.items():
        event_name = meter_info['event_name']
        display_name = meter_info['display_name']
        
        # Get dimension configuration from config
        dimension_keys = METER_CONFIG.get('dimension_payload_keys', [])
        dimension_values_map = METER_CONFIG.get('dimension_values', {})
        
        # If meter has dimensions, send one event per dimension value combination
        if dimension_keys:
            # For now, we support one dimension key (can be extended for multiple)
            dimension_key = dimension_keys[0]
            dimension_values = dimension_values_map.get(dimension_key, ['default'])
            
            for dimension_value in dimension_values:
                # Build payload with dimension
                payload = {
                    'stripe_customer_id': customer_id,
                    'tokens_used': str(usage_value),  # Use the correct event_payload_key
                    dimension_key: dimension_value     # Add dimension (e.g., 'model': 'basic')
                }
                
                # Send meter event
                try:
                    event = stripe.billing.MeterEvent.create(
                        event_name=event_name,
                        payload=payload
                    )
                    print(f"✓ Sent usage to '{display_name}' ({dimension_key}={dimension_value})")
                    print(f"  Event Name: {event_name}")
                    print(f"  Event ID: {event.identifier}")
                    print(f"  Value: {usage_value}")
                    print(f"  Dimension: {dimension_key}={dimension_value}\n")
                    success_count += 1
                except Exception as e:
                    print(f"✗ Error sending to '{display_name}' ({dimension_key}={dimension_value}): {str(e)}\n")
                    error_count += 1
        else:
            # No dimensions - send single event
            try:
                event = stripe.billing.MeterEvent.create(
                    event_name=event_name,
                    payload={
                        'stripe_customer_id': customer_id,
                        'tokens_used': str(usage_value)
                    }
                )
                print(f"✓ Sent usage to '{display_name}'")
                print(f"  Event Name: {event_name}")
                print(f"  Event ID: {event.identifier}")
                print(f"  Value: {usage_value}\n")
                success_count += 1
            except Exception as e:
                print(f"✗ Error sending to '{display_name}': {str(e)}\n")
                error_count += 1
    
    # Summary
    print(f"{'='*80}")
    print(f"USAGE SENDING COMPLETE")
    print(f"{'='*80}")
    print(f"✓ Success: {success_count}")
    if error_count > 0:
        print(f"✗ Errors: {error_count}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("\n" + "="*80)
        print("USAGE")
        print("="*80)
        print("python send_usage.py <customer_id> <pricing_plan_id> [usage_value]")
        print("\nArguments:")
        print("  customer_id    - Stripe customer ID (e.g., cus_xxxxx)")
        print("  pricing_plan_id - Stripe pricing plan ID (e.g., bpp_xxxxx)")
        print("  usage_value    - Optional: Usage value to send (default: 10)")
        print("\nExample:")
        print("  python send_usage.py cus_test_123 bpp_test_456")
        print("  python send_usage.py cus_test_123 bpp_test_456 25")
        print("="*80 + "\n")
        sys.exit(1)
    
    customer_id = sys.argv[1]
    pricing_plan_id = sys.argv[2]
    usage_value = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    
    send_usage_to_pricing_plan(customer_id, pricing_plan_id, usage_value)
