# Credit Burndown Model Scripts

This repository contains scripts for implementing a credit burndown billing model using Stripe's pricing plans and billing intents.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   
   Copy the example file:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Stripe API keys:
   ```
   STRIPE_SECRET_KEY_SANDBOX=sk_test_your_sandbox_key_here
   ```

   **Important:** Never commit the `.env` file to git!

## Scripts
```

### `create_credit_burndown.py`

Creates a complete credit burndown pricing plan with:
- Pricing plan with rate cards for usage-based billing
- Metered items for tracking usage
- Customer with billing profile and cadence
- Subscription via billing intent
- Low balance alerts

**Usage:**
```bash
python scripts/create_credit_burndown.py [num_plans] [--checkout]
```

**Arguments:**
- `num_plans` - Optional: Number of pricing plans to create (default: 1)
- `--checkout` - Optional: Use Checkout Session instead of Billing Intent

**Examples:**
```bash
# Create one pricing plan
python scripts/create_credit_burndown.py

# Create 3 pricing plans
python scripts/create_credit_burndown.py 3

# Create using Checkout Session
python scripts/create_credit_burndown.py 1 --checkout
```

### `create_credit_burndown_free_credits.py`

Creates a credit burndown pricing plan with a service action that grants free welcome credits:
- Pricing plan with rate cards for usage-based billing
- Service action that grants $10 in free credits monthly
- Customer with billing profile and cadence
- Subscription via billing intent
- Low balance alerts

**Usage:**
```bash
python scripts/create_credit_burndown_free_credits.py [num_plans] [--checkout]
```

**Arguments:**
- `num_plans` - Optional: Number of pricing plans to create (default: 1)
- `--checkout` - Optional: Use Checkout Session instead of Billing Intent

**Examples:**
```bash
# Create one pricing plan with free credits
python scripts/create_credit_burndown_free_credits.py

# Create 2 pricing plans with free credits
python scripts/create_credit_burndown_free_credits.py 2
```

### `send_usage.py`

Sends usage events to all meters in a pricing plan's rate cards for testing credit burndown.

**Usage:**
```bash
python scripts/send_usage.py <customer_id> <pricing_plan_id> [usage_value]
```

**Arguments:**
- `customer_id` - Stripe customer ID (e.g., `cus_xxxxx`)
- `pricing_plan_id` - Stripe pricing plan ID (e.g., `bpp_xxxxx`)
- `usage_value` - Optional: Usage value to send to each meter (default: 10)

**Examples:**
```bash
# Send default usage (10) to all meters
python scripts/send_usage.py cus_TuGbfYg1CU3aUm bpp_test_61U2F4

# Send custom usage value (25) to all meters
python scripts/send_usage.py cus_TuGbfYg1CU3aUm bpp_test_61U2F4 25
```

### `update_pricing_plan_rate_card.py`

Updates a pricing plan by increasing all rate card rates and migrates the customer to the new version.

**Usage:**
```bash
python scripts/update_pricing_plan_rate_card.py <pricing_plan_id> <customer_id> [increase_amount]
```

**Arguments:**
- `pricing_plan_id` - Pricing plan ID (e.g., `bpp_xxxxx`)
- `customer_id` - Customer ID to migrate (e.g., `cus_xxxxx`)
- `increase_amount` - Optional: Amount to increase each rate in cents (default: 1 = $0.01)

**What it does:**
1. Retrieves the pricing plan and its rate card component
2. Gets all rates from the rate card
3. Creates a new rate card with all rates increased by specified amount
4. Updates the pricing plan with the new rate card (creates new version)
5. Migrates the customer's subscription to the new pricing plan version

**Examples:**
```bash
# Increase all rates by $0.01 (default)
python scripts/update_pricing_plan_rate_card.py bpp_test_xxxxx cus_xxxxx

# Increase all rates by $0.05
python scripts/update_pricing_plan_rate_card.py bpp_test_xxxxx cus_xxxxx 5
```

### `update_pricing_plan_service_action.py`

Updates a pricing plan by increasing the service action credit grant and migrates the customer to the new version.

**Usage:**
```bash
python scripts/update_pricing_plan_service_action.py <pricing_plan_id> <customer_id> [increase_amount]
```

**Arguments:**
- `pricing_plan_id` - Pricing plan ID (e.g., `bpp_xxxxx`)
- `customer_id` - Customer ID to migrate (e.g., `cus_xxxxx`)
- `increase_amount` - Optional: Amount to increase credit grant in cents (default: 1000 = $10)

**What it does:**
1. Retrieves the pricing plan and service action component
2. Creates a new service action with increased credit grant
3. Updates the pricing plan with the new service action (creates new version)
4. Migrates the customer's subscription to the new pricing plan version

**Examples:**
```bash
# Increase credit grant by $10 (default)
python scripts/update_pricing_plan_service_action.py bpp_test_xxxxx cus_xxxxx

# Increase credit grant by $25
python scripts/update_pricing_plan_service_action.py bpp_test_xxxxx cus_xxxxx 2500
```

### `cancel_subscription.py`

Cancels an active pricing plan subscription using a billing intent.

**Usage:**
```bash
python scripts/cancel_subscription.py <subscription_id>
```

**Arguments:**
- `subscription_id` - The pricing plan subscription ID to cancel (e.g., `bppsub_test_xxxxx`)

**What it does:**
1. Retrieves the subscription details
2. Creates a billing intent with a cancel action
3. Commits the billing intent to execute the cancellation
4. Verifies that the subscription was canceled

**Example:**
```bash
python scripts/cancel_subscription.py bppsub_test_xxxxx
```

## Generated Files

- `meter_counter.json` - Tracks incremental numbering for pricing plans created by `create_credit_burndown.py` and `create_credit_burndown_free_credits.py`

These files are ignored by git.