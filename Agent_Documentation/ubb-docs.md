# Implement advanced usage-based billing with pricing plans

Bill your customers based on usage and recurring charges.

You can group different pricing components into a single pricing plan. For example, you can create a pricing plan that includes [rate cards](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md) for usage-based billing, [license fees](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/license-fees/about.md) for recurring charges, and [service actions](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/service-actions/about.md) for recurring credit grant allocations. When a customer subscribes to a pricing plan, all the recurring components are automatically enrolled and billed according to the cadence you configure.

Supported pricing models include:

- [Pay as you go](https://docs.stripe.com/billing/subscriptions/advanced-usage-based/pay-as-you-go.md)
- [Real-time credit burndown with top-ups](https://docs.stripe.com/billing/subscriptions/usage-based-v2/use-cases/credit-burndown-and-top-ups.md)
- [Flat fee and overages](https://docs.stripe.com/billing/subscriptions/usage-based-v2/use-cases/flat-fee-and-overages.md)

> Pricing plans are currently in [private preview](https://docs.stripe.com/release-phases.md) and could change in functionality and integration path before they’re generally available to all Stripe users. Contact us  to request access.

## Before you begin

You can also use a [guided API (Blueprint)](https://dashboard.stripe.com/test/workbench/blueprints/usage-based-billing?code-pane-shown=true) version of this guide in the Dashboard.

Pricing plans use `/v2` API endpoints. Learn more about the [/v2 and /v1 namespaces](https://docs.stripe.com/api-v2-overview.md).

Use [sandboxes](https://docs.stripe.com/sandboxes.md) to test your pricing plans integration. You can’t use test mode with `/v2` APIs.

## Create a pricing plan

Use the Stripe Dashboard or API to create a pricing plan that contains all the relevant billing components of your pricing model.

For each pricing plan, you can configure:

- **Currency**: Specify the currency for all the components in your pricing plan.
- **Include tax in prices**: Specify whether to include tax in your price (inclusive) or to add it to the invoice subtotal (exclusive). Learn more about  [inclusive and exclusive taxes for billing](https://docs.stripe.com/billing/taxes/tax-rates.md#inclusive-vs-exclusive-tax).
- **Metadata**: Optionally add your own metadata to the pricing plan.

After you set the currency and tax parameters, define the relevant components of your plan. Which components you include depends on your pricing model. This guide uses all three components ([rate card](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md#create-rate-card), [license fees](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/license-fees/about.md#create-license-fee), and [service actions](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/service-actions/about.md#create-service-action)), but which components you use depends on your pricing model. For example, with [pay-as-you-go pricing](https://docs.stripe.com/billing/subscriptions/advanced-usage-based/pay-as-you-go.md) and [real-time credit burndown with top-ups](https://docs.stripe.com/billing/subscriptions/usage-based-v2/use-cases/credit-burndown-and-top-ups.md) you only need a rate card. With [flat fee and overages](https://docs.stripe.com/billing/subscriptions/usage-based-v2/use-cases/flat-fee-and-overages.md), you need a rate card and a license fee, and for recurring credits with overage you need a rate card and a service action.

#### Dashboard

### Create the pricing plan

1. On the [Pricing plans](https://dashboard.stripe.com/test/pricing-plans) page, click **Create pricing plan**.
1. In the pricing plan editor:
   - Provide a display name, currency, and tax behavior.
   - (Optional) Under **Advanced settings**, specify the description, unique lookup key, and metadata.
1. Click **Continue**.

### Add a rate card

1. In the pricing plan editor, click + and **Rate card**.
1. In the rate card editor:
   - Provide a display name.
   - Specify the servicing period (learn more about [service and billing intervals](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#cadence-service-interval)).
   - (Optional) Under **Advanced settings**, provide a lookup key and metadata.
1. Click **Continue**.

#### Attach a rate to the rate card

1. In the rate editor:
   - Provide a display name for the metered item. For example, `Hypernian tokens`.
   - Select an existing **Meter** or create a new one by clicking +.
   - Select the **Price type**: **Fixed rate**, [Volume](https://docs.stripe.com/subscriptions/pricing-models/tiered-pricing.md#volume-based-pricing), or [Graduated](https://docs.stripe.com/subscriptions/pricing-models/tiered-pricing.md#graduated-pricing). For example, Hypernian uses fixed rate.
     - Select **Sell as** Individual units or a Packaged group of units. For example, an AI company might sell their tokens as packages of `100` units, at `0.04 USD` per package.
     - For packages, enter the **Units per package**.
     - Select whether to round up or down for **Partial packages**. If you round up, a user that uses 110 units is charged 0.08 USD.
     - Enter the **Price per package**.
   - (Optional) Configure **Advanced settings** for your metered item, such as specifying a **Product tax code** (learn more about [tax codes](https://docs.stripe.com/tax/tax-codes.md)), **Unit label**, **Lookup key**, and **Metadata**. You can also add metadata to the rate.
1. Click **Done**.
1. (Optional) Click + **Add rate** to add additional rates to the rate card.

### Add a license fee

1. In the pricing plan editor, click + and **License fee**.
1. In the license fee editor:
   - Provide a display name for the licensed item.
   - Specify the servicing period (learn more about [service and billing intervals](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#cadence-service-interval)).
   - Select the **Price type**: **Fixed rate**, [Volume](https://docs.stripe.com/subscriptions/pricing-models/tiered-pricing.md#volume-based-pricing), or [Graduated](https://docs.stripe.com/subscriptions/pricing-models/tiered-pricing.md#graduated-pricing). For example, `50.00 USD` per unit.
   - (Optional) Configure **Advanced settings** for your licensed item, such as specifying a **Product tax code** (learn more about [tax codes](https://docs.stripe.com/tax/tax-codes.md)), **Unit label**, **Lookup key**, and **Metadata**. You can also add metadata to the fee.
1. Click **Done**.

### Add a service action

1. In the pricing plan editor, click + and **Credit grant**.
1. In the recurring credit grant editor:
   - Provide a display name for the credit grant.
   - Specify the servicing period (learn more about [service and billing intervals](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#cadence-service-interval)).
   - Provide a credit amount.
   - (Optional) Configure **Advanced settings** for your recurring credit grant, such as specifying an **Application** or **Lookup key**.
1. Click **Done**.

After you finish configuring the pricing plan, click **Create pricing plan**.

#### API

### Create the pricing plan

When you create a [pricing plan](https://docs.stripe.com/api/v2/pricing-plans.md?api-version=preview), provide a display name, currency, and specify the tax behavior (learn more about [tax behavior and rate cards](https://docs.stripe.com/tax/subscriptions/rate-card-tax-codes-tax-behavior.md#set-a-default-tax-behavior-\(recommended\))).

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Pro Pricing Plan",
    "currency": "usd",
    "tax_behavior": "exclusive"
  }'
```

After you submit the pricing plan request, Stripe returns the active `Pricing Plan` object. You can’t subscribe new customers to an inactive pricing plan.

```json
{
  "id": "bpp_test_61SjPwyNGx88hyuOg16SjPfE4ZSQFjWjdqlzQfWMCH1E",
  "object": "v2.billing.pricing_plan",
  "active": true,
  "created": "2025-06-14T21:52:04.000Z",
  "currency": "usd",
  "description": null,
  "display_name": "Pro Pricing Plan",
  "latest_version": "bppv_test_123",
  "live_version": "bppv_test_123",
  "lookup_key": null,
  "metadata": {},
  "tax_behavior": "exclusive"
}
```

### Add a rate card

To attach a rate card to your pricing plan to bill your customers based on usage, [create a rate card](https://docs.stripe.com/api/v2/product-catalog/create-ratecard.md?api-version=preview) and provide a display name, currency, service interval, and tax behavior.

```curl
curl -X POST https://api.stripe.com/v2/billing/rate_cards \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Hypernian",
    "service_interval": "month",
    "service_interval_count": 1,
    "currency": "usd",
    "tax_behavior": "exclusive"
  }'
```

#### Create a meter 

```curl
curl https://api.stripe.com/v1/billing/meters \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d display_name="Hypernian tokens" \
  -d event_name=hypernian_tokens \
  -d "default_aggregation[formula]"=sum \
  -d "customer_mapping[event_payload_key]"=stripe_customer_id \
  -d "customer_mapping[type]"=by_id \
  -d "value_settings[event_payload_key]"=value
```

```cli
stripe billing meters create  \
  --display-name="Hypernian tokens" \
  --event-name=hypernian_tokens \
  -d "default_aggregation[formula]"=sum \
  -d "customer_mapping[event_payload_key]"=stripe_customer_id \
  -d "customer_mapping[type]"=by_id \
  -d "value_settings[event_payload_key]"=value
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

meter = client.v1.billing.meters.create({
  display_name: 'Hypernian tokens',
  event_name: 'hypernian_tokens',
  default_aggregation: {formula: 'sum'},
  customer_mapping: {
    event_payload_key: 'stripe_customer_id',
    type: 'by_id',
  },
  value_settings: {event_payload_key: 'value'},
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
meter = client.v1.billing.meters.create({
  "display_name": "Hypernian tokens",
  "event_name": "hypernian_tokens",
  "default_aggregation": {"formula": "sum"},
  "customer_mapping": {"event_payload_key": "stripe_customer_id", "type": "by_id"},
  "value_settings": {"event_payload_key": "value"},
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$meter = $stripe->billing->meters->create([
  'display_name' => 'Hypernian tokens',
  'event_name' => 'hypernian_tokens',
  'default_aggregation' => ['formula' => 'sum'],
  'customer_mapping' => [
    'event_payload_key' => 'stripe_customer_id',
    'type' => 'by_id',
  ],
  'value_settings' => ['event_payload_key' => 'value'],
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

MeterCreateParams params =
  MeterCreateParams.builder()
    .setDisplayName("Hypernian tokens")
    .setEventName("hypernian_tokens")
    .setDefaultAggregation(
      MeterCreateParams.DefaultAggregation.builder()
        .setFormula(MeterCreateParams.DefaultAggregation.Formula.SUM)
        .build()
    )
    .setCustomerMapping(
      MeterCreateParams.CustomerMapping.builder()
        .setEventPayloadKey("stripe_customer_id")
        .setType(MeterCreateParams.CustomerMapping.Type.BY_ID)
        .build()
    )
    .setValueSettings(
      MeterCreateParams.ValueSettings.builder().setEventPayloadKey("value").build()
    )
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
Meter meter = client.v1().billing().meters().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const meter = await stripe.billing.meters.create({
  display_name: 'Hypernian tokens',
  event_name: 'hypernian_tokens',
  default_aggregation: {
    formula: 'sum',
  },
  customer_mapping: {
    event_payload_key: 'stripe_customer_id',
    type: 'by_id',
  },
  value_settings: {
    event_payload_key: 'value',
  },
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.BillingMeterCreateParams{
  DisplayName: stripe.String("Hypernian tokens"),
  EventName: stripe.String("hypernian_tokens"),
  DefaultAggregation: &stripe.BillingMeterCreateDefaultAggregationParams{
    Formula: stripe.String(stripe.BillingMeterDefaultAggregationFormulaSum),
  },
  CustomerMapping: &stripe.BillingMeterCreateCustomerMappingParams{
    EventPayloadKey: stripe.String("stripe_customer_id"),
    Type: stripe.String("by_id"),
  },
  ValueSettings: &stripe.BillingMeterCreateValueSettingsParams{
    EventPayloadKey: stripe.String("value"),
  },
}
result, err := sc.V1BillingMeters.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.Billing.MeterCreateOptions
{
    DisplayName = "Hypernian tokens",
    EventName = "hypernian_tokens",
    DefaultAggregation = new Stripe.Billing.MeterDefaultAggregationOptions
    {
        Formula = "sum",
    },
    CustomerMapping = new Stripe.Billing.MeterCustomerMappingOptions
    {
        EventPayloadKey = "stripe_customer_id",
        Type = "by_id",
    },
    ValueSettings = new Stripe.Billing.MeterValueSettingsOptions
    {
        EventPayloadKey = "value",
    },
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Billing.Meters;
Stripe.Billing.Meter meter = service.Create(options);
```

#### Create a metered item

After you create a meter, create a metered item to represent the specific item that the customer is paying for, such as an LLM model or tier of token usage.

```curl
curl -X POST https://api.stripe.com/v2/billing/metered_items \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Hypernian tokens",
    "meter": "{{METER_ID}}",
    "lookup_key": "hypernian_tokens"
  }'
```

#### Attach a rate to the meter

After you create a metered item, attach a rate to the meter.

```curl
curl -X POST https://api.stripe.com/v2/billing/rate_cards/{{RATE_CARD_ID}}/rates \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "metered_item": "{{METERED_ITEM_ID}}",
    "unit_amount": "5"
  }'
```

```cli
stripe v2 billing rate_cards rates create {{RATE_CARD_ID}} \
  --metered-item={{METERED_ITEM_ID}} \
  --unit-amount=5
```

```ruby
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

rate_card_rate = client.v2.billing.rate_cards.rates.create(
  '{{RATE_CARD_ID}}',
  {
    metered_item: '{{METERED_ITEM_ID}}',
    unit_amount: '5',
  },
)
```

```python
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

rate_card_rate = client.v2.billing.rate_cards.rates.create(
  "{{RATE_CARD_ID}}",
  {"metered_item": "{{METERED_ITEM_ID}}", "unit_amount": "5"},
)
```

```php
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$rateCardRate = $stripe->v2->billing->rateCards->rates->create(
  '{{RATE_CARD_ID}}',
  [
    'metered_item' => '{{METERED_ITEM_ID}}',
    'unit_amount' => '5',
  ]
);
```

```java
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

RateCreateParams params =
  RateCreateParams.builder()
    .setMeteredItem("{{METERED_ITEM_ID}}")
    .setUnitAmount("5")
    .build();

RateCardRate rateCardRate =
  client.v2().billing().rateCards().rates().create("{{RATE_CARD_ID}}", params);
```

```node
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const rateCardRate = await stripe.v2.billing.rateCards.rates.create(
  '{{RATE_CARD_ID}}',
  {
    metered_item: '{{METERED_ITEM_ID}}',
    unit_amount: '5',
  }
);
```

```go
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.V2BillingRateCardsRateCreateParams{
  MeteredItem: stripe.String("{{METERED_ITEM_ID}}"),
  UnitAmount: stripe.String("5"),
  RateCardID: stripe.String("{{RATE_CARD_ID}}"),
}
result, err := sc.V2BillingRateCardsRates.Create(context.TODO(), params)
```

```dotnet
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.V2.Billing.RateCards.RateCreateOptions
{
    MeteredItem = "{{METERED_ITEM_ID}}",
    UnitAmount = "5",
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V2.Billing.RateCards.Rates;
Stripe.V2.Billing.RateCardRate rateCardRate = service.Create("{{RATE_CARD_ID}}", options);
```

#### Attach a rate card to a pricing plan

After you create the rate, attach the rate card to the pricing plan:

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "type": "rate_card",
    "rate_card": {
        "id": "{{RATE_CARD_ID}}",
        "version": "{{RATE_CARD_VERSION}}"
    },
    "metadata": {
        "existing_key": "updated_value",
        "new_key": "new value"
    }
  }'
```

### Add a license fee

License fees are fixed recurring charges, which you can use to charge up-front fees.

First, create a license item:

```curl
curl -X POST https://api.stripe.com/v2/billing/licensed_items \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Pricing Plan Licensed Item"
  }'
```

Then, create a license fee:

```curl
curl -X POST https://api.stripe.com/v2/billing/license_fees \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "E2E License",
    "licensed_item": "{{LICENSED_ITEM_ID}}",
    "unit_amount": "50000",
    "service_interval": "month",
    "service_interval_count": 1,
    "currency": "usd",
    "tax_behavior": "exclusive"
  }'
```

Finally, attach the license fee to a pricing plan:

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "type": "license_fee",
    "license_fee": {
        "id": "{{LICENSE_FEE_ID}}",
        "version": "{{LICENSE_FEE_VERSION}}"
    },
    "lookup_key": "monthly-fee-component",
    "metadata": {
        "existing_key": "updated_value",
        "new_key": "new value"
    }
  }'
```

### Add a service action

You can add new components, including recurring credit grants, to your pricing plan. Use recurring credit grants if you use a [credit burndown pricing model](https://docs.stripe.com/subscriptions/pricing-models/usage-based-pricing.md#credit-burndown). Service actions let you offer recurring credits to customers, which can offset charges for specific billable items, such as usage-based fees.

When you create a service action, you configure:

- Amount
- Billing frequency
- Applicable billable items

To create a monthly credit grant of 10 USD that expires at the end of the service interval:

```curl
curl -X POST https://api.stripe.com/v2/billing/service_actions \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "service_interval": "month",
    "service_interval_count": 1,
    "type": "credit_grant",
    "lookup_key": "credit grant 28",
    "credit_grant": {
        "name": "Credit grant 28",
        "expiry_config": {
            "type": "end_of_service_period"
        },
        "applicability_config": {
            "scope": {
                "price_type": "metered"
            }
        },
        "amount": {
            "type": "monetary",
            "monetary": {
                "value": 1000,
                "currency": "usd"
            }
        }
    }
  }'
```

Attach the service action to your pricing plan:

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "type": "service_action",
    "service_action": {
        "id": "{{SERVICE_ACTION_ID}}"
    },
    "lookup_key": "credit-grant-28",
    "metadata": {
        "existing_key": "updated_value",
        "new_key": "new value"
    }
  }'
```

### Activate the pricing plan

After you’ve added the relevant components for your pricing model, activate that version of the pricing plan. After the plan is activated, you can [subscribe customers to it](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md#subscribe).

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}} \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "live_version": "latest"
  }'
```

## Subscribe your customer to a pricing plan

After you set up a pricing plan, you can subscribe a customer to it. You can create a subscription by using the [Checkout Sessions API](https://docs.stripe.com/api/checkout/sessions.md) with [either a Stripe-hosted page or embedded components as a payment UI](https://docs.stripe.com/payments/checkout.md) (the Checkout Session also creates a customer). You can also use the API to directly create a pricing plan subscription. If you use the direct API method, you need to create [a customer](https://docs.stripe.com/api/customers/create.md), [collection setting](https://docs.stripe.com/api/v2/billing-settings/billing/collection-settings/create.md?api-version=preview), [billing cadence](https://docs.stripe.com/api/v2/product-catalog/create-cadence.md?api-version=preview), and [billing intent](https://docs.stripe.com/api/v2/billing-intents/create.md?api-version=preview), which creates the pricing plan subscription.

#### Stripe-hosted page

Use the [Checkout Sessions API](https://docs.stripe.com/api/checkout/sessions.md) to create a payment page for your customers. When a customer clicks **Subscribe**, the Checkout Session creates a [Customer](https://docs.stripe.com/api/customers.md) object (if you didn’t provide a customer ID for the Session) and a [pricing plan subscription](https://docs.stripe.com/api/v2/pricing-plan-subscriptions.md?api-version=preview). If you have multiple items in `checkout_items`, a pricing plan subscription is created for each item.

Here’s an example of what a complete pricing plan looks like with Checkout.
![Pricing plan example](https://b.stripecdn.com/docs-statics-srv/assets/checkout_pricing_plan_example.2156a15535345b113c30e7efabe72867.png)

A pricing plan displayed in Stripe Checkout

### Checkout Session limitations during private preview

During the private preview:

- You can pass a maximum of five [checkout_items](https://docs.stripe.com/api/checkout/sessions/create.md#create_checkout_session-checkout_items).
- You can only accept cards, Link, Apple Pay, and Google Pay.
- You can’t pass in a specific [billing cycle anchor](https://docs.stripe.com/billing/subscriptions/billing-cycle.md).
- You can’t use [tax rates](https://docs.stripe.com/billing/taxes/tax-rates.md), only automatic tax calculation.
- You can’t use discounts.
- You can’t [limit customers to one subscription](https://docs.stripe.com/payments/checkout/limit-subscriptions.md).
- You can’t use [Connect](https://docs.stripe.com/connect.md).
- You can’t add [optional items](https://docs.stripe.com/payments/checkout/optional-items.md) or [cross-sells](https://docs.stripe.com/payments/checkout/cross-sells.md).

Contact [advanced-ubb-private-preview@stripe.com](mailto:advanced-ubb-private-preview@stripe.com) to gain early access and share any product feedback or requests.

To [create a Checkout Session](https://docs.stripe.com/api/checkout/sessions/create.md) with pricing plans, include an object in the [checkout_items](https://docs.stripe.com/api/checkout/sessions/create.md#create_checkout_session-checkout_items) array that has its [type](https://docs.stripe.com/api/checkout/sessions/create.md#create_checkout_session-checkout_items-type) set to `pricing_plan_subscription_item` and includes a `pricing_plan_subscription_item` configuration. When you use `checkout_items` instead of `line_items`, you don’t need to specify the [mode](https://docs.stripe.com/api/checkout/sessions/create.md#create_checkout_session-mode).

```curl
curl https://api.stripe.com/v1/checkout/sessions \
  -u "<<YOUR_SECRET_KEY>>:" \
  -H "Stripe-Version: 2025-09-30.preview;checkout_product_catalog_preview=v1" \
  -d customer={{CUSTOMER_ID}} \
  -d "checkout_items[0][type]"=pricing_plan_subscription_item \
  -d "checkout_items[0][pricing_plan_subscription_item][pricing_plan]"={{PRICING_PLAN_ID}} \
  -d success_url={{SUCCESS_URL}}
```

If your pricing plan includes a license fee you need to include the license fee quantity:

Get the license fee component ID:

```curl
curl https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-09-30.preview"
```

Create the Checkout Session using the license fee component ID:

```curl
curl https://api.stripe.com/v1/checkout/sessions \
  -u "<<YOUR_SECRET_KEY>>:" \
  -H "Stripe-Version: 2025-09-30.preview;checkout_product_catalog_preview=v1" \
  -d customer={{CUSTOMER_ID}} \
  -d "checkout_items[0][type]"=pricing_plan_subscription_item \
  -d "checkout_items[0][pricing_plan_subscription_item][pricing_plan]"={{PRICING_PLAN_ID}} \
  -d "checkout_items[0][pricing_plan_subscription_item][component_configurations][{{LICENSE_COMPONENT_ID}}][type]"=license_fee_component \
  -d "checkout_items[0][pricing_plan_subscription_item][component_configurations][{{LICENSE_COMPONENT_ID}}][license_fee_component][quantity]"=1
```

The page displays your pricing plan’s details and collects the customer’s payment information. After the customer completes the session, the pricing plan subscription is created and the customer is redirected to the URL you specified for `success_url`. Learn more about [customizing redirect behavior with Checkout](https://docs.stripe.com/payments/checkout/custom-success-page.md).

#### Embedded components

For more control over the appearance of your pricing plan’s payment page, you can use [embedded components](https://docs.stripe.com/payments/quickstart-checkout-sessions.md) with the Checkout Session API. The embedded components [Session](https://docs.stripe.com/js/custom_checkout/session_object) object exposes your pricing plan’s details in [session.orderSummaryItems](https://docs.stripe.com/js/custom_checkout/session_object#custom_checkout_session_object-orderSummaryItems), enabling you to render an order summary for your pricing plan, license fees, and rate cards.

You still need to use the same `checkout_items` parameter when creating the Checkout Session on your server.

### Checkout Session limitations during private preview

During the private preview:

- You can pass a maximum of five [checkout_items](https://docs.stripe.com/api/checkout/sessions/create.md#create_checkout_session-checkout_items).
- You can only accept cards, Link, Apple Pay, and Google Pay.
- You can’t pass in a specific [billing cycle anchor](https://docs.stripe.com/billing/subscriptions/billing-cycle.md).
- You can’t use [tax rates](https://docs.stripe.com/billing/taxes/tax-rates.md), only automatic tax calculation.
- You can’t use discounts.
- You can’t [limit customers to one subscription](https://docs.stripe.com/payments/checkout/limit-subscriptions.md).
- You can’t use [Connect](https://docs.stripe.com/connect.md).
- You can’t add [optional items](https://docs.stripe.com/payments/checkout/optional-items.md) or [cross-sells](https://docs.stripe.com/payments/checkout/cross-sells.md).

Contact [advanced-ubb-private-preview@stripe.com](mailto:advanced-ubb-private-preview@stripe.com) to gain early access and share any product feedback or requests.

#### Use the product catalog beta header

When initializing a Stripe instance on your front end with your publishable key, pass in the `custom_checkout_product_catalog_1` beta header.

```js
const stripe = Stripe(
  '<<YOUR_PUBLISHABLE_KEY>>',{betas: ['custom_checkout_product_catalog_1']},
);
```

```javascript
import {loadStripe} from '@stripe/stripe-js';
const stripe = loadStripe("<<YOUR_PUBLISHABLE_KEY>>", {betas: ['custom_checkout_product_catalog_1'],
});
```

#### API

Use the APIs directly to [create a customer](https://docs.stripe.com/api/customers/create.md), then to [create a billing interval](https://docs.stripe.com/api/v2/product-catalog/create-cadence.md?api-version=preview). You can charge the customer’s default payment method automatically or send them the invoice to pay manually.

After you create a customer and a billing interval, you can [create a pricing plan subscription](https://docs.stripe.com/api/v2/billing-intents/create.md?api-version=preview).

By default, we charge a customer’s saved payment method automatically. To send an invoice, [create a collection setting](https://docs.stripe.com/api/v2/billing-settings/billing/collection-settings/create.md?api-version=preview) with the `collection_method` set to `send_invoice`. Then, pass in the collection setting when you create the cadence.

To subscribe a customer to a pricing plan, you need to:

1. [Create a Customer](https://docs.stripe.com/api/customers/create.md). This could be the customer created [during the Checkout Session](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md#set-up-checkout).
1. [Create a Billing profile](https://docs.stripe.com/api/v2/billing-profile.md?api-version=preview) for the pricing plan subscription.
1. [Create a Billing setting](https://docs.stripe.com/api/v2/billing-settings.md?api-version=preview) with tax enabled.
1. [Create a billing cadence](https://docs.stripe.com/api/v2/product-catalog/create-cadence.md).
1. Create a [billing intent](https://docs.stripe.com/api/v2/billing-intents/create.md), which creates a [pricing plan subscription](https://docs.stripe.com/api/v2/pricing-plan-subscriptions.md) that references the pricing plan and billing cadence.

Create a customer:

```curl
curl https://api.stripe.com/v1/customers \
  -u "<<YOUR_SECRET_KEY>>:" \
  --data-urlencode email="jenny.rosen@example.com" \
  -d name="Jenny Rosen"
```

```cli
stripe customers create  \
  --email="jenny.rosen@example.com" \
  --name="Jenny Rosen"
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

customer = client.v1.customers.create({
  email: 'jenny.rosen@example.com',
  name: 'Jenny Rosen',
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
customer = client.v1.customers.create({
  "email": "jenny.rosen@example.com",
  "name": "Jenny Rosen",
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$customer = $stripe->customers->create([
  'email' => 'jenny.rosen@example.com',
  'name' => 'Jenny Rosen',
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

CustomerCreateParams params =
  CustomerCreateParams.builder()
    .setEmail("jenny.rosen@example.com")
    .setName("Jenny Rosen")
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
Customer customer = client.v1().customers().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const customer = await stripe.customers.create({
  email: 'jenny.rosen@example.com',
  name: 'Jenny Rosen',
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.CustomerCreateParams{
  Email: stripe.String("jenny.rosen@example.com"),
  Name: stripe.String("Jenny Rosen"),
}
result, err := sc.V1Customers.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new CustomerCreateOptions
{
    Email = "jenny.rosen@example.com",
    Name = "Jenny Rosen",
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Customers;
Customer customer = service.Create(options);
```

Create a billing profile:

```curl
curl -X POST https://api.stripe.com/v2/billing/profiles \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "customer": "{{CUSTOMER_ID}}",
    "display_name": "Automatic collection settings",
    "lookup_key": "billing_profile_cus_123",
    "metadata": {
        "test": "data"
    }
  }'
```

Then add the billing profile and [bill settings](https://docs.stripe.com/api/v2/billing-settings/create.md) to the billing cadence:

```curl
curl -X POST https://api.stripe.com/v2/billing/cadences \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "payer": {
        "billing_profile": "{{BILLING_PROFILE_ID}}"
    },
    "billing_cycle": {
        "type": "month",
        "interval_count": 1,
        "month": {
            "day_of_month": 20
        }
    }
  }'
```

Subscribe your customer to the pricing plan by creating a [billing intent](https://docs.stripe.com/api/v2/billing-intents/object.md) and passing the pricing plan and billing cadence IDs.

```curl
curl -X POST https://api.stripe.com/v2/billing/intents \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "currency": "usd",
    "cadence": "{{CADENCE_ID}}",
    "actions": [
        {
            "type": "subscribe",
            "subscribe": {
                "type": "pricing_plan_subscription_details",
                "pricing_plan_subscription_details": {
                    "pricing_plan": "{{PRICING_PLAN_ID}}",
                    "pricing_plan_version": "{{PRICING_PLAN_VERSION}}",
                    "component_configurations": []
                }
            }
        }
    ]
  }'
```

Next, reserve the billing intent. You can determine how much to charge your customer based on the preview that generates when you [reserve](https://docs.stripe.com/api/v2/billing-intents/reserve.md?api-version=preview) the billing intent.

```curl
curl -X POST https://api.stripe.com/v2/billing/intents/{{BILLING_INTENT_ID}}/reserve \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview"
```

Next, commit the billing intent to activate the pricing plan subscription and bill the customer according to the plan and cadence. You also need to specify the [PaymentIntent](https://docs.stripe.com/api/payment_intents.md) ID if your collection setting is set to charge automatically. (You don’t need to do this if you set the collection setting to `send_invoice`.) To get the PaymentIntent ID, find it in the response, [list all PaymentIntents](https://docs.stripe.com/api/payment_intents/list.md), or find it in the [Payments page in the Dashboard](https://dashboard.stripe.com/payments).

```curl
curl https://api.stripe.com/v1/payment_intents \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d amount=1000 \
  -d currency=usd \
  -d customer={{CUSTOMER_ID}} \
  -d payment_method={{PAYMENT_METHOD_ID}} \
  --data-urlencode return_url="https://example.com/return" \
  -d confirm=true
```

```cli
stripe payment_intents create  \
  --amount=1000 \
  --currency=usd \
  --customer={{CUSTOMER_ID}} \
  --payment-method={{PAYMENT_METHOD_ID}} \
  --return-url="https://example.com/return" \
  --confirm=true
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

payment_intent = client.v1.payment_intents.create({
  amount: 1000,
  currency: 'usd',
  customer: '{{CUSTOMER_ID}}',
  payment_method: '{{PAYMENT_METHOD_ID}}',
  return_url: 'https://example.com/return',
  confirm: 'true',
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
payment_intent = client.v1.payment_intents.create({
  "amount": 1000,
  "currency": "usd",
  "customer": "{{CUSTOMER_ID}}",
  "payment_method": "{{PAYMENT_METHOD_ID}}",
  "return_url": "https://example.com/return",
  "confirm": True,
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$paymentIntent = $stripe->paymentIntents->create([
  'amount' => 1000,
  'currency' => 'usd',
  'customer' => '{{CUSTOMER_ID}}',
  'payment_method' => '{{PAYMENT_METHOD_ID}}',
  'return_url' => 'https://example.com/return',
  'confirm' => true,
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

PaymentIntentCreateParams params =
  PaymentIntentCreateParams.builder()
    .setAmount(1000L)
    .setCurrency("usd")
    .setCustomer("{{CUSTOMER_ID}}")
    .setPaymentMethod("{{PAYMENT_METHOD_ID}}")
    .setReturnUrl("https://example.com/return")
    .setConfirm(true)
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
PaymentIntent paymentIntent = client.v1().paymentIntents().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const paymentIntent = await stripe.paymentIntents.create({
  amount: 1000,
  currency: 'usd',
  customer: '{{CUSTOMER_ID}}',
  payment_method: '{{PAYMENT_METHOD_ID}}',
  return_url: 'https://example.com/return',
  confirm: true,
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.PaymentIntentCreateParams{
  Amount: stripe.Int64(1000),
  Currency: stripe.String(stripe.CurrencyUSD),
  Customer: stripe.String("{{CUSTOMER_ID}}"),
  PaymentMethod: stripe.String("{{PAYMENT_METHOD_ID}}"),
  ReturnURL: stripe.String("https://example.com/return"),
  Confirm: stripe.Bool(true),
}
result, err := sc.V1PaymentIntents.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new PaymentIntentCreateOptions
{
    Amount = 1000,
    Currency = "usd",
    Customer = "{{CUSTOMER_ID}}",
    PaymentMethod = "{{PAYMENT_METHOD_ID}}",
    ReturnUrl = "https://example.com/return",
    Confirm = true,
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.PaymentIntents;
PaymentIntent paymentIntent = service.Create(options);
```

```curl
curl -X POST https://api.stripe.com/v2/billing/intents/{{BILLING_INTENT_ID}}/commit \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "payment_intent": "{{PAYMENT_INTENT_ID}}"
  }'
```

Learn more about [billing intent states](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions/manage.md#billing-intent-states).

You can optionally pass a specific version of a pricing plan when subscribing a customer. If you don’t specify a version, the subscription applies the pricing plan’s live version.

```curl
curl -X POST https://api.stripe.com/v2/billing/intents \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "currency": "usd",
    "effective_at": "on_commit",
    "cadence": "bc_test_61SrjnScUwT6mNskZ16SjPfE4ZSQFjWjdqlzQfWMCVnM",
    "actions": [
        {
            "type": "subscribe",
            "subscribe": {
                "type": "pricing_plan_subscription_details",
                "proration_behavior": "none",
                "pricing_plan_subscription_details": {
                    "pricing_plan": "{{PRICING_PLAN_ID}}",
                    "pricing_plan_version": "{{PRICING_PLAN_VERSION}}",
                    "component_configurations": []
                }
            }
        }
    ]
  }'
```

## Record customer usage

After you subscribe a customer to a pricing plan consisting of a rate card, record their usage of your service by sending meter events to a meter.

#### Dashboard

1. Go to the [Pricing plan subscriptions](https://dashboard.stripe.com/test/pricing-plans/subscriptions) tab.
1. Click the subscription you want to record usage for.
1. Select **View** to see the underlying pricing plan components, and navigate to the rate card you want to add usage for.
1. Click the overflow menu (⋯) in the row of the item you want to record usage for, then click **View meter details**.
1. In the meter details page, click **+ Add usage** then select **Manually input usage**.
1. In the **Add usage** dialog:
   - Select a customer.
   - Enter a **Value** for the usage.
   - Select a date for the **Timestamp**.
1. Click **Submit**.

#### API

Use [meter events](https://docs.stripe.com/api/billing/meter-event.md) to [record customer usage](https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage.md) for your meter. At the end of the billing interval, Stripe bills the reported usage.

To test usage-based billing, send meter events through the Stripe Dashboard or API. When using the API, specify the customer ID and usage value in the `payload`. Learn more about [testing a pricing plans integration](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md#test-the-integration).

```curl
curl https://api.stripe.com/v1/billing/meter_events \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d event_name=hypernian_tokens \
  -d "payload[stripe_customer_id]"={{CUSTOMER_ID}} \
  -d "payload[value]"=25
```

## Create a preview invoice

Create a preview invoice to see a preview of a customer’s invoice. The preview includes the relevant line items from the various pricing plan components.

#### Dashboard

1. Go to the [Pricing plan subscriptions](https://dashboard.stripe.com/test/pricing-plan/subscriptions) tab.
1. Click the subscription you want to preview an invoice for.
1. Scroll down to the **Upcoming invoice** section. The preview invoice shows the subscription amount to bill the customer on the specified date, and reflects the corresponding metered items, license items, and credits.

#### API

```curl
curl https://api.stripe.com/v1/invoices/create_preview \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d billing_cadence=bc_test_61SrjnScUwT6mNskZ16SjPfE4ZSQFjWjdqlzQfWMCVnM
```

```json
{"hosted_invoice_url": "example.com/invoice",
  "invoice_pdf": null,
  "billing_reason": "manual",
  "collection_method": "charge_automatically",
  "created": 1680644467,
  "currency": "usd",
  "custom_fields": null,
  "customer": "cus_NeZwdNtLEOXuvB",
  "customer_address": null,
  "customer_email": "jennyrosen@example.com",
  "customer_name": "Jenny Rosen",
  "customer_phone": null,
  "customer_shipping": null,
  "customer_tax_exempt": "none",
  "customer_tax_ids": [],
  "default_payment_method": null,
  "default_source": null,
  "default_tax_rates": [],
  "description": null,
  "discounts": [],
  "due_date": null,
  "ending_balance": null,
  "footer": null,
  "from_invoice": null,
  "last_finalization_error": null,
  "latest_revision": null,
  "lines": {
    "object": "list",
    "data": [],
    "has_more": false,
    "total_count": 0,
    "url": "/v1/invoices/in_1MtHbELkdIwHu7ixl4OzzPMv/lines"
  },
{
  "id": "upcoming_in_1MtHbELkdIwHu7ixl4OzzPMv",
  "object": "invoice",
  "account_country": "US",
  "account_name": "Stripe Docs",
  "account_tax_ids": null,
  "amount_due": 0,
  "amount_paid": 0,
  "amount_overpaid": 0,
  "amount_remaining": 0,
  "amount_shipping": 0,
  "application": null,
  "application_fee_amount": null,
  "attempt_count": 0,
  "attempted": false,
  "auto_advance": false,
  "automatic_tax": {
    "enabled": false,
    "status": null
  },
  "livemode": false,
  "metadata": {},
  "next_payment_attempt": null,
  "number": null,
  "on_behalf_of": null,
  "parent": null,
  "payment_settings": {
    "default_mandate": null,
    "payment_method_options": null,
    "payment_method_types": null
  },
  "period_end": 1680644467,
  "period_start": 1680644467,
  "post_payment_credit_notes_amount": 0,
  "pre_payment_credit_notes_amount": 0,
  "receipt_number": null,
  "shipping_cost": null,
  "shipping_details": null,
  "starting_balance": 0,
  "statement_descriptor": null,
  "status": "draft",
  "status_transitions": {
    "finalized_at": null,
    "marked_uncollectible_at": null,
    "paid_at": null,
    "voided_at": null
  },
  "subtotal": 0,
  "subtotal_excluding_tax": 0,
  "test_clock": null,
  "total": 0,
  "total_discount_amounts": [],
  "total_excluding_tax": 0,
  "total_taxes": [],
  "webhooks_delivered_at": 1680644467
}
```

## Monitor servicing events

Pricing plan subscriptions send event notifications whenever the servicing and collection states change.

Listen for these events and use them to construct your business logic:

| Event                                                                      | Description                                                 |
| -------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `v2.billing.pricing_plan_subscription.servicing_activated`                 | The user pays the subscription which activates the service. |
| `v2.billing.pricing_plan_subscription.servicing_paused`                    | The user pauses the subscription.                           |
| `v2.billing.pricing_plan_subscription.servicing_canceled`                  | The user cancels the service.                               |
| `v2.billing.pricing_plan_subscription.collection_current`                  | The collection of the subscription is ongoing.              |
| `v2.billing.pricing_plan_subscription.collection_awaiting_customer_action` | The collection is waiting for the customer to do something. |
| `v2.billing.pricing_plan_subscription.collection_paused`                   | The collection is paused.                                   |
| `v2.billing.rate_card_subscription.collection_past_due`                    | The collection is past due.                                 |
| `v2.billing.rate_card_subscription.collection_unpaid`                      | The collection is considered unpaid.                        |

To handle these [v2 Events](https://docs.stripe.com/api/v2/core/events.md?api-version=preview), configure an [Event Destination](https://docs.stripe.com/api/v2/core/event_destinations.md?api-version=preview) and point it at your webhook endpoint. You can either:

- Create the Event Destination from [Workbench](https://docs.stripe.com/workbench/event-destinations.md).
- Create the Event Destination [through the Stripe API](https://docs.stripe.com/api/v2/core/event_destinations.md?api-version=preview).

After you’ve created a destination, you can set up your webhook endpoint to handle these events:

```ruby
require 'stripe'

post '/v2_webhook_endpoint' do
  payload = request.body.read
  sig_header = request.env['HTTP_STRIPE_SIGNATURE']
  event = nil

  begin
    event = Stripe::Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  rescue JSON::ParserError => e
    status 400
    return
  rescue Stripe::SignatureVerificationError => e
    status 400
    return
  end

  client = Stripe::StripeClient("<<YOUR_SECRET_KEY>>")

  case event.type
  when 'v2.billing.pricing_plan_subscription.servicing_activated'
    # The customer clicked Pay on Stripe Checkout, which activates the service.
    subscription_id = event.related_object.id
    subscription = client.v2.billing.pricing_plan_subscriptions
      .retrieve(subscription_id)

    # Look up your user in the database using the metadata passed into
    # Checkout Session create
    user_id = subscription.metadata["my_user_id"]
    user = User.find_by_id(user_id)

    # Fill in your logic here:
    mark_subscription_active(user, subscription)
  when 'v2.billing.pricing_plan_subscription.servicing_paused'
    # The customer paused the subscription.
    subscription_id = event.related_object.id
    subscription = client.v2.billing.pricing_plan_subscriptions
      .retrieve(subscription_id)

    # Look up your user in the database using the metadata passed into
    # Checkout Session create
    user_id = subscription.metadata["my_user_id"]
    user = User.find_by_id(user_id)

    # Fill in your logic here:
    mark_subscription_paused(user, subscription)
  when 'v2.billing.pricing_plan_subscription.servicing_canceled'
    # The customer canceled the subscription.
    subscription_id = event.related_object.id
    subscription = client.v2.billing.pricing_plan_subscriptions
      .retrieve(subscription_id)

    # Look up your user in the database using the metadata passed into
    # Checkout Session create
    user_id = subscription.metadata["my_user_id"]
    user = User.find_by_id(user_id)

    # Fill in your logic here:
    mark_subscription_canceled(user, subscription)
  end

  status 200
end
```

## Test the integration

To test your integration:

- [Create a sandbox](https://docs.stripe.com/sandboxes/dashboard/manage.md#create-a-sandbox).
- Create a test pricing plan and at least one underlying pricing component in your sandbox.
- Use [test cards](https://docs.stripe.com/testing.md) to simulate successful and failed payments.
- Create [test meter events](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md#create-meter) to simulate usage.
- Use [test clocks](https://docs.stripe.com/billing/testing/test-clocks/simulate-subscriptions.md) to simulate billing.

> #### Don't create test clocks in the past
> 
> When you create a test clock for a pricing plan subscription, only create clocks in the future. If you create a clock in the past, invoice amounts won’t be correct.

Create a test clock with a UNIX timestamp:

```curl
curl https://api.stripe.com/v1/test_helpers/test_clocks \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d frozen_time=1577836800
```

```cli
stripe test_helpers test_clocks create  \
  --frozen-time=1577836800
```

```ruby
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

test_clock = client.v1.test_helpers.test_clocks.create({frozen_time: 1577836800})
```

```python
client = StripeClient("<<YOUR_SECRET_KEY>>")

test_clock = client.v1.test_helpers.test_clocks.create({"frozen_time": 1577836800})
```

```php
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$testClock = $stripe->testHelpers->testClocks->create(['frozen_time' => 1577836800]);
```

```java
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

TestClockCreateParams params =
  TestClockCreateParams.builder().setFrozenTime(1577836800L).build();

TestClock testClock = client.v1().testHelpers().testClocks().create(params);
```

```node
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const testClock = await stripe.testHelpers.testClocks.create({
  frozen_time: 1577836800,
});
```

```go
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.TestHelpersTestClockCreateParams{
  FrozenTime: stripe.Int64(1577836800),
}
result, err := sc.V1TestHelpersTestClocks.Create(context.TODO(), params)
```

```dotnet
var options = new Stripe.TestHelpers.TestClockCreateOptions
{
    FrozenTime = DateTimeOffset.FromUnixTimeSeconds(1577836800).UtcDateTime,
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.TestHelpers.TestClocks;
Stripe.TestHelpers.TestClock testClock = service.Create(options);
```

Make a note of the test clock’s ID. Next, create a test customer with the clock:

```curl
curl https://api.stripe.com/v1/customers \
  -u "<<YOUR_SECRET_KEY>>:" \
  --data-urlencode email="test@example.com" \
  -d test_clock={{TEST_CLOCK_ID}}
```

```cli
stripe customers create  \
  --email="test@example.com" \
  --test-clock={{TEST_CLOCK_ID}}
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

customer = client.v1.customers.create({
  email: 'test@example.com',
  test_clock: '{{TEST_CLOCK_ID}}',
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
customer = client.v1.customers.create({
  "email": "test@example.com",
  "test_clock": "{{TEST_CLOCK_ID}}",
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$customer = $stripe->customers->create([
  'email' => 'test@example.com',
  'test_clock' => '{{TEST_CLOCK_ID}}',
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

CustomerCreateParams params =
  CustomerCreateParams.builder()
    .setEmail("test@example.com")
    .setTestClock("{{TEST_CLOCK_ID}}")
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
Customer customer = client.v1().customers().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const customer = await stripe.customers.create({
  email: 'test@example.com',
  test_clock: '{{TEST_CLOCK_ID}}',
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.CustomerCreateParams{
  Email: stripe.String("test@example.com"),
  TestClock: stripe.String("{{TEST_CLOCK_ID}}"),
}
result, err := sc.V1Customers.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new CustomerCreateOptions
{
    Email = "test@example.com",
    TestClock = "{{TEST_CLOCK_ID}}",
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Customers;
Customer customer = service.Create(options);
```

Create a billing profile:

```curl
curl -X POST https://api.stripe.com/v2/billing/profiles \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "customer": "{{CUSTOMER_ID}}"
  }'
```

```cli
stripe preview v2 billing profiles create  \
  --customer={{CUSTOMER_ID}}
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
# This example uses the beta SDK. See https://github.com/stripe/stripe-ruby#public-preview-sdks
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

profile = client.v2.billing.profiles.create({customer: '{{CUSTOMER_ID}}'})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
# This example uses the beta SDK. See https://github.com/stripe/stripe-python#public-preview-sdks
client = StripeClient("<<YOUR_SECRET_KEY>>")

profile = client.v2.billing.profiles.create({"customer": "{{CUSTOMER_ID}}"})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
// This example uses the beta SDK. See https://github.com/stripe/stripe-php#public-preview-sdks
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$profile = $stripe->v2->billing->profiles->create(['customer' => '{{CUSTOMER_ID}}']);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
// This example uses the beta SDK. See https://github.com/stripe/stripe-java#public-preview-sdks
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

ProfileCreateParams params =
  ProfileCreateParams.builder().setCustomer("{{CUSTOMER_ID}}").build();

Profile profile = client.v2().billing().profiles().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
// This example uses the beta SDK. See https://github.com/stripe/stripe-node#public-preview-sdks
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const profile = await stripe.v2.billing.profiles.create({
  customer: '{{CUSTOMER_ID}}',
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
// This example uses the beta SDK. See https://github.com/stripe/stripe-go#public-preview-sdks
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.V2BillingProfileCreateParams{Customer: stripe.String("{{CUSTOMER_ID}}")}
result, err := sc.V2BillingProfiles.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
// This example uses the beta SDK. See https://github.com/stripe/stripe-dotnet#public-preview-sdks
var options = new Stripe.V2.Billing.ProfileCreateOptions { Customer = "{{CUSTOMER_ID}}" };
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V2.Billing.Profiles;
Stripe.V2.Billing.Profile profile = service.Create(options);
```

Create a billing interval to define when to bill the customer. Save the ID.

```curl
curl -X POST https://api.stripe.com/v2/billing/cadences \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "payer": {
        "billing_profile": "{{BILLING_PROFILE_ID}}"
    },
    "billing_cycle": {
        "type": "month",
        "interval_count": 3
    },
    "settings": {
        "collection": {
            "id": "{{COLLECTION_SETTINGS_ID}}"
        }
    }
  }'
```

[Create a pricing plan subscription](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md#subscribe) for the test customer.

Create a [billing intent](https://docs.stripe.com/api/v2/billing-intents/create.md?api-version=preview) to track the status of the pricing plan subscription. First, you create a draft billing intent. Save the ID of the intent.

```curl
curl -X POST https://api.stripe.com/v2/billing/intents \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "currency": "usd",
    "cadence": "{{CADENCE_ID}}",
    "actions": {
        "type": "subscribe",
        "subscribe": {
            "type": "pricing_plan_subscription_details",
            "pricing_plan_subscription_details": {
                "pricing_plan": "{{PRICING_PLAN_ID}}",
                "pricing_plan_version": "{{PRICING_PLAN_VERSION}}"
            }
        }
    }
  }'
```

Next, reserve the billing intent:

```curl
curl -X POST https://api.stripe.com/v2/billing/intents/{{BILLING_INTENT_ID}}/reserve \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview"
```

Next, commit the billing intent to activate the pricing plan subscription and bill the customer according to the plan and cadence. (If you configured collection settings to `automatic`, you must have a successful [PaymentIntent](https://docs.stripe.com/api/payment_intents.md) to commit the Intent. If you have the collection setting set to `send_invoice`, you don’t need to pass the Payment Intent.)

```curl
curl https://api.stripe.com/payment_intent \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d amount={{AMOUNT}} \
  -d currency={{CURRENCY}} \
  -d customer={{CUSTOMER_ID}} \
  -d payment_method={{PM_ID}} \
  -d return_url="example.com" \
  -d confirm=true
```

For testing purposes, you can set `payment_method` to “pm_card_visa”.

```curl
curl -X POST https://api.stripe.com/v2/billing/intents/{{BILLING_INTENT_ID}}/commit \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "payment_intent": "{{PAYMENT_INTENT_ID}}"
  }'
```

Pay the invoice generated by the subscription. After the invoice is paid, you can simulate usage and advance the clock, which triggers the next month’s billing. If you use Checkout, you can open the returned Checkout Session’s `url` in your browser and complete payment with a [test card](https://docs.stripe.com/testing.md#use-test-cards).

Record some test usage:

```curl
curl -X POST https://api.stripe.com/v2/billing/meter_events \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "event_name": "hypernian_tokens",
    "payload": {
        "stripe_customer_id": "{{CUSTOMER_ID}}",
        "value": 100
    }
  }'
```

Advance the test clock’s frozen time forward by a month. In this example, the test clock currently has a timestamp of `1577836800`. To add a month, add `30 * 24 * 60 * 60`, or `2592000` seconds. The new timestamp a month from now is `1580428800`.

```curl
curl https://api.stripe.com/v1/test_helpers/test_clocks/{{TEST_CLOCK_ID}}/advance \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d frozen_time=1580428800
```

```cli
stripe test_helpers test_clocks advance {{TEST_CLOCK_ID}} \
  --frozen-time=1580428800
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

test_clock = client.v1.test_helpers.test_clocks.advance(
  '{{TEST_CLOCK_ID}}',
  {frozen_time: 1580428800},
)
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
test_clock = client.v1.test_helpers.test_clocks.advance(
  "{{TEST_CLOCK_ID}}",
  {"frozen_time": 1580428800},
)
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$testClock = $stripe->testHelpers->testClocks->advance(
  '{{TEST_CLOCK_ID}}',
  ['frozen_time' => 1580428800]
);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

TestClockAdvanceParams params =
  TestClockAdvanceParams.builder().setFrozenTime(1580428800L).build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
TestClock testClock =
  client.v1().testHelpers().testClocks().advance("{{TEST_CLOCK_ID}}", params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const testClock = await stripe.testHelpers.testClocks.advance(
  '{{TEST_CLOCK_ID}}',
  {
    frozen_time: 1580428800,
  }
);
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.TestHelpersTestClockAdvanceParams{FrozenTime: stripe.Int64(1580428800)}
result, err := sc.V1TestHelpersTestClocks.Advance(
  context.TODO(), "{{TEST_CLOCK_ID}}", params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.TestHelpers.TestClockAdvanceOptions
{
    FrozenTime = DateTimeOffset.FromUnixTimeSeconds(1580428800).UtcDateTime,
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.TestHelpers.TestClocks;
Stripe.TestHelpers.TestClock testClock = service.Advance("{{TEST_CLOCK_ID}}", options);
```

## Optional: Collect taxes

To collect taxes automatically, [create a Checkout Session ](https://docs.stripe.com/api/checkout/sessions/create.md) that includes [checkout_items](https://docs.stripe.com/api/checkout/sessions/object.md#checkout_session_object-checkout_items) and set `automatic_tax.enabled` to true.

```curl
curl https://api.stripe.com/v1/checkout/sessions \
  -u "<<YOUR_SECRET_KEY>>:" \
  -H "Stripe-Version: 2025-09-30.preview;checkout_product_catalog_preview=v1" \
  -d customer={{CUSTOMER_ID}} \
  -d "checkout_items[0][type]"=pricing_plan_subscription_item \
  -d "checkout_items[0][pricing_plan_subscription_item][pricing_plan]"={{PRICING_PLAN_ID}} \
  -d success_url={{SUCCESS_URL}}
```

The page displays your pricing plan’s details and collects the customer’s payment information. After the customer completes the session, they’re redirected to the URL you specified for `success_url`.

## Optional: Set up the customer portal

You can provide self-service functions to your customers by setting up a [customer portal](https://docs.stripe.com/customer-management/activate-no-code-customer-portal.md).

Using the customer portal with pricing plan subscriptions is currently read-only: customers can’t cancel, change plans, or update their payment methods for pricing plan billing subscriptions. Currently, you can only configure a customer portal session through the Dashboard.

Using the customer portal with pricing plan subscriptions lets your customers view:

- The plan they’re subscribed to, including details of the hybrid plan you’re offering.
- Upcoming invoices that help them understand how much they’ll be billed at the end of the month.
- The payment method on file for the Subscription in question.
- Past invoices they’ve been charged for.
- Their billing information.

# How advanced usage-based billing works

Learn how you can launch common usage-based pricing models on Stripe.

SaaS and AI businesses often want to charge customers based on the usage of their product while also charging recurring fees up front and offering recurring credits. With advanced usage-based billing, you can:

- Define and charge customers based on specific usage data attributes (dimensions)
- Manage dozens to hundreds of rates across one or many meters
- Set up real-time credit burndown and automate credit issuance
- Manage price migrations

Supported pricing models include:

- [Pay as you go](https://docs.stripe.com/billing/subscriptions/advanced-usage-based/pay-as-you-go.md) for many rates or meters
- [Flat fee and overages](https://docs.stripe.com/billing/subscriptions/usage-based-v2/use-cases/flat-fee-and-overages.md)
- [Real-time credit burndown with automatic top-ups](https://docs.stripe.com/billing/subscriptions/usage-based-v2/use-cases/credit-burndown-and-top-ups.md)

With advanced usage-based billing, you charge customers based on the usage of their product while also charging flat recurring fees and burning down credits.
 (See full diagram at https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about)
## Advanced usage-based billing concepts

Here are the key concepts for understanding how advanced usage-based billing works.

| Term                                                                                                                                         | Definition                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| -------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Billable item                                                                                                                                | A line item that appears on an invoice that corresponds to a pricing plan subscription. Can be metered or licensed.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| [License fee](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#license-fee-concepts)                              | A fixed, recurring charge for a billable item, such as a monthly subscription fee. It includes details such as price, billing frequency, and tax behavior. Learn more about [license fees](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#license-fee-concepts).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| Licensed item                                                                                                                                | A billable item that’s licensed and appears on the invoice sent to your customer. You pass in the ID of the licensed item when you [create the license fee](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/license-fees/about.md#create-license-fee).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Meter                                                                                                                                        | [Meters](https://docs.stripe.com/api/billing/meter.md) specify how to aggregate [meter events](https://docs.stripe.com/api/billing/meter-event.md) over a service interval. Meter events represent all actions that customers take in your system (for example, API requests). Metered items attach to meters and form the line items for what’s billed. For example, a business offering AI services might have meter events that represent the number of tokens a customer uses in a query. The meter tracks the sum of tokens over a month. The aggregated usage forms the basis for the invoices generated for each billing interval. You can use the Stripe Dashboard or API to [configure a meter](https://docs.stripe.com/billing/subscriptions/usage-based/meters/configure.md). |
| Metered item                                                                                                                                 | A billable item that’s metered. You can create a [metered item](https://docs.stripe.com/api/v2/metered-items.md?api-version=preview) to represent the specific item that the customer is paying for, such as an LLM model or tier of token usage. You can apply a metered item to multiple rate card rates. Each metered item must be associated with a meter.                                                                                                                                                                                                                                                                                                                                                                                                                           |
| [Pricing plan](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#pricing-plan-concepts)                            | A customizable container of pricing components (such as rate cards, license fees, and recurring credit grants). Learn more about [pricing plans](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#pricing-plan-concepts).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| [Pricing plan subscriptions](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#pricing-plan-subscription-concepts) | A pricing plan subscription is created when a customer is subscribed to a specific pricing plan version. Learn more about [pricing plan subscriptions](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#pricing-plan-subscription-concepts).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Rate                                                                                                                                         | The pricing configuration for a metered item in a rate card. Learn more about [rate cards and rates](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#rate-card-concepts).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| [Rate card](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#rate-card-concepts)                                  | A collection of usage-based rates for a product. Learn more about [rate cards](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#rate-card-concepts).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| [Service action](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#service-action-concepts)                        | Defines a recurring credit grant and applicable billable items. Learn more about [service actions](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#service-action-concepts).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Service interval                                                                                                                             | [Service intervals](https://docs.stripe.com/api/v2/product-catalog/create-ratecard.md?api-version=preview#v2_create_rate_cards-service_interval) define two things: the time period for evaluating the usage of your service against your pricing model and when your customer should have access to the service. If you’ve configured volume or graduated pricing (for example, offering the first 100 units free), the limits reset for each service interval.                                                                                                                                                                                                                                                                                                                         |

### Pricing plan concepts 

You use pricing plans to group a set of pricing components into a single package that you can charge for. You subscribe customers to one pricing plan that contains one or more components for usage-based pricing, recurring fees, or recurring credits. You can modify existing components or add new ones to pricing plans to create new versions of that plan and choose whether to migrate existing customers to the latest version or not.

A pricing plan can contain any combination of:

- [A rate card](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md)
- [A license fee](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/license-fees/about.md)
- [A service action](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/service-actions/about.md)

Here’s what a pricing plan looks like with all of its components.
![Example image of a pricing plan with a rate card, license fee, and service action](https://b.stripecdn.com/docs-statics-srv/assets/pricing-plan.295b34e2ba8880b8c20edc782958f4a9.png)

A pricing plan with a rate card, license fee, and service action.

Here’s an example of what a complete pricing plan looks like with *Checkout* (A low-code payment integration that creates a customizable form for collecting payments. You can embed Checkout directly in your website, redirect customers to a Stripe-hosted payment page, or create a customized checkout page with Stripe Elements). Learn how to [use Checkout to subscribe customers to a pricing plan](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md?payment-ui=checkout).
![Pricing plan example](https://b.stripecdn.com/docs-statics-srv/assets/checkout_pricing_plan_example.2156a15535345b113c30e7efabe72867.png)

A pricing plan displayed in Stripe Checkout

| Term                      | Definition                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Pricing plan              | A customizable container of pricing components (such as rate cards, license fees, and recurring credit grants) that defines how you bill for your service. For example, you can create a pricing plan that includes [rate cards](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md) for usage-based billing, [license fees](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/license-fees/about.md) for recurring charges, and [service actions](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/service-actions/about.md) for recurring credit grant allocations. When a customer subscribes to a pricing plan, all the recurring components are automatically enrolled and billed according to the cadence you configure. |
| Pricing plan component    | A part of the pricing plan, such as a [rate card](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md), [license fee](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/license-fees/about.md), or [service action](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/service-actions/about.md). Each component has a version to ensure that they’re used consistently in pricing plans. If you don’t specify a component version when you attach it to the pricing plan, the default version is used.                                                                                                                                                                                                                           |
| Pricing plan subscription | A pricing plan subscription is created when a customer is subscribed to a specific pricing plan version. Subscriptions generate and charge customers according to an underlying billing cadence.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Pricing plan version      | A pricing plan version is a versioned snapshot of a pricing plan. When you create a pricing plan, you need to set a live version before you can activate the plan or subscribe customers to it. Modifying or deleting existing components creates a new version. Adding a license fee or service action creates a new version. Adding a rate card doesn’t create a new version. When subscribing customers, you can specify a version or let Stripe assign the current live version. Customers stay on their assigned version unless manually changed, which lets you set different pricing for new and existing customers.                                                                                                                                                                            |

#### Pricing plan versioning 

Pricing plans support versioning to manage changes to your billing structure over time. Each version of a pricing plan is immutable. When you update a pricing plan by modifying or deleting existing components, a new version is created. Adding a license fee or service action creates a new version. Adding a rate card doesn’t create a new version. This versioning system helps you:

- Schedule and communicate pricing changes to customers.
- Manage different pricing for various customer segments.
- Track and maintain a history of your pricing models.

Each pricing plan has two version properties:

- [latest_version](https://docs.stripe.com/api/v2/pricing-plans/pricing-plan/object.md?api-version=preview#v2_pricing_plan_object-latest_version): This is the most recent version after updates.
- [live_version](https://docs.stripe.com/api/v2/pricing-plans/pricing-plan/object.md?api-version=preview#v2_pricing_plan_object-live_version): This is the version used by default for new subscriptions unless a specific version is provided.

Learn more about [working with pricing plan versions and managing components](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions/manage.md#manage-pricing-plan-components).

### Pricing plan subscription concepts 

Here are the key concepts for understanding how pricing plan subscriptions work.

| Term                       | Definition                                                                                                                                                                                                                                                                                                                                |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Billing interval (cadence) | A [billing cadence](https://docs.stripe.com/api/v2/billing-cadences.md?api-version=preview) defines when you send and generate invoices. The generated invoice only consolidates charges that have accrued during one or more service intervals. You can configure different billing intervals to match your business model. For example: |

  - **Monthly**: The customer receives a monthly invoice for all service usage in the previous month.
  - **Quarterly**: Usage fees accrue monthly, but you only generate invoices once every 3 months.
  - **Annual**: You bill the customer once a year for all services used during that year.

  Billing intervals belong to customers—one billing interval has one customer. (Each customer can have multiple billing intervals.) |
| Pricing plan subscriptions | A [pricing plan subscription](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions.md) is created when a customer is subscribed to a specific pricing plan version. Subscriptions generate and charge customers according to an underlying billing [cadence](https://docs.stripe.com/api/v2/billing-cadences.md?api-version=preview).                                                                                                                                                                                                                                                                                                                                                                                                            |

### Rate card concepts 

Here are the key concepts for understanding how rate cards work.

| Term              | Definition                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Dimension         | Dimensions let you create usage-based pricing models that vary based on one or more properties. You can specify dimensions when you [create a meter](https://docs.stripe.com/api/billing/meter/create.md?api-version=preview) (in the [dimension_payload_keys](https://docs.stripe.com/api/billing/meter/create.md?api-version=preview#create_billing_meter-dimension_payload_keys) parameter) or [metered item](https://docs.stripe.com/api/v2/metered-items/create.md?api-version=preview) (in the [meter_segment_conditions](https://docs.stripe.com/api/v2/metered-items/create.md?api-version=preview#v2_create_metered_items-meter_segment_conditions-dimension) array), or [submit usage](https://docs.stripe.com/api/v2/billing/meter-event/create.md?api-version=preview) (in the [payload](https://docs.stripe.com/api/v2/billing/meter-event/create.md?api-version=preview)). |
| Rate card         | A [rate card](https://docs.stripe.com/api/v2/product-catalog/create-ratecard.md?api-version=preview) is a collection of usage-based rates, representing a product. You can subscribe customers to a rate card by creating a pricing plan subscription that’s associated with a billing interval.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Rate card rate    | A [rate card rate](https://docs.stripe.com/api/v2/product-catalog/create-ratecardrate.md?api-version=preview) is the pricing configuration for a metered item in a rate card. The rate defines the price type (fixed rate, volume, graduated, or overage), price amount, and quantity configuration (you can sell individual units or packages of units). Each rate card can contain multiple rates (up to 500).                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Rate card version | A rate card version is a versioned snapshot of a rate card. When you create a rate card, an initial live version is set as the default for new subscribers. Modifying or deleting existing rates creates a new version; adding new rates doesn’t create a new version. When subscribing customers, you can specify a version or let Stripe assign the current live version. Customers stay on their assigned version unless manually changed, which lets you set different pricing for new and existing customers.                                                                                                                                                                                                                                                                                                                                                                       |

### License fee concepts 

| Term                | Definition                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| License fee         | A [license fee](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/license-fees/about.md) is a fixed, recurring charge for a billable item, such as a monthly subscription fee. It includes details such as price, billing frequency, and tax behavior.                                                                                                                                                                      |
| License fee version | A snapshot of the license fee. When you create a license fee, an initial live version is set as the default for new subscribers. When you add a license fee to a pricing plan, you can specify a version or let Stripe assign the current live version. Attaching or updating a license fee to a pricing plan increments the pricing plan version. You can make additional changes to the pricing plan, or set the new pricing plan live version. |

### Service action concepts 

| Term           | Definition                                                                                                                                                                                               |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Service action | A service action defines a recurring credit grant, specifying the amount, billing frequency, and applicable billable items. This credit can reduce charges for specific items, such as usage-based fees. |
| Type           | The specific recurring action you create. (Currently, only `credit_grant` is supported.)                                                                                                                 |

## Lifecycle

Here’s what the lifecycle of a pricing plan looks like:

1. You create the pricing plan, which can include rate cards, license fees, and service actions.
1. Subscribe a customer to the pricing plan using Checkout or the API.
1. Usage is recorded and aggregated for each service interval.
1. An invoice is created for the subscription according to the billing interval.
1. The customer’s payment method is charged.

## Billing interval and service interval 

The [billing cadence](https://docs.stripe.com/api/v2/billing-cadences.md?api-version=preview) defines when you generate invoices. The generated invoice consolidates charges that have accrued during one or more service intervals. You can configure different billing intervals to match your business model and pricing structures. You must configure the service interval to be longer than or equal to the billing interval. For example, you can configure a quarterly service interval on a quarterly or monthly cadence but not a monthly service interval on a quarterly cadence.

When a service interval ends, Stripe calculates charges based on usage and recurring fees during that period (for example, a customer’s usage for the past week). These charges are added to the customer’s account, and a new invoice item is created but isn’t necessarily billed immediately.

When a billing interval ends, all accrued charges since the last billing interval are compiled into an invoice and sent to the customer.

This separation allows for flexible billing arrangements, such as monthly service measurement with yearly invoicing, or daily service measurement with weekly billing.

### Examples

Customers are only billed for completed service intervals. If a customer is billed while a service interval is still accruing usage, the pricing plan subscription only includes the usage from the previous service interval. Any new usage is added to the invoice for the next billing interval.

License fees are billed one service interval in advance regardless of the billing interval.

#### Service interval of 5 months with an annual billing interval

In this example, a business has the following setup:

- **Service interval**: Every 5 months
- **Billing interval**: Every year on March 31

The customer is only billed for the completed service intervals within the annual billing interval. In this example, the invoice is for 10 months of usage, representing the two completed service intervals.
![Diagram illustrating how a 5-month service interval is invoiced on an annual billing interval.](https://b.stripecdn.com/docs-statics-srv/assets/service-interval-5-month-cadence-annual-diagram.0ce339d4cc38cd8956e0dda7ad39d9d7.png)

With a 5-month service interval and annual billing interval, the customer is only billed for the completed service intervals.

### Set up a separate billing interval and service interval 

You can provide customers with more frequent usage periods by assessing usage on a weekly basis (this is the service interval). However, to reduce administrative overhead, you might only want to generate invoices on a monthly basis (this is the billing interval).

Defining the service interval and billing interval separately gives you the flexibility to aggregate usage and provision access at one frequency (for example, weekly) but bill customers at another (for example, monthly). This can help to optimize your cash flow.

#### Dashboard

To set up a separate billing interval and service interval in the Dashboard:

1. [Create a rate card](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md#create-rate-card).
1. Define a service interval that determines how often usage is aggregated (for example, weekly).
1. [Subscribe a customer to a pricing plan](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md#subscribe).
1. Define a billing interval that determines how often invoices are generated (for example, monthly—this doesn’t have to be the same frequency as the service interval).

#### API

To set up a separate billing interval and service interval using the API:

First, [create a rate card](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md#create-rate-card). This is when you define the `service_interval`, along with a display name and tax behavior. In this example, it’s a weekly service interval.

```curl
curl -X POST https://api.stripe.com/v2/billing/rate_cards \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Hypernian",
    "service_interval": "week",
    "service_interval_count": 1,
    "currency": "usd",
    "tax_behavior": "exclusive"
  }'
```

You also need to [create metered items](https://docs.stripe.com/api/v2/metered-items/create.md?api-version=preview) and [rates](https://docs.stripe.com/api/v2/product-catalog/create-ratecardrate.md?api-version=preview).

Define a monthly billing interval for your customer. The `billing_cycle` parameter defines when and how the payer is invoiced.

```curl
curl -X POST https://api.stripe.com/v2/billing/cadences \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "payer": {
        "type": "customer",
        "customer": "{{CUSTOMER_ID}}"
    },
    "billing_cycle": {
        "type": "month",
        "interval_count": 1,
        "month": {
            "day_of_month": 20
        }
    }
  }'
```

Finally, [create a pricing plan subscription](https://docs.stripe.com/api/v2/billing-intents/create.md?api-version=preview#v2_create_billing_intents-actions-subscribe) to connect the pricing plan to the billing interval:

```curl
curl -X POST https://api.stripe.com/v2/billing/intents \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "cadence": "{{BILLING_CADENCE_ID}}",
    "currency": "usd",
    "effective_at": "on_commit",
    "actions": [
        {
            "type": "subscribe",
            "subscribe": {
                "type": "pricing_plan_subscription_details",
                "proration_behavior": "none",
                "pricing_plan_subscription_details": {
                    "pricing_plan": "{{PRICING_PLAN_ID}}",
                    "pricing_plan_version": "{{PRICING_PLAN_VERSION_ID}}",
                    "component_configurations": []
                }
            }
        }
    ]
  }'
```

## Revenue Recognition

[Revenue Recognition](https://docs.stripe.com/revenue-recognition.md) for [usage-based billing](https://docs.stripe.com/billing/subscriptions/usage-based-v2/overview.md) ensures that you have accurate financial reporting while enabling your AI or SaaS business to leverage flexible, consumption-based pricing models. It follows a delivery-based approach where revenue is recognized when the service is actually delivered or consumed, not when it’s sold or invoiced.

Revenue Recognition has two key components:

- **Sales transaction**: Records the sale of usage-based services and when the service was actually consumed.
- **Invoice line items**: Records when the customer was billed.

### How revenue recognition works with usage-based billing

With usage-based billing, revenue recognition has three main stages:

- **Revenue accrual**: Revenue is recognized at the time of delivery, based on the actual consumption of services.
- **Revenue reversal**: When invoices are finalized, a revenue reversal on the original revenue accrual occurs. This step is essential for ensuring the revenue recognition accurately reflects the amounts billed to the customer.
- **Rebooking the invoice**: When the invoice is finalized, rebooking the invoice involves recognizing the actual treatment against the invoiced amount.

#### Example

In this example, a customer consumes 100 USD worth of API calls over 3 months, then gets billed:

- January (Revenue accrual): In the first month, they consume 40 USD worth of API calls.
- February (Revenue accrual): In the second month, they consume 35 USD worth of API calls.
- March (Revenue accrual): In the third month, they consume 25 USD worth of API calls.
- April (Revenue reversal and rebooking of the invoice): After three months, the customer receives an invoice for 100 USD (their total usage).
- May (Payment): The customer pays the invoice of 100 USD.

| Account     | Jan 2025 | Feb 2025 | Mar 2025 | Apr 2025 | May 2025 | Total    |
| ----------- | -------- | -------- | -------- | -------- | -------- | -------- |
| Revenue     | +40 USD  | +35 USD  | +25 USD  |          |          | +100 USD |
| Unbilled AR | +40 USD  | +35 USD  | +25 USD  | -100 USD |          |          |
| AR          |          |          |          | +100 USD | -100 USD |          |
| Cash        |          |          |          |          | +100 USD | +100 USD |

### Limitations

Using Revenue Recognition with usage-based billing has the following limitations during private preview:

- Meters using `last` or `max` aggregation types are currently not supported.
- Advanced usage-based billing uses [billable_items](https://docs.stripe.com/api/billing/credit-grant/object.md?api-version=preview#billing_credit_grant_object-applicability_config-scope-billable_items), which aren’t fully supported in the current reports.
- Journal entries for usage-based billing transactions display the `billable_item` ID as the product ID. However, product details such as product name, description, and other attributes appear empty in reports.

## Automatic tax

You can enable automatic tax on [pricing plan subscriptions](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions.md) by using [Stripe Checkout](https://docs.stripe.com/payments/checkout.md) or by directly using the API.

#### Checkout

```curl
curl https://api.stripe.com/v1/checkout/sessions \
  -u "<<YOUR_SECRET_KEY>>:" \
  -H "Stripe-Version: 2025-09-30.preview;checkout_product_catalog_preview=v1" \
  -d customer={{CUSTOMER_ID}} \
  -d "checkout_items[0][type]"=pricing_plan_subscription_item \
  -d "checkout_items[0][pricing_plan_subscription_item][pricing_plan]"={{PRICING_PLAN_ID}} \
  -d "checkout_items[0][pricing_plan_subscription_item][component_configurations][{{LICENSE_COMPONENT_ID}}][type]"=license_fee_component \
  -d "checkout_items[0][pricing_plan_subscription_item][component_configurations][{{LICENSE_COMPONENT_ID}}][license_fee_component][quantity]"=1 \
  -d "automatic_tax[enabled]"=true
```

#### API

To subscribe a customer to a pricing plan, you need to:

1. [Create a Customer](https://docs.stripe.com/api/customers/create.md). This could be the customer created [during the Checkout Session](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#set-up-checkout).
1. [Create a Billing profile](https://docs.stripe.com/api/v2/billing-profile.md?api-version=preview) for the pricing plan subscription.
1. [Create a Billing setting](https://docs.stripe.com/api/v2/billing-settings.md?api-version=preview) with tax enabled.
1. [Create a billing cadence](https://docs.stripe.com/api/v2/product-catalog/create-cadence.md).
1. Create a [billing intent](https://docs.stripe.com/api/v2/billing-intents/create.md), which creates a [pricing plan subscription](https://docs.stripe.com/api/v2/pricing-plan-subscriptions.md) that references the pricing plan and billing cadence.

Create a customer:

```curl
curl https://api.stripe.com/v1/customers \
  -u "<<YOUR_SECRET_KEY>>:" \
  --data-urlencode email="jenny.rosen@example.com" \
  -d name="Jenny Rosen"
```

```cli
stripe customers create  \
  --email="jenny.rosen@example.com" \
  --name="Jenny Rosen"
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

customer = client.v1.customers.create({
  email: 'jenny.rosen@example.com',
  name: 'Jenny Rosen',
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
customer = client.v1.customers.create({
  "email": "jenny.rosen@example.com",
  "name": "Jenny Rosen",
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$customer = $stripe->customers->create([
  'email' => 'jenny.rosen@example.com',
  'name' => 'Jenny Rosen',
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

CustomerCreateParams params =
  CustomerCreateParams.builder()
    .setEmail("jenny.rosen@example.com")
    .setName("Jenny Rosen")
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
Customer customer = client.v1().customers().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const customer = await stripe.customers.create({
  email: 'jenny.rosen@example.com',
  name: 'Jenny Rosen',
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.CustomerCreateParams{
  Email: stripe.String("jenny.rosen@example.com"),
  Name: stripe.String("Jenny Rosen"),
}
result, err := sc.V1Customers.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new CustomerCreateOptions
{
    Email = "jenny.rosen@example.com",
    Name = "Jenny Rosen",
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Customers;
Customer customer = service.Create(options);
```

Create a billing profile:

```curl
curl -X POST https://api.stripe.com/v2/billing/profiles \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "customer": "{{CUSTOMER_ID}}",
    "display_name": "Automatic collection settings",
    "lookup_key": "billing_profile_cus_123",
    "metadata": {
        "test": "data"
    }
  }'
```

To control the tax behavior on a billing cadence, [create a bill settings](https://docs.stripe.com/api/v2/billing-settings/create.md) object:

```curl
curl -X POST https://api.stripe.com/v2/billing/bill_settings \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Re-selling configuration",
    "calculation": {
        "tax": {
            "type": "automatic"
        }
    }
  }'
```

Then add the billing profile and [bill settings](https://docs.stripe.com/api/v2/billing-settings/create.md) to the billing cadence:

```curl
curl -X POST https://api.stripe.com/v2/billing/cadences \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "payer": {
        "billing_profile": "{{BILLING_PROFILE_ID}}"
    },
    "billing_cycle": {
        "type": "month",
        "interval_count": 1,
        "month": {
            "day_of_month": 20
        }
    }
  }'
```

Subscribe your customer to the pricing plan by creating a [billing intent](https://docs.stripe.com/api/v2/billing-intents/object.md) and passing the pricing plan and billing cadence IDs.

```curl
curl -X POST https://api.stripe.com/v2/billing/intents \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "currency": "usd",
    "cadence": "{{CADENCE_ID}}",
    "actions": [
        {
            "type": "subscribe",
            "subscribe": {
                "type": "pricing_plan_subscription_details",
                "pricing_plan_subscription_details": {
                    "pricing_plan": "{{PRICING_PLAN_ID}}",
                    "pricing_plan_version": "{{PRICING_PLAN_VERSION}}",
                    "component_configurations": []
                }
            }
        }
    ]
  }'
```

Next, reserve the billing intent. You can determine how much to charge your customer based on the preview that generates when you [reserve](https://docs.stripe.com/api/v2/billing-intents/reserve.md?api-version=preview) the billing intent.

```curl
curl -X POST https://api.stripe.com/v2/billing/intents/{{BILLING_INTENT_ID}}/reserve \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview"
```

Next, commit the billing intent to activate the pricing plan subscription and bill the customer according to the plan and cadence. You also need to specify the [PaymentIntent](https://docs.stripe.com/api/payment_intents.md) ID if your collection setting is set to charge automatically. (You don’t need to do this if you set the collection setting to `send_invoice`.) To get the PaymentIntent ID, find it in the response, [list all PaymentIntents](https://docs.stripe.com/api/payment_intents/list.md), or find it in the [Payments page in the Dashboard](https://dashboard.stripe.com/payments).

```curl
curl https://api.stripe.com/v1/payment_intents \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d amount=1000 \
  -d currency=usd \
  -d customer={{CUSTOMER_ID}} \
  -d payment_method={{PAYMENT_METHOD_ID}} \
  --data-urlencode return_url="https://example.com/return" \
  -d confirm=true
```

```cli
stripe payment_intents create  \
  --amount=1000 \
  --currency=usd \
  --customer={{CUSTOMER_ID}} \
  --payment-method={{PAYMENT_METHOD_ID}} \
  --return-url="https://example.com/return" \
  --confirm=true
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

payment_intent = client.v1.payment_intents.create({
  amount: 1000,
  currency: 'usd',
  customer: '{{CUSTOMER_ID}}',
  payment_method: '{{PAYMENT_METHOD_ID}}',
  return_url: 'https://example.com/return',
  confirm: 'true',
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
payment_intent = client.v1.payment_intents.create({
  "amount": 1000,
  "currency": "usd",
  "customer": "{{CUSTOMER_ID}}",
  "payment_method": "{{PAYMENT_METHOD_ID}}",
  "return_url": "https://example.com/return",
  "confirm": True,
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$paymentIntent = $stripe->paymentIntents->create([
  'amount' => 1000,
  'currency' => 'usd',
  'customer' => '{{CUSTOMER_ID}}',
  'payment_method' => '{{PAYMENT_METHOD_ID}}',
  'return_url' => 'https://example.com/return',
  'confirm' => true,
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

PaymentIntentCreateParams params =
  PaymentIntentCreateParams.builder()
    .setAmount(1000L)
    .setCurrency("usd")
    .setCustomer("{{CUSTOMER_ID}}")
    .setPaymentMethod("{{PAYMENT_METHOD_ID}}")
    .setReturnUrl("https://example.com/return")
    .setConfirm(true)
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
PaymentIntent paymentIntent = client.v1().paymentIntents().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const paymentIntent = await stripe.paymentIntents.create({
  amount: 1000,
  currency: 'usd',
  customer: '{{CUSTOMER_ID}}',
  payment_method: '{{PAYMENT_METHOD_ID}}',
  return_url: 'https://example.com/return',
  confirm: true,
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.PaymentIntentCreateParams{
  Amount: stripe.Int64(1000),
  Currency: stripe.String(stripe.CurrencyUSD),
  Customer: stripe.String("{{CUSTOMER_ID}}"),
  PaymentMethod: stripe.String("{{PAYMENT_METHOD_ID}}"),
  ReturnURL: stripe.String("https://example.com/return"),
  Confirm: stripe.Bool(true),
}
result, err := sc.V1PaymentIntents.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new PaymentIntentCreateOptions
{
    Amount = 1000,
    Currency = "usd",
    Customer = "{{CUSTOMER_ID}}",
    PaymentMethod = "{{PAYMENT_METHOD_ID}}",
    ReturnUrl = "https://example.com/return",
    Confirm = true,
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.PaymentIntents;
PaymentIntent paymentIntent = service.Create(options);
```

```curl
curl -X POST https://api.stripe.com/v2/billing/intents/{{BILLING_INTENT_ID}}/commit \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "payment_intent": "{{PAYMENT_INTENT_ID}}"
  }'
```

Learn more about [billing intent states](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions/manage.md#billing-intent-states).

You can optionally pass a specific version of a pricing plan when subscribing a customer. If you don’t specify a version, the subscription applies the pricing plan’s live version.

```curl
curl -X POST https://api.stripe.com/v2/billing/intents \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "currency": "usd",
    "effective_at": "on_commit",
    "cadence": "bc_test_61SrjnScUwT6mNskZ16SjPfE4ZSQFjWjdqlzQfWMCVnM",
    "actions": [
        {
            "type": "subscribe",
            "subscribe": {
                "type": "pricing_plan_subscription_details",
                "proration_behavior": "none",
                "pricing_plan_subscription_details": {
                    "pricing_plan": "{{PRICING_PLAN_ID}}",
                    "pricing_plan_version": "{{PRICING_PLAN_VERSION}}",
                    "component_configurations": []
                }
            }
        }
    ]
  }'
```

# Set up a pay-as-you-go pricing model

Charge customers according to how much they consume on your platform.

[Pay-as-you-go pricing](https://docs.stripe.com/subscriptions/pricing-models/usage-based-pricing.md#pay-as-you-go) is a flexible, scalable model that lets you charge customers in arrears for the usage they accrue. AI businesses, SaaS platforms, and cloud services often use this pricing model. Learn more about how [advanced usage-based billing works](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md).

> Pricing plans are currently in [private preview](https://docs.stripe.com/release-phases.md) and could change in functionality and integration path before they’re generally available to all Stripe users. Contact us  to request access.

## What you’ll build

This guide describes how to implement pay-as-you-go pricing on Stripe with [advanced usage-based billing](https://docs.stripe.com/billing/subscriptions/usage-based-v2/overview.md) for a fictional company called Hypernian. Hypernian charges their customers the following rates for their LLM models, Hypernian 1 and Hypernian Max:

- 0.05 USD per Hypernian_1 token
- 0.1 USD per Hypernian_max token

To implement this pricing model, you create a pricing plan and set up a meter to record usage on both of Hypernian’s LLM models.

## Create a pricing plan

[Pricing plans](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md) let you group a set of pricing components into a single package that you can charge customers for.

#### Dashboard

1. On the [Pricing plans](https://dashboard.stripe.com/test/pricing-plans) page, click **Create pricing plan**.
1. In the pricing plan editor:
   - Provide a display name, currency, and tax behavior.
   - (Optional) Under **Advanced settings**, specify the description, unique lookup key, and metadata.
1. Click **Continue**.

#### API

Use the API to [create a pricing plan](https://docs.stripe.com/api/v2/pricing-plans/create.md?api-version=preview).

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Pricing plan",
    "currency": "usd",
    "tax_behavior": "exclusive"
  }'
```

```cli
stripe v2 billing pricing_plans create  \
  --display-name="Pricing plan" \
  --currency=usd \
  --tax-behavior=exclusive
```

```ruby
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

pricing_plan = client.v2.billing.pricing_plans.create({
  display_name: 'Pricing plan',
  currency: 'usd',
  tax_behavior: 'exclusive',
})
```

```python
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

pricing_plan = client.v2.billing.pricing_plans.create({
  "display_name": "Pricing plan",
  "currency": "usd",
  "tax_behavior": "exclusive",
})
```

```php
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$pricingPlan = $stripe->v2->billing->pricingPlans->create([
  'display_name' => 'Pricing plan',
  'currency' => 'usd',
  'tax_behavior' => 'exclusive',
]);
```

```java
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

PricingPlanCreateParams params =
  PricingPlanCreateParams.builder()
    .setDisplayName("Pricing plan")
    .setCurrency("usd")
    .setTaxBehavior(PricingPlanCreateParams.TaxBehavior.EXCLUSIVE)
    .build();

PricingPlan pricingPlan = client.v2().billing().pricingPlans().create(params);
```

```node
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const pricingPlan = await stripe.v2.billing.pricingPlans.create({
  display_name: 'Pricing plan',
  currency: 'usd',
  tax_behavior: 'exclusive',
});
```

```go
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.V2BillingPricingPlanCreateParams{
  DisplayName: stripe.String("Pricing plan"),
  Currency: stripe.String(stripe.CurrencyUSD),
  TaxBehavior: stripe.String("exclusive"),
}
result, err := sc.V2BillingPricingPlans.Create(context.TODO(), params)
```

```dotnet
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.V2.Billing.PricingPlanCreateOptions
{
    DisplayName = "Pricing plan",
    Currency = "usd",
    TaxBehavior = "exclusive",
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V2.Billing.PricingPlans;
Stripe.V2.Billing.PricingPlan pricingPlan = service.Create(options);
```

## Create a rate card and add rates

To define how much to charge your customers for usage, create a [rate card](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md) and add rates for each metered item.

#### Dashboard

### Create the rate card

1. In the pricing plan editor, click + and **Rate card**.
1. In the rate card editor:
   - Provide a display name.
   - Specify the servicing period (for example, monthly).
   - (Optional) Under **Advanced settings**, provide a lookup key and metadata.
1. Click **Continue**.

### Add rates for each model

You need to create a [meter](https://docs.stripe.com/api/billing/meter.md?api-version=preview) first if you haven’t already. Meters specify how to aggregate [Meter Events](https://docs.stripe.com/api/v2/billing-meter.md?api-version=preview), which represent the actions that customers take in your system, over a billing period. In the Dashboard, you can create a new meter while adding rates to the rate card.

For the Hypernian_1 model:

1. In the rate editor:
   - Provide a display name (for example, `Hypernian_1 tokens`).
   - Select an existing **Meter** or create a new one by clicking +.
     - If creating a new meter, provide:
       - Meter name: `Prompts meter`
       - Event name: `prompt_meter`
       - Aggregation method: `sum`
       - Dimension payload key: `model`
       - Value key override: `tokens_used`
   - Add the pricing dimension `model`.
   - Provide the `model` dimension value: `hypernian_1`
   - Select the **Price type**: **Fixed rate**.
   - Select **Sell as**: Individual units.
   - Enter the **Price per unit**: `0.05 USD`.
   - (Optional) Configure **Advanced settings** like **Product tax code**, **Unit label**, **Lookup key**, and **Metadata**.
1. Click **Done**.

For the Hypernian_max model:

1. Click + **Add rate** to add another rate to the rate card.
1. In the rate editor:
   - Provide a display name (for example, `Hypernian_max tokens`).
   - Select the same **Meter** you created or selected earlier.
   - Add the pricing dimension `model`.
   - Provide the `model` dimension value: `hypernian_max`
   - Select the **Price type**: **Fixed rate**.
   - Select **Sell as**: Individual units.
   - Enter the **Price per unit**: `0.10 USD`.
   - (Optional) Configure **Advanced settings**.
1. Click **Done**.

After you finish configuring the pricing plan, click **Create pricing plan**.

#### API

### Create a meter

[Meters](https://docs.stripe.com/api/billing/meter.md?api-version=preview&) specify how to aggregate [Meter Events](https://docs.stripe.com/api/v2/billing-meter.md?api-version=preview), which represent the actions that customers take in your system, over a billing period.

Use the API to [create a meter](https://docs.stripe.com/api/v1/billing/meters/create.md?api-version=preview).

```curl
curl https://api.stripe.com/v1/billing/meters \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d display_name="Prompts meter" \
  -d event_name=prompt_meter \
  -d "default_aggregation[formula]"=sum \
  -d "value_settings[event_payload_key]"=tokens_used \
  -d "dimension_payload_keys[]"=model
```

### Create metered items

A [Metered Item](https://docs.stripe.com/api/v2/metered-items.md?api-version=preview) represents any item that you bill customers for based on how much they use it, such as hourly cloud CPU usage or tokens generated by an AI service.

Use the API to [create a metered item](https://docs.stripe.com/api/v2/metered-items/create.md?api-version=preview) for the `Hypernian_1` model.

```curl
curl -X POST https://api.stripe.com/v2/billing/metered_items \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Hypernian_1_model",
    "meter": "{{METER_ID}}",
    "meter_segment_conditions": [
        {
            "dimension": "model",
            "value": "hypernian_1"
        }
    ]
  }'
```

```cli
stripe v2 billing metered_items create  \
  --display-name=Hypernian_1_model \
  --meter={{METER_ID}} \
  --meter-segment-conditions.dimension=model \
  --meter-segment-conditions.value=hypernian_1
```

```ruby
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

metered_item = client.v2.billing.metered_items.create({
  display_name: 'Hypernian_1_model',
  meter: '{{METER_ID}}',
  meter_segment_conditions: [
    {
      dimension: 'model',
      value: 'hypernian_1',
    },
  ],
})
```

```python
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

metered_item = client.v2.billing.metered_items.create({
  "display_name": "Hypernian_1_model",
  "meter": "{{METER_ID}}",
  "meter_segment_conditions": [{"dimension": "model", "value": "hypernian_1"}],
})
```

```php
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$meteredItem = $stripe->v2->billing->meteredItems->create([
  'display_name' => 'Hypernian_1_model',
  'meter' => '{{METER_ID}}',
  'meter_segment_conditions' => [
    [
      'dimension' => 'model',
      'value' => 'hypernian_1',
    ],
  ],
]);
```

```java
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

MeteredItemCreateParams params =
  MeteredItemCreateParams.builder()
    .setDisplayName("Hypernian_1_model")
    .setMeter("{{METER_ID}}")
    .addMeterSegmentCondition(
      MeteredItemCreateParams.MeterSegmentCondition.builder()
        .setDimension("model")
        .setValue("hypernian_1")
        .build()
    )
    .build();

MeteredItem meteredItem = client.v2().billing().meteredItems().create(params);
```

```node
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const meteredItem = await stripe.v2.billing.meteredItems.create({
  display_name: 'Hypernian_1_model',
  meter: '{{METER_ID}}',
  meter_segment_conditions: [
    {
      dimension: 'model',
      value: 'hypernian_1',
    },
  ],
});
```

```go
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.V2BillingMeteredItemCreateParams{
  DisplayName: stripe.String("Hypernian_1_model"),
  Meter: stripe.String("{{METER_ID}}"),
  MeterSegmentConditions: []*stripe.V2BillingMeteredItemCreateMeterSegmentConditionParams{
    &stripe.V2BillingMeteredItemCreateMeterSegmentConditionParams{
      Dimension: stripe.String("model"),
      Value: stripe.String("hypernian_1"),
    },
  },
}
result, err := sc.V2BillingMeteredItems.Create(context.TODO(), params)
```

```dotnet
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.V2.Billing.MeteredItemCreateOptions
{
    DisplayName = "Hypernian_1_model",
    Meter = "{{METER_ID}}",
    MeterSegmentConditions = new List<Stripe.V2.Billing.MeteredItemCreateMeterSegmentConditionOptions>
    {
        new Stripe.V2.Billing.MeteredItemCreateMeterSegmentConditionOptions
        {
            Dimension = "model",
            Value = "hypernian_1",
        },
    },
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V2.Billing.MeteredItems;
Stripe.V2.Billing.MeteredItem meteredItem = service.Create(options);
```

And another metered item to aggregate customer usage of the `Hypernian_max` model.

```curl
curl -X POST https://api.stripe.com/v2/billing/metered_items \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Hypernian_max_model",
    "meter": "{{METER_ID}}",
    "meter_segment_conditions": [
        {
            "dimension": "model",
            "value": "hypernian_max"
        }
    ]
  }'
```

```cli
stripe v2 billing metered_items create  \
  --display-name=Hypernian_max_model \
  --meter={{METER_ID}} \
  --meter-segment-conditions.dimension=model \
  --meter-segment-conditions.value=hypernian_max
```

```ruby
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

metered_item = client.v2.billing.metered_items.create({
  display_name: 'Hypernian_max_model',
  meter: '{{METER_ID}}',
  meter_segment_conditions: [
    {
      dimension: 'model',
      value: 'hypernian_max',
    },
  ],
})
```

```python
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

metered_item = client.v2.billing.metered_items.create({
  "display_name": "Hypernian_max_model",
  "meter": "{{METER_ID}}",
  "meter_segment_conditions": [{"dimension": "model", "value": "hypernian_max"}],
})
```

```php
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$meteredItem = $stripe->v2->billing->meteredItems->create([
  'display_name' => 'Hypernian_max_model',
  'meter' => '{{METER_ID}}',
  'meter_segment_conditions' => [
    [
      'dimension' => 'model',
      'value' => 'hypernian_max',
    ],
  ],
]);
```

```java
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

MeteredItemCreateParams params =
  MeteredItemCreateParams.builder()
    .setDisplayName("Hypernian_max_model")
    .setMeter("{{METER_ID}}")
    .addMeterSegmentCondition(
      MeteredItemCreateParams.MeterSegmentCondition.builder()
        .setDimension("model")
        .setValue("hypernian_max")
        .build()
    )
    .build();

MeteredItem meteredItem = client.v2().billing().meteredItems().create(params);
```

```node
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const meteredItem = await stripe.v2.billing.meteredItems.create({
  display_name: 'Hypernian_max_model',
  meter: '{{METER_ID}}',
  meter_segment_conditions: [
    {
      dimension: 'model',
      value: 'hypernian_max',
    },
  ],
});
```

```go
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.V2BillingMeteredItemCreateParams{
  DisplayName: stripe.String("Hypernian_max_model"),
  Meter: stripe.String("{{METER_ID}}"),
  MeterSegmentConditions: []*stripe.V2BillingMeteredItemCreateMeterSegmentConditionParams{
    &stripe.V2BillingMeteredItemCreateMeterSegmentConditionParams{
      Dimension: stripe.String("model"),
      Value: stripe.String("hypernian_max"),
    },
  },
}
result, err := sc.V2BillingMeteredItems.Create(context.TODO(), params)
```

```dotnet
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.V2.Billing.MeteredItemCreateOptions
{
    DisplayName = "Hypernian_max_model",
    Meter = "{{METER_ID}}",
    MeterSegmentConditions = new List<Stripe.V2.Billing.MeteredItemCreateMeterSegmentConditionOptions>
    {
        new Stripe.V2.Billing.MeteredItemCreateMeterSegmentConditionOptions
        {
            Dimension = "model",
            Value = "hypernian_max",
        },
    },
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V2.Billing.MeteredItems;
Stripe.V2.Billing.MeteredItem meteredItem = service.Create(options);
```

### Create a rate card

To define how much to charge your customers per metered item, create a [rate card](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md), which keeps track of the rates associated with a subscription.

You add rates to the rate card, then attach the rate card to a pricing plan.

Use the API to [create a rate card](https://docs.stripe.com/api/v2/rate-cards/create.md?api-version=preview).

```curl
curl -X POST https://api.stripe.com/v2/billing/rate_cards \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Rate Card",
    "service_interval": "month",
    "service_interval_count": 1,
    "currency": "usd",
    "tax_behavior": "exclusive"
  }'
```

### Add rates to the rate card

After you create the rate card, add rates to it to define how much to charge your customers per metered item. This example uses the following pricing model, where each type of token is a metered item with a defined rate:

- 0.05 USD per Hypernian_1 token
- 0.1 USD per Hypernian_max token

Set the rate for the Hypernian_1 model as 0.05 USD per token. Save the rate card ID and version in the response.

```curl
curl -X POST https://api.stripe.com/v2/billing/rate_cards/{{RATE_CARD_ID}}/rates \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "metered_item": "{{METERED_ITEM_ID_1}}",
    "unit_amount": "5"
  }'
```

Then, set the rate for the Hypernian Max model as 0.1 USD per token. Save the rate card ID and version in the response.

```curl
curl -X POST https://api.stripe.com/v2/billing/rate_cards/{{RATE_CARD_ID}}/rates \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "metered_item": "{{METERED_ITEM_ID_2}}",
    "unit_amount": "10"
  }'
```

### Attach the rate card to the pricing plan

After you create the rate card and set the rates, attach the rate card to the pricing plan.

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "type": "rate_card",
    "rate_card": {
        "id": "{{RATE_CARD_ID}}",
        "version": "{{RATE_CARD_VERSION}}"
    }
  }'
```

### Activate the pricing plan

After you add the rate card to your pricing plan, activate that version of the pricing plan. After the plan is activated, you can subscribe customers to it.

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}} \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "live_version": "latest"
  }'
```

## Subscribe a customer to the pricing plan

After you create the pricing plan and rate card, subscribe a customer to the pricing plan. You can use a [Checkout Session](https://docs.stripe.com/api/checkout/sessions.md?api-version=preview) to collect payment information and create the subscription, or you can [directly subscribe a customer using the API](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md?payment-ui=direct-api#subscribe).

For testing, you can use a [test clock](https://docs.stripe.com/billing/testing/test-clocks.md) to simulate subscription billing cycles.

```curl
curl https://api.stripe.com/v1/checkout/sessions \
  -u "<<YOUR_SECRET_KEY>>:" \
  -H "Stripe-Version: 2025-09-30.preview;checkout_product_catalog_preview=v1" \
  -d customer={{CUSTOMER_ID}} \
  -d "checkout_items[0][type]"=pricing_plan_subscription_item \
  -d "checkout_items[0][pricing_plan_subscription_item][pricing_plan]"={{PRICING_PLAN_ID}} \
  -d success_url={{SUCCESS_URL}}
```

## Record usage

After you create the pricing plan subscription you can start recording usage to the metered items.

Use [Meter Events](https://docs.stripe.com/api/billing/meter-events.md) to report usage:

```curl
curl https://api.stripe.com/v1/billing/meter_events \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d event_name={{METER_EVENT_NAME}} \
  -d "payload[stripe_customer_id]"={{CUSTOMER_ID}} \
  -d "payload[model]"=hypernian_1 \
  -d "payload[quantity]"=10
```

```cli
stripe billing meter_events create  \
  --event-name={{METER_EVENT_NAME}} \
  -d "payload[stripe_customer_id]"={{CUSTOMER_ID}} \
  -d "payload[model]"=hypernian_1 \
  -d "payload[quantity]"=10
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

meter_event = client.v1.billing.meter_events.create({
  event_name: '{{METER_EVENT_NAME}}',
  payload: {
    stripe_customer_id: '{{CUSTOMER_ID}}',
    model: 'hypernian_1',
    quantity: '10',
  },
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
meter_event = client.v1.billing.meter_events.create({
  "event_name": "{{METER_EVENT_NAME}}",
  "payload": {
    "stripe_customer_id": "{{CUSTOMER_ID}}",
    "model": "hypernian_1",
    "quantity": "10",
  },
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$meterEvent = $stripe->billing->meterEvents->create([
  'event_name' => '{{METER_EVENT_NAME}}',
  'payload' => [
    'stripe_customer_id' => '{{CUSTOMER_ID}}',
    'model' => 'hypernian_1',
    'quantity' => '10',
  ],
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

MeterEventCreateParams params =
  MeterEventCreateParams.builder()
    .setEventName("{{METER_EVENT_NAME}}")
    .putPayload("stripe_customer_id", "{{CUSTOMER_ID}}")
    .putPayload("model", "hypernian_1")
    .putPayload("quantity", "10")
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
MeterEvent meterEvent = client.v1().billing().meterEvents().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const meterEvent = await stripe.billing.meterEvents.create({
  event_name: '{{METER_EVENT_NAME}}',
  payload: {
    stripe_customer_id: '{{CUSTOMER_ID}}',
    model: 'hypernian_1',
    quantity: '10',
  },
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.BillingMeterEventCreateParams{
  EventName: stripe.String("{{METER_EVENT_NAME}}"),
  Payload: map[string]string{
    "stripe_customer_id": "{{CUSTOMER_ID}}",
    "model": "hypernian_1",
    "quantity": "10",
  },
}
result, err := sc.V1BillingMeterEvents.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.Billing.MeterEventCreateOptions
{
    EventName = "{{METER_EVENT_NAME}}",
    Payload = new Dictionary<string, string>
    {
        { "stripe_customer_id", "{{CUSTOMER_ID}}" },
        { "model", "hypernian_1" },
        { "quantity", "10" },
    },
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Billing.MeterEvents;
Stripe.Billing.MeterEvent meterEvent = service.Create(options);
```

## View upcoming invoices

Create a preview invoice to see a preview of a customer’s invoice. The preview includes the relevant line items from the various pricing plan components.

#### Dashboard

1. Go to the [Pricing plan subscriptions](https://dashboard.stripe.com/test/pricing-plan/subscriptions) tab.
1. Click the subscription you want to preview an invoice for.
1. Scroll down to the **Upcoming invoice** section. The preview invoice shows the subscription amount to bill the customer on the specified date, and reflects the corresponding metered items, license items, and credits.

#### API

```curl
curl https://api.stripe.com/v1/invoices/create_preview \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d billing_cadence=bc_test_61SrjnScUwT6mNskZ16SjPfE4ZSQFjWjdqlzQfWMCVnM
```

```json
{"hosted_invoice_url": "example.com/invoice",
  "invoice_pdf": null,
  "billing_reason": "manual",
  "collection_method": "charge_automatically",
  "created": 1680644467,
  "currency": "usd",
  "custom_fields": null,
  "customer": "cus_NeZwdNtLEOXuvB",
  "customer_address": null,
  "customer_email": "jennyrosen@example.com",
  "customer_name": "Jenny Rosen",
  "customer_phone": null,
  "customer_shipping": null,
  "customer_tax_exempt": "none",
  "customer_tax_ids": [],
  "default_payment_method": null,
  "default_source": null,
  "default_tax_rates": [],
  "description": null,
  "discounts": [],
  "due_date": null,
  "ending_balance": null,
  "footer": null,
  "from_invoice": null,
  "last_finalization_error": null,
  "latest_revision": null,
  "lines": {
    "object": "list",
    "data": [],
    "has_more": false,
    "total_count": 0,
    "url": "/v1/invoices/in_1MtHbELkdIwHu7ixl4OzzPMv/lines"
  },
{
  "id": "upcoming_in_1MtHbELkdIwHu7ixl4OzzPMv",
  "object": "invoice",
  "account_country": "US",
  "account_name": "Stripe Docs",
  "account_tax_ids": null,
  "amount_due": 0,
  "amount_paid": 0,
  "amount_overpaid": 0,
  "amount_remaining": 0,
  "amount_shipping": 0,
  "application": null,
  "application_fee_amount": null,
  "attempt_count": 0,
  "attempted": false,
  "auto_advance": false,
  "automatic_tax": {
    "enabled": false,
    "status": null
  },
  "livemode": false,
  "metadata": {},
  "next_payment_attempt": null,
  "number": null,
  "on_behalf_of": null,
  "parent": null,
  "payment_settings": {
    "default_mandate": null,
    "payment_method_options": null,
    "payment_method_types": null
  },
  "period_end": 1680644467,
  "period_start": 1680644467,
  "post_payment_credit_notes_amount": 0,
  "pre_payment_credit_notes_amount": 0,
  "receipt_number": null,
  "shipping_cost": null,
  "shipping_details": null,
  "starting_balance": 0,
  "statement_descriptor": null,
  "status": "draft",
  "status_transitions": {
    "finalized_at": null,
    "marked_uncollectible_at": null,
    "paid_at": null,
    "voided_at": null
  },
  "subtotal": 0,
  "subtotal_excluding_tax": 0,
  "test_clock": null,
  "total": 0,
  "total_discount_amounts": [],
  "total_excluding_tax": 0,
  "total_taxes": [],
  "webhooks_delivered_at": 1680644467
}
```

## See also

- [Migrate customers to new or updated pricing plans](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions/manage.md#migrate)
- [Update existing subscriptions](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions/manage.md#update-existing-subscriptions)
- [Cancel pricing plan subscriptions](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions/manage.md#cancel)

# Set up a flat fee and overages pricing model

Charge customers a flat rate with the option to pay for additional usage in arrears.

Flat fee with overages combines predictable billing with the flexibility to scale. Customers pay a set recurring fee for a base package, and any usage beyond that limit is billed separately. This model works well if you want steady, reliable revenue while still giving customers room to grow. The base fee covers core value, while overages ensure that heavy users pay in proportion to what they consume. For example, if you run a video hosting platform, you might include 1,000 monthly video streams in a 200 USD flat fee. If a customer streams more than that, each additional stream is billed as an overage. At the end of the month, Stripe sends an invoice that combines the flat fee with any usage above the included limit, automatically charging the customer’s payment method on file or prompting them to add one.

> #### Private preview
> 
> Pricing Plans are currently in [private preview](https://docs.stripe.com/release-phases.md) and might change in functionality and integration set up before they’re available to all Stripe users.

## What you’ll build

In this guide, build a flat fee and overages pricing model for a fictional company called Hypernian, which provides LLM. They charge customers at the following rates:

> #### Note
> 
> Usage is calculated at the dimension level, not at the customer level. If you want to give your customer 1500 tokens that they can use across all dimensions, you need to use credits instead of graduated pricing.

| Component                                               | Base                                                    |
| ------------------------------------------------------- | ------------------------------------------------------- |
| **License Fee**                                         | 20 USD per user                                         |
| **Rate**                                                | 0.05 USD per Hypernian_1 token (first 1000 tokens free) |
| 0.1 USD per Hypernian_Max token (first 500 tokens free) |

To implement this model, you create rates and license fees and attach those to the pricing plan.

## Create the pricing plan

[Pricing plans](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md) let you group a set of pricing components into a single package that you can charge customers for.

#### Dashboard

1. On the [Pricing plans](https://dashboard.stripe.com/test/pricing-plans) page, click **Create pricing plan**.
1. In the pricing plan editor:
   - Provide a display name, currency, and tax behavior.
   - (Optional) Under **Advanced settings**, specify the description, unique lookup key, and metadata.
1. Click **Continue**.

#### API

Use the API to [create a pricing plan](https://docs.stripe.com/api/v2/pricing-plans/create.md?api-version=preview).

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Pricing Plan",
    "currency": "usd",
    "tax_behavior": "exclusive"
  }'
```

## Create a rate card and add rates

To define how much to charge your customers for usage, create a [rate card](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md) and add graduated pricing rates for each metered item.

#### Dashboard

### Create the rate card

1. In the pricing plan editor, click + and **Rate card**.
1. In the rate card editor:
   - Provide a display name.
   - Specify the servicing period (for example, monthly).
   - (Optional) Under **Advanced settings**, provide a lookup key and metadata.
1. Click **Continue**.

### Add graduated pricing rates for each model

You need to create a [meter](https://docs.stripe.com/api/billing/meter.md?api-version=preview) first if you haven’t already. Meters specify how to aggregate [Meter Events](https://docs.stripe.com/api/v2/billing-meter.md?api-version=preview), which represent the actions that customers take in your system, over a billing period. In the Dashboard, you can create a new meter while adding rates to the rate card.

For the Hypernian_1 model with graduated pricing (first 1,000 tokens free):

1. In the rate editor:
   - Provide a display name (for example, `Hypernian_1 tokens`).
   - Select an existing **Meter** or create a new one by clicking +.
     - If creating a new meter, provide:
       - Meter name: `Prompts meter`
       - Event name: `prompt_meter`
       - Aggregation method: `sum`
       - Dimension payload key: `model`
       - Value key override: `tokens_used`
   - Add the pricing dimension `model`.
   - Provide the `model` dimension value: `hypernian_1`
   - Select the **Price type**: **Graduated**.
   - Configure the pricing tiers:
     - Tier 1: First `1000` units at `0.00 USD` per unit
     - Tier 2: Remaining units at `0.05 USD` per unit
   - (Optional) Configure **Advanced settings** like **Product tax code**, **Unit label**, **Lookup key**, and **Metadata**.
1. Click **Done**.

For the Hypernian_max model with graduated pricing (first 500 tokens free):

1. Click + **Add rate** to add another rate to the rate card.
1. In the rate editor:
   - Provide a display name (for example, `Hypernian_max tokens`).
   - Select the same **Meter** you created or selected earlier.
   - Add the pricing dimension `model`.
   - Provide the `model` dimension value: `hypernian_max`
   - Select the **Price type**: **Graduated**.
   - Configure the pricing tiers:
     - Tier 1: First `500` units at `0.00 USD` per unit
     - Tier 2: Remaining units at `0.10 USD` per unit
   - (Optional) Configure **Advanced settings**.
1. Click **Done**.

#### API

### Create a meter

[Meters](https://docs.stripe.com/api/billing/meter.md?api-version=preview&) specify how to aggregate [Meter Events](https://docs.stripe.com/api/v2/billing-meter.md?api-version=preview), which represent the actions that customers take in your system, over a billing period.

Use the API to [create a meter](https://docs.stripe.com/api/v1/billing/meters/create.md?api-version=preview).

```curl
curl https://api.stripe.com/v1/billing/meters \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d display_name="Prompts meter" \
  -d event_name=prompt_meter \
  -d "default_aggregation[formula]"=sum \
  -d "value_settings[event_payload_key]"=tokens_used \
  -d "dimension_payload_keys[]"=model
```

```cli
stripe billing meters create  \
  --display-name="Prompts meter" \
  --event-name=prompt_meter \
  -d "default_aggregation[formula]"=sum \
  -d "value_settings[event_payload_key]"=tokens_used \
  -d "dimension_payload_keys[0]"=model
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

meter = client.v1.billing.meters.create({
  display_name: 'Prompts meter',
  event_name: 'prompt_meter',
  default_aggregation: {formula: 'sum'},
  value_settings: {event_payload_key: 'tokens_used'},
  dimension_payload_keys: ['model'],
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
meter = client.v1.billing.meters.create({
  "display_name": "Prompts meter",
  "event_name": "prompt_meter",
  "default_aggregation": {"formula": "sum"},
  "value_settings": {"event_payload_key": "tokens_used"},
  "dimension_payload_keys": ["model"],
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$meter = $stripe->billing->meters->create([
  'display_name' => 'Prompts meter',
  'event_name' => 'prompt_meter',
  'default_aggregation' => ['formula' => 'sum'],
  'value_settings' => ['event_payload_key' => 'tokens_used'],
  'dimension_payload_keys' => ['model'],
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

MeterCreateParams params =
  MeterCreateParams.builder()
    .setDisplayName("Prompts meter")
    .setEventName("prompt_meter")
    .setDefaultAggregation(
      MeterCreateParams.DefaultAggregation.builder()
        .setFormula(MeterCreateParams.DefaultAggregation.Formula.SUM)
        .build()
    )
    .setValueSettings(
      MeterCreateParams.ValueSettings.builder().setEventPayloadKey("tokens_used").build()
    )
    .putExtraParam("dimension_payload_keys[0]", "model")
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
Meter meter = client.v1().billing().meters().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const meter = await stripe.billing.meters.create({
  display_name: 'Prompts meter',
  event_name: 'prompt_meter',
  default_aggregation: {
    formula: 'sum',
  },
  value_settings: {
    event_payload_key: 'tokens_used',
  },
  dimension_payload_keys: ['model'],
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.BillingMeterCreateParams{
  DisplayName: stripe.String("Prompts meter"),
  EventName: stripe.String("prompt_meter"),
  DefaultAggregation: &stripe.BillingMeterCreateDefaultAggregationParams{
    Formula: stripe.String(stripe.BillingMeterDefaultAggregationFormulaSum),
  },
  ValueSettings: &stripe.BillingMeterCreateValueSettingsParams{
    EventPayloadKey: stripe.String("tokens_used"),
  },
}
params.AddExtra("dimension_payload_keys[0]", "model")
result, err := sc.V1BillingMeters.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.Billing.MeterCreateOptions
{
    DisplayName = "Prompts meter",
    EventName = "prompt_meter",
    DefaultAggregation = new Stripe.Billing.MeterDefaultAggregationOptions
    {
        Formula = "sum",
    },
    ValueSettings = new Stripe.Billing.MeterValueSettingsOptions
    {
        EventPayloadKey = "tokens_used",
    },
};
options.AddExtraParam("dimension_payload_keys[0]", "model");
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Billing.Meters;
Stripe.Billing.Meter meter = service.Create(options);
```

### Create metered items

A [Metered Item](https://docs.stripe.com/api/v2/metered-items.md?api-version=preview) represents any item that you bill customers for based on how much they use it, such as hourly cloud CPU usage or tokens generated by an AI service.

Use the API to [create a metered item](https://docs.stripe.com/api/v2/metered-items/create.md?api-version=preview) for the `Hypernian_1` model.

```curl
curl -X POST https://api.stripe.com/v2/billing/metered_items \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Hypernian_1_model",
    "meter": "{{METER_ID}}",
    "meter_segment_conditions": [
        {
            "dimension": "model",
            "value": "hypernian_1"
        }
    ]
  }'
```

Add another metered item to aggregate customer usage of the `Hypernian_max` model.

```curl
curl -X POST https://api.stripe.com/v2/billing/metered_items \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Hypernian_max_model",
    "meter": "{{METER_ID}}",
    "meter_segment_conditions": [
        {
            "dimension": "model",
            "value": "hypernian_max"
        }
    ]
  }'
```

### Create a rate card

To define how much to charge your customers per metered item, create a [rate card](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md), which keeps track of the rates associated with a subscription.

You add rates to the rate card, then attach the rate card to a pricing plan.

Use the API to [create a rate card](https://docs.stripe.com/api/v2/rate-cards/create.md?api-version=preview). Save the rate card ID.

```curl
curl -X POST https://api.stripe.com/v2/billing/rate_cards \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Rate Card",
    "service_interval": "month",
    "service_interval_count": 1,
    "currency": "usd",
    "tax_behavior": "exclusive"
  }'
```

### Add graduated pricing rates to the rate card

After you create the rate card, add rates to it to define how much to charge your customers per metered item when they use more tokens than the included free tier. In this example, Hypernian charges customers after they use their first 1,000 tokens on the Hypernian_1 model. They begin charging overages on the Hypernian_Max model after 500 tokens.

| Component                                               | Base                                                     |
| ------------------------------------------------------- | -------------------------------------------------------- |
| **License Fee**                                         | 20 USD per user                                          |
| **Rate**                                                | 0.05 USD per Hypernian_1 token (first 1,000 tokens free) |
| 0.1 USD per Hypernian_Max token (first 500 tokens free) |

Set the tiered pricing rate for the Hypernian_1 model as 0.05 USD per token for usage over 1000 tokens.

```curl
curl -X POST https://api.stripe.com/v2/billing/rate_cards/{{RATE_CARD_ID}}/rates \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "metered_item": "{{METERED_ITEM_ID_1}}",
    "tiering_mode": "graduated",
    "tiers": [
        {
            "unit_amount": "0",
            "up_to_decimal": "1000"
        },
        {
            "unit_amount": "5",
            "up_to_inf": "inf"
        }
    ]
  }'
```

Then, set the tiered pricing rate for the Hypernian_Max model as 0.1 USD per token for usage over 500 tokens. Save the rate card ID and version.

```curl
curl -X POST https://api.stripe.com/v2/billing/rate_cards/{{RATE_CARD_ID}}/rates \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "metered_item": "{{METERED_ITEM_ID_2}}",
    "tiers": [
        {
            "unit_amount": "0",
            "up_to_decimal": "500"
        },
        {
            "unit_amount": "10",
            "up_to_inf": "inf"
        }
    ]
  }'
```

### Attach the rate card to the pricing plan

After you create the rate card and set the rates, attach the rate card to the pricing plan.

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "type": "rate_card",
    "rate_card": {
        "id": "{{RATE_CARD_ID}}",
        "version": "{{RATE_CARD_VERSION}}"
    }
  }'
```

## Add a license fee

Add a license fee to charge a flat recurring amount.

#### Dashboard

1. In the pricing plan editor, click + and **License fee**.
1. In the license fee editor:
   - Provide a display name for the licensed item (for example, `Per Seat License`).
   - Specify the servicing period (for example, monthly).
   - Select the **Price type**: **Fixed rate**.
   - Enter the price per unit: `20.00 USD`.
   - (Optional) Configure **Advanced settings** like **Product tax code**, **Unit label**, **Lookup key**, and **Metadata**.
1. Click **Done**.

After you finish configuring the pricing plan, click **Create pricing plan**.

#### API

Create the license item component to attach it to the license fee to the pricing plan. Save the licensed item ID.

```curl
curl -X POST https://api.stripe.com/v2/billing/licensed_items \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Per Seat License"
  }'
```

Create the license fee to price the license item. Save the license fee ID and version. You can also build out more complicated License fees with [volume or graduated pricing](https://docs.stripe.com/api/v2/license-fees/create.md?api-version=preview#v2_create_license_fees-tiering_mode), [tiers](https://docs.stripe.com/api/v2/license-fees/create.md?api-version=preview#v2_create_license_fees-tiers), and [transform quantities](https://docs.stripe.com/api/v2/license-fees/create.md?api-version=preview#v2_create_license_fees-transform_quantity).

```curl
curl -X POST https://api.stripe.com/v2/billing/license_fees \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Per Seat License Fee",
    "currency": "usd",
    "service_interval": "month",
    "service_interval_count": 1,
    "tax_behavior": "exclusive",
    "unit_amount": "2000",
    "licensed_item": "{{LICENSED_ITEM_ID}}"
  }'
```

Attach the license fee to the pricing plan.

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "type": "license_fee",
    "license_fee": {
        "id": "licf_123",
        "version": "licfv_123"
    }
  }'
```

### Activate the pricing plan

After you add all components to your pricing plan, activate that version of the pricing plan. After the plan is activated, you can subscribe customers to it.

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}} \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "live_version": "latest"
  }'
```

## Subscribe a customer to the pricing plan

After you create the pricing plan with a rate card and license fee, subscribe a customer to the pricing plan. You can use a [Checkout Session](https://docs.stripe.com/api/checkout/sessions.md?api-version=preview) to collect payment information and create the subscription, or you can [directly subscribe a customer using the API](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md?payment-ui=direct-api#subscribe).

When your pricing plan includes a license fee, you need to specify the quantity for the license fee when creating the Checkout Session. For testing, you can use a [test clock](https://docs.stripe.com/billing/testing/test-clocks.md) to simulate subscription billing cycles.

Get the license fee component ID:

```curl
curl https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-09-30.preview"
```

Create the Checkout Session using the license fee component ID:

```curl
curl https://api.stripe.com/v1/checkout/sessions \
  -u "<<YOUR_SECRET_KEY>>:" \
  -H "Stripe-Version: 2025-09-30.preview;checkout_product_catalog_preview=v1" \
  -d customer={{CUSTOMER_ID}} \
  -d "checkout_items[0][type]"=pricing_plan_subscription_item \
  -d "checkout_items[0][pricing_plan_subscription_item][pricing_plan]"={{PRICING_PLAN_ID}} \
  -d "checkout_items[0][pricing_plan_subscription_item][component_configurations][{{LICENSE_COMPONENT_ID}}][type]"=license_fee_component \
  -d "checkout_items[0][pricing_plan_subscription_item][component_configurations][{{LICENSE_COMPONENT_ID}}][license_fee_component][quantity]"=1
```

## Use meter events to record usage

After you create a pricing plan subscription, you can begin sending usage data to the metered items you created.

```curl
curl https://api.stripe.com/v1/billing/meter_events \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d event_name={{METER_EVENT_NAME}} \
  -d "payload[stripe_customer_id]"={{CUSTOMER_ID}} \
  -d "payload[model]"=hypernian_1 \
  -d "payload[quantity]"=10
```

```cli
stripe billing meter_events create  \
  --event-name={{METER_EVENT_NAME}} \
  -d "payload[stripe_customer_id]"={{CUSTOMER_ID}} \
  -d "payload[model]"=hypernian_1 \
  -d "payload[quantity]"=10
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

meter_event = client.v1.billing.meter_events.create({
  event_name: '{{METER_EVENT_NAME}}',
  payload: {
    stripe_customer_id: '{{CUSTOMER_ID}}',
    model: 'hypernian_1',
    quantity: '10',
  },
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
meter_event = client.v1.billing.meter_events.create({
  "event_name": "{{METER_EVENT_NAME}}",
  "payload": {
    "stripe_customer_id": "{{CUSTOMER_ID}}",
    "model": "hypernian_1",
    "quantity": "10",
  },
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$meterEvent = $stripe->billing->meterEvents->create([
  'event_name' => '{{METER_EVENT_NAME}}',
  'payload' => [
    'stripe_customer_id' => '{{CUSTOMER_ID}}',
    'model' => 'hypernian_1',
    'quantity' => '10',
  ],
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

MeterEventCreateParams params =
  MeterEventCreateParams.builder()
    .setEventName("{{METER_EVENT_NAME}}")
    .putPayload("stripe_customer_id", "{{CUSTOMER_ID}}")
    .putPayload("model", "hypernian_1")
    .putPayload("quantity", "10")
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
MeterEvent meterEvent = client.v1().billing().meterEvents().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const meterEvent = await stripe.billing.meterEvents.create({
  event_name: '{{METER_EVENT_NAME}}',
  payload: {
    stripe_customer_id: '{{CUSTOMER_ID}}',
    model: 'hypernian_1',
    quantity: '10',
  },
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.BillingMeterEventCreateParams{
  EventName: stripe.String("{{METER_EVENT_NAME}}"),
  Payload: map[string]string{
    "stripe_customer_id": "{{CUSTOMER_ID}}",
    "model": "hypernian_1",
    "quantity": "10",
  },
}
result, err := sc.V1BillingMeterEvents.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.Billing.MeterEventCreateOptions
{
    EventName = "{{METER_EVENT_NAME}}",
    Payload = new Dictionary<string, string>
    {
        { "stripe_customer_id", "{{CUSTOMER_ID}}" },
        { "model", "hypernian_1" },
        { "quantity", "10" },
    },
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Billing.MeterEvents;
Stripe.Billing.MeterEvent meterEvent = service.Create(options);
```

## View upcoming invoices

Create a preview invoice to see a preview of a customer’s invoice. The preview includes the relevant line items from the various pricing plan components.

#### Dashboard

1. Go to the [Pricing plan subscriptions](https://dashboard.stripe.com/test/pricing-plan/subscriptions) tab.
1. Click the subscription you want to preview an invoice for.
1. Scroll down to the **Upcoming invoice** section. The preview invoice shows the subscription amount to bill the customer on the specified date, and reflects the corresponding metered items, license items, and credits.

#### API

```curl
curl https://api.stripe.com/v1/invoices/create_preview \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d billing_cadence=bc_test_61SrjnScUwT6mNskZ16SjPfE4ZSQFjWjdqlzQfWMCVnM
```

```json
{"hosted_invoice_url": "example.com/invoice",
  "invoice_pdf": null,
  "billing_reason": "manual",
  "collection_method": "charge_automatically",
  "created": 1680644467,
  "currency": "usd",
  "custom_fields": null,
  "customer": "cus_NeZwdNtLEOXuvB",
  "customer_address": null,
  "customer_email": "jennyrosen@example.com",
  "customer_name": "Jenny Rosen",
  "customer_phone": null,
  "customer_shipping": null,
  "customer_tax_exempt": "none",
  "customer_tax_ids": [],
  "default_payment_method": null,
  "default_source": null,
  "default_tax_rates": [],
  "description": null,
  "discounts": [],
  "due_date": null,
  "ending_balance": null,
  "footer": null,
  "from_invoice": null,
  "last_finalization_error": null,
  "latest_revision": null,
  "lines": {
    "object": "list",
    "data": [],
    "has_more": false,
    "total_count": 0,
    "url": "/v1/invoices/in_1MtHbELkdIwHu7ixl4OzzPMv/lines"
  },
{
  "id": "upcoming_in_1MtHbELkdIwHu7ixl4OzzPMv",
  "object": "invoice",
  "account_country": "US",
  "account_name": "Stripe Docs",
  "account_tax_ids": null,
  "amount_due": 0,
  "amount_paid": 0,
  "amount_overpaid": 0,
  "amount_remaining": 0,
  "amount_shipping": 0,
  "application": null,
  "application_fee_amount": null,
  "attempt_count": 0,
  "attempted": false,
  "auto_advance": false,
  "automatic_tax": {
    "enabled": false,
    "status": null
  },
  "livemode": false,
  "metadata": {},
  "next_payment_attempt": null,
  "number": null,
  "on_behalf_of": null,
  "parent": null,
  "payment_settings": {
    "default_mandate": null,
    "payment_method_options": null,
    "payment_method_types": null
  },
  "period_end": 1680644467,
  "period_start": 1680644467,
  "post_payment_credit_notes_amount": 0,
  "pre_payment_credit_notes_amount": 0,
  "receipt_number": null,
  "shipping_cost": null,
  "shipping_details": null,
  "starting_balance": 0,
  "statement_descriptor": null,
  "status": "draft",
  "status_transitions": {
    "finalized_at": null,
    "marked_uncollectible_at": null,
    "paid_at": null,
    "voided_at": null
  },
  "subtotal": 0,
  "subtotal_excluding_tax": 0,
  "test_clock": null,
  "total": 0,
  "total_discount_amounts": [],
  "total_excluding_tax": 0,
  "total_taxes": [],
  "webhooks_delivered_at": 1680644467
}
```

## See also

- [Migrate customers to new or updated pricing plans](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions/manage.md#migrate)
- [Update existing subscriptions](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions/manage.md#update-existing-subscriptions)
- [Cancel pricing plan subscriptions](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions/manage.md#cancel)

# Set up real-time credit burndown with top-ups

Charge customers for pre-purchase credits and for top-ups.

Real-time credit burndown gives customers the flexibility to pre-purchase credits and use them at their own pace. Each action or unit of usage reduces their balance in real time, making costs transparent and easy to track. This model works well when you want to give customers upfront predictability while aligning revenue directly to usage. For example, if you sell an API that processes images, a customer might buy 10,000 credits at the start of the month. Every time they process an image, credits are deducted from their balance until they reach zero. Stripe tracks usage against the credit balance, automatically notifying customers when they’re running low.

Stripe doesn’t have access to your internal logic to limit usage and can’t stop a user from using your system after they burn down all of their credits. To [monitor usage](https://docs.stripe.com/billing/subscriptions/usage-based-v2/monitor-usage.md), you must set up a billing threshold alert to send a [billing.alert.triggered](https://docs.stripe.com/api/events/types.md?api-version=preview#event_types-billing.alert.triggered) webhook when a threshold is reached. You must register an endpoint to listen to those webhooks and then restrict their usage to your platform accordingly. When a customer’s credit balance goes back above the threshold (for example, after a top-up), Stripe sends a [billing.alert.recovered](https://docs.stripe.com/api/events/types.md?api-version=preview#event_types-billing.alert.recovered) webhook that you can use to restore their access.

To learn how to set up these objects, see the [get started guide](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md).

> #### Private preview
> 
> Pricing Plans are currently in [private preview](https://docs.stripe.com/release-phases.md) and could change in functionality and integration path before they’re generally available to all Stripe users.

## What you’ll build

In this guide, build the following credit burndown subscription for a fictional company called Hypernian, which provides an LLM. Upon signup, users are given 10 USD worth of free credits. When a user burns their credits down, they must top up their credits to continue using Hypernian.

Hypernian charges customers at the following rates:

| Component                       | Base                           |
| ------------------------------- | ------------------------------ |
| **Credit Grant**                | 10 USD credits                 |
| **Rate**                        | 0.05 USD per Hypernian_1 token |
| 0.1 USD per Hypernian_Max token |

To implement this model, you create ad-hoc credit grants and a pricing plan with your rates.

## Create the pricing plan

[Pricing plans](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md) let you group a set of pricing components into a single package that you can charge customers for.

#### Dashboard

1. On the [Pricing plans](https://dashboard.stripe.com/test/pricing-plans) page, click **Create pricing plan**.
1. In the pricing plan editor:
   - Provide a display name, currency, and tax behavior.
   - (Optional) Under **Advanced settings**, specify the description, unique lookup key, and metadata.
1. Click **Continue**.

#### API

Use the API to [create a pricing plan](https://docs.stripe.com/api/v2/pricing-plans/create.md?api-version=preview).

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Pricing Plan",
    "currency": "usd",
    "tax_behavior": "exclusive"
  }'
```

## Create a rate card and add rates

To define how much to charge your customers for usage, create a [rate card](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md) and add rates for each metered item.

#### Dashboard

### Create the rate card

1. In the pricing plan editor, click + and **Rate card**.
1. In the rate card editor:
   - Provide a display name.
   - Specify the servicing period (for example, monthly).
   - (Optional) Under **Advanced settings**, provide a lookup key and metadata.
1. Click **Continue**.

### Add rates for each model

You need to create a [meter](https://docs.stripe.com/api/billing/meter.md?api-version=preview) first if you haven’t already. Meters specify how to aggregate [Meter Events](https://docs.stripe.com/api/v2/billing-meter.md?api-version=preview), which represent the actions that customers take in your system over a billing period. In the Dashboard, you can create a new meter while adding rates to the rate card.

For the Hypernian_1 model:

1. In the rate editor:
   - Provide a display name (for example, `Hypernian_1 tokens`).
   - Select an existing **Meter** or create a new one by clicking +.
     - If creating a new meter, provide:
       - Meter name: `Prompts meter`
       - Event name: `prompt_meter`
       - Aggregation method: `sum`
       - Dimension payload key: `model`
       - Value key override: `tokens_used`
   - Add the pricing dimension `model`.
   - Provide the `model` dimension value: `hypernian_1`
   - Select the **Price type**: **Fixed rate**.
   - Select **Sell as**: Individual units.
   - Enter the **Price per unit**: `0.05 USD`.
   - (Optional) Configure **Advanced settings** like **Product tax code**, **Unit label**, **Lookup key**, and **Metadata**.
1. Click **Done**.

For the Hypernian_max model:

1. Click + **Add rate** to add another rate to the rate card.
1. In the rate editor:
   - Provide a display name (for example, `Hypernian_max tokens`).
   - Select the same **Meter** you created or selected earlier.
   - Add the pricing dimension `model`.
   - Provide the `model` dimension value: `hypernian_max`
   - Select the **Price type**: **Fixed rate**.
   - Select **Sell as**: Individual units.
   - Enter the **Price per unit**: `0.10 USD`.
   - (Optional) Configure **Advanced settings**.
1. Click **Done**.

After you finish configuring the pricing plan, click **Create pricing plan**.

#### API

### Create a meter

[Meters](https://docs.stripe.com/api/billing/meter.md?api-version=preview&) specify how to aggregate [Meter Events](https://docs.stripe.com/api/v2/billing-meter.md?api-version=preview), which represent the actions that customers take in your system, over a billing period.

Use the API to [create a meter](https://docs.stripe.com/api/v1/billing/meters/create.md?api-version=preview). Save the meter ID.

```curl
curl https://api.stripe.com/v1/billing/meters \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d display_name="Prompts meter" \
  -d event_name=prompt_meter \
  -d "default_aggregation[formula]"=sum \
  -d "value_settings[event_payload_key]"=tokens_used \
  -d "dimension_payload_keys[]"=model
```

```cli
stripe billing meters create  \
  --display-name="Prompts meter" \
  --event-name=prompt_meter \
  -d "default_aggregation[formula]"=sum \
  -d "value_settings[event_payload_key]"=tokens_used \
  -d "dimension_payload_keys[0]"=model
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

meter = client.v1.billing.meters.create({
  display_name: 'Prompts meter',
  event_name: 'prompt_meter',
  default_aggregation: {formula: 'sum'},
  value_settings: {event_payload_key: 'tokens_used'},
  dimension_payload_keys: ['model'],
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
meter = client.v1.billing.meters.create({
  "display_name": "Prompts meter",
  "event_name": "prompt_meter",
  "default_aggregation": {"formula": "sum"},
  "value_settings": {"event_payload_key": "tokens_used"},
  "dimension_payload_keys": ["model"],
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$meter = $stripe->billing->meters->create([
  'display_name' => 'Prompts meter',
  'event_name' => 'prompt_meter',
  'default_aggregation' => ['formula' => 'sum'],
  'value_settings' => ['event_payload_key' => 'tokens_used'],
  'dimension_payload_keys' => ['model'],
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

MeterCreateParams params =
  MeterCreateParams.builder()
    .setDisplayName("Prompts meter")
    .setEventName("prompt_meter")
    .setDefaultAggregation(
      MeterCreateParams.DefaultAggregation.builder()
        .setFormula(MeterCreateParams.DefaultAggregation.Formula.SUM)
        .build()
    )
    .setValueSettings(
      MeterCreateParams.ValueSettings.builder().setEventPayloadKey("tokens_used").build()
    )
    .putExtraParam("dimension_payload_keys[0]", "model")
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
Meter meter = client.v1().billing().meters().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const meter = await stripe.billing.meters.create({
  display_name: 'Prompts meter',
  event_name: 'prompt_meter',
  default_aggregation: {
    formula: 'sum',
  },
  value_settings: {
    event_payload_key: 'tokens_used',
  },
  dimension_payload_keys: ['model'],
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.BillingMeterCreateParams{
  DisplayName: stripe.String("Prompts meter"),
  EventName: stripe.String("prompt_meter"),
  DefaultAggregation: &stripe.BillingMeterCreateDefaultAggregationParams{
    Formula: stripe.String(stripe.BillingMeterDefaultAggregationFormulaSum),
  },
  ValueSettings: &stripe.BillingMeterCreateValueSettingsParams{
    EventPayloadKey: stripe.String("tokens_used"),
  },
}
params.AddExtra("dimension_payload_keys[0]", "model")
result, err := sc.V1BillingMeters.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.Billing.MeterCreateOptions
{
    DisplayName = "Prompts meter",
    EventName = "prompt_meter",
    DefaultAggregation = new Stripe.Billing.MeterDefaultAggregationOptions
    {
        Formula = "sum",
    },
    ValueSettings = new Stripe.Billing.MeterValueSettingsOptions
    {
        EventPayloadKey = "tokens_used",
    },
};
options.AddExtraParam("dimension_payload_keys[0]", "model");
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Billing.Meters;
Stripe.Billing.Meter meter = service.Create(options);
```

### Create metered items

A [Metered Item](https://docs.stripe.com/api/v2/metered-items.md?api-version=preview)represents any item that you bill customers for based on usage, such as hourly cloud CPU usage or tokens generated by an AI service.

Create one metered item to aggregate customer usage of the Hypernian_1 model.

```curl
curl -X POST https://api.stripe.com/v2/billing/metered_items \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Hypernian_1_model",
    "meter": "{{METER_ID}}",
    "meter_segment_conditions": [
        {
            "dimension": "model",
            "value": "hypernian_1"
        }
    ]
  }'
```

Add another metered item to aggregate customer usage of the `Hypernian_max` model. Save the metered item ID.

```curl
curl -X POST https://api.stripe.com/v2/billing/metered_items \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Hypernian_max_model",
    "meter": "{{METER_ID}}",
    "meter_segment_conditions": [
        {
            "dimension": "model",
            "value": "hypernian_max"
        }
    ]
  }'
```

### Create a rate card

To define how much to charge your customers per metered item, create a [rate card](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md), which keeps track of the rates associated with a subscription.

You add rates to the rate card, then attach the rate card to a pricing plan.

Use the API to [create a rate card](https://docs.stripe.com/api/v2/rate-cards/create.md?api-version=preview). Save the rate card ID.

```curl
curl -X POST https://api.stripe.com/v2/billing/rate_cards \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Rate Card",
    "service_interval": "month",
    "service_interval_count": 1,
    "currency": "usd",
    "tax_behavior": "exclusive"
  }'
```

### Add rates to the rate card

After you create the rate card, add rates to it to define how much to charge your customers per metered item. This example uses the following pricing model, where each type of token is a metered item with a defined rate:

- 0.05 USD per Hypernian_1 token
- 0.1 USD per Hypernian_Max token

Set the rate for the Hypernian_1 model as 0.05 USD per usage. Save the rate card ID and version.

```curl
curl -X POST https://api.stripe.com/v2/billing/rate_cards/{{RATE_CARD_ID}}/rates \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "metered_item": "{{METERED_ITEM_ID_1}}",
    "unit_amount": "5"
  }'
```

Then, set the rate for the Hypernian_Max model as 0.1 USD per token. Save the rate card ID and version.

```curl
curl -X POST https://api.stripe.com/v2/billing/rate_cards/{{RATE_CARD_ID}}/rates \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "metered_item": "{{METERED_ITEM_ID_2}}",
    "unit_amount": "10"
  }'
```

### Attach the rate card to the pricing plan

After you create the rate card and set the rates, attach the rate card to the pricing plan.

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "type": "rate_card",
    "rate_card": {
        "id": "{{RATE_CARD_ID}}",
        "version": "{{RATE_CARD_VERSION}}"
    }
  }'
```

### Activate the pricing plan

After you add the rate card to your pricing plan, activate that version of the pricing plan. After the plan is activated, you can subscribe customers to it.

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}} \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "live_version": "latest"
  }'
```

## Subscribe a customer to the pricing plan

After you create the pricing plan and rate card, subscribe a customer to the pricing plan. You can use a [Checkout Session](https://docs.stripe.com/api/checkout/sessions.md?api-version=preview) to collect payment information and create the subscription, or you can [directly subscribe a customer using the API](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md?payment-ui=direct-api#subscribe).

For testing, you can use a [test clock](https://docs.stripe.com/billing/testing/test-clocks.md) to simulate subscription billing cycles.

```curl
curl https://api.stripe.com/v1/checkout/sessions \
  -u "<<YOUR_SECRET_KEY>>:" \
  -H "Stripe-Version: 2025-09-30.preview;checkout_product_catalog_preview=v1" \
  -d customer={{CUSTOMER_ID}} \
  -d "checkout_items[0][type]"=pricing_plan_subscription_item \
  -d "checkout_items[0][pricing_plan_subscription_item][pricing_plan]"={{PRICING_PLAN_ID}} \
  -d success_url={{SUCCESS_URL}}
```

## Grant credits to your customer

Hypernian grants the initial 10 USD signup to all users without needing to add a payment method. To grant credits to a customer only after they add a payment method, listen to the [checkout.session.completed](https://docs.stripe.com/api/v2/core/events/event-types.md?api-version=preview#v2_event_types-v1.checkout.session.completed) event from [subscribing your customer](https://docs.stripe.com/billing/subscriptions/usage-based-v2/use-cases/credit-burndown-and-top-ups.md#subscribe-to-pricing-plan) before granting credits.

To grant credits:

```curl
curl https://api.stripe.com/v1/billing/credit_grants \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d "amount[type]"=monetary \
  -d "amount[monetary][currency]"=usd \
  -d "amount[monetary][value]"=1000 \
  -d "applicability_config[scope][price_type]"=metered \
  -d category=paid \
  -d customer={{CUSTOMER_ID}} \
  -d name="Credit Grant"
```

```cli
stripe billing credit_grants create  \
  -d "amount[type]"=monetary \
  -d "amount[monetary][currency]"=usd \
  -d "amount[monetary][value]"=1000 \
  -d "applicability_config[scope][price_type]"=metered \
  --category=paid \
  --customer={{CUSTOMER_ID}} \
  --name="Credit Grant"
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

credit_grant = client.v1.billing.credit_grants.create({
  amount: {
    type: 'monetary',
    monetary: {
      currency: 'usd',
      value: 1000,
    },
  },
  applicability_config: {scope: {price_type: 'metered'}},
  category: 'paid',
  customer: '{{CUSTOMER_ID}}',
  name: 'Credit Grant',
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
credit_grant = client.v1.billing.credit_grants.create({
  "amount": {"type": "monetary", "monetary": {"currency": "usd", "value": 1000}},
  "applicability_config": {"scope": {"price_type": "metered"}},
  "category": "paid",
  "customer": "{{CUSTOMER_ID}}",
  "name": "Credit Grant",
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$creditGrant = $stripe->billing->creditGrants->create([
  'amount' => [
    'type' => 'monetary',
    'monetary' => [
      'currency' => 'usd',
      'value' => 1000,
    ],
  ],
  'applicability_config' => ['scope' => ['price_type' => 'metered']],
  'category' => 'paid',
  'customer' => '{{CUSTOMER_ID}}',
  'name' => 'Credit Grant',
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

CreditGrantCreateParams params =
  CreditGrantCreateParams.builder()
    .setAmount(
      CreditGrantCreateParams.Amount.builder()
        .setType(CreditGrantCreateParams.Amount.Type.MONETARY)
        .setMonetary(
          CreditGrantCreateParams.Amount.Monetary.builder()
            .setCurrency("usd")
            .setValue(1000L)
            .build()
        )
        .build()
    )
    .setApplicabilityConfig(
      CreditGrantCreateParams.ApplicabilityConfig.builder()
        .setScope(
          CreditGrantCreateParams.ApplicabilityConfig.Scope.builder()
            .setPriceType(
              CreditGrantCreateParams.ApplicabilityConfig.Scope.PriceType.METERED
            )
            .build()
        )
        .build()
    )
    .setCategory(CreditGrantCreateParams.Category.PAID)
    .setCustomer("{{CUSTOMER_ID}}")
    .setName("Credit Grant")
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
CreditGrant creditGrant = client.v1().billing().creditGrants().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const creditGrant = await stripe.billing.creditGrants.create({
  amount: {
    type: 'monetary',
    monetary: {
      currency: 'usd',
      value: 1000,
    },
  },
  applicability_config: {
    scope: {
      price_type: 'metered',
    },
  },
  category: 'paid',
  customer: '{{CUSTOMER_ID}}',
  name: 'Credit Grant',
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.BillingCreditGrantCreateParams{
  Amount: &stripe.BillingCreditGrantCreateAmountParams{
    Type: stripe.String("monetary"),
    Monetary: &stripe.BillingCreditGrantCreateAmountMonetaryParams{
      Currency: stripe.String(stripe.CurrencyUSD),
      Value: stripe.Int64(1000),
    },
  },
  ApplicabilityConfig: &stripe.BillingCreditGrantCreateApplicabilityConfigParams{
    Scope: &stripe.BillingCreditGrantCreateApplicabilityConfigScopeParams{
      PriceType: stripe.String("metered"),
    },
  },
  Category: stripe.String(stripe.BillingCreditGrantCategoryPaid),
  Customer: stripe.String("{{CUSTOMER_ID}}"),
  Name: stripe.String("Credit Grant"),
}
result, err := sc.V1BillingCreditGrants.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.Billing.CreditGrantCreateOptions
{
    Amount = new Stripe.Billing.CreditGrantAmountOptions
    {
        Type = "monetary",
        Monetary = new Stripe.Billing.CreditGrantAmountMonetaryOptions
        {
            Currency = "usd",
            Value = 1000,
        },
    },
    ApplicabilityConfig = new Stripe.Billing.CreditGrantApplicabilityConfigOptions
    {
        Scope = new Stripe.Billing.CreditGrantApplicabilityConfigScopeOptions
        {
            PriceType = "metered",
        },
    },
    Category = "paid",
    Customer = "{{CUSTOMER_ID}}",
    Name = "Credit Grant",
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Billing.CreditGrants;
Stripe.Billing.CreditGrant creditGrant = service.Create(options);
```

## Set up top-ups for credit grants

You can enable Stripe to manage the top-up flow two different ways:

- [Credit Grant API](https://docs.stripe.com/api/billing/credit-grant.md?api-version=preview): Use this API to set up ad hoc top-ups.
- [Stripe Workflows](https://docs.stripe.com/workflows.md): A visual automation builder that lets you automate tasks for multi-step processes.

To maintain observability into your integration we recommend using the API.

#### Credit Grant API

First, create an alert to notify you when a customer’s credit balance is below the threshold (10 credits in this example). When you receive this notification, restrict their access to your platform.

```curl
curl https://api.stripe.com/v1/billing/alerts \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d alert_type=credit_balance_threshold \
  -d title="Credit Balance Low Alert" \
  -d "credit_balance_threshold[lte][balance_type]"=monetary \
  -d "credit_balance_threshold[lte][monetary][value]"=0 \
  -d "credit_balance_threshold[lte][monetary][currency]"=usd
```

If you want to  set up different alerts for different customers you can also apply filters.

```curl
curl https://api.stripe.com/v1/billing/alerts \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d alert_type=credit_balance_threshold \
  -d title="Credit Balance Low Alert" \
  -d "credit_balance_threshold[lte][balance_type]"=monetary \
  -d "credit_balance_threshold[lte][monetary][value]"=0 \
  -d "credit_balance_threshold[lte][monetary][currency]"=usd \
  -d "filters[0][type]"=customer \
  -d "filters[0][customer]"={{CUSTOMER_ID}} \
  -d status=active
```

When a `billing.alert.triggered` event fires, it includes the `customer_id`. Restrict the customer’s usage based on your internal policy. Stripe doesn’t prevent you from registering usage on a customer if you continue to send usage.

```json
{
  "object": {
    "object": "billing.alert_triggered",
    "alert": {
      "id": "alrt_test_61T7eah2z8l8a2193416ZU9yVCs7VBlA",
      "object": "billing.alert",
      "alert_type": "credit_balance_threshold",
      "credit_balance_threshold": {
        "filters": [
          {
            "customer": null,
            "type": "customer"
          }
        ],
        "lte": {
          "balance_type": "monetary",
          "custom_pricing_unit": null,
          "monetary": {
            "currency": "usd",
            "value": 0
          }
        },
        "recurrence": "one_time"
      },
      "livemode": false,
      "status": "active",
      "title": "Low Balance Alert",
      "usage_threshold": null
    },
    "created": 1756414920,
    "currency": "usd",
    "custom_pricing_unit": null,
    "customer": "cus_Su65aU14rK29BS",
    "external_customer_id": "cus_Su65aU14rK29BS",
    "livemode": false,
    "value": 0
  },
  "previous_attributes": null
}
```

Charge your customer for the extra credits using an invoice. First, get the customers payment method, which is saved on the pricing plan’s billing profile.

Get the billing cadence from the pricing plan subscription:

```curl
curl https://api.stripe.com/v2/billing/pricing_plan_subscriptions/{{PRICING_PLAN_SUBSCRIPTION_ID}} \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview"
```

Get the billing profile from the billing cadence:

```curl
curl https://api.stripe.com/v2/billing/cadences/{{CADENCE_ID}} \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview"
```

Get the default payment method from the billing profile:

```curl
curl https://api.stripe.com/v2/billing/profiles/{{PROFILES_ID}} \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview"
```

Create an invoice that charges the customers default payment method:

```curl
curl https://api.stripe.com/v1/invoices \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d customer={{CUSTOMER_ID}} \
  -d collection_method=charge_automatically \
  -d auto_advance=true \
  -d default_payment_method={{PAYMENT_METHOD_ID}}
```

```cli
stripe invoices create  \
  --customer={{CUSTOMER_ID}} \
  --collection-method=charge_automatically \
  --auto-advance=true \
  --default-payment-method={{PAYMENT_METHOD_ID}}
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

invoice = client.v1.invoices.create({
  customer: '{{CUSTOMER_ID}}',
  collection_method: 'charge_automatically',
  auto_advance: true,
  default_payment_method: '{{PAYMENT_METHOD_ID}}',
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
invoice = client.v1.invoices.create({
  "customer": "{{CUSTOMER_ID}}",
  "collection_method": "charge_automatically",
  "auto_advance": True,
  "default_payment_method": "{{PAYMENT_METHOD_ID}}",
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$invoice = $stripe->invoices->create([
  'customer' => '{{CUSTOMER_ID}}',
  'collection_method' => 'charge_automatically',
  'auto_advance' => true,
  'default_payment_method' => '{{PAYMENT_METHOD_ID}}',
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

InvoiceCreateParams params =
  InvoiceCreateParams.builder()
    .setCustomer("{{CUSTOMER_ID}}")
    .setCollectionMethod(InvoiceCreateParams.CollectionMethod.CHARGE_AUTOMATICALLY)
    .setAutoAdvance(true)
    .setDefaultPaymentMethod("{{PAYMENT_METHOD_ID}}")
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
Invoice invoice = client.v1().invoices().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const invoice = await stripe.invoices.create({
  customer: '{{CUSTOMER_ID}}',
  collection_method: 'charge_automatically',
  auto_advance: true,
  default_payment_method: '{{PAYMENT_METHOD_ID}}',
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.InvoiceCreateParams{
  Customer: stripe.String("{{CUSTOMER_ID}}"),
  CollectionMethod: stripe.String(stripe.InvoiceCollectionMethodChargeAutomatically),
  AutoAdvance: stripe.Bool(true),
  DefaultPaymentMethod: stripe.String("{{PAYMENT_METHOD_ID}}"),
}
result, err := sc.V1Invoices.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new InvoiceCreateOptions
{
    Customer = "{{CUSTOMER_ID}}",
    CollectionMethod = "charge_automatically",
    AutoAdvance = true,
    DefaultPaymentMethod = "{{PAYMENT_METHOD_ID}}",
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Invoices;
Invoice invoice = service.Create(options);
```

Attach an invoice item to the invoice you created with the credit amount. In this example, the customer is going to top up 10 USD:

```curl
curl https://api.stripe.com/v1/invoiceitems \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d customer={{CUSTOMER_ID}} \
  -d currency={{CURRENCY}} \
  -d amount=1000 \
  -d invoice={{INVOICE_ID}}
```

```cli
stripe invoiceitems create  \
  --customer={{CUSTOMER_ID}} \
  --currency={{CURRENCY}} \
  --amount=1000 \
  --invoice={{INVOICE_ID}}
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

invoice_item = client.v1.invoice_items.create({
  customer: '{{CUSTOMER_ID}}',
  currency: '{{CURRENCY}}',
  amount: 1000,
  invoice: '{{INVOICE_ID}}',
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
invoice_item = client.v1.invoice_items.create({
  "customer": "{{CUSTOMER_ID}}",
  "currency": "{{CURRENCY}}",
  "amount": 1000,
  "invoice": "{{INVOICE_ID}}",
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$invoiceItem = $stripe->invoiceItems->create([
  'customer' => '{{CUSTOMER_ID}}',
  'currency' => '{{CURRENCY}}',
  'amount' => 1000,
  'invoice' => '{{INVOICE_ID}}',
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

InvoiceItemCreateParams params =
  InvoiceItemCreateParams.builder()
    .setCustomer("{{CUSTOMER_ID}}")
    .setCurrency("{{CURRENCY}}")
    .setAmount(1000L)
    .setInvoice("{{INVOICE_ID}}")
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
InvoiceItem invoiceItem = client.v1().invoiceItems().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const invoiceItem = await stripe.invoiceItems.create({
  customer: '{{CUSTOMER_ID}}',
  currency: '{{CURRENCY}}',
  amount: 1000,
  invoice: '{{INVOICE_ID}}',
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.InvoiceItemCreateParams{
  Customer: stripe.String("{{CUSTOMER_ID}}"),
  Currency: stripe.String(stripe.Currency{{CURRENCY}}),
  Amount: stripe.Int64(1000),
  Invoice: stripe.String("{{INVOICE_ID}}"),
}
result, err := sc.V1InvoiceItems.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new InvoiceItemCreateOptions
{
    Customer = "{{CUSTOMER_ID}}",
    Currency = "{{CURRENCY}}",
    Amount = 1000,
    Invoice = "{{INVOICE_ID}}",
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.InvoiceItems;
InvoiceItem invoiceItem = service.Create(options);
```

Finalize and charge the invoice:

```curl
curl -X POST https://api.stripe.com/v1/invoices/{{INVOICE_ID}}/pay \
  -u "<<YOUR_SECRET_KEY>>:"
```

```cli
stripe invoices pay {{INVOICE_ID}}
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

invoice = client.v1.invoices.pay('{{INVOICE_ID}}')
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
invoice = client.v1.invoices.pay("{{INVOICE_ID}}")
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$invoice = $stripe->invoices->pay('{{INVOICE_ID}}', []);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

InvoicePayParams params = InvoicePayParams.builder().build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
Invoice invoice = client.v1().invoices().pay("{{INVOICE_ID}}", params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const invoice = await stripe.invoices.pay('{{INVOICE_ID}}');
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.InvoicePayParams{}
result, err := sc.V1Invoices.Pay(context.TODO(), "{{INVOICE_ID}}", params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Invoices;
Invoice invoice = service.Pay("{{INVOICE_ID}}");
```

Next, listen to the [invoice.paid](https://docs.stripe.com/api/v2/core/events/event-types.md?api-version=preview#v2_event_types-v1.invoice.paid) event. The event object includes the items paid for in the invoice and the customer. Use those items to check whether to grant credits to the customer. Use the [Credit Grant API](https://docs.stripe.com/api/billing/credit-grant.md?api-version=preview) to grant customers credit grants on an ad-hoc basis.

```curl
curl https://api.stripe.com/v1/billing/credit_grants \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d "amount[type]"=monetary \
  -d "amount[monetary][currency]"=usd \
  -d "amount[monetary][value]"=1000 \
  -d "applicability_config[scope][price_type]"=metered \
  -d category=paid \
  -d customer={{CUSTOMER_ID}} \
  -d name="Credit Grant"
```

```cli
stripe billing credit_grants create  \
  -d "amount[type]"=monetary \
  -d "amount[monetary][currency]"=usd \
  -d "amount[monetary][value]"=1000 \
  -d "applicability_config[scope][price_type]"=metered \
  --category=paid \
  --customer={{CUSTOMER_ID}} \
  --name="Credit Grant"
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

credit_grant = client.v1.billing.credit_grants.create({
  amount: {
    type: 'monetary',
    monetary: {
      currency: 'usd',
      value: 1000,
    },
  },
  applicability_config: {scope: {price_type: 'metered'}},
  category: 'paid',
  customer: '{{CUSTOMER_ID}}',
  name: 'Credit Grant',
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
credit_grant = client.v1.billing.credit_grants.create({
  "amount": {"type": "monetary", "monetary": {"currency": "usd", "value": 1000}},
  "applicability_config": {"scope": {"price_type": "metered"}},
  "category": "paid",
  "customer": "{{CUSTOMER_ID}}",
  "name": "Credit Grant",
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$creditGrant = $stripe->billing->creditGrants->create([
  'amount' => [
    'type' => 'monetary',
    'monetary' => [
      'currency' => 'usd',
      'value' => 1000,
    ],
  ],
  'applicability_config' => ['scope' => ['price_type' => 'metered']],
  'category' => 'paid',
  'customer' => '{{CUSTOMER_ID}}',
  'name' => 'Credit Grant',
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

CreditGrantCreateParams params =
  CreditGrantCreateParams.builder()
    .setAmount(
      CreditGrantCreateParams.Amount.builder()
        .setType(CreditGrantCreateParams.Amount.Type.MONETARY)
        .setMonetary(
          CreditGrantCreateParams.Amount.Monetary.builder()
            .setCurrency("usd")
            .setValue(1000L)
            .build()
        )
        .build()
    )
    .setApplicabilityConfig(
      CreditGrantCreateParams.ApplicabilityConfig.builder()
        .setScope(
          CreditGrantCreateParams.ApplicabilityConfig.Scope.builder()
            .setPriceType(
              CreditGrantCreateParams.ApplicabilityConfig.Scope.PriceType.METERED
            )
            .build()
        )
        .build()
    )
    .setCategory(CreditGrantCreateParams.Category.PAID)
    .setCustomer("{{CUSTOMER_ID}}")
    .setName("Credit Grant")
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
CreditGrant creditGrant = client.v1().billing().creditGrants().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const creditGrant = await stripe.billing.creditGrants.create({
  amount: {
    type: 'monetary',
    monetary: {
      currency: 'usd',
      value: 1000,
    },
  },
  applicability_config: {
    scope: {
      price_type: 'metered',
    },
  },
  category: 'paid',
  customer: '{{CUSTOMER_ID}}',
  name: 'Credit Grant',
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.BillingCreditGrantCreateParams{
  Amount: &stripe.BillingCreditGrantCreateAmountParams{
    Type: stripe.String("monetary"),
    Monetary: &stripe.BillingCreditGrantCreateAmountMonetaryParams{
      Currency: stripe.String(stripe.CurrencyUSD),
      Value: stripe.Int64(1000),
    },
  },
  ApplicabilityConfig: &stripe.BillingCreditGrantCreateApplicabilityConfigParams{
    Scope: &stripe.BillingCreditGrantCreateApplicabilityConfigScopeParams{
      PriceType: stripe.String("metered"),
    },
  },
  Category: stripe.String(stripe.BillingCreditGrantCategoryPaid),
  Customer: stripe.String("{{CUSTOMER_ID}}"),
  Name: stripe.String("Credit Grant"),
}
result, err := sc.V1BillingCreditGrants.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.Billing.CreditGrantCreateOptions
{
    Amount = new Stripe.Billing.CreditGrantAmountOptions
    {
        Type = "monetary",
        Monetary = new Stripe.Billing.CreditGrantAmountMonetaryOptions
        {
            Currency = "usd",
            Value = 1000,
        },
    },
    ApplicabilityConfig = new Stripe.Billing.CreditGrantApplicabilityConfigOptions
    {
        Scope = new Stripe.Billing.CreditGrantApplicabilityConfigScopeOptions
        {
            PriceType = "metered",
        },
    },
    Category = "paid",
    Customer = "{{CUSTOMER_ID}}",
    Name = "Credit Grant",
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Billing.CreditGrants;
Stripe.Billing.CreditGrant creditGrant = service.Create(options);
```

### Restore access when credits are replenished

After you grant credits to the customer, Stripe automatically fires a `billing.alert.recovered` event when the customer’s credit balance goes back above the alert threshold. Listen for this event to restore the customer’s access to your platform.

```json
{
  "object": {
    "object": "billing.alert_recovered",
    "alert": {
      "id": "alrt_test_61T7eah2z8l8a2193416ZU9yVCs7VBlA",
      "object": "billing.alert",
      "alert_type": "credit_balance_threshold",
      "credit_balance_threshold": {
        "filters": [
          {
            "customer": null,
            "type": "customer"
          }
        ],
        "lte": {
          "balance_type": "monetary",
          "custom_pricing_unit": null,
          "monetary": {
            "currency": "usd",
            "value": 0
          }
        },
        "recurrence": "one_time"
      },
      "livemode": false,
      "status": "active",
      "title": "Low Balance Alert",
      "usage_threshold": null
    },
    "created": 1756414980,
    "currency": "usd",
    "custom_pricing_unit": null,
    "customer": "cus_Su65aU14rK29BS",
    "external_customer_id": "cus_Su65aU14rK29BS",
    "livemode": false,
    "value": 1000
  },
  "previous_attributes": null
}
```

When you receive this event, you can choose to restore the customer’s access based on your internal policy. The `value` field indicates the customer’s current credit balance after the top-up.

#### Workflows

[Stripe Workflows](https://docs.stripe.com/workflows.md) is a visual builder that allows you to automate tasks and quickly iterate through multi-step processes.

Go to **Dashboard** > **Workflows** > [Create workflow](https://dashboard.stripe.com/test/workflows/create) to use the workflow editor. Add the following steps and conditions:

### Initiate a topup triggered by a customer change

Use this workflow to initiate a topup triggered by a customer change, like reaching a threshold or running out of credits.

1. Go to **Dashboard** > **Workflows** > [Create workflow](https://dashboard.stripe.com/test/workflows/create).
1. Set up the workflow trigger:
   - Add a **Billing alert triggered** trigger.
   - In the **Trigger conditions** panel, set the condition:
     - **If**
     - Alert -> Title (`Alert | Title`)
     - **is equal to**
     - `{alert title}`
1. Add a **Retrieve a customer** action:
   - In the **Configuration** panel, click the + button and select Customer ID. This sets **Customer ID (required)** to `Billing alert triggered | Customer ID`.
1. Add a **Create an invoice** action:
   - In the **Configuration** panel, configure the following fields:
     - **Auto advance** : True
     - **Collection method**: Charge automatically
     - **Customer ID** : `Customer | ID`
   - Leave other fields at their default values.
1. Add a **Create an invoice item** action:
   - In the **Configuration** panel, configure the following fields:
     - **Customer ID**: `Customer | ID`
     - **Amount**: `Customer | Metadata | topup_amount`
     - **Invoice ID (required)**: `Invoice | ID`
1. Add a **Finalize an invoice** action:
   - In the **Configuration** panel, set **Invoice ID (required)** to `Invoice | ID`.
1. Add a condition after the finalize step:
   - Add a branch condition: **If this condition is met** `Invoice | Status` **is equal to** `Paid`.
1. In the “condition is met” branch, add a **Create a billing credit grant** action:
   - In the **Configuration** panel, configure the following fields:
     - **Value**: `Invoice Item | Amount`
     - **Currency**: `USD - US Dollar`
     - **Type**: `Monetary`
     - **Applicability config -> Scope -> Price type**: Metered
     - **Category**: Paid
     - **Customer ID**: `Customer | ID`
1. Click **Activate** to save and activate your workflow.

### Initiate topup based on customer request

Use this workflow to initiate topup in your platform based on a customer request.

1. Set up the workflow trigger:
   - Add a **Invoice is Paid** trigger.
   - Add a condition that defines this as an invoice for topups: in the **Trigger conditions** panel, set the condition:
     - **If**
     - **Metadata**
     - `{reason}` **is equal to**
     - `{topup}`
1. Add a **Create a billing credit grant** action:
   - In the **Configuration** panel, configure the following fields:
     - **Value**: `Invoice Item | Amount`
     - **Currency**: `USD - US Dollar`
     - **Type**: `Monetary`
     - **Customer ID**: `Customer | ID`
1. Click **Apply changes** to save and activate your workflow.

### Restore access when credits are replenished

After credits are granted, Stripe automatically fires a `billing.alert.recovered` event when the customer’s credit balance goes back above the alert threshold.

> The `billing.alert.recovered` event isn’t available as a Workflows trigger. To restore access when credits are replenished, listen for the event using a [webhook endpoint](https://docs.stripe.com/webhooks.md) instead.

## Record usage

After you create a pricing plan subscription, you can begin sending usage data to the metered items you created.

```curl
curl https://api.stripe.com/v1/billing/meter_events \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d event_name={{METER_EVENT_NAME}} \
  -d "payload[stripe_customer_id]"={{CUSTOMER_ID}} \
  -d "payload[model]"=hypernian_1 \
  -d "payload[tokens_used]"=10
```

```cli
stripe billing meter_events create  \
  --event-name={{METER_EVENT_NAME}} \
  -d "payload[stripe_customer_id]"={{CUSTOMER_ID}} \
  -d "payload[model]"=hypernian_1 \
  -d "payload[tokens_used]"=10
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

meter_event = client.v1.billing.meter_events.create({
  event_name: '{{METER_EVENT_NAME}}',
  payload: {
    stripe_customer_id: '{{CUSTOMER_ID}}',
    model: 'hypernian_1',
    tokens_used: '10',
  },
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
meter_event = client.v1.billing.meter_events.create({
  "event_name": "{{METER_EVENT_NAME}}",
  "payload": {
    "stripe_customer_id": "{{CUSTOMER_ID}}",
    "model": "hypernian_1",
    "tokens_used": "10",
  },
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$meterEvent = $stripe->billing->meterEvents->create([
  'event_name' => '{{METER_EVENT_NAME}}',
  'payload' => [
    'stripe_customer_id' => '{{CUSTOMER_ID}}',
    'model' => 'hypernian_1',
    'tokens_used' => '10',
  ],
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

MeterEventCreateParams params =
  MeterEventCreateParams.builder()
    .setEventName("{{METER_EVENT_NAME}}")
    .putPayload("stripe_customer_id", "{{CUSTOMER_ID}}")
    .putPayload("model", "hypernian_1")
    .putPayload("tokens_used", "10")
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
MeterEvent meterEvent = client.v1().billing().meterEvents().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const meterEvent = await stripe.billing.meterEvents.create({
  event_name: '{{METER_EVENT_NAME}}',
  payload: {
    stripe_customer_id: '{{CUSTOMER_ID}}',
    model: 'hypernian_1',
    tokens_used: '10',
  },
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.BillingMeterEventCreateParams{
  EventName: stripe.String("{{METER_EVENT_NAME}}"),
  Payload: map[string]string{
    "stripe_customer_id": "{{CUSTOMER_ID}}",
    "model": "hypernian_1",
    "tokens_used": "10",
  },
}
result, err := sc.V1BillingMeterEvents.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.Billing.MeterEventCreateOptions
{
    EventName = "{{METER_EVENT_NAME}}",
    Payload = new Dictionary<string, string>
    {
        { "stripe_customer_id", "{{CUSTOMER_ID}}" },
        { "model", "hypernian_1" },
        { "tokens_used", "10" },
    },
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Billing.MeterEvents;
Stripe.Billing.MeterEvent meterEvent = service.Create(options);
```

## View upcoming invoices

Create a preview invoice to see a preview of a customer’s invoice. The preview includes the relevant line items from the various pricing plan components.

#### Dashboard

1. Go to the [Pricing plan subscriptions](https://dashboard.stripe.com/test/pricing-plan/subscriptions) tab.
1. Click the subscription you want to preview an invoice for.
1. Scroll down to the **Upcoming invoice** section. The preview invoice shows the subscription amount to bill the customer on the specified date, and reflects the corresponding metered items, license items, and credits.

#### API

```curl
curl https://api.stripe.com/v1/invoices/create_preview \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d billing_cadence=bc_test_61SrjnScUwT6mNskZ16SjPfE4ZSQFjWjdqlzQfWMCVnM
```

```cli
stripe invoices create_preview  \
  --billing-cadence=bc_test_61SrjnScUwT6mNskZ16SjPfE4ZSQFjWjdqlzQfWMCVnM
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

invoice = client.v1.invoices.create_preview({
  billing_cadence: 'bc_test_61SrjnScUwT6mNskZ16SjPfE4ZSQFjWjdqlzQfWMCVnM',
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
# This example uses the beta SDK. See https://github.com/stripe/stripe-python#public-preview-sdks
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
invoice = client.v1.invoices.create_preview({
  "billing_cadence": "bc_test_61SrjnScUwT6mNskZ16SjPfE4ZSQFjWjdqlzQfWMCVnM",
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
// This example uses the beta SDK. See https://github.com/stripe/stripe-php#public-preview-sdks
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$invoice = $stripe->invoices->createPreview([
  'billing_cadence' => 'bc_test_61SrjnScUwT6mNskZ16SjPfE4ZSQFjWjdqlzQfWMCVnM',
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
// This example uses the beta SDK. See https://github.com/stripe/stripe-java#public-preview-sdks
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

InvoiceCreatePreviewParams params =
  InvoiceCreatePreviewParams.builder()
    .setBillingCadence("bc_test_61SrjnScUwT6mNskZ16SjPfE4ZSQFjWjdqlzQfWMCVnM")
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
Invoice invoice = client.v1().invoices().createPreview(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
// This example uses the beta SDK. See https://github.com/stripe/stripe-node#public-preview-sdks
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const invoice = await stripe.invoices.createPreview({
  billing_cadence: 'bc_test_61SrjnScUwT6mNskZ16SjPfE4ZSQFjWjdqlzQfWMCVnM',
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
// This example uses the beta SDK. See https://github.com/stripe/stripe-go#public-preview-sdks
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.InvoiceCreatePreviewParams{
  BillingCadence: stripe.String("bc_test_61SrjnScUwT6mNskZ16SjPfE4ZSQFjWjdqlzQfWMCVnM"),
}
result, err := sc.V1Invoices.CreatePreview(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
// This example uses the beta SDK. See https://github.com/stripe/stripe-dotnet#public-preview-sdks
var options = new InvoiceCreatePreviewOptions
{
    BillingCadence = "bc_test_61SrjnScUwT6mNskZ16SjPfE4ZSQFjWjdqlzQfWMCVnM",
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Invoices;
Invoice invoice = service.CreatePreview(options);
```

```json
{"hosted_invoice_url": "example.com/invoice",
  "invoice_pdf": null,
  "billing_reason": "manual",
  "collection_method": "charge_automatically",
  "created": 1680644467,
  "currency": "usd",
  "custom_fields": null,
  "customer": "cus_NeZwdNtLEOXuvB",
  "customer_address": null,
  "customer_email": "jennyrosen@example.com",
  "customer_name": "Jenny Rosen",
  "customer_phone": null,
  "customer_shipping": null,
  "customer_tax_exempt": "none",
  "customer_tax_ids": [],
  "default_payment_method": null,
  "default_source": null,
  "default_tax_rates": [],
  "description": null,
  "discounts": [],
  "due_date": null,
  "ending_balance": null,
  "footer": null,
  "from_invoice": null,
  "last_finalization_error": null,
  "latest_revision": null,
  "lines": {
    "object": "list",
    "data": [],
    "has_more": false,
    "total_count": 0,
    "url": "/v1/invoices/in_1MtHbELkdIwHu7ixl4OzzPMv/lines"
  },
{
  "id": "upcoming_in_1MtHbELkdIwHu7ixl4OzzPMv",
  "object": "invoice",
  "account_country": "US",
  "account_name": "Stripe Docs",
  "account_tax_ids": null,
  "amount_due": 0,
  "amount_paid": 0,
  "amount_overpaid": 0,
  "amount_remaining": 0,
  "amount_shipping": 0,
  "application": null,
  "application_fee_amount": null,
  "attempt_count": 0,
  "attempted": false,
  "auto_advance": false,
  "automatic_tax": {
    "enabled": false,
    "status": null
  },
  "livemode": false,
  "metadata": {},
  "next_payment_attempt": null,
  "number": null,
  "on_behalf_of": null,
  "parent": null,
  "payment_settings": {
    "default_mandate": null,
    "payment_method_options": null,
    "payment_method_types": null
  },
  "period_end": 1680644467,
  "period_start": 1680644467,
  "post_payment_credit_notes_amount": 0,
  "pre_payment_credit_notes_amount": 0,
  "receipt_number": null,
  "shipping_cost": null,
  "shipping_details": null,
  "starting_balance": 0,
  "statement_descriptor": null,
  "status": "draft",
  "status_transitions": {
    "finalized_at": null,
    "marked_uncollectible_at": null,
    "paid_at": null,
    "voided_at": null
  },
  "subtotal": 0,
  "subtotal_excluding_tax": 0,
  "test_clock": null,
  "total": 0,
  "total_discount_amounts": [],
  "total_excluding_tax": 0,
  "total_taxes": [],
  "webhooks_delivered_at": 1680644467
}
```

## See also

- [Migrate customers to new or updated pricing plans](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions/manage.md#migrate)
- [Update existing subscriptions](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions/manage.md#update-existing-subscriptions)
- [Cancel pricing plan subscriptions](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions/manage.md#cancel)

# Set up pricing plans

Learn how to set up pricing plans and pricing plan components.

You can group different pricing components into a single pricing plan. For example, you can create a pricing plan that includes [rate cards](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md) for usage-based billing, [license fees](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/license-fees/about.md) for recurring charges, and [service actions](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/service-actions/about.md) for recurring credit grant allocations. When a customer subscribes to a pricing plan, all the recurring components are automatically enrolled and billed according to the cadence you configure.

> Pricing plans are currently in [private preview](https://docs.stripe.com/release-phases.md) and could change in functionality and integration path before they’re generally available to all Stripe users. Contact us  to request access.

## Create a pricing plan

Use the Stripe Dashboard or API to create a pricing plan that contains all the relevant billing components of your pricing model.

For each pricing plan, you can configure:

- **Components**: Add [rate cards](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md) for usage-based billing, [license fees](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/license-fees/about.md) for recurring charges, and [service actions](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/service-actions/about.md) for recurring credit grant allocations. You can add all or only selected components to a pricing plan, depending on your pricing model.
- **Currency**: Specify the currency for all the components in your pricing plan.
- **Include tax in prices**: Specify whether to include tax in your price (inclusive) or to add it to the invoice subtotal (exclusive). Learn more about  [inclusive and exclusive taxes for billing](https://docs.stripe.com/billing/taxes/tax-rates.md#inclusive-vs-exclusive-tax).
- **Metadata**: Optionally add your own metadata to the pricing plan.

After you set the currency and tax parameters, define the relevant components of your plan. Which components you include depends on your pricing model. For usage-based billing, you also need to [create a meter](https://docs.stripe.com/billing/subscriptions/usage-based/meters/configure.md) (or use an existing one) to record usage events.

#### Dashboard

1. On the [Pricing plans](https://dashboard.stripe.com/test/pricing-plans) page, click **Create pricing plan**.
1. In the pricing plan editor:
   - Provide a display name, currency, and tax behavior.
   - (Optional) Under **Advanced settings**, specify the description, unique lookup key, and metadata.
1. Click **Continue**.

After you create the pricing plan, you can add components such as rate cards, license fees, and service actions. See the sections below for details on adding each component type.

#### API

When you create a [pricing plan](https://docs.stripe.com/api/v2/pricing-plans.md?api-version=preview), provide a display name, currency, and specify the tax behavior (learn more about [tax behavior and rate cards](https://docs.stripe.com/tax/subscriptions/rate-card-tax-codes-tax-behavior.md#set-a-default-tax-behavior-\(recommended\))).

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Pro Pricing Plan",
    "currency": "usd",
    "tax_behavior": "exclusive"
  }'
```

After you submit the pricing plan request, Stripe returns the active `Pricing Plan` object. You can’t subscribe new customers to an inactive pricing plan.

```json
{
  "id": "bpp_test_61SjPwyNGx88hyuOg16SjPfE4ZSQFjWjdqlzQfWMCH1E",
  "object": "v2.billing.pricing_plan",
  "active": true,
  "created": "2025-06-14T21:52:04.000Z",
  "currency": "usd",
  "description": null,
  "display_name": "Pro Pricing Plan",
  "latest_version": "bppv_test_123",
  "live_version": "bppv_test_123",
  "lookup_key": null,
  "metadata": {},
  "tax_behavior": "exclusive"
}
```

You can add an existing component to your pricing plan by referencing its ID and version.

## Add a rate card

To attach a rate card to your pricing plan, create a [rate card](https://docs.stripe.com/api/v2/product-catalog/create-ratecard.md?api-version=preview) within the pricing plan editor or through the API.

#### Dashboard

1. In the pricing plan editor, click + and **Rate card**.
1. In the rate card configuration:
   - Provide a display name.
   - Specify the servicing period.
   - (Optional) Under **Advanced settings**, provide a lookup key and metadata.
1. Click **Continue**.
1. Add rates to the rate card by providing metered items and pricing details.
1. Click **Done**.

#### API

First, create a rate card and provide a display name, currency, service interval, and tax behavior.

```curl
curl -X POST https://api.stripe.com/v2/billing/rate_cards \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Hypernian",
    "service_interval": "month",
    "service_interval_count": 1,
    "currency": "usd",
    "tax_behavior": "exclusive"
  }'
```

After you create the rate card, you can add it to the pricing plan:

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "type": "rate_card",
    "rate_card": {
        "id": "{{RATE_CARD_ID}}",
        "version": "{{RATE_CARD_VERSION}}"
    },
    "metadata": {
        "existing_key": "updated_value",
        "new_key": "new value"
    }
  }'
```

## Add a license fee

License fees are fixed recurring charges that you can collect up front.

#### Dashboard

1. In the pricing plan editor, click + and **License fee**.
1. In the license fee configuration:
   - Provide a display name for the licensed item.
   - Specify the servicing period.
   - Select the **Price type** and enter the price.
   - (Optional) Configure **Advanced settings**.
1. Click **Done**.

#### API

First, create a license item:

```curl
curl -X POST https://api.stripe.com/v2/billing/licensed_items \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Pricing Plan Licensed Item"
  }'
```

Then, create a license fee:

```curl
curl -X POST https://api.stripe.com/v2/billing/license_fees \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "E2E License",
    "licensed_item": "{{LICENSED_ITEM_ID}}",
    "unit_amount": "50000",
    "service_interval": "month",
    "service_interval_count": 1,
    "currency": "usd",
    "tax_behavior": "exclusive"
  }'
```

Finally, attach the license fee to a pricing plan:

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "type": "license_fee",
    "license_fee": {
        "id": "{{LICENSE_FEE_ID}}",
        "version": "{{LICENSE_FEE_VERSION}}"
    },
    "lookup_key": "monthly-fee-component",
    "metadata": {
        "existing_key": "updated_value",
        "new_key": "new value"
    }
  }'
```

## Add a service action

You can add new components, including recurring credit grants, to your pricing plan. Use recurring credit grants if you use a [credit burndown pricing model](https://docs.stripe.com/subscriptions/pricing-models/usage-based-pricing.md#credit-burndown). Service actions let you offer recurring credits to customers, which can offset charges for specific billable items, such as usage-based fees.

When you create a service action, you configure:

- Amount
- Billing frequency
- Applicable billable items

#### Dashboard

1. In the pricing plan editor, click + and **Credit grant**.
1. In the recurring credit grant configuration:
   - Provide a display name for the credit grant.
   - Specify the servicing period.
   - Provide a credit amount.
   - (Optional) Configure **Advanced settings**.
1. Click **Done**.

#### API

To create a monthly credit grant of 10 USD that applies to a specific billable item and expires at the end of the service interval:

```curl
curl -X POST https://api.stripe.com/v2/billing/service_actions \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "service_interval": "month",
    "service_interval_count": 1,
    "type": "credit_grant",
    "lookup_key": "credit grant 28",
    "credit_grant": {
        "name": "Credit grant 28",
        "expiry_config": {
            "type": "end_of_service_period"
        },
        "applicability_config": {
            "scope": {
                "billable_items": "{{BILLABLE_ITEM_ID}}"
            }
        },
        "amount": {
            "type": "monetary",
            "monetary": {
                "value": "1000",
                "currency": "usd"
            }
        }
    }
  }'
```

Attach the service action to your pricing plan:

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "type": "service_action",
    "service_action": {
        "id": "{{SERVICE_ACTION_ID}}",
        "version": "{{PRICING_PLAN_ID}}"
    },
    "lookup_key": "credit-grant-28",
    "metadata": {
        "existing_key": "updated_value",
        "new_key": "new value"
    }
  }'
```

## Activate the pricing plan

After you add the relevant components for your pricing model, activate that version of the pricing plan. When the plan is active, you can [subscribe customers to it](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/pricing-packaging.md#subscribe).

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}} \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "live_version": "latest"
  }'
```

## Update the pricing plan

To update a pricing plan, you can add a new component or remove an existing component and replace it with a new component. Each change creates a new version, which is tracked as the [latest_version](https://docs.stripe.com/api/v2/pricing-plans/pricing-plan/object.md?api-version=preview#v2_pricing_plan_object-latest_version), while preserving older versions for existing subscriptions or reference.

To manage updates effectively:

1. **Update the pricing plan**: Add or modify components, creating a new `latest_version`.
1. **Set the live version**: Update `live_version` to `latest` for new subscriptions.
1. **Notify existing customers**: Inform customers or segments about upcoming changes.
1. **Migrate subscriptions**: On your schedule, update pricing plan subscriptions to the new version for selected customers.

This flow ensures smooth transitions while addressing customer communication and segmentation needs.

For example, you can add a license fee to an existing pricing plan that has a rate card component. First, create the license fee:

```curl
curl -X POST https://api.stripe.com/v2/billing/license_fees \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "currency": "usd",
    "display_name": "Monthly fee",
    "lookup_key": "monthly_fee",
    "metadata": {
        "internal_id": "1234567890"
    },
    "tax_behavior": "exclusive",
    "licensed_item": "{{LICENSED_ITEM_ID}}",
    "service_interval": "month",
    "service_interval_count": 1,
    "unit_amount": "20.00"
  }'
```

Then, attach the license fee to the pricing plan:

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "type": "license_fee_component",
    "license_fee_component": {
        "license_fee": "{{LICENSE_FEE_ID}}",
        "version": "{{LICENSE_FEE_VERSION}}"
    }
  }'
```

The response shows the new component and increments the pricing plan’s version:

```json
{
  "id": "{{PRICING_PLAN_COMPONENT_ID}}",
  "object": "v2.billing.pricing_plan_component",
  "created": "2025-06-20T16:30:00.000Z",
  "type": "license_fee_component",
  "pricing_plan": "{{PRICING_PLAN_ID}}",
  "pricing_plan_version": "{{PRICING_PLAN_VERSION}}",
  "license_fee_component": {
    "license_fee": "{{LICENSE_FEE_ID}}",
    "version": "{{NEW_LICENSE_FEE_VERSION}}"
  }
}
```

### Replace a component

To replace a component, you must remove the existing component before you can add a new one.

First, retrieve the components to find a given component’s ID.

```curl
curl https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview"
```

Then, delete the component.

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components/{{COMPONENT_ID}} \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview"
```

### Set the live version

By default, new pricing plan versions don’t affect new subscriptions unless you update the [live_version](https://docs.stripe.com/api/v2/pricing-plans/pricing-plan/object.md?api-version=preview#v2_pricing_plan_object-live_version). To make the latest version (for example, v3) the default for new subscriptions, set it as the live version. If you don’t specify a version, the live version is used by default.

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}} \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "live_version": "latest"
  }'
```

The response reflects the update:

```json
{
  "id": "{{PRICING_PLAN_ID}}",
  "object": "v2.billing.pricing_plan",
  "active": true,
  "created": "2025-06-14T21:52:04.000Z",
  "currency": "usd",
  "display_name": "USD pro plan",
  "latest_version": "{{PRICING_PLAN_VERSION_3}}",
  "live_version": "{{PRICING_PLAN_VERSION_3}}",
  "livemode": false
}
```

All new subscriptions use the version you specified (v3 in this example) unless you set a different live version.

### Update existing subscriptions

Existing pricing plan subscriptions remain on their original version unless you manually update them. To migrate existing customers to the new version, use a [billing intent](https://docs.stripe.com/api/v2/billing-intents.md?api-version=preview) to update their subscription’s pricing plan version.

```curl
curl -X POST https://api.stripe.com/v2/billing/intents \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "cadence": "{{BILLING_CADENCE_ID}}",
    "currency": "usd",
    "effective_at": "current_billing_period_start",
    "actions": [
        {
            "type": "deactivate",
            "deactivate": {
                "type": "pricing_plan_subscription_details",
                "proration_behavior": "none",
                "pricing_plan_subscription_details": {
                    "pricing_plan_subscription": "{{PRICING_PLAN_SUBSCRIPTION_ID}}",
                    "pricing_plan_version": "{{PRICING_PLAN_VERSION_ID}}",
                    "component_configurations": []
                }
            }
        }
    ]
  }'
```

# Rate cards

Learn how you can create a pricing plan component for your usage-based pricing.

Rate cards add usage-based pricing to your pricing plans. You can add new rates to a rate card without triggering a version change for existing subscriptions. Modifying or deleting existing rates creates a new version of the rate card.

> Pricing plans are currently in [private preview](https://docs.stripe.com/release-phases.md) and could change in functionality and integration path before they’re generally available to all Stripe users. 

## Example rate card

Here’s an example of what a complete card looks like:
![Example image of a rate card](https://b.stripecdn.com/docs-statics-srv/assets/pricing-plan-rate-card.654dc92b0d3c16a909423fcb1324c96c.png)

A rate card with a rate that contains a metered item.

## Create a rate card 

Use the Stripe Dashboard or API to create a rate card that contains multiple rates, with each rate specifying a metered item, a meter, and a pricing model. You create rate cards as components within a [pricing plan](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md).

For each rate card, you can configure:

- **Service interval**: Monthly, annual, weekly, or custom.
- **Currency**
- **Include tax in prices**: Specify whether to include tax in your price (inclusive) or to add it to the invoice subtotal (exclusive). Learn more about  [inclusive and exclusive taxes for billing](https://docs.stripe.com/billing/taxes/tax-rates.md#inclusive-vs-exclusive-tax).
- **Metadata**: Add metadata to the rate card.
- **Lookup key**: Unique and internal identifier.

You can’t change the service interval, currency, or tax calculation parameters after you create the rate card. Rate cards support up to 500 rates.

After you set the service interval, currency, and tax parameters, you can define multiple rates within the rate card by using [rate card rates](https://docs.stripe.com/api/v2/product-catalog/create-ratecardrate.md?api-version=preview). Each rate specifies a [metered item](https://docs.stripe.com/api/v2/product-catalog/create-ratecardrate.md?api-version=preview#v2_create_billing_rate_cards_rates-metered_item) (what you’re selling), the [meter](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#meter) that tracks usage of that item, and the pricing model applied to the usage:

- **Price type**: Fixed rate, volume, or graduated.
- **Sell as**: Charge by individual units or by a packaged group of units. If you use packages, you specify the number of units per package and how to round (up or down) for partial packages.
- **Advanced settings**: You can optionally [specify the product tax code](https://docs.stripe.com/tax/subscriptions/rate-card-tax-codes-tax-behavior.md). You can also add metadata on the rate and the metered item.

You can add new rates to a rate card at any time. If you modify or delete existing rates, a new version of the rate card is created.

#### Dashboard

You create rate cards within the pricing plan editor as part of a pricing plan.

1. On the [Pricing plans](https://dashboard.stripe.com/test/pricing-plans) page, click **Create pricing plan** (or open an existing pricing plan).
1. In the pricing plan editor:
   - Provide a display name, currency, and tax behavior for the pricing plan.
   - Click **Continue**.
1. In the pricing plan editor, click + and **Rate card**.
1. In the rate card editor:
   - Provide a display name for your rate card. For example, `Hypernian`.
   - Specify the servicing period. Learn more about the [service interval](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#cadence-service-interval).
   - (Optional) Under **Advanced settings**, provide a lookup key and metadata.
   - Click **Continue**.
1. Add a rate to the rate card:
   - Provide a display name for the metered item. For example, `Hypernian tokens`.
   - Select an existing **Meter** or create a new one by clicking +.
   - Select the **Price type**: **Fixed rate**, [Volume](https://docs.stripe.com/subscriptions/pricing-models/tiered-pricing.md#volume-based-pricing), or [Graduated](https://docs.stripe.com/subscriptions/pricing-models/tiered-pricing.md#graduated-pricing).
     - Select **Sell as** Individual units or a Packaged group of units. For example, an AI company might sell their tokens as packages of `100` units, at `0.04 USD` per package.
     - For packages, enter the **Units per package**.
     - Select whether to round up or down for **Partial packages**. If you round up, a user that uses `110` units is charged `0.08 USD`.
     - Enter the **Price per package**.
   - (Optional) Configure **Advanced settings** for your metered item, such as specifying a **Product tax code** (learn more about [tax codes](https://docs.stripe.com/tax/tax-codes.md)), **Unit label**, **Lookup key**, and **Metadata**. You can also add metadata to the rate.
   - Click **Done**.
1. (Optional) Click + **Add rate** to add additional rates to the rate card.
1. After you finish configuring the pricing plan, click **Create pricing plan**.

#### API

When you [create a rate card](https://docs.stripe.com/api/v2/product-catalog/create-ratecard.md?api-version=preview), provide:

- [currency](https://docs.stripe.com/api/v2/product-catalog/create-ratecard.md?api-version=preview#v2_create_rate_cards-currency)
- [display_name](https://docs.stripe.com/api/v2/product-catalog/create-ratecard.md?api-version=preview#v2_create_rate_cards-display_name)
- [service_interval](https://docs.stripe.com/api/v2/product-catalog/create-ratecard.md?api-version=preview#v2_create_rate_cards-service_interval)
- [service_interval_count](https://docs.stripe.com/api/v2/product-catalog/create-ratecard.md?api-version=preview#v2_create_rate_cards-service_interval_count)
- [tax_behavior](https://docs.stripe.com/api/v2/product-catalog/create-ratecard.md?api-version=preview#v2_create_rate_cards-tax_behavior)

In the following example, the customer’s fees accumulate on a monthly basis. If you change the `service_interval` to `year`, the fees would accumulate on a yearly basis. The service interval defines the period when the customer accumulates fees. (The service interval is distinct from the billing interval, which defines when the customer is billed.)

```curl
curl -X POST https://api.stripe.com/v2/billing/rate_cards \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Hypernian",
    "service_interval": "month",
    "service_interval_count": 1,
    "currency": "usd",
    "tax_behavior": "exclusive"
  }'
```

After you submit the rate card request, Stripe returns the active rate card object.

```json
{
  "id": "{{RATE_CARD_ID}}",
  "object": "billing.rate_card",
  "active": true,
  "created": "2024-11-17T21:49:50.000Z",
  "currency": "usd",
  "display_name": "Hypernian",
  "metadata": {},
  "service_interval": "month",
  "service_interval_count": 1,
  "latest_version": "{{RATE_CARD_VERSION_ID}}",
  "live_version": "{{RATE_CARD_VERSION_ID}}",
  "tax_behavior": "exclusive"
}
```

Before you create a metered item, you need to [create a meter](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md#create-meter) to record your usage.

[Create a metered item](https://docs.stripe.com/api/v2/metered-items/create.md?api-version=preview) to define the granular item you’re selling, like `Hypernian tokens`. The `unit_label` defines how the price is displayed on your payment page. When you create a metered item, you can optionally specify dimensions to tag your usage data in the  [meter_segment_conditions](https://docs.stripe.com/api/v2/metered-items/create.md?api-version=preview#v2_create_metered_items-meter_segment_conditions) array.

```curl
curl -X POST https://api.stripe.com/v2/billing/metered_items \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Hypernian tokens",
    "meter": "{{METER_ID}}",
    "lookup_key": "hypernian_tokens",
    "unit_label": "per 1 million events",
    "meter_segment_conditions": [
        {
            "dimension": "dimension_1",
            "value": "value_1"
        }
    ]
  }'
```

Set the rate for the metered item by [creating a rate card rate](https://docs.stripe.com/api/v2/product-catalog/create-ratecardrate.md?api-version=preview). This rate charges the customer 0.01 USD per meter event.

```curl
curl -X POST https://api.stripe.com/v2/billing/rate_cards/{{RATECARD_ID}}/rates \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "metered_item": "{{METERED_ITEM_ID}}",
    "unit_amount": "100"
  }'
```

You can also create a rate card rate that uses [tiered pricing](https://docs.stripe.com/products-prices/pricing-models.md#tiered-pricing):

```curl
curl -X POST https://api.stripe.com/v2/billing/rate_cards/{{RATECARD_ID}}/rates \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "metered_item": "{{METERED_ITEM_ID}}",
    "tiers": [
        {
            "up_to": 10,
            "unit_amount": "100",
            "flat_amount": "40"
        },
        {
            "up_to": 20,
            "unit_amount": "90",
            "flat_amount": "30"
        }
    ],
    "tiering_mode": "graduated"
  }'
```

### Attach a rate card to a pricing plan

After you create and configure a rate card, attach it to a [pricing plan](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md).

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "type": "rate_card",
    "rate_card": {
        "id": "{{RATE_CARD_ID}}",
        "version": "{{RATE_CARD_VERSION}}"
    },
    "lookup_key": "rate-card-component",
    "metadata": {
        "existing_key": "updated_value",
        "new_key": "new value"
    }
  }'
```

# License fees

Include recurring fees as a component of your pricing plan.

You can set up recurring fees charged up front using licensed fees. Use license fees if you’re building a [flat-fee and overages](https://docs.stripe.com/billing/subscriptions/usage-based-v2/use-cases/flat-fee-and-overages.md) or [credit burndown](https://docs.stripe.com/billing/subscriptions/usage-based-v2/use-cases/credit-burndown-and-top-ups.md) model. The license fee version changes whenever you update the pricing model.

Only one service interval is billed up front even when the billing interval is longer. For example, if you have a monthly service interval and quarterly billing interval, only a single service interval is billed.

> Pricing Plans are currently in [private preview](https://docs.stripe.com/release-phases.md) and could change in functionality and integration path before they’re generally available to all Stripe users. 

## Example license fee
![Example image of a license fee](https://b.stripecdn.com/docs-statics-srv/assets/pricing-plan-license-fee.29c762a84ed3477b9cf3ee3160bdb396.png)

A license fee component that’s part of a pricing plan.

## Create a license fee 

You can create license fees if you use [flat rate](https://docs.stripe.com/products-prices/pricing-models.md#flat-rate) or [per-seat](https://docs.stripe.com/products-prices/pricing-models.md#per-seat) pricing models in your pricing plan. You create license fees as components within a pricing plan.

You can’t change the service interval, currency, or tax calculation parameters after you create the license fee.

#### Dashboard

You create license fees within the pricing plan editor as part of a pricing plan.

1. On the [Pricing plans](https://dashboard.stripe.com/test/pricing-plans) page, click **Create pricing plan** (or open an existing pricing plan).
1. In the pricing plan editor:
   - Provide a display name, currency, and tax behavior for the pricing plan.
   - Click **Continue**.
1. In the pricing plan editor, click + and **License fee**.
1. In the license fee configuration:
   - Provide a display name for the licensed item.
   - Specify the servicing period.
   - Select the **Price type**: **Fixed rate**, [Volume](https://docs.stripe.com/subscriptions/pricing-models/tiered-pricing.md#volume-based-pricing), or [Graduated](https://docs.stripe.com/subscriptions/pricing-models/tiered-pricing.md#graduated-pricing). For example, `50.00 USD` per unit.
   - (Optional) Configure **Advanced settings** for your licensed item, such as specifying a **Product tax code** (learn more about [tax codes](https://docs.stripe.com/tax/tax-codes.md)), **Unit label**, **Lookup key**, and **Metadata**. You can also add metadata to the fee.
1. Click **Done**.
1. After you finish configuring the pricing plan, click **Create pricing plan**.

#### API

To [create a license fee](https://docs.stripe.com/api/v2/license-fees/create.md?api-version=preview) through the API:

```curl
curl -X POST https://api.stripe.com/v2/billing/license_fees \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "currency": "usd",
    "display_name": "Monthly fee",
    "lookup_key": "monthly_fee",
    "metadata": {
        "internal_id": "1234567890"
    },
    "tax_behavior": "exclusive",
    "licensed_item": "{{LICENSED_ITEM_ID}}",
    "service_interval": "month",
    "service_interval_count": 1,
    "unit_amount": "20.00"
  }'
```

Then, attach the license fee to a pricing plan:

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "type": "license_fee",
    "license_fee": {
        "id": "{{LICENSE_FEE_ID}}",
        "version": "{{LICENSE_FEE_VERSION}}"
    },
    "lookup_key": "monthly-fee-component",
    "metadata": {
        "existing_key": "updated_value",
        "new_key": "new value"
    }
  }'
```

When you create a billing intent, you can specify the quantity of the component in the `component_configurations` array:

```curl
curl -X POST https://api.stripe.com/v2/billing/intents \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "effective_at": "on_commit",
    "currency": "usd",
    "cadence": "{{CADENCE_ID}}",
    "actions": {
        "type": "subscribe",
        "subscribe": {
            "type": "pricing_plan_subscription_details",
            "proration_behavior": "none",
            "pricing_plan_subscription_details": {
                "pricing_plan": "{{PRICING_PLAN_ID}}",
                "pricing_plan_version": "{{PRICING_PLAN_VERSION}}",
                "component_configurations": [
                    {
                        "pricing_plan_component": "{{LICENSE_FEE_ID}}",
                        "quantity": 5
                    }
                ]
            }
        }
    }
  }'
```


# Service actions

Automate recurring, service-oriented benefits as a component of your pricing plan.

Service actions represent recurring benefits offered as part of a subscription, such as monthly credit grants. Unlike other pricing plan components (such as [rate cards](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md) and [license fees](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/license-fees/about.md)), service actions focus on delivering consistent, automated value to subscribers without direct billing.

With service actions, you can:

- Automate service actions on a specific service interval so you don’t need to manage these yourself with external tools.
- Attach service actions to pricing plans, which lets you tie subscriber benefits directly to payment status and expiration rules.
- Clearly define and manage recurring benefits as components within your offerings, which allows you to package and represent services.

> Pricing plans are currently in [private preview](https://docs.stripe.com/release-phases.md) and could change in functionality and integration path before they’re generally available to all Stripe users. 

## Example service action
![Example image of a service action](https://b.stripecdn.com/docs-statics-srv/assets/pricing-plan-service-action.75469ec59eae65dba71ad7a1f210b025.png)

A recurring credit grant created through a service action.

## Create a service action 

When you create a service action, you pass in information about the credit grant you want to create, including the service interval, when the grant is applicable, and when the grant expires. When creating a credit grant, you can configure the applicability scope to specify which [billable items](https://docs.stripe.com/api/billing/credit-grant/create.md?api-version=preview#create_billing_credit_grant-applicability_config-scope-billable_items) to apply to the credit grant. Only [metered items](https://docs.stripe.com/api/v2/metered-items.md?api-version=preview) are supported ([licensed items](https://docs.stripe.com/api/v2/licensed-items.md?api-version=preview) aren’t). The credit grant is drawn down by metered items on your invoices. You create service actions as components within a pricing plan.

#### Dashboard

You create service actions within the pricing plan editor as part of a pricing plan.

1. On the [Pricing plans](https://dashboard.stripe.com/test/pricing-plans) page, click **Create pricing plan** (or open an existing pricing plan).
1. In the pricing plan editor:
   - Provide a display name, currency, and tax behavior for the pricing plan.
   - Click **Continue**.
1. In the pricing plan editor, click + and **Credit grant**.
1. In the recurring credit grant configuration:
   - Provide a display name for the credit grant.
   - Specify the servicing period.
   - Provide a credit amount.
   - (Optional) Configure **Advanced settings** for your recurring credit grant, such as specifying an **Application** or **Lookup key**.
1. Click **Done**.
1. After you finish configuring the pricing plan, click **Create pricing plan**.

#### API

To [create a service action](https://docs.stripe.com/api/v2/service-actions/create.md?api-version=preview) through the API:

```curl
curl -X POST https://api.stripe.com/v2/billing/service_actions \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "type": "credit_grant",
    "lookup_key": "monthly_grant_1",
    "service_interval": "month",
    "service_interval_count": 1,
    "credit_grant": {
        "name": "Monthly grant 1",
        "expiry_config": {
            "type": "end_of_service_period"
        },
        "amount": {
            "type": "monetary",
            "monetary": {
                "currency": "usd",
                "value": 10000
            }
        },
        "applicability_config": {
            "scope": {
                "billable_items": [
                    "{{BILLABLE_ITEM_ID}}",
                    "{{BILLABLE_ITEM_ID_2}}"
                ]
            }
        }
    }
  }'
```

Then attach the service action to your pricing plan:

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "type": "service_action",
    "service_action": {
        "id": "{{SERVICE_ACTION_ID}}",
        "version": "{{SERVICE_ACTION_VERSION}}"
    },
    "lookup_key": "credit-grant-28",
    "metadata": {
        "existing_key": "updated_value",
        "new_key": "new value"
    }
  }'
```



# Record usage for billing

Learn how to record customer usage data.

Throughout each billing interval, you can record usage in Stripe to reflect your customers usage of your platform. You can record usage in Stripe using the Dashboard or API.

To begin, first create and configure your meter, then add the recorded usage through the Stripe Dashboard or API.

Stripe processes meter events asynchronously, so aggregated usage in meter event summaries and on upcoming invoices might not immediately reflect recently received meter events.

## Create a meter

Meters specify how to aggregate meter events over a billing interval. Meter events represent all actions that customers take in your system (for example, API requests). Meters are attached to one or more metered items which form the basis of what’s billed.

For the Hypernian example, meter events are the number of tokens a customer uses in a query. The meter is the sum of tokens over a month.

You can use the Stripe Dashboard or API to [configure a meter](https://docs.stripe.com/billing/subscriptions/usage-based/meters/configure.md). To use the API with the Stripe CLI to create a meter, [get started with the Stripe CLI](https://docs.stripe.com/stripe-cli.md).

#### Dashboard

1. On the [Meters](https://dashboard.stripe.com/test/meters) page, click **Create meter**.
1. On the **Create meter** page, do the following:
   - For **Meter name**, enter the name of the meter to display and for organization purposes. For the Hypernian example, enter “Hypernian tokens.”
   - For **Event name**, enter the name to display in meter events when reporting usage to Stripe. For the Hypernian example, enter “hypernian_tokens.”
   - Set the approproriate **Aggregation method** in the dropdown:
     - For the Hypernian example, select **Sum**. This will *sum the values* reported (in this example, number of tokens a customer uses) to determine the usage to bill for.
     - Choose **Count** to bill based on the *number* of events reported.
     - Choose **Last** to bill based on the *last value* reported.
     - Use the preview pane to set example usage events and verify the aggregation method.
   - Click **Create meter**.
   - (Optional) Under **Advanced settings**, specify **Dimensions**, or keys, that you want to tag your usage data with. To generate granular segment specific alerts, or to granularly price usage based on a combination of attributes, submit your usage data with dimensions that are populated for analytics and reporting. Some example dimensions are region and event type.

#### API

```curl
curl https://api.stripe.com/v1/billing/meters \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d display_name="Hypernian tokens" \
  -d event_name=hypernian_tokens \
  -d "default_aggregation[formula]"=sum \
  -d "customer_mapping[event_payload_key]"={{STRIPE_CUSTOMER_ID}} \
  -d "customer_mapping[type]"=by_id \
  -d "value_settings[event_payload_key]"=value \
  -d "dimension_payload_keys[0]"=model \
  -d "dimension_payload_keys[1]"=token_type
```

```cli
stripe billing meters create  \
  --display-name="Hypernian tokens" \
  --event-name=hypernian_tokens \
  -d "default_aggregation[formula]"=sum \
  -d "customer_mapping[event_payload_key]"={{STRIPE_CUSTOMER_ID}} \
  -d "customer_mapping[type]"=by_id \
  -d "value_settings[event_payload_key]"=value \
  -d "dimension_payload_keys[0]"=model \
  -d "dimension_payload_keys[1]"=token_type
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

meter = client.v1.billing.meters.create({
  display_name: 'Hypernian tokens',
  event_name: 'hypernian_tokens',
  default_aggregation: {formula: 'sum'},
  customer_mapping: {
    event_payload_key: '{{STRIPE_CUSTOMER_ID}}',
    type: 'by_id',
  },
  value_settings: {event_payload_key: 'value'},
  dimension_payload_keys: {
    :'0' => 'model',
    :'1' => 'token_type',
  },
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
meter = client.v1.billing.meters.create({
  "display_name": "Hypernian tokens",
  "event_name": "hypernian_tokens",
  "default_aggregation": {"formula": "sum"},
  "customer_mapping": {"event_payload_key": "{{STRIPE_CUSTOMER_ID}}", "type": "by_id"},
  "value_settings": {"event_payload_key": "value"},
  "dimension_payload_keys": {"0": "model", "1": "token_type"},
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$meter = $stripe->billing->meters->create([
  'display_name' => 'Hypernian tokens',
  'event_name' => 'hypernian_tokens',
  'default_aggregation' => ['formula' => 'sum'],
  'customer_mapping' => [
    'event_payload_key' => '{{STRIPE_CUSTOMER_ID}}',
    'type' => 'by_id',
  ],
  'value_settings' => ['event_payload_key' => 'value'],
  'dimension_payload_keys' => [
    '0' => 'model',
    '1' => 'token_type',
  ],
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

MeterCreateParams params =
  MeterCreateParams.builder()
    .setDisplayName("Hypernian tokens")
    .setEventName("hypernian_tokens")
    .setDefaultAggregation(
      MeterCreateParams.DefaultAggregation.builder()
        .setFormula(MeterCreateParams.DefaultAggregation.Formula.SUM)
        .build()
    )
    .setCustomerMapping(
      MeterCreateParams.CustomerMapping.builder()
        .setEventPayloadKey("{{STRIPE_CUSTOMER_ID}}")
        .setType(MeterCreateParams.CustomerMapping.Type.BY_ID)
        .build()
    )
    .setValueSettings(
      MeterCreateParams.ValueSettings.builder().setEventPayloadKey("value").build()
    )
    .putExtraParam("dimension_payload_keys[0]", "model")
    .putExtraParam("dimension_payload_keys[1]", "token_type")
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
Meter meter = client.v1().billing().meters().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const meter = await stripe.billing.meters.create({
  display_name: 'Hypernian tokens',
  event_name: 'hypernian_tokens',
  default_aggregation: {
    formula: 'sum',
  },
  customer_mapping: {
    event_payload_key: '{{STRIPE_CUSTOMER_ID}}',
    type: 'by_id',
  },
  value_settings: {
    event_payload_key: 'value',
  },
  dimension_payload_keys: {
    '0': 'model',
    '1': 'token_type',
  },
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.BillingMeterCreateParams{
  DisplayName: stripe.String("Hypernian tokens"),
  EventName: stripe.String("hypernian_tokens"),
  DefaultAggregation: &stripe.BillingMeterCreateDefaultAggregationParams{
    Formula: stripe.String(stripe.BillingMeterDefaultAggregationFormulaSum),
  },
  CustomerMapping: &stripe.BillingMeterCreateCustomerMappingParams{
    EventPayloadKey: stripe.String("{{STRIPE_CUSTOMER_ID}}"),
    Type: stripe.String("by_id"),
  },
  ValueSettings: &stripe.BillingMeterCreateValueSettingsParams{
    EventPayloadKey: stripe.String("value"),
  },
}
params.AddExtra("dimension_payload_keys[0]", "model")
params.AddExtra("dimension_payload_keys[1]", "token_type")
result, err := sc.V1BillingMeters.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.Billing.MeterCreateOptions
{
    DisplayName = "Hypernian tokens",
    EventName = "hypernian_tokens",
    DefaultAggregation = new Stripe.Billing.MeterDefaultAggregationOptions
    {
        Formula = "sum",
    },
    CustomerMapping = new Stripe.Billing.MeterCustomerMappingOptions
    {
        EventPayloadKey = "{{STRIPE_CUSTOMER_ID}}",
        Type = "by_id",
    },
    ValueSettings = new Stripe.Billing.MeterValueSettingsOptions
    {
        EventPayloadKey = "value",
    },
};
options.AddExtraParam("dimension_payload_keys[0]", "model");
options.AddExtraParam("dimension_payload_keys[1]", "token_type");
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Billing.Meters;
Stripe.Billing.Meter meter = service.Create(options);
```

After you configure the meter, you can’t make any changes aside from the display name.

### Meter configuration attributes

| Meter attribute | Description                                                                                                                                                                                                                                                                                                                                                           |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Event name      | The name of the meter event that you want to record usage for with the meter. When you send usage to Stripe, specify this event name in the `event_name` field for the [Meter Event](https://docs.stripe.com/api/billing/meter-event/object.md). This allows the correct meter to record and aggregate the usage. You can only use an event name with a single meter. |
| Event ingestion | Specify how to send events to Stripe:                                                                                                                                                                                                                                                                                                                                 |

  - **Raw**: Handle all meter events as standalone events. Multiple events sent for the same timestamp don’t overwrite each other. The aggregation includes the multiple events. This is the default option if you don’t specify anything.
  - **Pre-aggregated**: If you send events for a specific time interval (hourly or daily), Stripe only uses the most recently received meter event in that time interval. A newer event sent within the same hourly or daily window overwrites the previous one. The meter event timestamp in UTC dictates the hour and day boundaries. |
| Aggregation formula   | Specify how to aggregate usage over the billing interval:

  - **Sum**: Bill customers based on the sum of all usage values for the billing interval.
  - **Count**: Bill customers based on the count of all usage for the billing interval.
  - **Last**: Bill customers based on the most recent usage event’s value for the billing interval.                                                                                                                                                                                                                                                                         |
| Payload key overrides | Specify which keys in the event payload refer to the customer and numerical usage values:

  - **value\_settings**: Use this parameter to define the key in the event payload that refers to the numerical usage value. The default key is `value`, but you can specify a different key, such as tokens.
  - **customer\_mapping**: Use this parameter to define the key in the event payload that refers to the [Customer ID](https://docs.stripe.com/api/customers/object.md#customer_object-id). The default key is `stripe_customer_id`, but you can specify a different key, such as `customer_id`.                  |
| Dimension             | A single key, such as `[request_type]`. Dimensions allow you to configure your meter to accept segmented usage data. You can include 2 dimensions on your meter. If you need to include more dimensions, contact our [support team](https://support.stripe.com/contact/login).                                                                                                                                                                                                                                                                                                                                            |
| Segment               | A full set of keys and values, such as `[{dimension: 'request_type', value: 'POST'}, {dimension: 'status_code', value: '200'}]`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Sub segment           | A single key/value pair, such as `[{dimension: 'request_type', value: 'POST'}]`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

## Record usage with the Dashboard, API, or S3

You can record usage in Stripe to reflect customer usage on your platform.

#### Dashboard

To record usage, you can manually add usage data or upload a CSV file with the usage data in the Dashboard. Stripe parses, validates, and transforms the usage data into meter events.

After the events upload successfully, you can see them in the live meter feed. You can also check the status of your uploaded files on the [Data management](https://dashboard.stripe.com/data-management/import-set) page.

### Add usage data manually 

To manually add usage data:

1. On the [Meters](https://dashboard.stripe.com/test/meters) page, select the meter name.
1. On the meter page, click **Add usage** > **Manually input usage**.
1. On the **Add usage** page, do the following:
   - Select your customer from the **Customer** dropdown.
   - For **Value**, enter a sample value.
   - Click **Submit**.

### Upload a CSV file with usage data 

After you prepare your CSV file with the usage data, you can upload it in the Stripe Dashboard. Make sure to format your file to match the template that’s available in the Dashboard. The maximum file size allowed is 5 MB.

#### CSV file format and fields 

Make sure your CSV file follows this sample file format:

| `timestamp` | `event_name`  | `payload_stripe_customer_id` | `payload_value` |
| ----------- | ------------- | ---------------------------- | --------------- |
| 2024-09-25  | ai_search_api | cus_QMJJtcu70R1x46           | 400             |
| 2024-09-26  | ai_search_api | cus_GAXJtSu6021a6s           | 600             |
| 2024-09-27  | cpu_usage     | cus_Qz0fwcfSysB9Z3           | 600             |

Follow the [Meter Event](https://docs.stripe.com/api/billing/meter-event/object.md) schema when including the following fields in your file:

| Field       | Description                                                                   |
| ----------- | ----------------------------------------------------------------------------- |
| `timestamp` | The date that the event occurred. We support the following timestamp formats: |

  - `yyyy-MM-dd` – For example, `2024-09-23`.
  - `yyyy-MM-dd'T'HH:mm:ssZ` – For example, `2024-09-23T16:22:25+0530`.
  - `Epoch` – For example, `1727108545`.                                                                         |
| `event_name`                 | The name of the meter event.                                                                                                                                                                                                                                                                                          |
| `payload_stripe_customer_id` | The [Customer ID](https://docs.stripe.com/api/customers/object.md#customer_object-id) that the event gets created against. You can obtain the `customer_id` details on the [Customers](https://dashboard.stripe.com/customers) page.                                                                                  |
| `payload_value`              | The numerical usage value of the meter event, such as the number of hours to invoice for. If you specified a different key in the `value_settings`, you must update the column name to match the key value. For example, if you specify `tokens` in the `value_settings`, update the column name to `payload_tokens`. |

#### Upload your CSV file

If your file contains errors, you can download an error file that includes the reason for each failed record. After you fix the errors, you can upload the updated file.

1. On the [Meters](https://dashboard.stripe.com/meters) page, select the meter name that you want to add usage events to.
1. On the meter page, click **Add usage** > **Upload file to add usage**.
1. On the **Upload file to add usage** page, select your file.
1. Click **Upload file**.
1. Verify the meter event count and aggregated value on the meter page.

#### API

To record usage using the API, first [configure your meter](https://docs.stripe.com/billing/subscriptions/usage-based-v2/record-usage.md?#meter-configuration-attributes), and then send meter events that include the event name configured on the meter, customer ID, numerical value, and a timestamp (optional).

You can decide how often you record usage in Stripe, for example as it occurs or in batches. Stripe processes meter events asynchronously, so aggregated usage in meter event summaries and on upcoming invoices might not immediately reflect recently received meter events.

### Create meter events 

Create a [Meter Event](https://docs.stripe.com/api/billing/meter-event/create.md) using the API.

```curl
curl https://api.stripe.com/v1/billing/meter_events \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d event_name=hypernian_tokens \
  -d "payload[value]"=25 \
  -d "payload[stripe_customer_id]"={{CUSTOMER_ID}} \
  -d "payload[dimension_1]"=value_1 \
  -d "payload[dimension_2]"=value_2
```

```cli
stripe billing meter_events create  \
  --event-name=hypernian_tokens \
  -d "payload[value]"=25 \
  -d "payload[stripe_customer_id]"={{CUSTOMER_ID}} \
  -d "payload[dimension_1]"=value_1 \
  -d "payload[dimension_2]"=value_2
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

meter_event = client.v1.billing.meter_events.create({
  event_name: 'hypernian_tokens',
  payload: {
    value: '25',
    stripe_customer_id: '{{CUSTOMER_ID}}',
    dimension_1: 'value_1',
    dimension_2: 'value_2',
  },
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
meter_event = client.v1.billing.meter_events.create({
  "event_name": "hypernian_tokens",
  "payload": {
    "value": "25",
    "stripe_customer_id": "{{CUSTOMER_ID}}",
    "dimension_1": "value_1",
    "dimension_2": "value_2",
  },
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$meterEvent = $stripe->billing->meterEvents->create([
  'event_name' => 'hypernian_tokens',
  'payload' => [
    'value' => '25',
    'stripe_customer_id' => '{{CUSTOMER_ID}}',
    'dimension_1' => 'value_1',
    'dimension_2' => 'value_2',
  ],
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

MeterEventCreateParams params =
  MeterEventCreateParams.builder()
    .setEventName("hypernian_tokens")
    .putPayload("value", "25")
    .putPayload("stripe_customer_id", "{{CUSTOMER_ID}}")
    .putPayload("dimension_1", "value_1")
    .putPayload("dimension_2", "value_2")
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
MeterEvent meterEvent = client.v1().billing().meterEvents().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const meterEvent = await stripe.billing.meterEvents.create({
  event_name: 'hypernian_tokens',
  payload: {
    value: '25',
    stripe_customer_id: '{{CUSTOMER_ID}}',
    dimension_1: 'value_1',
    dimension_2: 'value_2',
  },
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.BillingMeterEventCreateParams{
  EventName: stripe.String("hypernian_tokens"),
  Payload: map[string]string{
    "value": "25",
    "stripe_customer_id": "{{CUSTOMER_ID}}",
    "dimension_1": "value_1",
    "dimension_2": "value_2",
  },
}
result, err := sc.V1BillingMeterEvents.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.Billing.MeterEventCreateOptions
{
    EventName = "hypernian_tokens",
    Payload = new Dictionary<string, string>
    {
        { "value", "25" },
        { "stripe_customer_id", "{{CUSTOMER_ID}}" },
        { "dimension_1", "value_1" },
        { "dimension_2", "value_2" },
    },
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Billing.MeterEvents;
Stripe.Billing.MeterEvent meterEvent = service.Create(options);
```

#### Idempotency

Use [idempotency keys](https://docs.stripe.com/api/idempotent_requests.md) to prevent reporting usage for each event more than one time because of latency or other issues. Every meter event corresponds to an [identifier](https://docs.stripe.com/api/billing/meter-event/create.md#create_billing_meter_event-identifier) that you can specify in your request. If you don’t specify an identifier, we auto-generate one for you.

#### Event timestamps

Make sure the timestamp is within the past 35 calendar days and isn’t more than 5 minutes in the future. The 5-minute window is for clock drift between your server and Stripe systems.

#### Usage values

The numerical usage value in the payload only accepts whole number values. If the overall cycle usage is negative, Stripe reports the invoice line item usage quantity as 0.

#### Dimensions

Key-value pairs that you can add to enrich your meter event. You can enrich your usage events with up to three dimensions.

#### Rate limits

The [Meter Event](https://docs.stripe.com/api/billing/meter-event/create.md) endpoint allows 1000 calls per second in live mode, and one concurrent call per customer per meter. If your service might exceed this limit, you can “bundle” your product into amounts. For example, if you charge per 1000 requests, you can bundle your product into “per 1000 transactions” and then send 1 usage record every 1000 times.

In sandbox mode, calls to the `meter event` and `meter event stream` endpoint count toward the [basic limit](https://docs.stripe.com/rate-limits.md#rate-limiter).

> If you’re a Connect platform making requests on behalf of a connected account using the `Stripe-Account` header, you’re subject to [regular Stripe rate limits](https://docs.stripe.com/rate-limits.md), which is 100 operations per second.

You can monitor for `429` status codes and implement a retry mechanism with an exponential back-off schedule to manage request volume.

### High-throughput ingestion with higher rate limits (API v2)

With the [API v2](https://docs.stripe.com/api-v2-overview.md), you can send up to 10,000 events per second to Stripe using meter event streams. This works in live mode only.

[Contact sales](https://stripe.com/contact/sales) if you need to send up to 100,000 events per second.

This endpoint uses stateless authentication sessions. First, create a [Meter Event Session](https://docs.stripe.com/api/v2/billing/meter-event-stream/session/create.md?api-version=preview) to receive an authentication token. Authentication tokens are only valid for 15 minutes, so you must create a new meter event session when your token expires.

Next, use the returned authentication token to create your high-throughput meter events with the [Meter Event Stream](https://docs.stripe.com/api/v2/billing/meter-event-stream/create.md?api-version=preview).

> Because of the large volume of API requests, we don’t include meter event stream requests in the [Workbench Logs tab](https://docs.stripe.com/workbench/overview.md#request-logs).

You can monitor for `429` status codes and implement a retry mechanism with an exponential backoff schedule to manage request volume.

### Handle meter event errors 

Stripe asynchronously processes meter events. If we find an error, we create one of the following [Events](https://docs.stripe.com/api/events.md):

| Event                                     | Description                                                            | Payload type |
| ----------------------------------------- | ---------------------------------------------------------------------- | ------------ |
| `v1.billing.meter.error_report_triggered` | This event occurs when a meter has invalid usage events.               | `thin`       |
| `v1.billing.meter.no_meter_found`         | This event occurs when usage events have missing or invalid meter IDs. | `thin`       |

1. Correct and resend invalid events for re-processing.

#### S3

To record usage using Amazon S3, send meter usage events to Stripe from your Amazon S3 storage bucket. Stripe parses, validates, and transforms the usage data into meter events.

After the events upload successfully, you can see them on your subscription invoice.

## Before you begin

Make sure you have the following:

- Admin account access to the [Stripe Dashboard](https://dashboard.stripe.com/dashboard)
- AWS account access to the [AWS Management Console](https://console.aws.amazon.com/) and your S3 bucket

### Upload meter usage events

You can upload your meter usage events as a CSV, JSON, or JSON Lines file.

> #### Need support for a different file format?
> 
> If you want to upload files with a different structure or in a custom format, [contact us](mailto:user-data-acquisition-platform@stripe.com).

#### File format and fields

Make sure your file follows the sample file format:

#### CSV
![Example of the CSV file format](https://b.stripecdn.com/docs-statics-srv/assets/udap_ubb_csv_format.e5c12ef6a48b407ae9c0cf6c3b873aeb.png)

CSV file format

To include dimensions in your CSV file, add them as additional columns using the format `payload_{dimension_key}` and enter the dimension value in the corresponding row cell. Dimensions are optional.

| Dimension    | Example value  |
| ------------ | -------------- |
| `timestamp`  | `event_name`   | `payload_stripe_customer_id` | `payload_value` | `payload_{dimension_key}` |
| `2025-10-16` | `event_name_1` | `cus_123`                    | `31`            | `value_1`                 |

#### JSON

```json
[
  {
    "identifier": "26ac9e54-6a13-4b2e-90b0-fedae80bb8f7",
    "timestamp": 1692852080,
    "event_name": "ai_search_api",
    "payload": {
      "value": 200,
      "stripe_customer_id": "cus_123"
    }
  },
  {
    "timestamp": 1692852080,
    "event_name": "ai_search_api",
    "payload": {
      "value": 500,
      "stripe_customer_id": "cus_123",
      "dimension_key": "value"
    }
  }
]
```

To include dimensions in your JSON file, add them as keys directly under the `payload` object (no prefix needed). Dimensions are optional.

#### JSON Lines

```jsonline
{"identifier":"123456","timestamp":1692852080,"event_name":"ai_search_api","payload":{"value":200,"stripe_customer_id":"cus_123","dimension_key":"value"}}
{"timestamp":1692852080,"event_name":"ai_search_api","payload":{"value":500,"stripe_customer_id":"cus_123"}}
```

To include dimensions in your JSON Lines file, add them as keys directly under the `payload` object (no prefix needed). Dimensions are optional.

Follow the [Meter Event](https://docs.stripe.com/api/billing/meter-event/object.md) schema when including the following fields in your file:

| Field             | Description                                                                                                                                              |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `identifier`      | A unique identifier for the event. If you don’t provide one, Stripe can generate the unique identifier. We recommend using a globally unique identifier. |
| `timestamp`       | The time that the event occurred, measured in seconds since the Unix epoch.                                                                              |
| `event_name`      | The name of the meter event.                                                                                                                             |
| `payload_columns` | The set of columns that contain key names for customer and numerical usage values:                                                                       |

  - `payload_stripe_customer_id`: The [Customer ID](https://docs.stripe.com/api/customers/object.md#customer_object-id) that the event gets created against.
  - `payload_value`: The numerical usage value of the meter event. By default, the column name is `payload_value`. If you specified a different field name when creating the meter event, you must update the column name to match the key value. For example, if you specify tokens in the `value_settings`, update the column name to `payload_tokens`. |

### Prepare your files in Amazon S3

You can validate your connection configuration using well-formatted data in your S3 bucket. The configuration process shows the available files, and runs an initial sync when configuring the connection.

1. Go to your [Amazon S3 console](https://s3.console.aws.amazon.com/).

1. Make sure to store your files in a designated S3 bucket that’s organized according to your import preferences. If needed, follow the [AWS guidelines](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html) to create an S3 bucket.

   For successful retrieval, Stripe requires that file names adhere to [S3 object naming conventions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html) and files are 1 GB maximum.

1. Remember the bucket name and region because you need them for future steps.

1. Keep your [AWS Management Console](https://console.aws.amazon.com) open to configure an IAM role later.

### Configure the Amazon S3 Connector to import files

First, use the Stripe Dashboard to add the Amazon S3 Connector.

1. In the Stripe Dashboard, on the **Data management** > [Connectors](https://dashboard.stripe.com/data-management/connectors) tab, click **Add connector**.
1. In the **Choose connector** dialog, select **Amazon S3**.
1. In the **Requirements** dialog, enter a unique name for **Connector name**, then click **Next**.
1. Complete the steps in the **Permissions** dialog.

Next, configure the appropriate permissions for the Amazon S3 Connector.

1. In the AWS Management Console, go to the [IAM console](https://console.aws.amazon.com/iam/).
1. Create a custom trust policy:
   - In the navigation pane, click **Policies** > **Create policy**.
   - Select **JSON**, and replace the existing policy text by copying and pasting the code block provided in the Stripe Dashboard.
   - In the `Resource` section of the **Policy editor** code block, replace `USER_TARGET_BUCKET` with your intended bucket name.
   - Click **Next**.
   - Under **Policy details**, add a policy name. Optionally add any tags.
   - Click **Create policy**.
1. Create a role:
   - In the navigation pane, click **Roles** > **Create role**.
   - Select **Custom trust policy**, and copy and paste the code block provided in the Stripe Dashboard.
   - Click **Next**.
   - Locate and select the newly created permission policy to enable it, then click **Next**.
   - Copy and paste the provided role name, then click **Create role** to create a role name.

Then, make sure to establish a connection between Stripe and your Amazon S3 bucket.

1. In the AWS Management Console, do the following:
   - Provide your [AWS account ID](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-identifiers.html#FindAccountId).
   - Provide the Bucket Name and Region.
   - If you use folders to organize your files in your Amazon S3 bucket, specify a folder within the above bucket. We only fetch data from the specified folder, not the entire bucket.
1. After you set up a connector, the file preview validates that your credentials connect Stripe with the expected Amazon S3 bucket and folder. Stripe fetches all data modified in the last 90 days. This occurs every 5 minutes for objects with a `LastModified` date later than the last sync.
1. Preview the files available in the connected Amazon S3 bucket:
   - File names must be under 255 characters and include the appropriate extension, such as `.csv`, `.json`, or `.jsonl`.
   - Initial and recurring imports have an expected file format:
     - JSON files have **Billing Meter Event Transaction Template - JSON**.
     - JSON Lines files have **Billing Meter Event Transaction Template - JSONLINE**.
     - CSV files have **Billing Meter Event Transaction Template - CSV**.
1. To create an active data connection and initiate the data import, click **Done**.

After you upload a file to the Amazon S3 Connector, the usage events update within 5 minutes. This might take longer if your bucket contains a lot of unprocessed files.

You can check the status and details of processed files on the [Import set](https://dashboard.stripe.com/data-management/import-set) tab in the Stripe Dashboard.

### Rate limits

You can upload any number of files and records to your Amazon S3 bucket. Upload a file every 10 seconds or when the current file reaches one million records, whichever comes first. After upload, you can add events in a new file.

Avoid creating empty files, such as:

- CSV files that contain only the header row
- JSON files that contain only [] (empty square brackets)
- JSON Lines files that contain only {} (empty curly brackets)

Although Amazon S3 accepts non-zero byte files, they increase the object and file count, which might cause delays in the polling of files.

[Contact sales](https://stripe.com/contact/sales) if you need to process 100,000 events per second.

Amazon S3 polls a maximum of 50 files or up to 10 GB of data, and processes your uploaded data at a rate of 10,000 events per second. If you upload large files or a high volume of files, Stripe polls and processes the data to maintain this throughput rate.

For example, if you upload 100 files that each contain 100,000 records daily, it can take approximately 17 minutes to process the entire dataset (10 million events).

### Report and handle errors 

Stripe polls the files that you upload to the Amazon S3 bucket and then processes these files asynchronously. If we detect errors during processing, Stripe notifies you using [events](https://dashboard.stripe.com/events).

#### Format issues

Invalid file or record format errors occur when the contents in the uploaded file contain formatting or data issues.

You can subscribe to these events using a [webhook endpoint](https://dashboard.stripe.com/webhooks). Based on the event type, you can implement your own logic to handle these errors.

| Event                                  | Description                                                                                                                                                                                                                                                                                                                                                                           | Payload type |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| `data_management.import_set.failed`    | Stripe creates a [data_management.import_set.failed](https://docs.stripe.com/api/events/types.md#event_types-data_management.import_set.failed) event when processing fails for an entire file. For example, if you omit a mandatory column, such as `event_name`. You can find the reason for failure in the `failed_reason` parameter of the event, and fix it before re-uploading. | `Snapshot`   |
| `data_management.import_set.succeeded` | Stripe creates a [data_management.import_set.succeeded](https://docs.stripe.com/api/events/types.md#event_types-data_management.import_set.succeeded) event when individual records fail in a partially processed file. For example, if you omit a value for a mandatory field, such as `stripe_customer_id` or `event_name`.                                                         |

  You can find details of the failed records in the `status` parameter of the event. A `succeeded_with_errors` status indicates that at least one record failed because of invalid formatting. The `result.errors` gives the number of records that failed and the `file_id` of the file containing the failed records.

  Use the [Files](https://docs.stripe.com/file-upload.md#download-file-contents) API to download a complete list of the failed records and detailed error descriptions. | `Snapshot`   |

#### Data issues

Files with correct formatting can fail processing because of invalid data within the file, such as incorrect values for the `event_name` or `stripe_customer_id`.

For detailed information about these failures, you can subscribe to the following events using a [webhook endpoint](https://dashboard.stripe.com/webhooks).

| Event                                     | Description                                                            | Payload type |
| ----------------------------------------- | ---------------------------------------------------------------------- | ------------ |
| `v1.billing.meter.error_report_triggered` | This event occurs when a meter has invalid usage events.               | `thin`       |
| `v1.billing.meter.no_meter_found`         | This event occurs when usage events have missing or invalid meter IDs. | `thin`       |

#### Error codes

The `reason.error_types.code` provides the error categorization that triggered the error. Possible error codes include:

- `meter_event_customer_not_found`
- `meter_event_no_customer_defined`
- `meter_event_dimension_count_too_high`
- `archived_meter`
- `timestamp_too_far_in_past`
- `timestamp_in_future`
- `meter_event_value_not_found`
- `meter_event_invalid_value`
- `no_meter` (supported only for the `v1.billing.meter.no_meter_found` event type)

1. Correct the invalid events and save them to a new file. Then, upload the file to your Amazon S3 bucket for processing.

## Fix incorrect usage data 

If you identify incorrectly recorded events in the current billing interval, you can create a [Meter Event Adjustment](https://docs.stripe.com/api/billing/meter-event-adjustment/create.md) to cancel those events. You must specify the [identifier](https://docs.stripe.com/api/billing/meter-event/object.md#billing_meter_event_object-identifier) for the meter event.

You can only cancel events sent to Stripe within the last 24 hours. If you cancel usage that’s included on a finalized invoice, we won’t update the invoice or issue a corrected invoice for the canceled usage. We don’t support billing adjustments for canceled usage on a finalized invoice sent to a customer.

You can also fix incorrectly recorded usage data by recording negative quantities. If the overall cycle usage is negative, Stripe reports the invoice line item usage quantity as 0.

```curl
curl https://api.stripe.com/v1/billing/meter_event_adjustments \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d type=cancel \
  -d event_name=hypernian_tokens \
  -d "cancel[identifier]"={{METER_EVENT_IDENTIFIER}}
```

```cli
stripe billing meter_event_adjustments create  \
  --type=cancel \
  --event-name=hypernian_tokens \
  -d "cancel[identifier]"={{METER_EVENT_IDENTIFIER}}
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

meter_event_adjustment = client.v1.billing.meter_event_adjustments.create({
  type: 'cancel',
  event_name: 'hypernian_tokens',
  cancel: {identifier: '{{METER_EVENT_IDENTIFIER}}'},
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
meter_event_adjustment = client.v1.billing.meter_event_adjustments.create({
  "type": "cancel",
  "event_name": "hypernian_tokens",
  "cancel": {"identifier": "{{METER_EVENT_IDENTIFIER}}"},
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$meterEventAdjustment = $stripe->billing->meterEventAdjustments->create([
  'type' => 'cancel',
  'event_name' => 'hypernian_tokens',
  'cancel' => ['identifier' => '{{METER_EVENT_IDENTIFIER}}'],
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

MeterEventAdjustmentCreateParams params =
  MeterEventAdjustmentCreateParams.builder()
    .setType(MeterEventAdjustmentCreateParams.Type.CANCEL)
    .setEventName("hypernian_tokens")
    .setCancel(
      MeterEventAdjustmentCreateParams.Cancel.builder()
        .setIdentifier("{{METER_EVENT_IDENTIFIER}}")
        .build()
    )
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
MeterEventAdjustment meterEventAdjustment =
  client.v1().billing().meterEventAdjustments().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const meterEventAdjustment = await stripe.billing.meterEventAdjustments.create({
  type: 'cancel',
  event_name: 'hypernian_tokens',
  cancel: {
    identifier: '{{METER_EVENT_IDENTIFIER}}',
  },
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.BillingMeterEventAdjustmentCreateParams{
  Type: stripe.String("cancel"),
  EventName: stripe.String("hypernian_tokens"),
  Cancel: &stripe.BillingMeterEventAdjustmentCreateCancelParams{
    Identifier: stripe.String("{{METER_EVENT_IDENTIFIER}}"),
  },
}
result, err := sc.V1BillingMeterEventAdjustments.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.Billing.MeterEventAdjustmentCreateOptions
{
    Type = "cancel",
    EventName = "hypernian_tokens",
    Cancel = new Stripe.Billing.MeterEventAdjustmentCancelOptions
    {
        Identifier = "{{METER_EVENT_IDENTIFIER}}",
    },
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Billing.MeterEventAdjustments;
Stripe.Billing.MeterEventAdjustment meterEventAdjustment = service.Create(options);
```


# Manage pricing plan subscriptions

Update, modify, and cancel pricing plan subscriptions and components.

With pricing plan subscriptions, you can introduce new services to all subscribers and set up pricing versions by user cohort, in addition to other subscription management tasks, like migrating users and canceling subscriptions.

> Pricing plans are currently in [private preview](https://docs.stripe.com/release-phases.md) and could change in functionality and integration path before they’re generally available to all Stripe users. 

## Manage pricing plan components 

With pricing plan [versions](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#pricing-plan-versioning), you can:

- Update your pricing plan by adding a new component and creating a new version.
- Set the latest version as the live version for new subscriptions.
- Update existing pricing plan subscriptions to use the new version.

### Update your pricing plan

To update a pricing plan, you can add a new component or remove an existing component and replace it with a new component. Each change creates a new version, which is tracked as the [latest_version](https://docs.stripe.com/api/v2/pricing-plans/pricing-plan/object.md?api-version=preview#v2_pricing_plan_object-latest_version), while preserving older versions for existing subscriptions or reference.

For example, you can add a license fee to an existing pricing plan that has a rate card component. First, create the license fee:

```curl
curl -X POST https://api.stripe.com/v2/billing/license_fees \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "currency": "usd",
    "display_name": "Monthly fee",
    "lookup_key": "monthly_fee",
    "metadata": {
        "internal_id": "1234567890"
    },
    "tax_behavior": "exclusive",
    "licensed_item": "{{LICENSED_ITEM_ID}}",
    "service_interval": "month",
    "service_interval_count": 1,
    "unit_amount": "20.00"
  }'
```

Then, attach the license fee to the pricing plan:

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "type": "license_fee_component",
    "license_fee_component": {
        "license_fee": "{{LICENSE_FEE_ID}}",
        "version": "{{LICENSE_FEE_VERSION}}"
    }
  }'
```

The response shows the new component and increments the pricing plan’s version:

```json
{
  "id": "{{PRICING_PLAN_COMPONENT_ID}}",
  "object": "v2.billing.pricing_plan_component",
  "created": "2025-06-20T16:30:00.000Z",
  "type": "license_fee_component",
  "pricing_plan": "{{PRICING_PLAN_ID}}",
  "pricing_plan_version": "{{PRICING_PLAN_VERSION}}",
  "license_fee_component": {
    "license_fee": "{{LICENSE_FEE_ID}}",
    "version": "{{NEW_LICENSE_FEE_VERSION}}"
  }
}
```

### Replace a component

To replace a component, you must remove the existing component before you can add a new one.

First, retrieve the components to find a given component’s ID.

```curl
curl https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview"
```

Then, delete the component.

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}}/components/{{COMPONENT_ID}} \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview"
```

### Set the live version

By default, new pricing plan versions don’t affect new subscriptions unless you update the [live_version](https://docs.stripe.com/api/v2/pricing-plans/pricing-plan/object.md?api-version=preview#v2_pricing_plan_object-live_version). To make the latest version (for example, v3) the default for new subscriptions, set it as the live version. If you don’t specify a version, the live version is used by default.

```curl
curl -X POST https://api.stripe.com/v2/billing/pricing_plans/{{PRICING_PLAN_ID}} \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "live_version": "latest"
  }'
```

The response reflects the update:

```json
{
  "id": "{{PRICING_PLAN_ID}}",
  "object": "v2.billing.pricing_plan",
  "active": true,
  "created": "2025-06-14T21:52:04.000Z",
  "currency": "usd",
  "display_name": "USD pro plan",
  "latest_version": "{{PRICING_PLAN_VERSION_3}}",
  "live_version": "{{PRICING_PLAN_VERSION_3}}",
  "livemode": false
}
```

All new subscriptions use the version you specified (v3 in this example) unless you set a different live version.

### Update existing subscriptions

Existing pricing plan subscriptions remain on their original version unless you manually update them. To migrate existing customers to the new version, use a [billing intent](https://docs.stripe.com/api/v2/billing-intents.md?api-version=preview) to update their subscription’s pricing plan version.

```curl
curl -X POST https://api.stripe.com/v2/billing/intents \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "cadence": "{{BILLING_CADENCE_ID}}",
    "currency": "usd",
    "actions": [
        {
            "type": "modify",
            "modify": {
                "type": "pricing_plan_subscription_details",
                "pricing_plan_subscription_details": {
                    "pricing_plan_subscription": "{{PRICING_PLAN_SUBSCRIPTION_ID}}",
                    "pricing_plan_version": "{{PRICING_PLAN_VERSION_ID}}",
                    "component_configurations": []
                }
            }
        }
    ]
  }'
```

### Recommended pricing plan workflow

To manage updates effectively:

1. **Update the pricing plan**: Add or modify components, creating a new `latest_version`.
1. **Set the live version**: Update `live_version` to `latest` for new subscriptions.
1. **Notify existing customers**: Inform customers or segments about upcoming changes.
1. **Migrate subscriptions**: On your schedule, update pricing plan subscriptions to the new version for selected customers.

This flow ensures smooth transitions while addressing customer communication and segmentation needs.

## Roll out new services to all subscribers without code 

If you launch a new feature with new pricing, you can roll out that pricing to all of your subscribers by adding a new rate to the rate card. All subscribers on the live version have access to the new service you added, and the new rate applies immediately.

When you add a new rate to your rate card, it’s immediately available to all subscribers on that version. Any usage reported against the new rate’s meter is priced according to this rate and shows up on the next invoice. This lets you quickly launch new billable services (like a new AI model) without writing code.

To add new rates to your existing rate card through the Dashboard:

1. Go to the [Rate cards](https://dashboard.stripe.com/rate-cards?active=true) page.
1. Select a rate card, then click **Edit rate card**.
1. Click + to add a new rate.

## Billing intents 

Use [billing intents](https://docs.stripe.com/api/v2/billing-intents.md?api-version=preview) to create and manage subscriptions in the [API v2 namespace](https://docs.stripe.com/api-v2-overview.md). Billing intents are temporary objects that keep track of billing actions, like setting up or modifying [pricing plan subscriptions](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions.md), upgrading or migrating customers from one [pricing plan](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md) version to another, or canceling a customer’s subscription.

If you create a subscription through *Stripe Checkout* (A low-code payment integration that creates a customizable form for collecting payments. You can embed Checkout directly in your website, redirect customers to a Stripe-hosted payment page, or create a customized checkout page with Stripe Elements), you don’t need to directly manage billing intents since they’re handled for you.

### Billing intent states 

A billing intent has the following states:

- When you [create](https://docs.stripe.com/api/v2/billing-intents/create.md?api-version=preview) a billing intent by passing in the billing interval and pricing plan IDs, it’s in the `draft` state. The customer isn’t charged, but you can see what’s due.
- Then, you [reserve](https://docs.stripe.com/api/v2/billing-intents/reserve.md?api-version=preview) the intent. When the billing intent is `reserved`, you can [preview invoices](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md#create-preview-invoice). Reserving a billing intent allows you to calculate and preview what’s owed without charging your customer.
- Finally, you [commit](https://docs.stripe.com/api/v2/billing-intents/commit.md?api-version=preview). When the billing intent is `committed`, you [subscribe](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md#subscribe) the customer referenced on the cadence to the pricing plan and create a new [pricing plan subscription](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions.md). (For billing intents where the cadence has the `collection_method` set to `automatic`, you must pass a successful Payment Intent if any amount is owed by the customer.)
Billing intent states (See full diagram at https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions/manage)
### Supported configurations for billing intents 

Billing intents perform different [actions](https://docs.stripe.com/api/v2/billing-intents/intent-action/object.md?api-version=preview) on subscriptions, such as [subscribing](https://docs.stripe.com/api/v2/billing-intents/intent-action/object.md?api-version=preview#v2_intent_action_object-subscribe) a customer to a pricing plan or [modifying](https://docs.stripe.com/api/v2/billing-intents/intent-action/object.md?api-version=preview#v2_intent_action_object-modify) a subscription. You can use these actions to migrate a customer from one pricing plan (or version) to another and cancel subscriptions.

Currently, these billing intent actions have the following default configurations.

| Intent action                                                                                                                               | Default configuration                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [subscribe](https://docs.stripe.com/api/v2/billing-intents/intent-action/object.md?api-version=preview#v2_intent_action_object-subscribe)   | By default, the subscribe action prorates the amount based on the partial servicing period and makes the change effective when the billing intent is reserved. To not prorate the amount, pass in [proration_behavior](https://docs.stripe.com/api/v2/billing-intents/intent-action/object.md?api-version=preview#v2_intent_action_object-subscribe-billing_details-proration_behavior) set to `no_adjustment` when you create the billing intent. |
| [modify](https://docs.stripe.com/api/v2/billing-intents/intent-action/object.md?api-version=preview#v2_intent_action_object-modify)         | By default, the modify action doesn’t adjust the proration and makes the change effective when the billing intent is reserved.                                                                                                                                                                                                                                                                                                                     |
| [deactivate](https://docs.stripe.com/api/v2/billing-intents/intent-action/object.md?api-version=preview#v2_intent_action_object-deactivate) | By default, the deactivate action doesn’t adjust the proration and makes the change effective when the billing intent is reserved.                                                                                                                                                                                                                                                                                                                 |

## Set up different pricing versions by user cohort 

Pricing plans use [versioning](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#pricing-plan-versioning) to give you flexible pricing management.

To offer different pricing to different customer cohorts:

1. Subscribe new customers to the current live version (default) of a pricing plan.
1. Create different versions for different customer segments.
1. Subscribe specific customers to older versions.

When you create a billing intent (which creates a pricing plan subscription), you can specify which version to use:

```curl
curl -X POST https://api.stripe.com/v2/billing/intents \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "cadence": "{{BILLING_CADENCE_ID}}",
    "currency": "usd",
    "actions": [
        {
            "type": "subscribe",
            "subscribe": {
                "billing_details": {
                    "proration_behavior": "no_adjustment"
                },
                "effective_at": {
                    "type": "on_reserve"
                },
                "type": "pricing_plan_subscription_details",
                "pricing_plan_subscription_details": {
                    "pricing_plan": "{{PRICING_PLAN_ID}}",
                    "pricing_plan_version": "{{PRICING_PLAN_VERSION_ID}}",
                    "component_configurations": []
                }
            }
        }
    ]
  }'
```

If you don’t specify a version, Stripe automatically uses the current live version.

## Migrate customers to new or updated pricing plans 

To change the version for an existing subscriber, you must cancel their pricing plan subscription and create a new one with the new version. You can migrate existing customers from one pricing plan version to another using the billing intent. To do this, create a new billing intent to transition the customer to the new plan and version.

```curl
curl -X POST https://api.stripe.com/v2/billing/intents \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "cadence": "{{BILLING_CADENCE_ID}}",
    "currency": "usd",
    "actions": [
        {
            "type": "modify",
            "modify": {
                "type": "pricing_plan_subscription_details",
                "pricing_plan_subscription_details": {
                    "pricing_plan_subscription": "{{PRICING_PLAN_SUBSCRIPTION_ID}}",
                    "new_pricing_plan": "{{PRICING_PLAN_ID}}",
                    "new_pricing_plan_version": "{{PRICING_PLAN_VERSION_ID}}",
                    "component_configurations": []
                }
            }
        }
    ]
  }'
```

Reserve the billing intent:

```curl
curl -X POST https://api.stripe.com/v2/billing/intents/{{BILLING_INTENT_ID}}/reserve \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview"
```

Commit the billing intent:

```curl
curl -X POST https://api.stripe.com/v2/billing/intents/{{BILLING_INTENT_ID}}/commit \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview"
```

Confirm the change by looking at the subscription in the [Pricing plans page](https://dashboard.stripe.com/pricing-plans?active=true) in the Dashboard or by retrieving the subscription using the API:

```curl
curl https://api.stripe.com/v2/billing/pricing_plan_subscriptions/{{PRICING_PLAN_SUBSCRIPTION_ID}} \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview"
```

## Cancel pricing plan subscriptions 

To cancel a pricing plan subscription, use the API to [create a billing intent to deactivate](https://docs.stripe.com/api/v2/billing-intents/create.md?api-version=preview#v2_create_billing_intents-actions-deactivate) the subscription:

```curl
curl -X POST https://api.stripe.com/v2/billing/intents \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "cadence": "{{BILLING_CADENCE_ID}}",
    "currency": "usd",
    "actions": [
        {
            "type": "deactivate",
            "deactivate": {
                "type": "pricing_plan_subscription_details",
                "pricing_plan_subscription_details": {
                    "pricing_plan_subscription": "{{PRICING_PLAN_SUBSCRIPTION_ID}}",
                    "component_configurations": []
                }
            }
        }
    ]
  }'
```


# Pricing plan subscriptions

Charge customers on a recurring basis as they use your service.

When you set up your pricing model with pricing plans, you can use those pricing plans as the basis for subscriptions. Pricing plan subscriptions reflect the active state of a pricing plan for a customer, tied to a billing interval. The subscription orchestrates the underlying rate card and license fee subscriptions.

> Pricing Plans are currently in [private preview](https://docs.stripe.com/release-phases.md) and could change in functionality and integration path before they’re generally available to all Stripe users. 

## Collection status and servicing status 

Pricing plan subscriptions have two separate states:

- **Servicing state**: This is tied to the collection status and invoice status and indicates when to provision or de-provision services. The servicing state of a pricing plan subscription can be one of:
  - Active
  - Canceled
- **Collection state**: This is tied to the state of the invoices generated by the billing interval and defines the payment status of the pricing plan subscription. The collection state can be one of:
  - Current
  - Past due
  - Unpaid

Here’s how the statuses work together for subscriptions that charge a customer’s payment method automatically:

| Action                                               | Servicing status | Collection status         |
| ---------------------------------------------------- | ---------------- | ------------------------- |
| Subscription created                                 | Active           | Current                   |
| Payment successfully received                        | Active           | Current                   |
| Payment received for all associated overdue invoices | Active           | Current                   |
| User cancels subscription                            | Canceled         | Remains in previous state |

Here’s how the statuses work together for subscriptions that send invoices:

| Action                                                   | Servicing status | Collection status         |
| -------------------------------------------------------- | ---------------- | ------------------------- |
| Subscription created                                     | Active           | Current                   |
| Invoice generated but not paid (before payment due date) | Active           | Current                   |
| Payment received for an associated overdue invoice       | Active           | Current                   |
| User cancels subscription                                | Canceled         | Remains in previous state |

## How payments work with pricing plan subscriptions

When you [create a pricing plan subscription](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md#subscribe), you define how to collect payments for the usage your customer accrues—either charge the customer’s payment method automatically or send them an invoice at the end of each billing interval. You can collect payment details when you create subscriptions for customers. At the end of the billing interval, Stripe generates an invoice.

If you charge automatically, Stripe generates an invoice but doesn’t notify your customer about the invoice. If you’ve [enabled customer emails](https://dashboard.stripe.com/account/emails), Stripe sends an email receipt for successful payments.

If you send invoices, Stripe generates an invoice and sends it to your customer, which they can pay with the supported payment methods you’ve enabled.

### Invoice lifecycle for pricing plan subscriptions

The basic lifecycle for invoices generated by pricing plan subscriptions looks like this:

1. The pricing plan subscription generates a new invoice in `draft` state.
1. The invoice finalizes immediately. You can’t make changes after the invoice is finalized.
1. The status is set to `open` and Stripe either automatically attempts to pay it using the customer’s default payment method or sends the customer an invoice.
1. If payment succeeds, the invoice status updates to `paid`.
1. If payment fails, the invoice remains `open` and the pricing plan subscription becomes `past_due`.

### Invoice grace period

Pricing plan subscriptions generate a finalized invoice an hour after the billing cadence tick. This period of time allows you to continue to report backdated usage for the period. After the grace period, a finalized invoice is created for the customer.

## Recovery settings for pricing plan subscriptions

When payments fail for pricing plan subscriptions, Stripe’s default recovery behavior helps you recover revenue.

### Automated retries

After creating a pricing plan subscription, payment failure is the most important event that can occur. Failures occur for many reasons:

- Lack of a payment method on the customer
- Expired payment method
- Declined payment

For pricing plan subscriptions, Stripe automatically retries failed payments based on your configured [subscription settings](https://dashboard.stripe.com/settings/billing/automatic). You can use either:

- [Smart Retries](https://dashboard.stripe.com/settings/billing/automatic), where machine learning picks the optimal retry time
- Scheduled retries, where you [configure the retry policy in the Dashboard](https://dashboard.stripe.com/settings/billing/automatic)

Use the [invoice.payment_failed](https://docs.stripe.com/api/events/types.md#event_types-invoice.payment_failed) event to monitor subscription payment failure events and retry attempt updates. After a payment attempt on an invoice, its [next_payment_attempt](https://docs.stripe.com/api/invoices/object.md#invoice_object-next_payment_attempt) value is set using the default retry settings.

If recovery fails after all retry attempts, the pricing plan subscription transitions to the `Unpaid` collection state, and the servicing status is set to `Canceled` as shown in the [collection status and servicing status](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions.md#collection-status-and-servicing-status) tables.

### Customer emails

Stripe sends different emails to customers using the email addresses associated with the [Customer](https://docs.stripe.com/api/customers.md) object:

- A [failed payment notification](https://docs.stripe.com/billing/revenue-recovery/customer-emails.md#failed-payment-notifications) that prompts customers to update their payment information when a payment attempt fails.
- An expiring card notification when a customer’s default payment method card is due to expire.

You can customize the logos and colors your customers see in emails and the Hosted Invoice Payment page by changing the [branding settings](https://dashboard.stripe.com/account/branding) in the Dashboard.


# Set up billing credits

Learn how to implement a prepaid billing solution with billing credits.

Use [Meters](https://docs.stripe.com/api/billing/meter.md) and [billing credits](https://docs.stripe.com/billing/subscriptions/usage-based/billing-credits.md) to collect payment upfront for usage-based products or services, or to offer promotional usage.

## Before you begin

Before you use billing credits, we recommend learning how to [set up advanced usage-based billing](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md):

- Create a [meter](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md#create-meter).
- Create a pricing model using [pricing plans](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md#pricing-plan-pricing-model).
- Create a [Pricing plan subscription](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md#subscribe) that includes your customer’s cadence and plan.

## Grant billing credits to your customer

You can use the Stripe Dashboard or API to create a credit grant for your customer. You can only scope credit grants to specific [billable_items](https://docs.stripe.com/api/v2/service-actions/object.md?api-version=preview&rds=1&lang=curl#v2_service_action_object-credit_grant-applicability_config-scope-billable_items) through the API.

You can also [create a service action](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/service-actions/about.md#create-service-action) component and add it to your pricing plan if you want to configure a recurring credit grant for a specific pricing plan.

You can apply billing credits across all [metered items on a rate card](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#rate-card-concepts) or scope them to specific ones.

#### Dashboard

To create a credit grant for your customer in the Dashboard:

1. Go to the [Customers](https://dashboard.stripe.com/test/customers) page, select the customer name.
1. On the customer page, under Credit grants, click the plus (+) symbol.
   - On the **New credit grant** page, do the following:

   - For **Name**, enter a name for your credit grant.

   - For **Amount**, specify the amount of the credit grant.

   - Select **Eligibility**.

   - Select the **Grant type**.

   - (Optional) Under **Effective date**, specify a date for when the credit becomes eligible. If the date falls in the middle of a service period, the grant is applicable for the entirety of that period.

   - (Optional) Under **Expiry date**, specify the date, if any, when the credits expire.

   - (Optional) Under **Priority**, specify the priority for this credit grant.
1. Click **Create grant**.

#### API

To create a credit grant for your customer in the API:

```curl
curl https://api.stripe.com/v1/billing/credit_grants \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d customer={{CUSTOMER_ID}} \
  -d name="Credit grant" \
  -d "applicability_config[scope][price_type]"=metered \
  -d category=paid \
  -d "amount[type]"=monetary \
  -d "amount[monetary][value]"=1000 \
  -d "amount[monetary][currency]"=usd
```

```cli
stripe billing credit_grants create  \
  --customer={{CUSTOMER_ID}} \
  --name="Credit grant" \
  -d "applicability_config[scope][price_type]"=metered \
  --category=paid \
  -d "amount[type]"=monetary \
  -d "amount[monetary][value]"=1000 \
  -d "amount[monetary][currency]"=usd
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

credit_grant = client.v1.billing.credit_grants.create({
  customer: '{{CUSTOMER_ID}}',
  name: 'Credit grant',
  applicability_config: {scope: {price_type: 'metered'}},
  category: 'paid',
  amount: {
    type: 'monetary',
    monetary: {
      value: 1000,
      currency: 'usd',
    },
  },
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
credit_grant = client.v1.billing.credit_grants.create({
  "customer": "{{CUSTOMER_ID}}",
  "name": "Credit grant",
  "applicability_config": {"scope": {"price_type": "metered"}},
  "category": "paid",
  "amount": {"type": "monetary", "monetary": {"value": 1000, "currency": "usd"}},
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$creditGrant = $stripe->billing->creditGrants->create([
  'customer' => '{{CUSTOMER_ID}}',
  'name' => 'Credit grant',
  'applicability_config' => ['scope' => ['price_type' => 'metered']],
  'category' => 'paid',
  'amount' => [
    'type' => 'monetary',
    'monetary' => [
      'value' => 1000,
      'currency' => 'usd',
    ],
  ],
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

CreditGrantCreateParams params =
  CreditGrantCreateParams.builder()
    .setCustomer("{{CUSTOMER_ID}}")
    .setName("Credit grant")
    .setApplicabilityConfig(
      CreditGrantCreateParams.ApplicabilityConfig.builder()
        .setScope(
          CreditGrantCreateParams.ApplicabilityConfig.Scope.builder()
            .setPriceType(
              CreditGrantCreateParams.ApplicabilityConfig.Scope.PriceType.METERED
            )
            .build()
        )
        .build()
    )
    .setCategory(CreditGrantCreateParams.Category.PAID)
    .setAmount(
      CreditGrantCreateParams.Amount.builder()
        .setType(CreditGrantCreateParams.Amount.Type.MONETARY)
        .setMonetary(
          CreditGrantCreateParams.Amount.Monetary.builder()
            .setValue(1000L)
            .setCurrency("usd")
            .build()
        )
        .build()
    )
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
CreditGrant creditGrant = client.v1().billing().creditGrants().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const creditGrant = await stripe.billing.creditGrants.create({
  customer: '{{CUSTOMER_ID}}',
  name: 'Credit grant',
  applicability_config: {
    scope: {
      price_type: 'metered',
    },
  },
  category: 'paid',
  amount: {
    type: 'monetary',
    monetary: {
      value: 1000,
      currency: 'usd',
    },
  },
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.BillingCreditGrantCreateParams{
  Customer: stripe.String("{{CUSTOMER_ID}}"),
  Name: stripe.String("Credit grant"),
  ApplicabilityConfig: &stripe.BillingCreditGrantCreateApplicabilityConfigParams{
    Scope: &stripe.BillingCreditGrantCreateApplicabilityConfigScopeParams{
      PriceType: stripe.String("metered"),
    },
  },
  Category: stripe.String(stripe.BillingCreditGrantCategoryPaid),
  Amount: &stripe.BillingCreditGrantCreateAmountParams{
    Type: stripe.String("monetary"),
    Monetary: &stripe.BillingCreditGrantCreateAmountMonetaryParams{
      Value: stripe.Int64(1000),
      Currency: stripe.String(stripe.CurrencyUSD),
    },
  },
}
result, err := sc.V1BillingCreditGrants.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.Billing.CreditGrantCreateOptions
{
    Customer = "{{CUSTOMER_ID}}",
    Name = "Credit grant",
    ApplicabilityConfig = new Stripe.Billing.CreditGrantApplicabilityConfigOptions
    {
        Scope = new Stripe.Billing.CreditGrantApplicabilityConfigScopeOptions
        {
            PriceType = "metered",
        },
    },
    Category = "paid",
    Amount = new Stripe.Billing.CreditGrantAmountOptions
    {
        Type = "monetary",
        Monetary = new Stripe.Billing.CreditGrantAmountMonetaryOptions
        {
            Value = 1000,
            Currency = "usd",
        },
    },
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Billing.CreditGrants;
Stripe.Billing.CreditGrant creditGrant = service.Create(options);
```

## Apply billing credits to invoices

You can see your credit grant applied on the upcoming invoice (or [preview invoice](https://docs.stripe.com/api/invoices/create_preview.md) endpoint) or after an invoice has been generated following a billing interval (when an invoice is automatically generated).

The *available balance* on the credit grant updates as it’s burned down by incoming rated usage. The *ledger balance* updates based on the amount of billing credits applied to the invoice.

After you’ve created an invoice for a customer with an eligible credit grant, you can:

1. Go to the [Customers](https://dashboard.stripe.com/test/customers) page and select the customer name.
1. On the customer page, under **Invoices**, select an invoice.
1. On the invoice page, under **Subtotal**, find the line for **Credit grant applied**.

## Retrieve the available billing credit balance

Use the Stripe Dashboard or API to see the available billing credit balance for a customer. When using the API, retrieve the [Credit Balance Summary](https://docs.stripe.com/api/billing/credit-balance-summary/retrieve.md) endpoint.

#### Dashboard

To see the available billing credit balance for a customer in the Dashboard:

1. Go to the [Customers](https://dashboard.stripe.com/test/customers) page and select the customer name.
1. On the customer page, under **Credit grants**, find the list of credit grants that can apply to invoices. You can see the credit grant’s [available_balance](https://docs.stripe.com/api/billing/credit-balance-summary/object.md#billing_credit_balance_summary_object-balances-available_balance) in the **Available** column.

#### API

To see the available billing credit balance for a customer in the API:

```curl
curl -G https://api.stripe.com/v1/billing/credit_balance_summary \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d customer={{CUSTOMER_ID}} \
  -d "filter[type]"=applicability_scope \
  -d "filter[applicability_scope][price_type]"=metered
```

```cli
stripe billing credit_balance_summaries retrieve  \
  --customer={{CUSTOMER_ID}} \
  -d "filter[type]"=applicability_scope \
  -d "filter[applicability_scope][price_type]"=metered
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

credit_balance_summary = client.v1.billing.credit_balance_summary.retrieve({
  customer: '{{CUSTOMER_ID}}',
  filter: {
    type: 'applicability_scope',
    applicability_scope: {price_type: 'metered'},
  },
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
credit_balance_summary = client.v1.billing.credit_balance_summary.retrieve({
  "customer": "{{CUSTOMER_ID}}",
  "filter": {
    "type": "applicability_scope",
    "applicability_scope": {"price_type": "metered"},
  },
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$creditBalanceSummary = $stripe->billing->creditBalanceSummary->retrieve([
  'customer' => '{{CUSTOMER_ID}}',
  'filter' => [
    'type' => 'applicability_scope',
    'applicability_scope' => ['price_type' => 'metered'],
  ],
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

CreditBalanceSummaryRetrieveParams params =
  CreditBalanceSummaryRetrieveParams.builder()
    .setCustomer("{{CUSTOMER_ID}}")
    .setFilter(
      CreditBalanceSummaryRetrieveParams.Filter.builder()
        .setType(CreditBalanceSummaryRetrieveParams.Filter.Type.APPLICABILITY_SCOPE)
        .setApplicabilityScope(
          CreditBalanceSummaryRetrieveParams.Filter.ApplicabilityScope.builder()
            .setPriceType(
              CreditBalanceSummaryRetrieveParams.Filter.ApplicabilityScope.PriceType.METERED
            )
            .build()
        )
        .build()
    )
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
CreditBalanceSummary creditBalanceSummary =
  client.v1().billing().creditBalanceSummary().retrieve(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const creditBalanceSummary = await stripe.billing.creditBalanceSummary.retrieve({
  customer: '{{CUSTOMER_ID}}',
  filter: {
    type: 'applicability_scope',
    applicability_scope: {
      price_type: 'metered',
    },
  },
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.BillingCreditBalanceSummaryRetrieveParams{
  Customer: stripe.String("{{CUSTOMER_ID}}"),
  Filter: &stripe.BillingCreditBalanceSummaryRetrieveFilterParams{
    Type: stripe.String("applicability_scope"),
    ApplicabilityScope: &stripe.BillingCreditBalanceSummaryRetrieveFilterApplicabilityScopeParams{
      PriceType: stripe.String("metered"),
    },
  },
}
result, err := sc.V1BillingCreditBalanceSummary.Retrieve(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.Billing.CreditBalanceSummaryGetOptions
{
    Customer = "{{CUSTOMER_ID}}",
    Filter = new Stripe.Billing.CreditBalanceSummaryFilterOptions
    {
        Type = "applicability_scope",
        ApplicabilityScope = new Stripe.Billing.CreditBalanceSummaryFilterApplicabilityScopeOptions
        {
            PriceType = "metered",
        },
    },
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Billing.CreditBalanceSummary;
Stripe.Billing.CreditBalanceSummary creditBalanceSummary = service.Get(options);
```

You can also filter the credit balance summary to only show the balance summary for a given credit grant:

```curl
curl -G https://api.stripe.com/v1/billing/credit_balance_summary \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d customer={{CUSTOMER_ID}} \
  -d "filter[type]"=credit_grant \
  -d "filter[credit_grant]"={{CREDIT_GRANT_ID}}
```

```cli
stripe billing credit_balance_summaries retrieve  \
  --customer={{CUSTOMER_ID}} \
  -d "filter[type]"=credit_grant \
  -d "filter[credit_grant]"={{CREDIT_GRANT_ID}}
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

credit_balance_summary = client.v1.billing.credit_balance_summary.retrieve({
  customer: '{{CUSTOMER_ID}}',
  filter: {
    type: 'credit_grant',
    credit_grant: '{{CREDIT_GRANT_ID}}',
  },
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
credit_balance_summary = client.v1.billing.credit_balance_summary.retrieve({
  "customer": "{{CUSTOMER_ID}}",
  "filter": {"type": "credit_grant", "credit_grant": "{{CREDIT_GRANT_ID}}"},
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$creditBalanceSummary = $stripe->billing->creditBalanceSummary->retrieve([
  'customer' => '{{CUSTOMER_ID}}',
  'filter' => [
    'type' => 'credit_grant',
    'credit_grant' => '{{CREDIT_GRANT_ID}}',
  ],
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

CreditBalanceSummaryRetrieveParams params =
  CreditBalanceSummaryRetrieveParams.builder()
    .setCustomer("{{CUSTOMER_ID}}")
    .setFilter(
      CreditBalanceSummaryRetrieveParams.Filter.builder()
        .setType(CreditBalanceSummaryRetrieveParams.Filter.Type.CREDIT_GRANT)
        .setCreditGrant("{{CREDIT_GRANT_ID}}")
        .build()
    )
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
CreditBalanceSummary creditBalanceSummary =
  client.v1().billing().creditBalanceSummary().retrieve(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const creditBalanceSummary = await stripe.billing.creditBalanceSummary.retrieve({
  customer: '{{CUSTOMER_ID}}',
  filter: {
    type: 'credit_grant',
    credit_grant: '{{CREDIT_GRANT_ID}}',
  },
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.BillingCreditBalanceSummaryRetrieveParams{
  Customer: stripe.String("{{CUSTOMER_ID}}"),
  Filter: &stripe.BillingCreditBalanceSummaryRetrieveFilterParams{
    Type: stripe.String("credit_grant"),
    CreditGrant: stripe.String("{{CREDIT_GRANT_ID}}"),
  },
}
result, err := sc.V1BillingCreditBalanceSummary.Retrieve(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.Billing.CreditBalanceSummaryGetOptions
{
    Customer = "{{CUSTOMER_ID}}",
    Filter = new Stripe.Billing.CreditBalanceSummaryFilterOptions
    {
        Type = "credit_grant",
        CreditGrant = "{{CREDIT_GRANT_ID}}",
    },
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Billing.CreditBalanceSummary;
Stripe.Billing.CreditBalanceSummary creditBalanceSummary = service.Get(options);
```

## List transactions for a credit grant

Use the Stripe Dashboard or API to see the transactions for a specific credit grant or customer. When using the API, call the [Credit Balance Transaction](https://docs.stripe.com/api/billing/credit-balance-transaction/list.md) endpoint.

#### Dashboard

To see the transactions for a specific credit grant or customer:

1. Go to the [Customers](https://dashboard.stripe.com/test/customers) page and select the customer name.
1. On the customer page, under **Credit grants**, select a credit grant.
1. View details for the credit balance transactions.

#### API

```curl
curl -G https://api.stripe.com/v1/billing/credit_balance_transactions \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d customer={{CUSTOMER_ID}} \
  -d credit_grant={{CREDIT_GRANT_ID}}
```

```cli
stripe billing credit_balance_transactions list  \
  --customer={{CUSTOMER_ID}} \
  --credit-grant={{CREDIT_GRANT_ID}}
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

credit_balance_transactions = client.v1.billing.credit_balance_transactions.list({
  customer: '{{CUSTOMER_ID}}',
  credit_grant: '{{CREDIT_GRANT_ID}}',
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
credit_balance_transactions = client.v1.billing.credit_balance_transactions.list({
  "customer": "{{CUSTOMER_ID}}",
  "credit_grant": "{{CREDIT_GRANT_ID}}",
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$creditBalanceTransactions = $stripe->billing->creditBalanceTransactions->all([
  'customer' => '{{CUSTOMER_ID}}',
  'credit_grant' => '{{CREDIT_GRANT_ID}}',
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

CreditBalanceTransactionListParams params =
  CreditBalanceTransactionListParams.builder()
    .setCustomer("{{CUSTOMER_ID}}")
    .setCreditGrant("{{CREDIT_GRANT_ID}}")
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
StripeCollection<CreditBalanceTransaction> stripeCollection =
  client.v1().billing().creditBalanceTransactions().list(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const creditBalanceTransactions = await stripe.billing.creditBalanceTransactions.list({
  customer: '{{CUSTOMER_ID}}',
  credit_grant: '{{CREDIT_GRANT_ID}}',
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.BillingCreditBalanceTransactionListParams{
  Customer: stripe.String("{{CUSTOMER_ID}}"),
  CreditGrant: stripe.String("{{CREDIT_GRANT_ID}}"),
}
result := sc.V1BillingCreditBalanceTransactions.List(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new Stripe.Billing.CreditBalanceTransactionListOptions
{
    Customer = "{{CUSTOMER_ID}}",
    CreditGrant = "{{CREDIT_GRANT_ID}}",
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Billing.CreditBalanceTransactions;
StripeList<Stripe.Billing.CreditBalanceTransaction> creditBalanceTransactions = service
    .List(options);
```

## Optional: Fund the credit grant

Use the Stripe Dashboard or API to create a one-off [invoice](https://docs.stripe.com/invoicing.md) to collect payment from a customer. When using the API, listen for the `invoice.paid` [event](https://docs.stripe.com/webhooks.md) and grant billing credits to your customer (if you aren’t using service actions or automating the issuing of a credit grant using workflows).

#### Dashboard

To create a one-off invoice to collect payment from a customer in the Dashboard:

1. Go to the [Customers](https://dashboard.stripe.com/test/customers) page and select the customer name.
1. On the customer page, click **Create invoice**.
1. Follow the instructions to [create an invoice](https://docs.stripe.com/invoicing/dashboard.md).

#### API

To create a one-off invoice to collect payment from a customer in the API:

```curl
curl https://api.stripe.com/v1/invoices \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d customer={{CUSTOMER_ID}} \
  -d description="credit purchase" \
  -d collection_method=charge_automatically
```

```cli
stripe invoices create  \
  --customer={{CUSTOMER_ID}} \
  --description="credit purchase" \
  --collection-method=charge_automatically
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

invoice = client.v1.invoices.create({
  customer: '{{CUSTOMER_ID}}',
  description: 'credit purchase',
  collection_method: 'charge_automatically',
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
invoice = client.v1.invoices.create({
  "customer": "{{CUSTOMER_ID}}",
  "description": "credit purchase",
  "collection_method": "charge_automatically",
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$invoice = $stripe->invoices->create([
  'customer' => '{{CUSTOMER_ID}}',
  'description' => 'credit purchase',
  'collection_method' => 'charge_automatically',
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

InvoiceCreateParams params =
  InvoiceCreateParams.builder()
    .setCustomer("{{CUSTOMER_ID}}")
    .setDescription("credit purchase")
    .setCollectionMethod(InvoiceCreateParams.CollectionMethod.CHARGE_AUTOMATICALLY)
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
Invoice invoice = client.v1().invoices().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const invoice = await stripe.invoices.create({
  customer: '{{CUSTOMER_ID}}',
  description: 'credit purchase',
  collection_method: 'charge_automatically',
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.InvoiceCreateParams{
  Customer: stripe.String("{{CUSTOMER_ID}}"),
  Description: stripe.String("credit purchase"),
  CollectionMethod: stripe.String(stripe.InvoiceCollectionMethodChargeAutomatically),
}
result, err := sc.V1Invoices.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new InvoiceCreateOptions
{
    Customer = "{{CUSTOMER_ID}}",
    Description = "credit purchase",
    CollectionMethod = "charge_automatically",
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Invoices;
Invoice invoice = service.Create(options);
```

```curl
curl https://api.stripe.com/v1/invoiceitems \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d customer={{CUSTOMER_ID}} \
  -d description="billing credits purchase" \
  -d unit_amount_decimal=1000 \
  -d currency=usd \
  -d invoice={{INVOICE_ID}}
```

```cli
stripe invoiceitems create  \
  --customer={{CUSTOMER_ID}} \
  --description="billing credits purchase" \
  --unit-amount-decimal=1000 \
  --currency=usd \
  --invoice={{INVOICE_ID}}
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

invoice_item = client.v1.invoice_items.create({
  customer: '{{CUSTOMER_ID}}',
  description: 'billing credits purchase',
  unit_amount_decimal: 1000,
  currency: 'usd',
  invoice: '{{INVOICE_ID}}',
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
invoice_item = client.v1.invoice_items.create({
  "customer": "{{CUSTOMER_ID}}",
  "description": "billing credits purchase",
  "unit_amount_decimal": "1000",
  "currency": "usd",
  "invoice": "{{INVOICE_ID}}",
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$invoiceItem = $stripe->invoiceItems->create([
  'customer' => '{{CUSTOMER_ID}}',
  'description' => 'billing credits purchase',
  'unit_amount_decimal' => '1000',
  'currency' => 'usd',
  'invoice' => '{{INVOICE_ID}}',
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

InvoiceItemCreateParams params =
  InvoiceItemCreateParams.builder()
    .setCustomer("{{CUSTOMER_ID}}")
    .setDescription("billing credits purchase")
    .setUnitAmountDecimal(new BigDecimal("1000"))
    .setCurrency("usd")
    .setInvoice("{{INVOICE_ID}}")
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
InvoiceItem invoiceItem = client.v1().invoiceItems().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const invoiceItem = await stripe.invoiceItems.create({
  customer: '{{CUSTOMER_ID}}',
  description: 'billing credits purchase',
  unit_amount_decimal: '1000',
  currency: 'usd',
  invoice: '{{INVOICE_ID}}',
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.InvoiceItemCreateParams{
  Customer: stripe.String("{{CUSTOMER_ID}}"),
  Description: stripe.String("billing credits purchase"),
  UnitAmountDecimal: stripe.Float64(1000),
  Currency: stripe.String(stripe.CurrencyUSD),
  Invoice: stripe.String("{{INVOICE_ID}}"),
}
result, err := sc.V1InvoiceItems.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new InvoiceItemCreateOptions
{
    Customer = "{{CUSTOMER_ID}}",
    Description = "billing credits purchase",
    UnitAmountDecimal = 1000M,
    Currency = "usd",
    Invoice = "{{INVOICE_ID}}",
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.InvoiceItems;
InvoiceItem invoiceItem = service.Create(options);
```

```curl
curl https://api.stripe.com/v1/invoices/{{INVOICE_ID}}/finalize \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d auto_advance=true
```

```cli
stripe invoices finalize_invoice {{INVOICE_ID}} \
  --auto-advance=true
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

invoice = client.v1.invoices.finalize_invoice('{{INVOICE_ID}}', {auto_advance: true})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
invoice = client.v1.invoices.finalize_invoice(
  "{{INVOICE_ID}}",
  {"auto_advance": True},
)
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$invoice = $stripe->invoices->finalizeInvoice('{{INVOICE_ID}}', ['auto_advance' => true]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

InvoiceFinalizeInvoiceParams params =
  InvoiceFinalizeInvoiceParams.builder().setAutoAdvance(true).build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
Invoice invoice = client.v1().invoices().finalizeInvoice("{{INVOICE_ID}}", params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const invoice = await stripe.invoices.finalizeInvoice(
  '{{INVOICE_ID}}',
  {
    auto_advance: true,
  }
);
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.InvoiceFinalizeInvoiceParams{AutoAdvance: stripe.Bool(true)}
result, err := sc.V1Invoices.FinalizeInvoice(context.TODO(), "{{INVOICE_ID}}", params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new InvoiceFinalizeOptions { AutoAdvance = true };
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Invoices;
Invoice invoice = service.FinalizeInvoice("{{INVOICE_ID}}", options);
```


# How billing credits work

Use billing credits for prepaid or promotional usage-based products or services.

Offer billing credits to your customers in your business workflows for the following:

- **Prepayment**: Grant billing credits to your customers that they can use to pay for usage-based products or services. You can leverage credits to power [fixed fee plus overage](https://docs.stripe.com/subscriptions/pricing-models/usage-based-pricing.md#fixed-fee-overage) and [real-time credit burndown and top up](https://docs.stripe.com/subscriptions/pricing-models/usage-based-pricing.md#credit-burndown) pricing models.
- **Promotional offering**: Grant billing credits for free to your customers as a promotional offering. Businesses often offer a limited amount of promotional credits that include an expiration date.

The following diagram shows how billing credits work with usage-based billing:
 (See full diagram at https://docs.stripe.com/billing/subscriptions/usage-based-v2/billing-credits/about)
## Prohibited uses

You can’t do the following with billing credits:

- Issue them as gift cards or gift certificates. Also, you can’t allow your customers to spend billing credits on, or exchange billing credits for, gift cards or gift certificates.
- Offer them as stored value to your customers. You can’t grant any billing credits that aren’t intended to be spent on your subscriptions.
- Allow your customers to use them for payments to third parties. For example, you can’t allow your customers to apply billing credits to purchases on the website or platform of another business.
- You can’t link them to digital wallets, or allow your customers to do so. For example, you can’t allow your customers to add billing credits to a digital wallet, such as Apple Pay or Google Pay.

## Automation

You can automate creation and assignment of credit grants to a customer two ways:

- [Service actions](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/service-actions/about.md) (Recommended): You can create and attach service actions as a component of a pricing plan. Subscriptions initiate the service action every service interval, automatically creating a credit grant of choice.

- [Workflows](https://docs.stripe.com/workflows.md): You can listen to `invoice.created` or a billing alert webhook and trigger the creation of a new credit grant.

## Billing credit concepts

| Term                       | Definition                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Credit grant               | A [Credit Grant](https://docs.stripe.com/api/billing/credit-grant.md) tracks a set of prepaid or promotional billing credits allocated to a customer. Learn more about [credit grant states](https://docs.stripe.com/billing/subscriptions/usage-based-v2/billing-credits/about.md#states).                                                                                                                                                                  |
| Credit grant applicability | You can apply credit grants to subscription line items that link to a [metered item](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/about.md#rate-card-concepts) in a rate card. Credit grants apply to invoices after discounts, but before taxes and the `invoice_credit_balance`. Learn more about [credit grant applicability scopes](https://docs.stripe.com/billing/subscriptions/usage-based-v2/billing-credits/about.md#scopes). |
| Credit grant eligibility   | You can apply credit grants to invoices if all of the following are true:                                                                                                                                                                                                                                                                                                                                                                                    |

  - The invoice’s [period_end](https://docs.stripe.com/api/invoices/object.md#invoice_object-period_end) is on or after the credit grant’s [effective_at](https://docs.stripe.com/api/billing/credit-grant/object.md#billing_credit_grant_object-effective_at) time.
  - The credit grant has an available balance when the invoice finalizes.
  - The credit grant’s currency matches the invoice currency.

  You can only apply credit grants to subscription items that use [metered](https://docs.stripe.com/api/prices/object.md#price_object-recurring-usage_type) prices and report usage through [Meters](https://docs.stripe.com/api/billing/meter.md).

  You can’t apply credit grants to:

  - One-off invoices that weren’t created by a subscription.
  - [Line items](https://docs.stripe.com/api/invoices/object.md#invoice_object-lines) on subscription invoices that use [licensed](https://docs.stripe.com/api/v2/licensed-items.md?api-version=preview) items.
  - [Line items](https://docs.stripe.com/api/invoices/object.md#invoice_object-lines) on subscription invoices that use [metered](https://docs.stripe.com/api/prices/object.md#price_object-recurring-usage_type) items but report usage through legacy [Usage Records](https://docs.stripe.com/api/usage_records.md). |
| Unused credit grants limit | Customers can have up to 20 active credit grants at a time. If you issue a credit grant after this limit, the request fails with an error message stating the max limit. A credit grant is active if it has a future effective date or a positive ledger balance.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Credit balance summary     | The [Credit Balance Summary](https://docs.stripe.com/api/billing/credit-balance-summary.md) shows the following for a customer:

  - Ledger balance: A credit grant backed by an immutable ledger. The balance amount reflects the billing credit balance after recording all relevant account ledger transactions.
  - Available balance: The billing credit balance available for the customer to use. This amount is equal to the ledger balance less any consumed credits or expired credits.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Credit balance transaction | A [Credit Balance Transaction](https://docs.stripe.com/api/billing/credit-balance-transaction.md) includes the credits and debits that impact a credit grant. For example, you might see a credit transaction for initial funding of the credit grant, or a debit transaction for a credit grant on an invoice.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Voiding                    | [Voiding an invoice](https://docs.stripe.com/api/invoices/void.md) with credits applied reinstates the applied balance to the credit grant. If the credit grant is past the expiration date, the reinstated credits expire immediately. Issuing a [Credit Note](https://docs.stripe.com/api/credit_notes/object.md) doesn’t refund credit grants applied to an invoice. To restore those billing credits, you must create a new credit grant.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

## Credit grant states 

Credit grants have the following states:

| State    | Description                                                                                                                                                                                                                                                                                                                                                                   |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Pending  | The [available_balance](https://docs.stripe.com/api/billing/credit-balance-summary/object.md#billing_credit_balance_summary_object-balances-available_balance) on the credit grant isn’t yet available for use.                                                                                                                                                               |
| Granted  | The credit grant is eligible for use based on the [effective_at](https://docs.stripe.com/api/billing/credit-grant/object.md#billing_credit_grant_object-effective_at) timestamp, which must occur in the future. If you don’t set this field, the credit grant is effective immediately.                                                                                      |
| Depleted | The credit grant’s available balance has been consumed.                                                                                                                                                                                                                                                                                                                       |
| Expired  | You can immediately [expire](https://docs.stripe.com/api/billing/credit-grant/expire.md) any remaining credits on a credit grant, or you can specify an expiration time for the credit grant using the [expires_at](https://docs.stripe.com/api/billing/credit-grant/object.md#billing_credit_grant_object-expires_at) field. Credits won’t expire unless you set this field. |
| Voided   | You can only [void](https://docs.stripe.com/api/billing/credit-grant/void.md) credit grants that you haven’t applied to an invoice, either partially or completely. You can’t apply voided credit grants to future invoices.                                                                                                                                                  |

## Credit grant applicability scopes 

You can apply credit grants at any of the scopes described in the following table.

| Scope                           | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Billable item level             | When creating a credit grant, you can configure the applicability scope to specify a list of [billable items](https://docs.stripe.com/api/billing/credit-grant/create.md?api-version=preview#create_billing_credit_grant-applicability_config-scope-billable_items) which you want to apply the credit grant to. Only [metered items](https://docs.stripe.com/api/v2/metered-items.md?api-version=preview) are supported ([licensed items](https://docs.stripe.com/api/v2/licensed-items.md?api-version=preview) aren’t). The credit grant is drawn down by metered items on your invoices. |
| Multiple invoices or line items | If you apply a credit grant to multiple invoices, the credit applies first to the invoice that finalizes first. In the event that subscription invoices finalize at the exact same time, we can’t guarantee the finalization order. If you apply a credit grant to multiple [lines](https://docs.stripe.com/api/invoices/object.md#invoice_object-lines) on the same invoice, the credit applies to the lines in the order they appear on the invoice.                                                                                                                                      |
| Multiple credit grants          | If you apply multiple credit grants to an invoice or line item, they’re prioritized as follows:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |

  - **Priority**: Credit grants with higher [priority](https://docs.stripe.com/api/billing/credit-grant/object.md#billing_credit_grant_object-priority) (lower number indicates a higher priority) apply first.
  - **Expiration date**: Credit grants with earlier [expires_at](https://docs.stripe.com/api/billing/credit-grant/object.md#billing_credit_grant_object-expires_at) timestamps apply first.
  - **Category**: Credit grants with the `promotional` category apply first.
  - **Effective date**: Credit grants with earlier [effective_at](https://docs.stripe.com/api/billing/credit-grant/object.md#billing_credit_grant_object-effective_at) timestamps apply first.
  - **Created date**: Credit grants with earlier [created](https://docs.stripe.com/api/billing/credit-grant/object.md#billing_credit_grant_object-created) timestamps apply first. |
| Finalized invoices              | Credits apply to invoices only at the time of [finalization](https://docs.stripe.com/invoicing/integration/workflow-transitions.md#finalized). If you apply credits to a [preview](https://docs.stripe.com/api/invoices/create_preview.md) invoice, those credits might change if a finalized invoice uses them first.
  - Example 1: At the end of a cycle, the same set of credits appear on both a draft invoice and a preview invoice. When finalized, the draft invoice uses the credits. The preview invoice adjusts to accurately reflect any remaining credits from the credit grant.
  - Example 2: A customer has multiple active subscriptions and the same set of credits appear on a preview invoice for all of the subscriptions. If there aren’t enough credits to apply to all the subscriptions when the invoices finalize, only some invoices receive the credits.                                                                                        |

## Unused credit grants limit

Customers can have up to 100 unused credit grants at a time. If you issue a credit grant after this limit, the request fails with an error message stating the max limit.

### When a credit grant is unused

A credit grant is unused if all of the following are true:

- The credit grant isn’t voided.
- The credit grant isn’t past its [expires_at](https://docs.stripe.com/api/billing/credit-grant/object.md#billing_credit_grant_object-expires_at) time.
- The credit grant is either pending (before [effective_at](https://docs.stripe.com/api/billing/credit-grant/object.md#billing_credit_grant_object-effective_at)) or has a positive [ledger balance](https://docs.stripe.com/api/billing/credit-balance-summary/object.md#billing_credit_balance_summary_object-balances-ledger_balance).

### When a credit grant stops being unused

A credit grant no longer counts toward the limit if any of the following occur:

| Event    | Description                                                                                                                                               |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Depleted | The credit grant’s ledger balance is zero after applying credits to a finalized invoice.                                                                  |
| Expired  | The credit grant reaches its `expires_at` time, or you expire it using the [Expire](https://docs.stripe.com/api/billing/credit-grant/expire.md) endpoint. |
| Voided   | You void the credit grant using the [Void](https://docs.stripe.com/api/billing/credit-grant/void.md) endpoint.                                            |

### Available balance versus ledger balance

The unused credit grant limit is based on the [ledger balance](https://docs.stripe.com/api/billing/credit-balance-summary/object.md#billing_credit_balance_summary_object-balances-ledger_balance) and not the [available balance](https://docs.stripe.com/api/billing/credit-balance-summary/object.md#billing_credit_balance_summary_object-balances-available_balance). Credits only apply to invoices at the time of finalization. For example, a credit grant with a zero available balance and a positive ledger balance still counts toward the limit.

If credits from a credit grant appear on a draft invoice, the available balance might show zero, but the ledger balance remains positive until the invoice finalizes. In this case, the credit grant still counts toward the unused limit.


# Monitor usage with alerts

Set up alert(s) to trigger webhook(s) when a customer exceeds a usage threshold.

Create alerts to notify you when customers exceed meter usage thresholds (spend alerts). You can create alerts that apply to specific customers or all customers.

You can create alerts to:

- **Email users**: Use alerts to trigger webhooks that you can use to notify customers when they hit usage limits.
- **Deprovision access**: Grant customers a free number of usage units to your service, and remove access when they exceed the limit.
- **Notify the sales team of an upsell**: Alert your sales team of an enterprise opportunity when a self-serve user exceeds a usage threshold.

## Before you begin

Alerts have the following limitations:

| Alert type                                                                                                                                                                       | Event                                                                                                                          | Limitations                                                                                                                                                             |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Usage alerts                                                                                                                                                                     | [billing.alert.triggered](https://docs.stripe.com/api/events/types.md?api-version=preview#event_types-billing.alert.triggered) | - We evaluate alerts after you create the alert and report usage data. However, the evaluation includes usage data that you reported before you created the alert.      |
| - You can create a maximum of 25 alerts for each combination of a specific meter and customer. However, you can create an alert for a specific meter for each of your customers. |
| All alert types                                                                                                                                                                  |                                                                                                                                | - We evaluate alerts when you report usage data after you create the alert. However, the evaluation includes usage data that you reported before you created the alert. |
| - You can create a maximum of 25 alerts for each combination of a specific meter and customer. However, you can create an alert for a specific meter for each of your customers. |

## Create alerts

Set up alerts to get notified when customers exceed meter usage thresholds. You can create alerts that apply to either specific customers or all customers.

You can create alerts based on either usage or credit balance:

- **Usage alerts**: Create a one-time usage threshold alert for customers that triggers when they reach 100 API calls. When a customer reaches 100 API calls, you receive an event notifying you that the customer has exceeded the threshold.

- **Credit balance alerts**: Create a one-time credit balance alert for customers that triggers when their credit balance is 0 USD. When a customer reaches 0 USD of credits, you receive an event notifying you that the customer no longer has credits.

You can configure alerts to apply only to a specific customer, apply once per customer, or to apply only once to a specific customer by selecting both options:

- **Only apply to a specific customer**: Triggers when a customer exceeds the specified usage level and only triggers for the specified customer.
- **One time per customer**: Triggers once during the customer’s lifetime when a customer’s usage reaches the unit threshold.

You must [create a meter](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md#create-meter) before you create an alert.

You can configure [alerts](https://docs.stripe.com/api/billing/alert/create.md) using the Stripe Dashboard or API.

#### Dashboard

To set up meter usage threshold alerts:

1. Go to the [Billing alerts](https://dashboard.stripe.com/settings/billing/alerts) page, click **Create alert**.
1. In the alert editor:
   - For **Name**, enter the name for your alert. This isn’t visible to customers.
   - For **Alert Type**, specify **Meter usage**
   - Under **Alert type**, select the meter that you want to set up alerts for.
   - Set the usage amount to reach for an alert to trigger.
   - (Optional) Under **Apply to**, select **Specific customer** and the customer name, if you want the alert to apply only to that customer. Otherwise, leave the default of **Any customer** to configure the alert for all customers.
   - Click **Create alert**.

#### API

To create a meter usage threshold alert:

```curl
curl https://api.stripe.com/v1/billing/alerts \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d title="Sample alert" \
  -d alert_type=usage_threshold \
  -d "usage_threshold[filters][0][type]"=customer \
  -d "usage_threshold[filters][0][customer]"="{{CUSTOMER_ID}}" \
  -d "usage_threshold[meter]"=mtr_1234 \
  -d "usage_threshold[gte]"=100 \
  -d "usage_threshold[recurrence]"=one_time
```

To create a credit balance threshold alert:

```curl
curl https://api.stripe.com/v1/billing/alerts \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d title="Sample alert" \
  -d alert_type=credit_balance_threshold \
  -d "credit_balance_threshold[lte][monetary][value]"=0 \
  -d "credit_balance_threshold[lte][monetary][currency]"=usd \
  -d "credit_balance_threshold[lte][balance_type]"=monetary
```

To create a credit balance threshold alert that triggers when specific credits are depleted:

```curl
curl https://api.stripe.com/v1/billing/alerts \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d title="Sample alert" \
  -d alert_type=credit_balance_threshold \
  -d "credit_balance_threshold[lte][monetary][value]"=0 \
  -d "credit_balance_threshold[lte][monetary][currency]"=usd \
  -d "credit_balance_threshold[lte][balance_type]"=monetary \
  -d "credit_balance_threshold[lte][filters][0][type]"=customer \
  -d "credit_balance_threshold[lte][filters][0][customer]"={{CUSTOMER_ID}} \
  -d "credit_balance_threshold[lte][filters][0][credit_grants][applicability_config][scope][billable_items][0][id]"=BILLABLE_ITEM_ID
```

### Recovery alerts

Recovery alerts are a feature specific to credit balance threshold alerts. When a customer’s credit balance falls to or below the configured threshold, a `billing.alert.triggered` event fires. If the customer’s credit balance later goes back above the threshold (for example, when they purchase additional credits), a `billing.alert.recovered` event fires.

This allows you to build workflows that respond to both states:

- **When credits are depleted**: Notify customers, restrict access to services, or prompt them to purchase more credits.
- **When credits are restored**: Re-enable access to services, send confirmation emails, or update internal systems.

Recovery alerts are automatically enabled for all credit balance threshold alerts—no additional configuration is required.

## Listen for events 

After you configure an alert and start sending usage for that meter, you can listen for [events](https://docs.stripe.com/webhooks.md) that trigger when there’s a status change in Stripe, such as creating a new subscription or invoice.

For credit balance threshold alerts, you can listen for two event types:

- `billing.alert.triggered`: Fires when a customer’s credit balance falls to or below the threshold.
- `billing.alert.recovered`: Fires when a customer’s credit balance goes back above the threshold after being triggered.

In your application, set up an HTTP handler to accept a POST request containing the event, and verify the signature of the event.

```ruby


post '/webhook' do
# You can use webhooks to receive information about asynchronous payment events.
# For more information, see https://stripe.com/docs/webhooks.
webhook_secret = ENV['STRIPE_WEBHOOK_SECRET']
payload = request.body.read
if !webhook_secret.empty?
  # Retrieve the event by verifying the signature using the raw body and secret, if webhook signing is configured.
  sig_header = request.env['HTTP_STRIPE_SIGNATURE']
  event = nil

  begin
    event = Stripe::Webhook.construct_event(
      payload, sig_header, webhook_secret
    )
  rescue JSON::ParserError => e
    # Invalid payload
    status 400
    return
  rescue Stripe::SignatureVerificationError => e
    # Invalid signature
    puts '⚠️  Webhook signature verification failed.'
    status 400
    return
  end
else
  data = JSON.parse(payload, symbolize_names: true)
  event = Stripe::Event.construct_from(data)
end
# Get the type of webhook event sent, which checks the status of PaymentIntents.
event_type = event['type']
data = event['data']
data_object = data['object']

if event_type == 'billing.alert.triggered'
  # Fires when the meter exceeds the defined threshold in the alert,
  # or when a customer's credit balance falls to or below the threshold.
  # Only triggers if it matches to at least one Stripe customer.
  # Example: Restrict access to services when usage has exceeded threhhold or credits are depleted.
elsif event_type == 'billing.alert.recovered'
  # Fires when a customer's credit balance goes back above the threshold
  # after a billing.alert.triggered event. Only applicable to credit balance alerts.
  # Example: Re-enable access to services when credits are restored.
end

content_type 'application/json'
{ status: 'success' }.to_json
end
```

During development, use the Stripe CLI to [monitor webhooks and forward them to your application](https://docs.stripe.com/webhooks.md#test-webhook). Run the following in a new terminal while your development app is running:

```
stripe listen --thin-events '*' --forward-thin-to localhost:4242/webhook
```

For production, set up a webhook endpoint URL in the Dashboard, or use [webhook endpoints](https://docs.stripe.com/api/webhook_endpoints.md).


# Monitor pricing plan events

Learn which events to monitor in your pricing plan integration.

Pricing plans, pricing plan subscriptions, and pricing plan components send [v2 Events](https://docs.stripe.com/api/v2/core/events.md?api-version=preview). To handle these events, configure an [Event Destination](https://docs.stripe.com/api/v2/core/event_destinations.md?api-version=preview) and direct it to your webhook endpoint. You can either:

- Create the Event Destination from [Workbench](https://docs.stripe.com/workbench/event-destinations.md).
- Create the Event Destination [through the Stripe API](https://docs.stripe.com/api/v2/core/event_destinations.md?api-version=preview).

See an example of how to [set up your webhook endpoint to handle these events](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md#monitor-servicing-events).

The following table describes the most common events related to pricing plans.

| Event                                       | Description                                                                                |
| ------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `v2.billing.pricing_plan.created`           | Sent when you create a pricing plan.                                                       |
| `v2.billing.pricing_plan.updated`           | Sent when you update a pricing plan.                                                       |
| `v2.billing.pricing_plan_component.created` | Sent when you create a pricing plan component.                                             |
| `v2.billing.pricing_plan_component.updated` | Sent when you update a pricing plan component.                                             |
| `v2.billing.pricing_plan_version.created`   | Sent when you add or update a component version, which creates a new pricing plan version. |

## Pricing plan subscription events 

Activating or canceling subscriptions triggers [v2 Events](https://docs.stripe.com/api/v2/core/events.md?api-version=preview). You can listen for events by using [Event Destinations](https://docs.stripe.com/api/v2/core/event_destinations.md?api-version=preview).

The following table describes the most common events related to pricing plan subscriptions. Use the event notifications to build your provisioning logic.

| Event                                                                      | Description                                                                                                    |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `v2.billing.pricing_plan_subscription.servicing_activated`                 | Sent when a customer pays the subscription that activates the service.                                         |
| `v2.billing.pricing_plan_subscription.servicing_paused`                    | Sent when the subscription is paused.                                                                          |
| `v2.billing.pricing_plan_subscription.servicing_canceled`                  | Sent when a customer cancels the subscription.                                                                 |
| `v2.billing.pricing_plan_subscription.collection_current`                  | Indicates that collection on the subscription is ongoing. Sent when the collection status is set to `current`. |
| `v2.billing.pricing_plan_subscription.collection_awaiting_customer_action` | Sent when collection is waiting for the customer to take action.                                               |
| `v2.billing.pricing_plan_subscription.collection_paused`                   | Sent when collection is paused.                                                                                |
| `v2.billing.cadence.created`                                               | Sent when you create a billing interval.                                                                       |
| `v2.billing.cadence.canceled`                                              | Sent when the billing interval status moves to canceled.                                                       |
| `v2.billing.cadence.billed`                                                | Sent when the billing interval is billed.                                                                      |
| `v2.billing.cadence.errored`                                               | Sent when an error occurs while generating the invoice.                                                        |

## Rate card events

The following table describes the most common events related to rate cards.

| Event                                  | Description                               |
| -------------------------------------- | ----------------------------------------- |
| `v2.billing.rate_card.created`         | Sent when you create a rate card.         |
| `v2.billing.rate_card.updated`         | Sent when you update a rate card.         |
| `v2.billing.rate_card_rate.created`    | Sent when you create a rate card rate.    |
| `v2.billing.rate_card_version.created` | Sent when you create a rate card version. |
| `v2.billing.metered_item.created`      | Sent when you create a metered item.      |
| `v2.billing.metered_item.updated`      | Sent when you update a metered item.      |

## License fee events

The following table describes the most common events related to license fees.

| Event                                    | Description                                 |
| ---------------------------------------- | ------------------------------------------- |
| `v2.billing.license_fee.created`         | Sent when you create a license fee.         |
| `v2.billing.license_fee.updated`         | Sent when you update a license fee.         |
| `v2.billing.license_fee_version.created` | Sent when you create a license fee version. |
| `v2.billing.licensed_item.created`       | Sent when you create a licensed item.       |
| `v2.billing.licensed_item.updated`       | Sent when you update a licensed item.       |


# Analyze and query meter usage

Learn how to query and analyze meter usage data.

Use the [Meter Usage Analytics API](https://docs.stripe.com/api/billing/analytics/meter-usage.md) to query and analyze your customers’ meter usage data. This enables you to build custom usage dashboards, generate reports, and determine consumption patterns across your meters.

This API is available in public preview.  to request access to this API.

## Query usage data

The [Meter Usage Analytics API](https://docs.stripe.com/api/billing/analytics/meter-usage.md)  returns aggregated usage data for a customer within a specified time interval. You can query for data by time periods, filter by meter dimensions, and query across multiple meters simultaneously.

> The API parameters were updated in the 2025-09-30.preview release. See the [changelog](https://docs.stripe.com/changelog/clover/2025-09-30/update-meter-usage-fields.md) to understand how the request and response shapes changed.

### Fetch usage for a single meter

Retrieve usage data for a specific customer and meter over a time range:

```curl
curl -G https://api.stripe.com/v1/billing/analytics/meter_usage \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d starts_at=1735689600 \
  -d ends_at=1738368000 \
  -d customer={{CUSTOMER_ID}} \
  -d "meters[0][meter]"={{METER_ID}} \
  -d value_grouping_window=day \
  --data-urlencode timezone="America/New_York"
```

### Fetch usage for a meter filtered and grouped by meter dimension

Query usage data that’s filtered by premium tier and grouped by model:

```curl
curl -G https://api.stripe.com/v1/billing/analytics/meter_usage \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d starts_at=1735689600 \
  -d ends_at=1738368000 \
  -d customer={{CUSTOMER_ID}} \
  -d "meters[0][meter]"={{METER_ID}} \
  -d "meters[0][dimension_group_by_keys][0]"=model \
  -d "meters[0][dimension_filters][tier]"=premium \
  -d value_grouping_window=day
```

### Fetch usage for a meter filtered by tenant

Query usage data that’s filtered by premium tier and grouped by model:

```curl
curl -G https://api.stripe.com/v1/billing/analytics/meter_usage \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d starts_at=1735689600 \
  -d ends_at=1738368000 \
  -d customer={{CUSTOMER_ID}} \
  -d "meters[0][meter]"={{METER_ID}} \
  -d "meters[0][tenant_filters][user_id]"=a8238bf39a1 \
  -d value_grouping_window=day
```

### Fetch usage across multiple meters

Query usage across multiple meters with different filters and groupings:

```curl
curl -G https://api.stripe.com/v1/billing/analytics/meter_usage \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d starts_at=1735689600 \
  -d ends_at=1738368000 \
  -d customer={{CUSTOMER_ID}} \
  -d "meters[0][meter]"={{METER_ID_1}} \
  -d "meters[0][dimension_group_by_keys][0]"=model \
  -d "meters[0][dimension_group_by_keys][1]"=tier \
  -d "meters[1][meter]"={{METER_ID_2}} \
  -d "meters[1][dimension_filters][region]"=us-east \
  -d value_grouping_window=day
```

### Build usage dashboards

You can use the API data to create visualizations, such as stacked charts that show usage across different dimensions. The following example demonstrates how you can structure data for a chart that shows API usage by model:

```curl
curl -G https://api.stripe.com/v1/billing/analytics/meter_usage \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d starts_at=1735689600 \
  -d ends_at=1738368000 \
  -d customer={{CUSTOMER_ID}} \
  -d "meters[0][meter]"={{METER_ID}} \
  -d "meters[0][dimension_group_by_keys][0]"=model \
  -d value_grouping_window=day
```

An example response to this request looks like:

**View response**

```json
{
  "data": [
    {
      "starts_at": 1735689600,
      "ends_at": 1735776000,
      "value": 1500,
      "meter": "mtr_1234567890",
      "dimensions": {
        "model": "gpt-4"
      }
    },
    {
      "starts_at": 1735689600,
      "ends_at": 1735776000,
      "value": 800,
      "meter": "mtr_1234567890",
      "dimensions": {
        "model": "gpt-3.5-turbo"
      }
    },
    {
      "starts_at": 1735776000,
      "ends_at": 1735862400,
      "value": 2100,
      "meter": "mtr_1234567890",
      "dimensions": {
        "model": "gpt-4"
      }
    },
    {
      "starts_at": 1735776000,
      "ends_at": 1735862400,
      "value": 950,
      "meter": "mtr_1234567890",
      "dimensions": {
        "model": "gpt-3.5-turbo"
      }
    }
  ]
}
```

Use this example code to pull data from the API in your back end and display it to users as a stacked bar chart in your front end.

**Your back end**

```javascript
// Step 1: Extract the data from the Stripe API response
const data = stripeApiResponse.data;

// Step 2: Create a dictionary to store the processed data
const processedData = {};

// Step 3: Iterate through the data and organize it by date and model
data.forEach(point => {
  const date = new Date(point.bucket_start_time * 1000).toISOString().split('T')[0];
  const model = point.dimensions.model;
  const value = point.bucket_value;

  if (!processedData[date]) {
    processedData[date] = {};
  }

  processedData[date][model] = value;
});

// Step 4: Create a list of unique models and sort them
const models = [...new Set(data.map(point => point.dimensions.model))].sort();

// Step 5: Prepare the data for charting
const chartData = [];
Object.keys(processedData).sort().forEach(date => {
  const dataPoint = { date };
  let cumulativeValue = 0;

  models.forEach(model => {
    const value = processedData[date][model] || 0;
    dataPoint[`${model}_start`] = cumulativeValue;
    cumulativeValue += value;
    dataPoint[`${model}_end`] = cumulativeValue;
    dataPoint[model] = value; // For simple stacked charts
  });

  chartData.push(dataPoint);
});

// Return chart data for front end chart library usage
return chartData;
```

**Your front end**

```javascript
// Step 1: Fetch usage chart data from your back end
const chartData = await fetch('/api/customer_usage/:customer_id').then(r => r.json());

// Step 2: Extract unique models from the chart data
const models = Object.keys(chartData[0]).filter(key =>
  key !== 'date' && !key.endsWith('_start') && !key.endsWith('_end')
);

// Step 3: Use the chart data to create your stacked bar chart
// Example using D3 or Recharts:
createStackedChart({
  data: chartData.map(point => ({
    date: point.date,
    'gpt-4': point['gpt-4'] || 0,
    'gpt-3.5-turbo': point['gpt-3.5-turbo'] || 0
  })),
  stackKeys: models,
  xKey: 'date',
  title: 'Daily API Usage by Model'
});
```

### Rate limits

The Meter Usage Analytics API has its own rate limit of 100 requests per second per account, which is separate from the Stripe overall API rate limits. If you exceed this limit, the API returns a `429 Too Many Requests` status code.

### Event timestamp granularity

The Meter Usage Analytics API truncates event timestamps to the nearest 15 minutes. For example, an event with `event_timestamp` of `08:42:15` is stored in our analytics database with a timestamp of `08:30:00`.

## Best practices

### Handle data freshness

Usage data might have a slight delay. You can use the `data_refreshed_at` field in the response to understand data freshness. Also consider this latency when building real-time dashboards or alerts.

### Customize your queries

Follow these best practices:

- Use appropriate `value_grouping_window` values to balance granularity with performance.
- Apply `dimension_filters` to reduce data volume when you only need specific segments.
- Query multiple meters in a single request when analyzing related usage patterns.

### Data size limits

To prevent overly large responses, the following limits apply per meter:

- A maximum of 5 `meters`
- A maximum of 2 `dimension_group_by_keys`
- A maximum of 10 `dimension_filters`
- A maximum of 3 `tenant_filters`

### Handle errors

The API returns standard HTTP status codes and structured error responses:

```json
{
  "error": {
    "type": "invalid_request_error",
    "code": "invalid_time_range",
    "message": "Param start_time should not be greater than end_time"
  }
}
```


# Manage your usage-based billing setup

Learn how to handle billing-related tasks for your usage-based billing model.

After you create your usage-based billing model, you can modify different parts of your billing setup. For example, you can update a subscription item’s price during a billing period, backdate a subscription to include usage in the next invoice, or cancel usage-based subscriptions.

## Transform quantities

You can use the [transform_quantity](https://docs.stripe.com/api/prices/create.md#create_price-transform_quantity) option to transform usage before applying the price, which you can use when you want pricing on packages of a product instead of individual units. This allows you to divide the reported usage by a specific number and round the result up or down.

> Quantity transformation isn’t compatible with [tiered pricing](https://docs.stripe.com/billing/subscriptions/usage-based/thresholds.md#tiered-pricing-threshold).

For example, say you have a car rental service and you want to charge customers for each hour they rent a car. In this case, you report usage as a number of minutes.

```curl
curl https://api.stripe.com/v1/products \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d name="Car Rental Service"
```

```cli
stripe products create  \
  --name="Car Rental Service"
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

product = client.v1.products.create({name: 'Car Rental Service'})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
product = client.v1.products.create({"name": "Car Rental Service"})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$product = $stripe->products->create(['name' => 'Car Rental Service']);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

ProductCreateParams params =
  ProductCreateParams.builder().setName("Car Rental Service").build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
Product product = client.v1().products().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const product = await stripe.products.create({
  name: 'Car Rental Service',
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.ProductCreateParams{Name: stripe.String("Car Rental Service")}
result, err := sc.V1Products.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new ProductCreateOptions { Name = "Car Rental Service" };
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Products;
Product product = service.Create(options);
```

Create a price for the car rental service product. Charge 10 USD per hour, and round up to charge for a full hour, even if the customer uses only part of the hour.

```curl
curl https://api.stripe.com/v1/prices \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d nickname="Car Rental Per Hour Rate" \
  -d unit_amount=1000 \
  -d currency=usd \
  -d "recurring[interval]"=month \
  -d "recurring[usage_type]"=metered \
  -d product={{CAR_RENTAL_SERVICE_PRODUCT_ID}} \
  -d "transform_quantity[divide_by]"=60 \
  -d "transform_quantity[round]"=up
```

```cli
stripe prices create  \
  --nickname="Car Rental Per Hour Rate" \
  --unit-amount=1000 \
  --currency=usd \
  -d "recurring[interval]"=month \
  -d "recurring[usage_type]"=metered \
  --product={{CAR_RENTAL_SERVICE_PRODUCT_ID}} \
  -d "transform_quantity[divide_by]"=60 \
  -d "transform_quantity[round]"=up
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

price = client.v1.prices.create({
  nickname: 'Car Rental Per Hour Rate',
  unit_amount: 1000,
  currency: 'usd',
  recurring: {
    interval: 'month',
    usage_type: 'metered',
  },
  product: '{{CAR_RENTAL_SERVICE_PRODUCT_ID}}',
  transform_quantity: {
    divide_by: 60,
    round: 'up',
  },
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
price = client.v1.prices.create({
  "nickname": "Car Rental Per Hour Rate",
  "unit_amount": 1000,
  "currency": "usd",
  "recurring": {"interval": "month", "usage_type": "metered"},
  "product": "{{CAR_RENTAL_SERVICE_PRODUCT_ID}}",
  "transform_quantity": {"divide_by": 60, "round": "up"},
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$price = $stripe->prices->create([
  'nickname' => 'Car Rental Per Hour Rate',
  'unit_amount' => 1000,
  'currency' => 'usd',
  'recurring' => [
    'interval' => 'month',
    'usage_type' => 'metered',
  ],
  'product' => '{{CAR_RENTAL_SERVICE_PRODUCT_ID}}',
  'transform_quantity' => [
    'divide_by' => 60,
    'round' => 'up',
  ],
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

PriceCreateParams params =
  PriceCreateParams.builder()
    .setNickname("Car Rental Per Hour Rate")
    .setUnitAmount(1000L)
    .setCurrency("usd")
    .setRecurring(
      PriceCreateParams.Recurring.builder()
        .setInterval(PriceCreateParams.Recurring.Interval.MONTH)
        .setUsageType(PriceCreateParams.Recurring.UsageType.METERED)
        .build()
    )
    .setProduct("{{CAR_RENTAL_SERVICE_PRODUCT_ID}}")
    .setTransformQuantity(
      PriceCreateParams.TransformQuantity.builder()
        .setDivideBy(60L)
        .setRound(PriceCreateParams.TransformQuantity.Round.UP)
        .build()
    )
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
Price price = client.v1().prices().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const price = await stripe.prices.create({
  nickname: 'Car Rental Per Hour Rate',
  unit_amount: 1000,
  currency: 'usd',
  recurring: {
    interval: 'month',
    usage_type: 'metered',
  },
  product: '{{CAR_RENTAL_SERVICE_PRODUCT_ID}}',
  transform_quantity: {
    divide_by: 60,
    round: 'up',
  },
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.PriceCreateParams{
  Nickname: stripe.String("Car Rental Per Hour Rate"),
  UnitAmount: stripe.Int64(1000),
  Currency: stripe.String(stripe.CurrencyUSD),
  Recurring: &stripe.PriceCreateRecurringParams{
    Interval: stripe.String(stripe.PriceRecurringIntervalMonth),
    UsageType: stripe.String(stripe.PriceRecurringUsageTypeMetered),
  },
  Product: stripe.String("{{CAR_RENTAL_SERVICE_PRODUCT_ID}}"),
  TransformQuantity: &stripe.PriceCreateTransformQuantityParams{
    DivideBy: stripe.Int64(60),
    Round: stripe.String(stripe.PriceTransformQuantityRoundUp),
  },
}
result, err := sc.V1Prices.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new PriceCreateOptions
{
    Nickname = "Car Rental Per Hour Rate",
    UnitAmount = 1000,
    Currency = "usd",
    Recurring = new PriceRecurringOptions { Interval = "month", UsageType = "metered" },
    Product = "{{CAR_RENTAL_SERVICE_PRODUCT_ID}}",
    TransformQuantity = new PriceTransformQuantityOptions { DivideBy = 60, Round = "up" },
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Prices;
Price price = service.Create(options);
```

If a customer rents the car for 150 minutes, that customer is charged 30 USD for 3 hours of rental (2 hours and 30 minutes, rounded up).

## Update prices mid-cycle 

You can update a subscription item’s price during a billing period.

With `billing_mode=flexible` subscriptions, we create an invoice item that bills for previously reported metered usage when you remove a metered price from a subscription.

For example, say you have a monthly subscription that you switch from price A to price B on January 16. On January 16, we create an invoice item billing for usage from January 1 to January 16. When the subscription renews on February 1, we bill for price B from January 16 to February 1.

The [proration_behavior](https://docs.stripe.com/api/subscriptions/update.md#update_subscription-proration_behavior) you specify when removing a metered price affects these metered invoice items. If you want to remove a metered price without billing for it, set `proration_behavior` to `none`.

With `billing_mode=classic` subscriptions, limitations apply when switching from one [meter price](https://docs.stripe.com/api/prices/object.md#price_object-recurring-meter) to another.

On future invoices, we reflect only usage that occurs after the update. For example, say you have a monthly subscription that you switch from price A to price B on January 16. At the end of the month, the invoice includes usage from January 16 to January 31 at price B. Usage from January 1 to January 16 isn’t billed.

An exception exists if you use [billing thresholds](https://docs.stripe.com/billing/subscriptions/usage-based/thresholds.md) and have a threshold invoice already generated at the old price. For example, say you generate a threshold invoice on January 10 using price A. You still charge that threshold invoice to the customer. At the end of the month, the invoice includes usage from January 16 to January 31 at price B. The earlier threshold invoice doesn’t offset any usage for this end-of-month invoice.

Similar restrictions apply if you add a new subscription item with a billing meter price in the middle of the service period. For example, say you add a new subscription item with price C on January 16. At the end of the month, the invoice includes usage from January 16 to January 31 at price C for that subscription item.

To capture previously reported usage when changing prices, choose one of these options:

- Report the aggregated usage again to capture it in the cycle on the new price.
- Reset the [billing_cycle_anchor](https://docs.stripe.com/api/subscriptions/update.md#update_subscription-billing_cycle_anchor) parameter to `now`, applying the old price to previously reported usage.

To update the price for a subscription item:

```curl
curl https://api.stripe.com/v1/subscription_items/{{SUBSCRIPTION_ITEM_ID}} \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d price={{NEW_PRICE_ID}}
```

```cli
stripe subscription_items update {{SUBSCRIPTION_ITEM_ID}} \
  --price={{NEW_PRICE_ID}}
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

subscription_item = client.v1.subscription_items.update(
  '{{SUBSCRIPTION_ITEM_ID}}',
  {price: '{{NEW_PRICE_ID}}'},
)
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
subscription_item = client.v1.subscription_items.update(
  "{{SUBSCRIPTION_ITEM_ID}}",
  {"price": "{{NEW_PRICE_ID}}"},
)
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$subscriptionItem = $stripe->subscriptionItems->update(
  '{{SUBSCRIPTION_ITEM_ID}}',
  ['price' => '{{NEW_PRICE_ID}}']
);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

SubscriptionItemUpdateParams params =
  SubscriptionItemUpdateParams.builder().setPrice("{{NEW_PRICE_ID}}").build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
SubscriptionItem subscriptionItem =
  client.v1().subscriptionItems().update("{{SUBSCRIPTION_ITEM_ID}}", params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const subscriptionItem = await stripe.subscriptionItems.update(
  '{{SUBSCRIPTION_ITEM_ID}}',
  {
    price: '{{NEW_PRICE_ID}}',
  }
);
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.SubscriptionItemUpdateParams{Price: stripe.String("{{NEW_PRICE_ID}}")}
result, err := sc.V1SubscriptionItems.Update(
  context.TODO(), "{{SUBSCRIPTION_ITEM_ID}}", params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new SubscriptionItemUpdateOptions { Price = "{{NEW_PRICE_ID}}" };
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.SubscriptionItems;
SubscriptionItem subscriptionItem = service.Update("{{SUBSCRIPTION_ITEM_ID}}", options);
```

To delete a subscription item:

```curl
curl -X DELETE https://api.stripe.com/v1/subscription_items/{{SUBSCRIPTION_ITEM_ID}} \
  -u "<<YOUR_SECRET_KEY>>:"
```

```cli
stripe subscription_items delete {{SUBSCRIPTION_ITEM_ID}}
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

deleted = client.v1.subscription_items.delete('{{SUBSCRIPTION_ITEM_ID}}')
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
deleted = client.v1.subscription_items.delete("{{SUBSCRIPTION_ITEM_ID}}")
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$deleted = $stripe->subscriptionItems->delete('{{SUBSCRIPTION_ITEM_ID}}', []);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

SubscriptionItemDeleteParams params = SubscriptionItemDeleteParams.builder().build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
SubscriptionItem subscriptionItem =
  client.v1().subscriptionItems().delete("{{SUBSCRIPTION_ITEM_ID}}", params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const deleted = await stripe.subscriptionItems.del('{{SUBSCRIPTION_ITEM_ID}}');
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.SubscriptionItemDeleteParams{}
result, err := sc.V1SubscriptionItems.Delete(
  context.TODO(), "{{SUBSCRIPTION_ITEM_ID}}", params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.SubscriptionItems;
SubscriptionItem deleted = service.Delete("{{SUBSCRIPTION_ITEM_ID}}");
```

After deletion, the invoice doesn’t reflect any usage from that item.

## Create a backdated subscription 

You can record usage for a customer even before creating a subscription for them. After recording usage for a customer, use the [backdate_start_date](https://docs.stripe.com/api/subscriptions/create.md#create_subscription-backdate_start_date) to create a subscription before the first report.

With `billing_mode=flexible` subscriptions, the subscription’s first invoice includes this backdated usage.

With `billing_mode=classic` subscriptions, the subscription’s next invoice, generated when it cycles, includes this backdated usage.

```curl
curl https://api.stripe.com/v1/subscriptions \
  -u "<<YOUR_SECRET_KEY>>:" \
  -d customer={{CUSTOMER_ID}} \
  -d "items[0][price]"={{PRICE_ID}} \
  -d backdate_start_date=1710000000
```

```cli
stripe subscriptions create  \
  --customer={{CUSTOMER_ID}} \
  -d "items[0][price]"={{PRICE_ID}} \
  --backdate-start-date=1710000000
```

```ruby
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = Stripe::StripeClient.new("<<YOUR_SECRET_KEY>>")

subscription = client.v1.subscriptions.create({
  customer: '{{CUSTOMER_ID}}',
  items: [{price: '{{PRICE_ID}}'}],
  backdate_start_date: 1710000000,
})
```

```python
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
client = StripeClient("<<YOUR_SECRET_KEY>>")

# For SDK versions 12.4.0 or lower, remove '.v1' from the following line.
subscription = client.v1.subscriptions.create({
  "customer": "{{CUSTOMER_ID}}",
  "items": [{"price": "{{PRICE_ID}}"}],
  "backdate_start_date": 1710000000,
})
```

```php
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
$stripe = new \Stripe\StripeClient('<<YOUR_SECRET_KEY>>');

$subscription = $stripe->subscriptions->create([
  'customer' => '{{CUSTOMER_ID}}',
  'items' => [['price' => '{{PRICE_ID}}']],
  'backdate_start_date' => 1710000000,
]);
```

```java
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
StripeClient client = new StripeClient("<<YOUR_SECRET_KEY>>");

SubscriptionCreateParams params =
  SubscriptionCreateParams.builder()
    .setCustomer("{{CUSTOMER_ID}}")
    .addItem(SubscriptionCreateParams.Item.builder().setPrice("{{PRICE_ID}}").build())
    .setBackdateStartDate(1710000000L)
    .build();

// For SDK versions 29.4.0 or lower, remove '.v1()' from the following line.
Subscription subscription = client.v1().subscriptions().create(params);
```

```node
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');

const subscription = await stripe.subscriptions.create({
  customer: '{{CUSTOMER_ID}}',
  items: [
    {
      price: '{{PRICE_ID}}',
    },
  ],
  backdate_start_date: 1710000000,
});
```

```go
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
sc := stripe.NewClient("<<YOUR_SECRET_KEY>>")
params := &stripe.SubscriptionCreateParams{
  Customer: stripe.String("{{CUSTOMER_ID}}"),
  Items: []*stripe.SubscriptionCreateItemParams{
    &stripe.SubscriptionCreateItemParams{Price: stripe.String("{{PRICE_ID}}")},
  },
  BackdateStartDate: stripe.Int64(1710000000),
}
result, err := sc.V1Subscriptions.Create(context.TODO(), params)
```

```dotnet
// Set your secret key. Remember to switch to your live secret key in production.
// See your keys here: https://dashboard.stripe.com/apikeys
var options = new SubscriptionCreateOptions
{
    Customer = "{{CUSTOMER_ID}}",
    Items = new List<SubscriptionItemOptions>
    {
        new SubscriptionItemOptions { Price = "{{PRICE_ID}}" },
    },
    BackdateStartDate = DateTimeOffset.FromUnixTimeSeconds(1710000000).UtcDateTime,
};
var client = new StripeClient("<<YOUR_SECRET_KEY>>");
var service = client.V1.Subscriptions;
Subscription subscription = service.Create(options);
```

## Cancel usage-based subscriptions 

With usage-based billing, the bill the customer pays varies based on consumption during the billing period. When changing the billing period results in a service period ending early, you charge the customer for the usage accrued during the shortened billing period.

> We don’t support [proration](https://docs.stripe.com/billing/subscriptions/prorations.md) with usage-based billing.

You can’t reactivate canceled subscriptions. Instead, you can collect updated billing information from your customer, update their default payment method, and create a new subscription with their existing customer record.

If you use [cancel_at_period_end](https://docs.stripe.com/api/subscriptions/update.md#update_subscription-cancel_at_period_end) to schedule the cancellation of a subscription, you can reactivate the subscription at any time up to the end of the period. To do so, update `cancel_at_period_end` to `false`.

For subscriptions that cancel at the end of the period, the final invoice at the end of the period includes metered usage from the last billing period.


# Advanced usage-based billing

Learn how you can use advanced usage-based billing to build your business on Stripe.

SaaS and AI businesses often want to charge customers based on the usage of their product while also charging flat recurring fees and burning down credits. Advanced usage-based billing lets you:

- Define and charge customers based on specific usage data characteristics (dimensions) and manage dozens to hundreds of prices per meter
- Set up real-time credit burndown and automate credit issuance
- Roll out new usage-based prices to all your users

Supported pricing models include:

- Pay as you go for many prices or meters
- Flat fee and overages
- Credit burndown with automatic top-ups

If the features and compatibility described on this page sound like they’re for you, sign up for the private preview.

## Advanced usage-based billing concepts

With advanced usage-based billing, you use pricing plans to group a set of pricing components into a single package that you can charge for. You subscribe customers to one pricing plan that contains one or more components for usage-based pricing, recurring fees, or recurring credits. You can modify existing components or add new ones to pricing plans to create new versions of that plan and choose whether to migrate existing customers to the latest version or not.

| Term                      | Definition                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Pricing plan              | A customizable container of pricing components (such as rate cards, license fees, and recurring credit grants) that defines how you bill for your service. For example, you can create a pricing plan that includes [rate cards](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md) for usage-based billing, [license fees](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/license-fees/about.md) for recurring charges, and [service actions](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/service-actions/about.md) for recurring credit grant allocations. When a customer subscribes to a pricing plan, all the recurring components are automatically enrolled and billed according to the cadence you configure. |
| Pricing plan component    | A part of the pricing plan, such as a [rate card](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md), [license fee](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/license-fees/about.md), or [service action](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/service-actions/about.md). Each component has a version to ensure that they’re used consistently in pricing plans. If you don’t specify a component version when you attach it to the pricing plan, the default version is used.                                                                                                                                                                                                                           |
| Pricing plan subscription | A pricing plan subscription is created when a customer is subscribed to a specific pricing plan version. Subscriptions generate and charge customers according to an underlying billing cadence.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Pricing plan version      | A pricing plan version is a versioned snapshot of a pricing plan. When you create a pricing plan, you need to set a live version before you can activate the plan or subscribe customers to it. Modifying or deleting existing components creates a new version. Adding a license fee or service action creates a new version. Adding a rate card doesn’t create a new version. When subscribing customers, you can specify a version or let Stripe assign the current live version. Customers stay on their assigned version unless manually changed, which lets you set different pricing for new and existing customers.                                                                                                                                                                            |

A pricing plan can contain any combination of:

- [A rate card](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md)
- [A license fee](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/license-fees/about.md)
- [A service action](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/service-actions/about.md)

Here’s what a pricing plan looks like with all of its components.
![Example image of a pricing plan with a rate card, license fee, and service action](https://b.stripecdn.com/docs-statics-srv/assets/pricing-plan.295b34e2ba8880b8c20edc782958f4a9.png)

A pricing plan with a rate card, license fee, and service action.

Here’s an example of what a complete pricing plan looks like with *Checkout* (A low-code payment integration that creates a customizable form for collecting payments. You can embed Checkout directly in your website, redirect customers to a Stripe-hosted payment page, or create a customized checkout page with Stripe Elements). Learn how to [use Checkout to subscribe customers to a pricing plan](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md?payment-ui=checkout).
![Pricing plan example](https://b.stripecdn.com/docs-statics-srv/assets/checkout_pricing_plan_example.2156a15535345b113c30e7efabe72867.png)

A pricing plan displayed in Stripe Checkout

## Compare advanced and classic usage-based billing

Read the following sections to understand the basic differences between advanced and classic usage-based billing and which one works best for your business.

Classic and advanced usage based billing have different architectures.

- With classic usage-based billing, you subscribe your customers directly to prices for each item you want to bill for (based on usage or a flat recurring fee). Each usage-based price is connected to a meter that records usage.

- With advanced usage-based billing, you model the components of your plan (license fee, rate card, and service actions) and subscribe your customer to that plan.

### Classic usage-based billing
Usage-based billing with pricing models (See full diagram at https://docs.stripe.com/billing/subscriptions/usage-based/advanced/compare)
### Advanced usage-based billing
 (See full diagram at https://docs.stripe.com/billing/subscriptions/usage-based/advanced/compare)
The following sections describe the key differences in feature support and compatibility between advanced usage-based billing that uses pricing plans and the classic usage-based billing that uses products and prices.

### Billing functionality and feature support

The following table describes the use cases supported by pricing plans.

| Use case                                                                                                                                                             | **CLASSIC**   | [**ADVANCED**](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md) (Private preview) |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------ |
| [Set up multiple items per subscription](https://docs.stripe.com/billing/subscriptions/usage-based/rate-cards/about.md#create-rate-card)                             | 20            | Up to 500                                                                                                    |
| [Discounts and promo codes](https://docs.stripe.com/billing/subscriptions/coupons.md)                                                                                | ✓ Supported   | - Unsupported                                                                                                |
| [Promotional billing credits](https://docs.stripe.com/billing/subscriptions/usage-based/billing-credits.md)                                                          | ✓ Supported   | ✓ Supported                                                                                                  |
| [Trials](https://docs.stripe.com/billing/subscriptions/trials.md)                                                                                                    | ✓ Supported   | - Unsupported                                                                                                |
| [Roll out prices to all subscribers without code](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions/manage.md#roll-out-prices)   | - Unsupported | ✓ Supported                                                                                                  |
| [Set up different pricing versions by user cohort](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans/subscriptions/manage.md#customer-cohorts) | - Unsupported | ✓ Supported                                                                                                  |
| [Automate changes to subscriptions over time](https://docs.stripe.com/billing/subscriptions/subscription-schedules.md)                                               | ✓ Supported   | Coming soon                                                                                                  |
| [Automate sending threshold invoices](https://docs.stripe.com/billing/subscriptions/usage-based/alerts.md)                                                           | ✓ Supported   | - unsupported                                                                                                |
| [Configure an invoice finalization grace period](https://docs.stripe.com/billing/subscriptions/usage-based/configure-grace-period.md)                                | ✓ Supported   | 1 hour (non-configurable)                                                                                    |

### Stripe products support

The following table describes which products and features each integration path supports.

| Stripe product feature                                                                   | **CLASSIC**   | [**ADVANCED**](https://docs.stripe.com/billing/subscriptions/usage-based/pricing-plans.md) (Private preview) |
| ---------------------------------------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------ |
| [Collect payment with Checkout](https://docs.stripe.com/payments/checkout.md)            | ✓ Supported   | ✓ Supported                                                                                                  |
| [Customer portal](https://docs.stripe.com/customer-management.md)                        | - Unsupported | Limited 1                                                                                                    |
| [Automatic tax support](https://docs.stripe.com/billing/taxes.md)                        | ✓ Supported   | ✓ Supported                                                                                                  |
| Manual tax support                                                                       | ✓ Supported   | - Unsupported                                                                                                |
| [Invoicing](https://docs.stripe.com/billing/invoices/subscription.md)                    | ✓ Supported   | ✓ Supported                                                                                                  |
| [Automations](https://docs.stripe.com/billing/automations.md)                            | ✓ Supported   | - Unsupported                                                                                                |
| [Smart retries](https://docs.stripe.com/invoicing/automatic-collection.md#smart-retries) | ✓ Supported   | ✓ Supported                                                                                                  |
| [Embedded pricing table](https://docs.stripe.com/billing/automations.md)                 | ✓ Supported   | - Unsupported                                                                                                |

1 Users can download invoices and view payment methods and customer information. Users can’t cancel a subscription or upgrade and downgrade subscriptions.


# Billing for LLM tokens

Learn how to bill for LLM tokens.

Bill for LLM tokens without managing pricing complexity. Set your markup, pick your models, and route calls through our LLM proxy (or supported partners). We sync popular model prices, configure [advanced usage-based billing](https://docs.stripe.com/billing/subscriptions/usage-based/advanced/compare.md) for your margin, and record usage automatically. Billing for LLM tokens is a private preview feature, and we consider it experimental in nature.

> This is an experimental private preview. We’re looking for developers willing to test the functionality and share their feedback.

## Overview

Say you’re building an AI app: you want a consistent 30% margin over raw LLM token costs across providers.

Billing automates the process and Stripe:

- Syncs the latest model prices across providers.
- Configures Usage-Based Billing for your token markup.
- Records usage automatically through our LLM proxy or supported partners.

## Token prices in one place

See token prices across major providers on a single Dashboard page—we keep prices up to date so you always have the current pricing information. You can adjust your markup at any time. We notify you when provider pricing changes.

## One-click Usage-Based Billing setup for your token markup

Enter your desired markup (for example, 30%). Click **Submit** and we’ll configure the required Usage-Based Billing resources—prices, meters, and rate configuration. You only need to set your margin percentage to start using Usage-Based Billing.

## Call models and bill in one request

Instead of maintaining an LLM integration and a billing integration, use our LLM proxy to call models and record metered usage in one request. Provide your prompt, chosen model, and the Customer ID. We route to the provider, return the response, and attribute tokens by model and type.

If you’ve already integrated with a different LLM proxy, we’ve partnered with industry leaders to capture usage automatically (with no extra API calls).

## Join the waitlist

If you’re interested in the private preview, sign up and we’ll contact you if we have available space.

