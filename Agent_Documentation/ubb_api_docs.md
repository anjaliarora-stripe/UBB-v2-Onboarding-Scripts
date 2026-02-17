Meters 
Ask about this section
Copy for LLM

View as Markdown
Meters specify how to aggregate meter events over a billing period. Meter events represent the actions that customers take in your system. Meters attach to prices and form the basis of the bill.

Related guide: Usage based billing

Endpoints
POST
/v1/billing/meters
POST
/v1/billing/meters/:id
GET
/v1/billing/meters/:id
GET
/v1/billing/meters
POST
/v1/billing/meters/:id/deactivate
POST
/v1/billing/meters/:id/reactivate
The Meter object 
Ask about this section
Copy for LLM

View as Markdown
Attributes

id
string
Unique identifier for the object.


object
string
String representing the object’s type. Objects of the same type share the same value.


created
timestamp
Time at which the object was created. Measured in seconds since the Unix epoch.


customer_mapping
dictionary
Fields that specify how to map a meter event to a customer.

Show child attributes

default_aggregation
dictionary
The default settings to aggregate a meter’s events with.

Show child attributes

dimension_payload_keys
nullable array of strings
Preview feature
Set of keys that will be used to group meter events by.


display_name
string
The meter’s name.


event_name
string
The name of the meter event to record usage for. Corresponds with the event_name field on meter events.


event_time_window
nullable enum
The time window which meter events have been pre-aggregated for, if any.

Possible enum values
day
Events are pre-aggregated in daily buckets.

hour
Events are pre-aggregated in hourly buckets.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


status
enum
The meter’s status.

Possible enum values
active
The meter is active.

inactive
The meter is inactive. No more events for this meter will be accepted. The meter cannot be attached to a price.


status_transitions
dictionary
The timestamps at which the meter status changed.

Show child attributes

tenant_payload_keys
nullable array of strings
Preview feature
Set of keys to hold user/team level usage data, these key values can not be used for dimensional pricing and are only for alerting and analytics. Each key must be present in the event payload.


updated
timestamp
Time at which the object was last updated. Measured in seconds since the Unix epoch.


value_settings
dictionary
Fields that specify how to calculate a meter event’s value.

Show child attributes
The Meter object
{
  "id": "mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA",
  "object": "billing.meter",
  "created": 1704824589,
  "customer_mapping": {
    "type": "by_id",
    "event_payload_key": "stripe_customer_id"
  },
  "default_aggregation": {
    "formula": "sum"
  },
  "display_name": "Search API Calls",
  "event_name": "ai_search_api",
  "event_time_window": null,
  "livemode": false,
  "status": "active",
  "status_transitions": {
    "deactivated_at": null
  },
  "updated": 1704898330,
  "value_settings": {
    "event_payload_key": "value"
  }
}
Create a billing meter 
Ask about this section
Copy for LLM

View as Markdown
Creates a billing meter.

Parameters

default_aggregation
dictionary
Required
The default settings to aggregate a meter’s events with.

Show child parameters

display_name
string
Required
The meter’s name. Not visible to the customer.

The maximum length is 250 characters.


event_name
string
Required
The name of the meter event to record usage for. Corresponds with the event_name field on meter events.

The maximum length is 100 characters.


customer_mapping
dictionary
Fields that specify how to map a meter event to a customer.

Show child parameters

dimension_payload_keys
array of strings
Preview feature
Set of keys that will be used to group meter events by. Each key must be present in the event payload.


event_time_window
enum
The time window which meter events have been pre-aggregated for, if any.

Possible enum values
day
Events are pre-aggregated in daily buckets.

hour
Events are pre-aggregated in hourly buckets.


tenant_payload_keys
array of strings
Preview feature
Set of keys to hold user/team level usage data, these key values can not be used for dimensional pricing and are only for alerting and analytics. Each key must be present in the event payload.


value_settings
dictionary
Fields that specify how to calculate a meter event’s value.

Show child parameters
Returns
Returns a billing meter.

POST 
/v1/billing/meters
Server-side language
cURL
curl https://api.stripe.com/v1/billing/meters \
  -u "sk_123:" \
  -d display_name="Search API Calls" \
  -d event_name=ai_search_api \
  -d "default_aggregation[formula]"=sum \
  -d "value_settings[event_payload_key]"=value \
  -d "customer_mapping[type]"=by_id \
  -d "customer_mapping[event_payload_key]"=stripe_customer_id
Response
{
  "id": "mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA",
  "object": "billing.meter",
  "created": 1704824589,
  "customer_mapping": {
    "type": "by_id",
    "event_payload_key": "stripe_customer_id"
  },
  "default_aggregation": {
    "formula": "sum"
  },
  "display_name": "Search API Calls",
  "event_name": "ai_search_api",
  "event_time_window": null,
  "livemode": false,
  "status": "active",
  "status_transitions": {
    "deactivated_at": null
  },
  "updated": 1704824589,
  "value_settings": {
    "event_payload_key": "value"
  }
}
Update a billing meter 
Ask about this section
Copy for LLM

View as Markdown
Updates a billing meter.

Parameters

display_name
string
The meter’s name. Not visible to the customer.

The maximum length is 250 characters.

Returns
Returns a billing meter.

POST 
/v1/billing/meters/:id
Server-side language
cURL
curl https://api.stripe.com/v1/billing/meters/mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA \
  -u "sk_123:" \
  -d display_name="Updated Display Name"
Response
{
  "id": "mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA",
  "object": "billing.meter",
  "created": 1704824589,
  "customer_mapping": {
    "type": "by_id",
    "event_payload_key": "stripe_customer_id"
  },
  "default_aggregation": {
    "formula": "sum"
  },
  "display_name": "Updated Display Name",
  "event_name": "ai_search_api",
  "event_time_window": null,
  "livemode": false,
  "status": "active",
  "status_transitions": {
    "deactivated_at": null
  },
  "updated": 1704898330,
  "value_settings": {
    "event_payload_key": "value"
  }
}
Retrieve a billing meter 
Ask about this section
Copy for LLM

View as Markdown
Retrieves a billing meter given an ID.

Parameters
No parameters.

Returns
Returns a billing meter.

GET 
/v1/billing/meters/:id
Server-side language
cURL
curl https://api.stripe.com/v1/billing/meters/mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA \
  -u "sk_123:"
Response
{
  "id": "mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA",
  "object": "billing.meter",
  "created": 1704824589,
  "customer_mapping": {
    "type": "by_id",
    "event_payload_key": "stripe_customer_id"
  },
  "default_aggregation": {
    "formula": "sum"
  },
  "display_name": "Search API Calls",
  "event_name": "ai_search_api",
  "event_time_window": null,
  "livemode": false,
  "status": "active",
  "status_transitions": {
    "deactivated_at": null
  },
  "updated": 1704898330,
  "value_settings": {
    "event_payload_key": "value"
  }
}
List billing meters 
Ask about this section
Copy for LLM

View as Markdown
Retrieve a list of billing meters.

Parameters

status
enum
Filter results to only include meters with the given status.

Possible enum values
active
The meter is active.

inactive
The meter is inactive. No more events for this meter will be accepted. The meter cannot be attached to a price.

More parameters
Expand all

ending_before
string

limit
integer

starting_after
string
Returns
Returns a list of billing meters.

GET 
/v1/billing/meters
Server-side language
cURL
curl https://api.stripe.com/v1/billing/meters \
  -u "sk_123:"
Response
{
  "object": "list",
  "data": [
    {
      "id": "mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA",
      "object": "billing.meter",
      "created": 1704824589,
      "customer_mapping": {
        "type": "by_id",
        "event_payload_key": "stripe_customer_id"
      },
      "default_aggregation": {
        "formula": "sum"
      },
      "display_name": "Search API Calls",
      "event_name": "ai_search_api",
      "event_time_window": null,
      "livemode": false,
      "status": "active",
      "status_transitions": {
        "deactivated_at": null
      },
      "updated": 1704898330,
      "value_settings": {
        "event_payload_key": "value"
      }
    }
  ],
  "has_more": true,
  "url": "v1/billing/meters"
}
Deactivate a billing meter 
Ask about this section
Copy for LLM

View as Markdown
When a meter is deactivated, no more meter events will be accepted for this meter. You can’t attach a deactivated meter to a price.

Parameters
No parameters.

Returns
Returns a billing meter.

POST 
/v1/billing/meters/:id/deactivate
Server-side language
cURL
curl -X POST https://api.stripe.com/v1/billing/meters/mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA/deactivate \
  -u "sk_123:"
Response
{
  "id": "mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA",
  "object": "billing.meter",
  "created": 1704824589,
  "customer_mapping": {
    "type": "by_id",
    "event_payload_key": "stripe_customer_id"
  },
  "default_aggregation": {
    "formula": "sum"
  },
  "display_name": "Search API Calls",
  "event_name": "ai_search_api",
  "event_time_window": null,
  "livemode": false,
  "status": "active",
  "status_transitions": {
    "deactivated_at": 1704898330
  },
  "updated": 1704898330,
  "value_settings": {
    "event_payload_key": "value"
  }
}
Reactivate a billing meter 
Ask about this section
Copy for LLM

View as Markdown
When a meter is reactivated, events for this meter can be accepted and you can attach the meter to a price.

Parameters
No parameters.

Returns
Returns a billing meter.

POST 
/v1/billing/meters/:id/reactivate
Server-side language
cURL
curl -X POST https://api.stripe.com/v1/billing/meters/mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA/reactivate \
  -u "sk_123:"
Response
{
  "id": "mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA",
  "object": "billing.meter",
  "created": 1704824589,
  "customer_mapping": {
    "type": "by_id",
    "event_payload_key": "stripe_customer_id"
  },
  "default_aggregation": {
    "formula": "sum"
  },
  "display_name": "Search API Calls",
  "event_name": "ai_search_api",
  "event_time_window": null,
  "livemode": false,
  "status": "active",
  "status_transitions": {
    "deactivated_at": null
  },
  "updated": 1704898330,
  "value_settings": {
    "event_payload_key": "value"
  }
}


Meter Events 
Ask about this section
Copy for LLM

View as Markdown
Meter events represent actions that customers take in your system. You can use meter events to bill a customer based on their usage. Meter events are associated with billing meters, which define both the contents of the event’s payload and how to aggregate those events.

Endpoints
POST
/v1/billing/meter_events
The Meter Event object 
Ask about this section
Copy for LLM

View as Markdown
Attributes

object
string
String representing the object’s type. Objects of the same type share the same value.


created
timestamp
Time at which the object was created. Measured in seconds since the Unix epoch.


event_name
string
The name of the meter event. Corresponds with the event_name field on a meter.

The maximum length is 100 characters.


identifier
string
A unique identifier for the event.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


payload
dictionary
The payload of the event. This contains the fields corresponding to a meter’s customer_mapping.event_payload_key (default is stripe_customer_id) and value_settings.event_payload_key (default is value). Read more about the payload.


timestamp
timestamp
The timestamp passed in when creating the event. Measured in seconds since the Unix epoch.

The Meter Event object
{
  "object": "billing.meter_event",
  "created": 1704824589,
  "event_name": "ai_search_api",
  "identifier": "identifier_123",
  "livemode": true,
  "payload": {
    "value": "25",
    "stripe_customer_id": "cus_NciAYcXfLnqBoz"
  },
  "timestamp": 1680210639
}
Create a billing meter event 
Ask about this section
Copy for LLM

View as Markdown
Creates a billing meter event.

Parameters

event_name
string
Required
The name of the meter event. Corresponds with the event_name field on a meter.

The maximum length is 100 characters.


payload
dictionary
Required
The payload of the event. This must contain the fields corresponding to a meter’s customer_mapping.event_payload_key (default is stripe_customer_id) and value_settings.event_payload_key (default is value). Read more about the payload.


identifier
string
A unique identifier for the event. If not provided, one is generated. We recommend using UUID-like identifiers. We will enforce uniqueness within a rolling period of at least 24 hours. The enforcement of uniqueness primarily addresses issues arising from accidental retries or other problems occurring within extremely brief time intervals. This approach helps prevent duplicate entries and ensures data integrity in high-frequency operations.

The maximum length is 100 characters.


timestamp
timestamp
The time of the event. Measured in seconds since the Unix epoch. Must be within the past 35 calendar days or up to 5 minutes in the future. Defaults to current timestamp if not specified.

Returns
Returns a billing meter event.

POST 
/v1/billing/meter_events
Server-side language
cURL
curl https://api.stripe.com/v1/billing/meter_events \
  -u "sk_123:" \
  -d event_name=ai_search_api \
  -d "payload[value]"=25 \
  -d "payload[stripe_customer_id]"=cus_NciAYcXfLnqBoz \
  -d identifier=identifier_123
Response
{
  "object": "billing.meter_event",
  "created": 1704824589,
  "event_name": "ai_search_api",
  "identifier": "identifier_123",
  "livemode": true,
  "payload": {
    "value": "25",
    "stripe_customer_id": "cus_NciAYcXfLnqBoz"
  },
  "timestamp": 1680210639
}



Meter Event Summary 
Ask about this section
Copy for LLM

View as Markdown
A billing meter event summary represents an aggregated view of a customer’s billing meter events within a specified timeframe. It indicates how much usage was accrued by a customer for that period.

Note: Meters events are aggregated asynchronously so the meter event summaries provide an eventually consistent view of the reported usage.

Endpoints
GET
/v1/billing/meters/:id/event_summaries
The Meter Event Summary object 
Ask about this section
Copy for LLM

View as Markdown
Attributes

id
string
Unique identifier for the object.


object
string
String representing the object’s type. Objects of the same type share the same value.


aggregated_value
float
Aggregated value of all the events within start_time (inclusive) and end_time (inclusive). The aggregation strategy is defined on meter via default_aggregation.


dimensions
nullable dictionary
Preview feature
Key-value pairs of dimension values for event summaries with grouping on dimensions.


end_time
timestamp
End timestamp for this event summary (exclusive). Must be aligned with minute boundaries.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


meter
string
The meter associated with this event summary.


start_time
timestamp
Start timestamp for this event summary (inclusive). Must be aligned with minute boundaries.

The Meter Event Summary object
{
  "id": "mtrusg_test_6041CMAXJrFdZ56U76ce6L35Hz7xA3Tn58z5sY7bq6gM3XN5bx5Y459D4Xt2E17ko6M86kt7kV3bl5PM7LV59l4sY50b6oU5QD7bY3HP58z5sY7bq6gM3Y57LF2Dr7od3Hb8927gh4Tt4Lo4xO4ge60T81C6Y53gl4QS2D33ft3HC3Xi3Cy3Cy3Cy",
  "object": "billing.meter_event_summary",
  "aggregated_value": 10,
  "end_time": 1711659600,
  "livemode": false,
  "meter": "mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA",
  "start_time": 1711656000
}
List billing meter event summaries 
Ask about this section
Copy for LLM

View as Markdown
Retrieve a list of billing meter event summaries.

Parameters

customer
string
Required
The customer for which to fetch event summaries.


end_time
timestamp
Required
The timestamp from when to stop aggregating meter events (exclusive). Must be aligned with minute boundaries.


id
string
Required
Unique identifier for the object.


start_time
timestamp
Required
The timestamp from when to start aggregating meter events (inclusive). Must be aligned with minute boundaries.


dimension_filters
dictionary
Preview feature
Key-value pairs used to filter meter events by dimension values. If specified, event summaries will be generated with only matching meter events.


dimension_group_by_keys
array of strings
Preview feature
List of dimension payload keys to group by. If specified, event summaries will be grouped by the given dimension payload key values.


tenant_filters
dictionary
Preview feature
Key-value pairs used to filter meter events by tenant value. If specified, event summaries will be generated with only matching meter events.


value_grouping_window
enum
Specifies what granularity to use when generating event summaries. If not specified, a single event summary would be returned for the specified time range. For hourly granularity, start and end times must align with hour boundaries (e.g., 00:00, 01:00, …, 23:00). For daily granularity, start and end times must align with UTC day boundaries (00:00 UTC).

Possible enum values
day
Generate event summaries per day.

hour
Generate event summaries per hour.

More parameters
Expand all

ending_before
string

limit
integer

starting_after
string
Returns
Returns a list of billing meter event summaries.

GET 
/v1/billing/meters/:id/event_summaries
Server-side language
cURL
curl -G https://api.stripe.com/v1/billing/meters/mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA/event_summaries \
  -u "sk_123:" \
  -d customer=cus_Pp40waj64hdRxb \
  -d start_time=1711584000 \
  -d end_time=1711666800 \
  -d value_grouping_window=hour
Response
{
  "object": "list",
  "data": [
    {
      "id": "mtrusg_test_6041CMAXJrFdZ56U76ce6L35Hz7xA3Tn58z5sY7bq6gM3XN5bx5Y459D4Xt2E17ko6M86kt7kV3bl5PM7LV59l4sY50b6oU5QD7bY3HP58z5sY7bq6gM3Y57LF2Dr7od3Hb8927gh4Tt4Lo4xO4ge60T81C6Y53gl4QS2D33ft3HC3Xl3bk3Cy3Cy",
      "object": "billing.meter_event_summary",
      "aggregated_value": 15,
      "end_time": 1711663200,
      "livemode": false,
      "meter": "mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA",
      "start_time": 1711659600
    },
    {
      "id": "mtrusg_test_6041CMAXJrFdZ56U76ce6L35Hz7xA3Tn58z5sY7bq6gM3XN5bx5Y459D4Xt2E17ko6M86kt7kV3bl5PM7LV59l4sY50b6oU5QD7bY3HP58z5sY7bq6gM3Y57LF2Dr7od3Hb8927gh4Tt4Lo4xO4ge60T81C6Y53gl4QS2D33ft3HC3Xi3Cy3Cy3Cy",
      "object": "billing.meter_event_summary",
      "aggregated_value": 10,
      "end_time": 1711659600,
      "livemode": false,
      "meter": "mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA",
      "start_time": 1711656000
    }
  ],
  "has_more": false,
  "url": "/v1/billing/meters/:id/event_summaries"
}
Meter Usage Analytics 
Ask about this section
Copy for LLM

View as Markdown
A billing meter usage event represents an aggregated view of a customer’s billing meter events within a specified timeframe.

Endpoints
GET
/v1/billing/analytics/meter_usage
The Meter Usage Analytics object 
Ask about this section
Copy for LLM

View as Markdown
Attributes

object
string
String representing the object’s type. Objects of the same type share the same value.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


refreshed_at
timestamp
The timestamp to indicate data freshness, measured in seconds since the Unix epoch.


rows
dictionary
List of aggregate meter usage items, each with a start time, end time, value, and any meter or dimension details.

Show child attributes
The Meter Usage Analytics object
{
  "object": "billing.analytics.meter_usage",
  "refreshed_at": 1735689000,
  "livemode": false,
  "rows": {
    "url": "/v1/billing/analytics/meter_usage",
    "has_more": false,
    "total": 3,
    "data": [
      {
        "object": "billing.analytics.meter_usage_row",
        "starts_at": 1733097600,
        "ends_at": 1733184000,
        "meter": "mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA",
        "value": 1500,
        "dimensions": {
          "model": "gpt-4"
        }
      },
      {
        "object": "billing.analytics.meter_usage_row",
        "starts_at": 1733184000,
        "ends_at": 1733270400,
        "meter": "mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA",
        "value": 2250,
        "dimensions": {
          "model": "gpt-4"
        }
      },
      {
        "object": "billing.analytics.meter_usage_row",
        "starts_at": 1733270400,
        "ends_at": 1733356800,
        "meter": "mtr_test_61Q8nQMqIFK9fRQmr41CMAXJrFdZ5MnA",
        "value": 1875,
        "dimensions": {
          "model": "gpt-4"
        }
      }
    ]
  }
}
Retrieves aggregated meter usage data 
Ask about this section
Copy for LLM

View as Markdown
Returns aggregated meter usage data for a customer within a specified time interval. The data can be grouped by various dimensions and can include multiple meters if specified.

Parameters

customer
string
Required
The customer id to fetch meter usage data for.


ends_at
timestamp
Required
The timestamp from when to stop aggregating meter events (exclusive). Must be aligned with minute boundaries.


starts_at
timestamp
Required
The timestamp from when to start aggregating meter events (inclusive). Must be aligned with minute boundaries.


meters
array of dictionaries
An array of meter parameters to specify which meters to include in the usage data. If not specified, usage across all meters for the customer is included.

Show child parameters

timezone
string
The timezone to use for the start and end times. Defaults to UTC if not specified.


value_grouping_window
enum
Specifies what granularity to use when aggregating meter usage events. If not specified, a single event would be returned for the specified time range.

Possible enum values
day
hour
month
week
Returns
Aggregated meter usage data for a customer in the specified time interval.

Credit Grant 
Ask about this section
Copy for LLM

View as Markdown
A credit grant is an API resource that documents the allocation of some billing credits to a customer.

Related guide: Billing credits

Endpoints
POST
/v1/billing/credit_grants
POST
/v1/billing/credit_grants/:id
GET
/v1/billing/credit_grants/:id
GET
/v1/billing/credit_grants
POST
/v1/billing/credit_grants/:id/expire
POST
/v1/billing/credit_grants/:id/void
The Credit Grant object 
Ask about this section
Copy for LLM

View as Markdown
Attributes

id
string
Unique identifier for the object.


object
string
String representing the object’s type. Objects of the same type share the same value.


amount
dictionary
Amount of this credit grant.

Show child attributes

applicability_config
dictionary
Configuration specifying what this credit grant applies to. We currently only support metered prices that have a Billing Meter attached to them.

Show child attributes

category
enum
The category of this credit grant. This is for tracking purposes and isn’t displayed to the customer.

Possible enum values
paid
The credit grant was purchased by the customer for some amount.

promotional
The credit grant was given to the customer for free.


created
timestamp
Time at which the object was created. Measured in seconds since the Unix epoch.


customer
string
Expandable
ID of the customer receiving the billing credits.


customer_account
nullable string
ID of the account representing the customer receiving the billing credits


effective_at
nullable timestamp
The time when the billing credits become effective-when they’re eligible for use.


expires_at
nullable timestamp
The time when the billing credits expire. If not present, the billing credits don’t expire.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


metadata
dictionary
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


name
nullable string
A descriptive name shown in dashboard.


priority
nullable integer
Preview feature
The priority for applying this credit grant. The highest priority is 0 and the lowest is 100.


test_clock
nullable string
Expandable
ID of the test clock this credit grant belongs to.


updated
timestamp
Time at which the object was last updated. Measured in seconds since the Unix epoch.


voided_at
nullable timestamp
The time when this credit grant was voided. If not present, the credit grant hasn’t been voided.

The Credit Grant object
{
  "id": "credgr_test_61R9a6NUWsRmOW3RM41L6nFOS1ekDGHo",
  "object": "billing.credit_grant",
  "amount": {
    "monetary": {
      "currency": "usd",
      "value": 1000
    },
    "type": "monetary"
  },
  "applicability_config": {
    "scope": {
      "price_type": "metered"
    }
  },
  "category": "paid",
  "created": 1726620803,
  "customer": "cus_QrvQguzkIK8zTj",
  "effective_at": 1729297860,
  "expires_at": null,
  "livemode": false,
  "metadata": {},
  "name": "Purchased Credits",
  "priority": 50,
  "test_clock": null,
  "updated": 1726620803,
  "voided_at": null
}
Create a credit grant 
Ask about this section
Copy for LLM

View as Markdown
Creates a credit grant.

Parameters

amount
dictionary
Required
Amount of this credit grant.

Show child parameters

applicability_config
dictionary
Required
Configuration specifying what this credit grant applies to. We currently only support metered prices that have a Billing Meter attached to them.

Show child parameters

category
enum
The category of this credit grant. It defaults to paid if not specified.

Possible enum values
paid
The credit grant was purchased by the customer for some amount.

promotional
The credit grant was given to the customer for free.


customer
string
ID of the customer receiving the billing credits.


customer_account
string
ID of the account representing the customer receiving the billing credits.


effective_at
timestamp
The time when the billing credits become effective-when they’re eligible for use. It defaults to the current timestamp if not specified.


expires_at
timestamp
The time when the billing credits expire. If not specified, the billing credits don’t expire.


metadata
dictionary
Set of key-value pairs that you can attach to an object. You can use this to store additional information about the object (for example, cost basis) in a structured format.


name
string
A descriptive name shown in the Dashboard.

The maximum length is 100 characters.


priority
integer
Preview feature
The desired priority for applying this credit grant. If not specified, it will be set to the default value of 50. The highest priority is 0 and the lowest is 100.

Returns
Returns a credit grant.

POST 
/v1/billing/credit_grants
Server-side language
cURL
curl https://api.stripe.com/v1/billing/credit_grants \
  -u "sk_123:" \
  -d name="Purchased Credits" \
  -d customer=cus_QrvQguzkIK8zTj \
  -d "amount[monetary][currency]"=usd \
  -d "amount[monetary][value]"=1000 \
  -d "amount[type]"=monetary \
  -d "applicability_config[scope][price_type]"=metered \
  -d category=paid
Response
{
  "id": "credgr_test_61R9a6NUWsRmOW3RM41L6nFOS1ekDGHo",
  "object": "billing.credit_grant",
  "amount": {
    "monetary": {
      "currency": "usd",
      "value": 1000
    },
    "type": "monetary"
  },
  "applicability_config": {
    "scope": {
      "price_type": "metered"
    }
  },
  "category": "paid",
  "created": 1726620803,
  "customer": "cus_QrvQguzkIK8zTj",
  "effective_at": 1729297860,
  "expires_at": null,
  "livemode": false,
  "metadata": {},
  "name": "Purchased Credits",
  "priority": null,
  "test_clock": null,
  "updated": 1726620803
}
Update a credit grant 
Ask about this section
Copy for LLM

View as Markdown
Updates a credit grant.

Parameters

id
string
Required
Unique identifier for the object.


expires_at
timestamp
The time when the billing credits created by this credit grant expire. If set to empty, the billing credits never expire.


metadata
dictionary
Set of key-value pairs you can attach to an object. You can use this to store additional information about the object (for example, cost basis) in a structured format.

Returns
Returns the updated credit grant.

POST 
/v1/billing/credit_grants/:id
Server-side language
cURL
curl https://api.stripe.com/v1/billing/credit_grants/credgr_test_61R9rpFu8SZkXPTkU41L6nFOS1ekDKoa \
  -u "sk_123:" \
  -d "metadata[cost_basis]"="0.9" \
  -d expires_at=1759302000
Response
{
  "id": "credgr_test_61R9rpFu8SZkXPTkU41L6nFOS1ekDKoa",
  "object": "billing.credit_grant",
  "amount": {
    "monetary": {
      "currency": "usd",
      "value": 1000
    },
    "type": "monetary"
  },
  "applicability_config": {
    "scope": {
      "price_type": "metered"
    }
  },
  "category": "paid",
  "created": 1726688933,
  "customer": "cus_QsEHa3GKweMwih",
  "effective_at": 1726688933,
  "expires_at": 1759302000,
  "livemode": false,
  "metadata": {
    "cost_basis": "0.9"
  },
  "name": "Purchased Credits",
  "priority": 50,
  "test_clock": null,
  "updated": 1726688977,
  "voided_at": null
}
Retrieve a credit grant 
Ask about this section
Copy for LLM

View as Markdown
Retrieves a credit grant.

Parameters

id
string
Required
Unique identifier for the object.

Returns
Returns a credit grant.

GET 
/v1/billing/credit_grants/:id
Server-side language
cURL
curl https://api.stripe.com/v1/billing/credit_grants/credgr_test_61R9a6NUWsRmOW3RM41L6nFOS1ekDGHo \
  -u "sk_123:"
Response
{
  "id": "credgr_test_61R9a6NUWsRmOW3RM41L6nFOS1ekDGHo",
  "object": "billing.credit_grant",
  "amount": {
    "monetary": {
      "currency": "usd",
      "value": 1000
    },
    "type": "monetary"
  },
  "applicability_config": {
    "scope": {
      "price_type": "metered"
    }
  },
  "category": "paid",
  "created": 1726620803,
  "customer": "cus_QrvQguzkIK8zTj",
  "effective_at": 1729297860,
  "expires_at": null,
  "livemode": false,
  "metadata": {},
  "name": "Purchased Credits",
  "priority": 50,
  "test_clock": null,
  "updated": 1726620803
}
List credit grants 
Ask about this section
Copy for LLM

View as Markdown
Retrieve a list of credit grants.

Parameters

customer
string
Only return credit grants for this customer.


customer_account
string
Only return credit grants for this account representing the customer.

More parameters
Expand all

ending_before
string

limit
integer

starting_after
string
Returns
Returns a list of credit grants.

GET 
/v1/billing/credit_grants
Server-side language
cURL
curl https://api.stripe.com/v1/billing/credit_grants \
  -u "sk_123:"
Response
{
  "object": "list",
  "data": [
    {
      "id": "credgr_test_61R9a6NUWsRmOW3RM41L6nFOS1ekDGHo",
      "object": "billing.credit_grant",
      "amount": {
        "monetary": {
          "currency": "usd",
          "value": 1000
        },
        "type": "monetary"
      },
      "applicability_config": {
        "scope": {
          "price_type": "metered"
        }
      },
      "category": "paid",
      "created": 1726620803,
      "customer": "cus_QrvQguzkIK8zTj",
      "effective_at": 1729297860,
      "expires_at": null,
      "livemode": false,
      "metadata": {},
      "name": "Purchased Credits",
      "priority": 50,
      "test_clock": null,
      "updated": 1726620803,
      "voided_at": null
    }
  ],
  "has_more": false,
  "url": "/v1/billing/credit_grants"
}
Expire a credit grant 
Ask about this section
Copy for LLM

View as Markdown
Expires a credit grant.

Parameters

id
string
Required
Unique identifier for the object.

Returns
Returns the expired credit grant.

POST 
/v1/billing/credit_grants/:id/expire
Server-side language
cURL
curl -X POST https://api.stripe.com/v1/billing/credit_grants/credgr_test_61R9rm9vto9SMMvt041L6nFOS1ekDCim/expire \
  -u "sk_123:"
Response
{
  "id": "credgr_test_61R9rm9vto9SMMvt041L6nFOS1ekDCim",
  "object": "billing.credit_grant",
  "amount": {
    "monetary": {
      "currency": "usd",
      "value": 1000
    },
    "type": "monetary"
  },
  "applicability_config": {
    "scope": {
      "price_type": "metered"
    }
  },
  "category": "paid",
  "created": 1726688741,
  "customer": "cus_QsEHa3GKweMwih",
  "effective_at": 1726688741,
  "expires_at": 1726688796,
  "livemode": false,
  "metadata": {},
  "name": "Purchased Credits",
  "priority": 50,
  "test_clock": null,
  "updated": 1726688796,
  "voided_at": null
}
Void a credit grant 
Ask about this section
Copy for LLM

View as Markdown
Voids a credit grant.

Parameters

id
string
Required
Unique identifier for the object.

Returns
Returns the voided credit grant.

POST 
/v1/billing/credit_grants/:id/void
Server-side language
cURL
curl -X POST https://api.stripe.com/v1/billing/credit_grants/credgr_test_61R9rnNTDmZ657a2r41L6nFOS1ekD5Ae/void \
  -u "sk_123:"
Response
{
  "id": "credgr_test_61R9rnNTDmZ657a2r41L6nFOS1ekD5Ae",
  "object": "billing.credit_grant",
  "amount": {
    "monetary": {
      "currency": "usd",
      "value": 1000
    },
    "type": "monetary"
  },
  "applicability_config": {
    "scope": {
      "price_type": "metered"
    }
  },
  "category": "paid",
  "created": 1726688817,
  "customer": "cus_QsEHa3GKweMwih",
  "effective_at": 1726688817,
  "expires_at": null,
  "livemode": false,
  "metadata": {},
  "name": "Purchased Credits",
  "priority": 50,
  "test_clock": null,
  "updated": 1726688829,
  "voided_at": 1726688829
}

Credit Balance Summary 
Ask about this section
Copy for LLM

View as Markdown
Indicates the billing credit balance for billing credits granted to a customer.

Endpoints
GET
/v1/billing/credit_balance_summary
The Credit Balance Summary object 
Ask about this section
Copy for LLM

View as Markdown
Attributes

object
string
String representing the object’s type. Objects of the same type share the same value.


balances
array of dictionaries
The billing credit balances. One entry per credit grant currency. If a customer only has credit grants in a single currency, then this will have a single balance entry.

Show child attributes

customer
string
Expandable
The customer the balance is for.


customer_account
nullable string
The account the balance is for.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The Credit Balance Summary object
{
  "object": "billing.credit_balance_summary",
  "balances": [
    {
      "available_balance": {
        "monetary": {
          "currency": "usd",
          "value": 1000
        },
        "type": "monetary"
      },
      "ledger_balance": {
        "monetary": {
          "currency": "usd",
          "value": 1000
        },
        "type": "monetary"
      }
    }
  ],
  "customer": "cus_QsEHa3GKweMwih",
  "livemode": false
}
Retrieve the credit balance summary for a customer 
Ask about this section
Copy for LLM

View as Markdown
Retrieves the credit balance summary for a customer.

Parameters

filter
dictionary
Required
The filter criteria for the credit balance summary.

Show child parameters

customer
string
The customer whose credit balance summary you’re retrieving.


customer_account
string
The account representing the customer whose credit balance summary you’re retrieving.

Returns
Returns the credit balance summary.

GET 
/v1/billing/credit_balance_summary
Server-side language
cURL
curl -G https://api.stripe.com/v1/billing/credit_balance_summary \
  -u "sk_123:" \
  -d customer=cus_QsEHa3GKweMwih \
  -d "filter[type]"=credit_grant \
  -d "filter[credit_grant]"=credgr_test_61R9rvFh1HgrFIoCp41L6nFOS1ekDCeW
Response
{
  "object": "billing.credit_balance_summary",
  "balances": [
    {
      "available_balance": {
        "monetary": {
          "currency": "usd",
          "value": 1000
        },
        "type": "monetary"
      },
      "ledger_balance": {
        "monetary": {
          "currency": "usd",
          "value": 1000
        },
        "type": "monetary"
      }
    }
  ],
  "customer": "cus_QsEHa3GKweMwih",
  "livemode": false
}


Credit Balance Transaction 
Ask about this section
Copy for LLM

View as Markdown
A credit balance transaction is a resource representing a transaction (either a credit or a debit) against an existing credit grant.

Endpoints
GET
/v1/billing/credit_balance_transactions/:id
GET
/v1/billing/credit_balance_transactions
The Credit Balance Transaction object 
Ask about this section
Copy for LLM

View as Markdown
Attributes

id
string
Unique identifier for the object.


object
string
String representing the object’s type. Objects of the same type share the same value.


created
timestamp
Time at which the object was created. Measured in seconds since the Unix epoch.


credit
nullable dictionary
Credit details for this credit balance transaction. Only present if type is credit.

Show child attributes

credit_grant
string
Expandable
The credit grant associated with this credit balance transaction.


debit
nullable dictionary
Debit details for this credit balance transaction. Only present if type is debit.

Show child attributes

effective_at
timestamp
The effective time of this credit balance transaction.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


test_clock
nullable string
Expandable
ID of the test clock this credit balance transaction belongs to.


type
nullable enum
The type of credit balance transaction (credit or debit).

Possible enum values
credit
A credit transaction.

debit
A debit transaction.

The Credit Balance Transaction object
{
  "id": "cbtxn_test_61R9ZljjaFmdidb6e41L6nFOS1ekD9Ue",
  "object": "billing.credit_balance_transaction",
  "created": 1726619524,
  "credit": null,
  "credit_grant": "credgr_test_61R9ZkIkIzLSp0xze41L6nFOS1ekDTPE",
  "debit": {
    "amount": {
      "monetary": {
        "currency": "usd",
        "value": 1000
      },
      "type": "monetary"
    },
    "credits_applied": {
      "invoice": "in_1Q0BoLL6nFOS1ekDbwBM5ER1",
      "invoice_line_item": "il_1QB443L6nFOS1ekDwRiN3Z4n"
    },
    "type": "credits_applied"
  },
  "effective_at": 1729211351,
  "livemode": false,
  "test_clock": "clock_1Q0BoJL6nFOS1ekDbyYYuseM",
  "type": "debit"
}
Retrieve a credit balance transaction 
Ask about this section
Copy for LLM

View as Markdown
Retrieves a credit balance transaction.

Parameters

id
string
Required
Unique identifier for the object.

Returns
Returns a credit balance transaction.

GET 
/v1/billing/credit_balance_transactions/:id
Server-side language
cURL
curl https://api.stripe.com/v1/billing/credit_balance_transactions/cbtxn_test_61R9ZljjaFmdidb6e41L6nFOS1ekD9Ue \
  -u "sk_123:"
Response
{
  "id": "cbtxn_test_61R9ZljjaFmdidb6e41L6nFOS1ekD9Ue",
  "object": "billing.credit_balance_transaction",
  "created": 1726619524,
  "credit": null,
  "credit_grant": "credgr_test_61R9ZkIkIzLSp0xze41L6nFOS1ekDTPE",
  "debit": {
    "amount": {
      "monetary": {
        "currency": "usd",
        "value": 1000
      },
      "type": "monetary"
    },
    "credits_applied": {
      "invoice": "in_1Q0BoLL6nFOS1ekDbwBM5ER1",
      "invoice_line_item": "il_1QB443L6nFOS1ekDwRiN3Z4n"
    },
    "type": "credits_applied"
  },
  "effective_at": 1729211351,
  "livemode": false,
  "test_clock": "clock_1Q0BoJL6nFOS1ekDbyYYuseM",
  "type": "debit"
}
List credit balance transactions 
Ask about this section
Copy for LLM

View as Markdown
Retrieve a list of credit balance transactions.

Parameters

credit_grant
string
The credit grant for which to fetch credit balance transactions.


customer
string
The customer whose credit balance transactions you’re retrieving.


customer_account
string
The account representing the customer whose credit balance transactions you’re retrieving.

More parameters
Expand all

ending_before
string

limit
integer

starting_after
string
Returns
Returns a list of credit balance transactions.

GET 
/v1/billing/credit_balance_transactions
Server-side language
cURL
curl -G https://api.stripe.com/v1/billing/credit_balance_transactions \
  -u "sk_123:" \
  -d customer=cus_QrvQguzkIK8zTj \
  -d credit_grant=credgr_test_61R9ZkIkIzLSp0xze41L6nFOS1ekDTPE
Response
{
  "object": "list",
  "data": [
    {
      "id": "cbtxn_test_61R9ZljjaFmdidb6e41L6nFOS1ekD9Ue",
      "object": "billing.credit_balance_transaction",
      "created": 1726619524,
      "credit": null,
      "credit_grant": "credgr_test_61R9ZkIkIzLSp0xze41L6nFOS1ekDTPE",
      "debit": {
        "amount": {
          "monetary": {
            "currency": "usd",
            "value": 1000
          },
          "type": "monetary"
        },
        "credits_applied": {
          "invoice": "in_1Q0BoLL6nFOS1ekDbwBM5ER1",
          "invoice_line_item": "il_1QB443L6nFOS1ekDwRiN3Z4n"
        },
        "type": "credits_applied"
      },
      "effective_at": 1729211351,
      "livemode": false,
      "test_clock": "clock_1Q0BoJL6nFOS1ekDbyYYuseM",
      "type": "debit"
    },
    {
      "id": "cbtxn_test_61R9ZkIbb17ze4b2s41L6nFOS1ekDXHs",
      "object": "billing.credit_balance_transaction",
      "created": 1726619434,
      "credit": {
        "amount": {
          "monetary": {
            "currency": "usd",
            "value": 1000
          },
          "type": "monetary"
        },
        "type": "credits_granted"
      },



Alerts 
Ask about this section
Copy for LLM

View as Markdown
A billing alert is a resource that notifies you when a certain usage threshold on a meter is crossed. For example, you might create a billing alert to notify you when a certain user made 100 API requests.

Endpoints
POST
/v1/billing/alerts
GET
/v1/billing/alerts/:id
GET
/v1/billing/alerts
POST
/v1/billing/alerts/:id/activate
POST
/v1/billing/alerts/:id/archive
POST
/v1/billing/alerts/:id/deactivate
The Alert object 
Ask about this section
Copy for LLM

View as Markdown
Attributes

id
string
Unique identifier for the object.


object
string
String representing the object’s type. Objects of the same type share the same value.


alert_type
enum
Defines the type of the alert.

Possible enum values
credit_balance_threshold
Use credit_balance_threshold if you intend for an alert to fire when a customer’s available billing credit balance falls below a certain value.

usage_threshold
Use usage_threshold if you intend for an alert to fire when a usage threshold on a meter is crossed.


credit_balance_threshold
nullable dictionary
Preview feature
Encapsulates configuration of the alert to monitor billing credit balance.

Show child attributes

livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


status
nullable enum
Status of the alert. This can be active, inactive or archived.


title
string
Title of the alert.


usage_threshold
nullable dictionary
Encapsulates configuration of the alert to monitor usage on a specific Billing Meter.

Show child attributes
The Alert object
{
  "id": "alrt_12345",
  "object": "billing.alert",
  "title": "API Request usage alert",
  "livemode": true,
  "alert_type": "usage_threshold",
  "usage_threshold": {
    "gte": 10000,
    "meter": "mtr_12345",
    "recurrence": "one_time"
  },
  "status": "active"
}
Create a billing alert 
Ask about this section
Copy for LLM

View as Markdown
Creates a billing alert

Parameters

alert_type
enum
Required
The type of alert to create.

Possible enum values
credit_balance_threshold
Use credit_balance_threshold if you intend for an alert to fire when a customer’s available billing credit balance falls below a certain value.

usage_threshold
Use usage_threshold if you intend for an alert to fire when a usage threshold on a meter is crossed.


title
string
Required
The title of the alert.

The maximum length is 256 characters.


credit_balance_threshold
dictionary
Preview feature
The configuration of the credit balance threshold.

Show child parameters

usage_threshold
dictionary
The configuration of the usage threshold.

Show child parameters
Returns
Returns a billing alert

POST 
/v1/billing/alerts
Server-side language
cURL
curl https://api.stripe.com/v1/billing/alerts \
  -u "sk_123:" \
  -d title="API Request usage alert" \
  -d alert_type=usage_threshold \
  -d "usage_threshold[gte]"=10000 \
  -d "usage_threshold[meter]"=mtr_12345 \
  -d "usage_threshold[recurrence]"=one_time
Response
{
  "id": "alrt_12345",
  "object": "billing.alert",
  "title": "API Request usage alert",
  "livemode": true,
  "alert_type": "usage_threshold",
  "usage_threshold": {
    "gte": 10000,
    "meter": "mtr_12345",
    "recurrence": "one_time"
  },
  "status": "active"
}
Retrieve a billing alert 
Ask about this section
Copy for LLM

View as Markdown
Retrieves a billing alert given an ID

Parameters
No parameters.

Returns
Returns the alert

GET 
/v1/billing/alerts/:id
Server-side language
cURL
curl https://api.stripe.com/v1/billing/alerts/alrt_12345 \
  -u "sk_123:"
Response
{
  "id": "alrt_12345",
  "object": "billing.alert",
  "title": "API Request usage alert",
  "livemode": true,
  "alert_type": "usage_threshold",
  "usage_threshold": {
    "gte": 10000,
    "meter": "mtr_12345",
    "recurrence": "one_time"
  },
  "status": "active"
}
List billing alerts 
Ask about this section
Copy for LLM

View as Markdown
Lists billing active and inactive alerts

Parameters

alert_type
enum
Filter results to only include this type of alert.

Possible enum values
credit_balance_threshold
Use credit_balance_threshold if you intend for an alert to fire when a customer’s available billing credit balance falls below a certain value.

usage_threshold
Use usage_threshold if you intend for an alert to fire when a usage threshold on a meter is crossed.


meter
string
Filter results to only include alerts with the given meter.

More parameters
Expand all

ending_before
string

limit
integer

starting_after
string
Returns
Returns a list of billing alerts

GET 
/v1/billing/alerts
Server-side language
cURL
curl https://api.stripe.com/v1/billing/alerts \
  -u "sk_123:"
Response
{
  "data": [
    {
      "id": "alrt_12345",
      "object": "billing.alert",
      "title": "API Request usage alert",
      "livemode": true,
      "alert_type": "usage_threshold",
      "usage_threshold": {
        "gte": 10000,
        "meter": "mtr_12345",
        "recurrence": "one_time"
      },
      "status": "active"
    },
    {
      "id": "alrt_67890",
      "object": "billing.alert",
      "title": "API Request usage alert",
      "livemode": true,
      "alert_type": "usage_threshold",
      "usage_threshold": {
        "gte": 120,
        "meter": "mtr_67890",
        "recurrence": "one_time"
      },
      "status": "active"
    }
  ]
}
Activate a billing alert 
Ask about this section
Copy for LLM

View as Markdown
Reactivates this alert, allowing it to trigger again.

Parameters
No parameters.

Returns
Returns the alert with its updated status.

POST 
/v1/billing/alerts/:id/activate
Server-side language
cURL
curl -X POST https://api.stripe.com/v1/billing/alerts/alrt_12345/activate \
  -u "sk_123:"
Response
{
  "id": "alrt_12345",
  "object": "billing.alert",
  "title": "API Request usage alert",
  "livemode": true,
  "alert_type": "usage_threshold",
  "usage_threshold": {
    "gte": 10000,
    "meter": "mtr_12345",
    "recurrence": "one_time"
  },
  "status": "active"
}
Archive a billing alert 
Ask about this section
Copy for LLM

View as Markdown
Archives this alert, removing it from the list view and APIs. This is non-reversible.

Parameters
No parameters.

Returns
Returns the alert with its updated status.

POST 
/v1/billing/alerts/:id/archive
Server-side language
cURL
curl -X POST https://api.stripe.com/v1/billing/alerts/alrt_12345/archive \
  -u "sk_123:"
Response
{
  "id": "alrt_12345",
  "object": "billing.alert",
  "title": "API Request usage alert",
  "livemode": true,
  "alert_type": "usage_threshold",
  "usage_threshold": {
    "gte": 10000,
    "meter": "mtr_12345",
    "recurrence": "one_time"
  },
  "status": "archived"
}
Deactivate a billing alert 
Ask about this section
Copy for LLM

View as Markdown
Deactivates this alert, preventing it from triggering.

Parameters
No parameters.

Returns
Returns the alert with its updated status.

POST 
/v1/billing/alerts/:id/deactivate
Server-side language
cURL
curl -X POST https://api.stripe.com/v1/billing/alerts/alrt_12345/deactivate \
  -u "sk_123:"
Response
{
  "id": "alrt_12345",
  "object": "billing.alert",
  "title": "API Request usage alert",
  "livemode": true,
  "alert_type": "usage_threshold",
  "usage_threshold": {
    "gte": 10000,
    "meter": "mtr_12345",
    "recurrence": "one_time"
  },
  "status": "inactive"
}

Metered Items v2
Ask about this section
Copy for LLM

View as Markdown
A Metered Item represents any item that you bill customers for based on how much they use it, such as hourly cloud CPU usage or tokens generated by an AI service.

Learn more about calling API v2 endpoints. 
Endpoints
POST
/v2/billing/metered_items
POST
/v2/billing/metered_items/:id
GET
/v2/billing/metered_items/:id
GET
/v2/billing/metered_items
The Metered Item object v2
Ask about this section
Copy for LLM

View as Markdown
Attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.metered_item"
String representing the object’s type. Objects of the same type share the same value of the object field.


created
timestamp
Timestamp of when the object was created.


display_name
string
Description that customers will see in the invoice line item. Maximum length of 250 characters.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
An internal key you can use to search for a particular billable item. Maximum length of 200 characters.


metadata
nullable map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


meter
string
ID of the Meter that measures usage for this Metered Item.


tax_details
nullable dictionary
Preview feature
Stripe Tax details.

Show child attributes

unit_label
nullable string
The unit to use when displaying prices for this billable item in places like Checkout. For example, set this field to “CPU-hour” for Checkout to display “(price) per CPU-hour”, or “1 million events” to display “(price) per 1 million events”. Maximum length of 100 characters.

The Metered Item object
{
  "id": "bli_test_61SGRtYMvrf176Kmm16RM8VQESSQ4t1K5KYFAmKUSVdY",
  "object": "v2.billing.metered_item",
  "created": "2025-03-27T00:04:48.000Z",
  "display_name": "Premium Chat API",
  "lookup_key": null,
  "metadata": {},
  "meter": "mtr_test_61SD5KZ52hzuwbPJE41H5wvQ9UC0V34K",
  "meter_segment_conditions": [],
  "invoice_presentation_dimensions": [],
  "unit_label": null,
  "livemode": false
}
Create a Metered Item v2
Ask about this section
Copy for LLM

View as Markdown
Create a Metered Item object.

Learn more about calling API v2 endpoints. 
Parameters

display_name
string
Required
Description that customers will see in the invoice line item. Maximum length of 250 characters.


meter
string
Required
ID of the Meter that measures usage for this Metered Item.


lookup_key
string
An internal key you can use to search for a particular billable item. Must be unique among billable items. Maximum length of 200 characters.


metadata
map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


tax_details
dictionary
Preview feature
Stripe Tax details.

Show child parameters

unit_label
string
The unit to use when displaying prices for this billable item in places like Checkout. For example, set this field to “CPU-hour” for Checkout to display “(price) per CPU-hour”, or “1 million events” to display “(price) per 1 million events”. Maximum length of 100 characters.

Returns
Response attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.metered_item"
String representing the object’s type. Objects of the same type share the same value of the object field.


created
timestamp
Timestamp of when the object was created.


display_name
string
Description that customers will see in the invoice line item. Maximum length of 250 characters.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
An internal key you can use to search for a particular billable item. Maximum length of 200 characters.


metadata
nullable map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


meter
string
ID of the Meter that measures usage for this Metered Item.


tax_details
nullable dictionary
Preview feature
Stripe Tax details.

Show child attributes

unit_label
nullable string
The unit to use when displaying prices for this billable item in places like Checkout. For example, set this field to “CPU-hour” for Checkout to display “(price) per CPU-hour”, or “1 million events” to display “(price) per 1 million events”. Maximum length of 100 characters.

Error Codes
400
lookup_key_already_used
Returned when another object of the same type already has the given lookup key.

400
tax_code_invalid
Returned when tax_code.value does not correspond to a Stripe PTC.

404
meter_not_found
Returned when the provided meter ID cannot be found.

POST 
/v2/billing/metered_items
Server-side language
cURL
curl -X POST https://api.stripe.com/v2/billing/metered_items \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Premium Chat API",
    "meter": "mtr_test_61SD5KZ52hzuwbPJE41H5wvQ9UC0V34K",
    "lookup_key": "premium-chat-api"
  }'
Response
{
  "id": "bli_test_61SGRtYMvrf176Kmm16RM8VQESSQ4t1K5KYFAmKUSVdY",
  "object": "v2.billing.metered_item",
  "created": "2025-03-27T00:04:48.000Z",
  "display_name": "Premium Chat API",
  "lookup_key": "premium-chat-api",
  "metadata": {},
  "meter": "mtr_test_61SD5KZ52hzuwbPJE41H5wvQ9UC0V34K",
  "unit_label": null,
  "livemode": true
}
Update a Metered Item v2
Ask about this section
Copy for LLM

View as Markdown
Update a Metered Item object. At least one of the fields is required.

Learn more about calling API v2 endpoints. 
Parameters

id
string
Required
ID of the Metered Item to update.


display_name
string
Description that customers will see in the invoice line item. Maximum length of 250 characters.


lookup_key
string
An internal key you can use to search for a particular billable item. Maximum length of 200 characters. To remove the lookup_key from the object, set it to null in the request.


metadata
map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


tax_details
dictionary
Preview feature
Stripe Tax details.

Show child parameters

unit_label
string
The unit to use when displaying prices for this billable item in places like Checkout. For example, set this field to “CPU-hour” for Checkout to display “(price) per CPU-hour”, or “1 million events” to display “(price) per 1 million events”. Maximum length of 100 characters. To remove the unit_label from the object, set it to null in the request.

Returns
Response attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.metered_item"
String representing the object’s type. Objects of the same type share the same value of the object field.


created
timestamp
Timestamp of when the object was created.


display_name
string
Description that customers will see in the invoice line item. Maximum length of 250 characters.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
An internal key you can use to search for a particular billable item. Maximum length of 200 characters.


metadata
nullable map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


meter
string
ID of the Meter that measures usage for this Metered Item.


tax_details
nullable dictionary
Preview feature
Stripe Tax details.

Show child attributes

unit_label
nullable string
The unit to use when displaying prices for this billable item in places like Checkout. For example, set this field to “CPU-hour” for Checkout to display “(price) per CPU-hour”, or “1 million events” to display “(price) per 1 million events”. Maximum length of 100 characters.

Error Codes
400
field_only_mutable_on_draft_objects
Returned when trying to update a field that can only be updated on draft objects.

400
invalid_status_for_draft_object_operation
Returned when trying to perform an operation on a draft object with an invalid status.

400
lookup_key_already_used
Returned when another object of the same type already has the given lookup key.

400
tax_code_invalid
Returned when tax_code.value does not correspond to a Stripe PTC.

404
draft_session_not_found
Returned when the provided draft_session ID cannot be found.

404
metered_item_not_found
Returned when the provided metered_item ID cannot be found.

POST 
/v2/billing/metered_items/:id
Server-side language
cURL
curl -X POST https://api.stripe.com/v2/billing/metered_items/bli_test_61SGRtYMvrf176Kmm16RM8VQESSQ4t1K5KYFAmKUSVdY \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Pro Chat API",
    "lookup_key": "pro-chat-api"
  }'
Response
{
  "id": "bli_test_61SGRtYMvrf176Kmm16RM8VQESSQ4t1K5KYFAmKUSVdY",
  "object": "v2.billing.metered_item",
  "created": "2025-03-27T00:04:48.000Z",
  "display_name": "Pro Chat API",
  "lookup_key": "pro-chat-api",
  "metadata": {},
  "meter": "mtr_test_61SD5KZ52hzuwbPJE41H5wvQ9UC0V34K",
  "unit_label": null,
  "livemode": true
}
Retrieve a Metered Item v2
Ask about this section
Copy for LLM

View as Markdown
Retrieve a Metered Item object.

Learn more about calling API v2 endpoints. 
Parameters

id
string
Required
ID of the Metered Item to retrieve.

Returns
Response attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.metered_item"
String representing the object’s type. Objects of the same type share the same value of the object field.


created
timestamp
Timestamp of when the object was created.


display_name
string
Description that customers will see in the invoice line item. Maximum length of 250 characters.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
An internal key you can use to search for a particular billable item. Maximum length of 200 characters.


metadata
nullable map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


meter
string
ID of the Meter that measures usage for this Metered Item.


tax_details
nullable dictionary
Preview feature
Stripe Tax details.

Show child attributes

unit_label
nullable string
The unit to use when displaying prices for this billable item in places like Checkout. For example, set this field to “CPU-hour” for Checkout to display “(price) per CPU-hour”, or “1 million events” to display “(price) per 1 million events”. Maximum length of 100 characters.

Error Codes
404
metered_item_not_found
Returned when the provided metered_item ID cannot be found.

GET 
/v2/billing/metered_items/:id
Server-side language
cURL
curl https://api.stripe.com/v2/billing/metered_items/bli_test_61SGRtYMvrf176Kmm16RM8VQESSQ4t1K5KYFAmKUSVdY \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "id": "bli_test_61SGRtYMvrf176Kmm16RM8VQESSQ4t1K5KYFAmKUSVdY",
  "object": "v2.billing.metered_item",
  "created": "2025-03-27T00:04:48.000Z",
  "display_name": "Premium Chat API",
  "lookup_key": "premium-chat-api",
  "metadata": {},
  "meter": "mtr_test_61SD5KZ52hzuwbPJE41H5wvQ9UC0V34K",
  "unit_label": null,
  "livemode": true
}
List Metered Items v2
Ask about this section
Copy for LLM

View as Markdown
List all Metered Item objects in reverse chronological order of creation.

Learn more about calling API v2 endpoints. 
Parameters

limit
integer
Optionally set the maximum number of results per page. Defaults to 20.


lookup_keys
array of strings
Filter by lookup keys. You can specify up to 10 lookup keys.


page
string
Opaque page token.

Returns
Response attributes

data
array of dictionaries
The retrieved Metered Item objects.

Show child attributes

next_page_url
nullable string
The URL of the next page of results, if there is one.


previous_page_url
nullable string
The URL of the previous page of results, if there is one.

GET 
/v2/billing/metered_items
Server-side language
cURL
curl https://api.stripe.com/v2/billing/metered_items \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "data": [
    {
      "id": "bli_test_61SGRtYMvrf176Kmm16RM8VQESSQ4t1K5KYFAmKUSVdY",
      "object": "v2.billing.metered_item",
      "created": "2025-03-27T00:04:48.000Z",
      "display_name": "Premium Chat API",
      "lookup_key": "premium-chat-api",
      "metadata": {},
      "meter": "mtr_test_61SD5KZ52hzuwbPJE41H5wvQ9UC0V34K",
      "unit_label": null,
      "livemode": true
    }
  ]
}
Metered Item event types v2
Ask about this section
Copy for LLM

View as Markdown
This is a list of all public thin events we currently send for updates to Metered Item, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

Event types
TypeFilter events by type
Type
Filter events
v2.billing.metered_item.created
Occurs when a Metered Item is created.










v2.billing.metered_item.updated
Occurs when a Metered Item is updated.
Attributes

id
string
Unique identifier for the event.


object
string, value is "v2.core.event"
String representing the object’s type. Objects of the same type share the same value of the object field.


context
nullable string
Authentication context needed to fetch the event or related object.


created
timestamp
Time at which the object was created.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


reason
nullable dictionary
Reason for the event.

Show child attributes

related_object
nullable dictionary
Object containing the reference to API resource relevant to the event.

Show child attributes

type
string, value is "v2.billing.metered_item.updated"
The type of the event.

Fetched attributes

changes
dictionary
Changes the event makes to properties in the related object. See the Metered Item object for the structure of before and after.

Show child attributes

data
dictionary
Additional data about the event.


License Fee Subscriptions v2
Ask about this section
Copy for LLM

View as Markdown
A License Fee Subscription links one License Fee to a specific Billing Cadence. While the License Fee Subscription is active, Stripe will bill the payer according to the License Fee’s pricing and the quantity subscribed.

Learn more about calling API v2 endpoints. 
Endpoints
GET
/v2/billing/license_fee_subscriptions/:id
The License Fee Subscription object v2
Ask about this section
Copy for LLM

View as Markdown
Attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.license_fee_subscription"
String representing the object’s type. Objects of the same type share the same value of the object field.


billing_cadence
string
The ID of the Billing Cadence.


created
timestamp
Timestamp of when the object was created.


license_fee
string
The ID of the License Fee.


license_fee_version
string
The ID of the License Fee Version.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


metadata
nullable map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


quantity
integer
Quantity of the License Fee subscribed to.


test_clock
nullable string
The ID of the Test Clock, if any.

The License Fee Subscription object
{
  "billing_cadence": "bc_61SahwKGATwuyXMY516SBbsMNLSQJnWcho4VDz0fYLKi",
  "created": "2025-01-01T00:00:00.000Z",
  "id": "lfs_61Sai6XI0UDAyOhhh16SBbsMNLSQJnWcho4VDz0fYMIS",
  "license_fee": "licf_61SahqwY8y4J62hb416SBbsMNLSQJnWcho4VDz0fY2Rc",
  "license_fee_version": "licfv_61SahqwswB6xPIPuo16SBbsMNLSQJnWcho4VDz0fYTYW",
  "metadata": {},
  "object": "v2.billing.license_fee_subscription",
  "quantity": 1,
  "test_clock": null,
  "livemode": true
}
Retrieve a License Fee Subscription v2
Ask about this section
Copy for LLM

View as Markdown
Retrieve a License Fee Subscription object.

Learn more about calling API v2 endpoints. 
Parameters

id
string
Required
The ID of the License Fee Subscription to retrieve.

Returns
Response attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.license_fee_subscription"
String representing the object’s type. Objects of the same type share the same value of the object field.


billing_cadence
string
The ID of the Billing Cadence.


created
timestamp
Timestamp of when the object was created.


license_fee
string
The ID of the License Fee.


license_fee_version
string
The ID of the License Fee Version.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


metadata
nullable map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


quantity
integer
Quantity of the License Fee subscribed to.


test_clock
nullable string
The ID of the Test Clock, if any.

Error Codes
404
license_fee_subscription_not_found
Returned when the requested License Fee Subscription cannot be found.


License Fees v2
Ask about this section
Copy for LLM

View as Markdown
A License Fee describes quantity-based pricing such as seat-based pricing.

Learn more about calling API v2 endpoints. 
Endpoints
POST
/v2/billing/license_fees
POST
/v2/billing/license_fees/:id
GET
/v2/billing/license_fees/:id
GET
/v2/billing/license_fees/:id/versions/:id
GET
/v2/billing/license_fees
GET
/v2/billing/license_fees/:id/versions
The License Fee object v2
Ask about this section
Copy for LLM

View as Markdown
Attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.license_fee"
String representing the object’s type. Objects of the same type share the same value of the object field.


active
boolean
Whether this License Fee is active. Inactive License Fees cannot be used in new activations or be modified.


created
timestamp
Timestamp of when the object was created.


currency
string
Three-letter ISO currency code, in lowercase. Must be a supported currency.


display_name
string
A customer-facing name for the license fee. This name is used in Stripe-hosted products like the Customer Portal and Checkout. It does not show up on Invoices. Maximum length of 250 characters.


latest_version
string
The ID of the license fee’s most recently created version.


licensed_item
dictionary
The Licensed Item that this License Fee binds to.

Show child attributes

live_version
string
The ID of the License Fee Version that will be used by all subscriptions when no specific version is specified.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
An internal key you can use to search for a particular License Fee. Maximum length of 200 characters.


metadata
nullable map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


service_interval
enum
The interval for assessing service.

Possible enum values
day
Assess service by days.

month
Assess service by months.

week
Assess service by weeks.

year
Assess service by years.


service_interval_count
integer
The length of the interval for assessing service. For example, set this to 3 and service_interval to "month" in order to specify quarterly service.


tax_behavior
enum
The Stripe Tax tax behavior - whether the license fee is inclusive or exclusive of tax.

Possible enum values
exclusive
Price excludes tax.

inclusive
Price includes tax.


tiering_mode
nullable enum
Defines whether the tiering price should be graduated or volume-based. In volume-based tiering, the maximum quantity within a period determines the per-unit price. In graduated tiering, the pricing changes as the quantity grows into new tiers. Can only be set if tiers is set.

Possible enum values
graduated
Use graduated tiering: the pricing at each tier applies to the quantity within that tier.

volume
Use volume-based tiering: the maximum quantity within a period determines the per-unit price for that period.


tiers
array of dictionaries
Each element represents a pricing tier. Cannot be set if unit_amount is provided.

Show child attributes

transform_quantity
nullable dictionary
Apply a transformation to the reported usage or set quantity before computing the amount billed.

Show child attributes

unit_amount
nullable string
The per-unit amount to be charged, represented as a decimal string in minor currency units with at most 12 decimal places. Cannot be set if tiers is provided.

The License Fee object
{
  "active": true,
  "created": "2025-01-01T00:00:00.000Z",
  "currency": "usd",
  "display_name": "Monthly fee",
  "id": "licf_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "latest_version": "licfv_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "licensed_item": {
    "created": "2025-01-01T00:00:00.000Z",
    "display_name": "Monthly fee item",
    "id": "bli_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
    "lookup_key": "monthly-fee-item",
    "metadata": {
      "key": "value"
    },
    "object": "v2.billing.licensed_item",
    "unit_label": "per month",
    "livemode": true
  },
  "live_version": "licfv_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "lookup_key": "monthly-fee",
  "metadata": {
    "key": "value"
  },
  "object": "v2.billing.license_fee",
  "service_interval": "month",
  "service_interval_count": 1,
  "tax_behavior": "exclusive",
  "tiering_mode": "graduated",
  "tiers": [
    {
      "flat_amount": null,
      "unit_amount": "20.00",
      "up_to_decimal": null,
      "up_to_inf": "inf"
    }
  ],
  "transform_quantity": {
    "divide_by": 1000,
    "round": "down"
  },
  "unit_amount": "20.00",
  "livemode": true
}
The License Fee Version object v2
Ask about this section
Copy for LLM

View as Markdown
Attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.license_fee_version"
String representing the object’s type. Objects of the same type share the same value of the object field.


created
timestamp
Timestamp of when the object was created.


license_fee_id
string
The ID of the parent License Fee.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


tiering_mode
nullable enum
Defines whether the tiering price should be graduated or volume-based. In volume-based tiering, the maximum quantity within a period determines the per-unit price. In graduated tiering, the pricing changes as the quantity grows into new tiers. Can only be set if tiers is set.

Possible enum values
graduated
Use graduated tiering: the pricing at each tier applies to the quantity within that tier.

volume
Use volume-based tiering: the maximum quantity within a period determines the per-unit price for that period.


tiers
array of dictionaries
Each element represents a pricing tier. Cannot be set if unit_amount is provided.

Show child attributes

transform_quantity
nullable dictionary
Apply a transformation to the reported usage or set quantity before computing the amount billed.

Show child attributes

unit_amount
nullable string
The per-unit amount to be charged, represented as a decimal string in minor currency units with at most 12 decimal places. Cannot be set if tiers is provided.

The License Fee Version object
{
  "created": "2025-01-01T00:00:00.000Z",
  "id": "licfv_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "license_fee_id": "licf_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "object": "v2.billing.license_fee_version",
  "tiering_mode": "graduated",
  "tiers": [
    {
      "flat_amount": null,
      "unit_amount": "20.00",
      "up_to_decimal": null,
      "up_to_inf": "inf"
    }
  ],
  "transform_quantity": {
    "divide_by": 1000,
    "round": "down"
  },
  "unit_amount": "20.0",
  "livemode": true
}
Create a License Fee v2
Ask about this section
Copy for LLM

View as Markdown
Create a License Fee object.

Learn more about calling API v2 endpoints. 
Parameters

currency
string
Required
Three-letter ISO currency code, in lowercase. Must be a supported currency.


display_name
string
Required
A customer-facing name for the License Fee. This name is used in Stripe-hosted products like the Customer Portal and Checkout. It does not show up on Invoices. Maximum length of 250 characters.


licensed_item
string
Required
The Licensed Item that this License Fee binds to.


service_interval
enum
Required
The interval for assessing service. For example, a monthly license fee with a rate of $1 for the first 10 “workloads” and $2 thereafter means “$1 per workload up to 10 workloads during a month of service.” This is similar to but distinct from billing interval; the service interval deals with the rate at which the customer accumulates fees, while the billing interval in Cadence deals with the rate the customer is billed.

Possible enum values
day
Assess service by days.

month
Assess service by months.

week
Assess service by weeks.

year
Assess service by years.


service_interval_count
integer
Required
The length of the interval for assessing service. For example, set this to 3 and service_interval to "month" in order to specify quarterly service.


tax_behavior
enum
Required
The Stripe Tax tax behavior - whether the license fee is inclusive or exclusive of tax.

Possible enum values
exclusive
Price excludes tax.

inclusive
Price includes tax.


lookup_key
string
An internal key you can use to search for a particular license fee. Maximum length of 200 characters.


metadata
map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


tiering_mode
enum
Defines whether the tiered price should be graduated or volume-based. In volume-based tiering, the maximum quantity within a period determines the per-unit price. In graduated tiering, the pricing changes as the quantity grows into new tiers. Can only be set if tiers is set.

Possible enum values
graduated
Use graduated tiering: the pricing at each tier applies to the quantity within that tier.

volume
Use volume-based tiering: the maximum quantity within a period determines the per-unit price for that period.


tiers
array of dictionaries
Each element represents a pricing tier. Cannot be set if unit_amount is provided.

Show child parameters

transform_quantity
dictionary
Apply a transformation to the reported usage or set quantity before computing the amount billed.

Show child parameters

unit_amount
string
The per-unit amount to be charged, represented as a decimal string in minor currency units with at most 12 decimal places. Cannot be set if tiers is provided.

Returns
Response attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.license_fee"
String representing the object’s type. Objects of the same type share the same value of the object field.


active
boolean
Whether this License Fee is active. Inactive License Fees cannot be used in new activations or be modified.


created
timestamp
Timestamp of when the object was created.


currency
string
Three-letter ISO currency code, in lowercase. Must be a supported currency.


display_name
string
A customer-facing name for the license fee. This name is used in Stripe-hosted products like the Customer Portal and Checkout. It does not show up on Invoices. Maximum length of 250 characters.


latest_version
string
The ID of the license fee’s most recently created version.


licensed_item
dictionary
The Licensed Item that this License Fee binds to.

Show child attributes

live_version
string
The ID of the License Fee Version that will be used by all subscriptions when no specific version is specified.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
An internal key you can use to search for a particular License Fee. Maximum length of 200 characters.


metadata
nullable map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


service_interval
enum
The interval for assessing service.

Possible enum values
day
Assess service by days.

month
Assess service by months.

week
Assess service by weeks.

year
Assess service by years.


service_interval_count
integer
The length of the interval for assessing service. For example, set this to 3 and service_interval to "month" in order to specify quarterly service.


tax_behavior
enum
The Stripe Tax tax behavior - whether the license fee is inclusive or exclusive of tax.

Possible enum values
exclusive
Price excludes tax.

inclusive
Price includes tax.


tiering_mode
nullable enum
Defines whether the tiering price should be graduated or volume-based. In volume-based tiering, the maximum quantity within a period determines the per-unit price. In graduated tiering, the pricing changes as the quantity grows into new tiers. Can only be set if tiers is set.

Possible enum values
graduated
Use graduated tiering: the pricing at each tier applies to the quantity within that tier.

volume
Use volume-based tiering: the maximum quantity within a period determines the per-unit price for that period.


tiers
array of dictionaries
Each element represents a pricing tier. Cannot be set if unit_amount is provided.

Show child attributes

transform_quantity
nullable dictionary
Apply a transformation to the reported usage or set quantity before computing the amount billed.

Show child attributes

unit_amount
nullable string
The per-unit amount to be charged, represented as a decimal string in minor currency units with at most 12 decimal places. Cannot be set if tiers is provided.

Error Codes
400
display_name_too_long
Returned when the provided display_name is longer than the maximum length of 100 characters.

400
invalid_status_for_draft_object_operation
Returned when trying to perform an operation on a draft object with an invalid status.

404
billable_item_not_found
Returned when the provided billable_item ID cannot be found.

404
draft_session_not_found
Returned when the provided draft_session ID cannot be found.

POST 
/v2/billing/license_fees
Server-side language
cURL
curl -X POST https://api.stripe.com/v2/billing/license_fees \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "currency": "usd",
    "display_name": "Monthly fee",
    "lookup_key": "monthly-fee",
    "metadata": {
        "key": "value"
    },
    "tax_behavior": "exclusive",
    "licensed_item": "bli_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
    "service_interval": "month",
    "service_interval_count": 1,
    "unit_amount": "20.00"
  }'
Response
{
  "active": true,
  "created": "2025-01-01T00:00:00.000Z",
  "currency": "usd",
  "display_name": "Monthly fee",
  "id": "licf_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "latest_version": "licfv_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "licensed_item": {
    "created": "2025-01-01T00:00:00.000Z",
    "display_name": "Monthly fee item",
    "id": "bli_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
    "lookup_key": "monthly-fee-item",
    "metadata": {
      "key": "value"
    },
    "object": "v2.billing.licensed_item",
    "unit_label": "per month",
    "livemode": true
  },
  "live_version": "licfv_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "lookup_key": "monthly-fee",
  "metadata": {
    "key": "value"
  },
  "object": "v2.billing.license_fee",
  "service_interval": "month",
  "service_interval_count": 1,
  "tax_behavior": "exclusive",
  "tiers": [],
  "unit_amount": "20.00",
  "livemode": true
}
Update a License Fee v2
Ask about this section
Copy for LLM

View as Markdown
Update a License Fee object.

Learn more about calling API v2 endpoints. 
Parameters

id
string
Required
The ID of the License Fee to update.


display_name
string
A customer-facing name for the License Fee. This name is used in Stripe-hosted products like the Customer Portal and Checkout. It does not show up on Invoices. Maximum length of 250 characters.


live_version
string
Changes the version that new license fee will use. Providing live_version = "latest" will set the license fee’s live_version to its latest version.


lookup_key
string
An internal key you can use to search for a particular license fee. Maximum length of 200 characters.


metadata
map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


tiering_mode
enum
Defines whether the tiered price should be graduated or volume-based. In volume-based tiering, the maximum quantity within a period determines the per-unit price. In graduated tiering, the pricing changes as the quantity grows into new tiers. Can only be set if tiers is set.

Possible enum values
graduated
Use graduated tiering: the pricing at each tier applies to the quantity within that tier.

volume
Use volume-based tiering: the maximum quantity within a period determines the per-unit price for that period.


tiers
array of dictionaries
Each element represents a pricing tier. Cannot be set if unit_amount is provided.

Show child parameters

transform_quantity
dictionary
Apply a transformation to the reported usage or set quantity before computing the amount billed.

Show child parameters

unit_amount
string
The per-unit amount to be charged, represented as a decimal string in minor currency units with at most 12 decimal places. Cannot be set if tiers is provided.

Returns
Response attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.license_fee"
String representing the object’s type. Objects of the same type share the same value of the object field.


active
boolean
Whether this License Fee is active. Inactive License Fees cannot be used in new activations or be modified.


created
timestamp
Timestamp of when the object was created.


currency
string
Three-letter ISO currency code, in lowercase. Must be a supported currency.


display_name
string
A customer-facing name for the license fee. This name is used in Stripe-hosted products like the Customer Portal and Checkout. It does not show up on Invoices. Maximum length of 250 characters.


latest_version
string
The ID of the license fee’s most recently created version.


licensed_item
dictionary
The Licensed Item that this License Fee binds to.

Show child attributes

live_version
string
The ID of the License Fee Version that will be used by all subscriptions when no specific version is specified.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
An internal key you can use to search for a particular License Fee. Maximum length of 200 characters.


metadata
nullable map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


service_interval
enum
The interval for assessing service.

Possible enum values
day
Assess service by days.

month
Assess service by months.

week
Assess service by weeks.

year
Assess service by years.


service_interval_count
integer
The length of the interval for assessing service. For example, set this to 3 and service_interval to "month" in order to specify quarterly service.


tax_behavior
enum
The Stripe Tax tax behavior - whether the license fee is inclusive or exclusive of tax.

Possible enum values
exclusive
Price excludes tax.

inclusive
Price includes tax.


tiering_mode
nullable enum
Defines whether the tiering price should be graduated or volume-based. In volume-based tiering, the maximum quantity within a period determines the per-unit price. In graduated tiering, the pricing changes as the quantity grows into new tiers. Can only be set if tiers is set.

Possible enum values
graduated
Use graduated tiering: the pricing at each tier applies to the quantity within that tier.

volume
Use volume-based tiering: the maximum quantity within a period determines the per-unit price for that period.


tiers
array of dictionaries
Each element represents a pricing tier. Cannot be set if unit_amount is provided.

Show child attributes

transform_quantity
nullable dictionary
Apply a transformation to the reported usage or set quantity before computing the amount billed.

Show child attributes

unit_amount
nullable string
The per-unit amount to be charged, represented as a decimal string in minor currency units with at most 12 decimal places. Cannot be set if tiers is provided.

Error Codes
400
display_name_too_long
Returned when the provided display_name is longer than the maximum length of 100 characters.

400
field_only_mutable_on_draft_objects
Returned when trying to update a field that can only be updated on draft objects.

400
invalid_status_for_draft_object_operation
Returned when trying to perform an operation on a draft object with an invalid status.

404
draft_session_not_found
Returned when the provided draft_session ID cannot be found.

POST 
/v2/billing/license_fees/:id
cURL
curl -X POST https://api.stripe.com/v2/billing/license_fees/licf_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Updated Monthly fee",
    "metadata": {
        "existing_key": "updated_value",
        "new_key": "new_value"
    },
    "lookup_key": "updated-monthly-fee",
    "live_version": "licfv_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
    "unit_amount": "25.00"
  }'
Response
{
  "active": true,
  "created": "2025-01-01T00:00:00.000Z",
  "currency": "usd",
  "display_name": "Updated Monthly fee",
  "id": "licf_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "latest_version": "licfv_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "licensed_item": {
    "created": "2025-01-01T00:00:00.000Z",
    "display_name": "Monthly fee item",
    "id": "bli_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
    "lookup_key": "monthly-fee-item",
    "metadata": {
      "key": "value"
    },
    "object": "v2.billing.licensed_item",
    "unit_label": "per month",
    "livemode": true
  },
  "live_version": "licfv_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "lookup_key": "updated-monthly-fee",
  "metadata": {
    "existing_key": "updated_value",
    "new_key": "new_value"
  },
  "object": "v2.billing.license_fee",
  "service_interval": "month",
  "service_interval_count": 1,
  "tax_behavior": "exclusive",
  "tiers": [],
  "unit_amount": "25.00",
  "livemode": true
}
Retrieve a License Fee v2
Ask about this section
Copy for LLM

View as Markdown
Retrieve a License Fee object.

Learn more about calling API v2 endpoints. 
Parameters

id
string
Required
The ID of the License Fee object to retrieve.

Returns
Response attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.license_fee"
String representing the object’s type. Objects of the same type share the same value of the object field.


active
boolean
Whether this License Fee is active. Inactive License Fees cannot be used in new activations or be modified.


created
timestamp
Timestamp of when the object was created.


currency
string
Three-letter ISO currency code, in lowercase. Must be a supported currency.


display_name
string
A customer-facing name for the license fee. This name is used in Stripe-hosted products like the Customer Portal and Checkout. It does not show up on Invoices. Maximum length of 250 characters.


latest_version
string
The ID of the license fee’s most recently created version.


licensed_item
dictionary
The Licensed Item that this License Fee binds to.

Show child attributes

live_version
string
The ID of the License Fee Version that will be used by all subscriptions when no specific version is specified.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
An internal key you can use to search for a particular License Fee. Maximum length of 200 characters.


metadata
nullable map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


service_interval
enum
The interval for assessing service.

Possible enum values
day
Assess service by days.

month
Assess service by months.

week
Assess service by weeks.

year
Assess service by years.


service_interval_count
integer
The length of the interval for assessing service. For example, set this to 3 and service_interval to "month" in order to specify quarterly service.


tax_behavior
enum
The Stripe Tax tax behavior - whether the license fee is inclusive or exclusive of tax.

Possible enum values
exclusive
Price excludes tax.

inclusive
Price includes tax.


tiering_mode
nullable enum
Defines whether the tiering price should be graduated or volume-based. In volume-based tiering, the maximum quantity within a period determines the per-unit price. In graduated tiering, the pricing changes as the quantity grows into new tiers. Can only be set if tiers is set.

Possible enum values
graduated
Use graduated tiering: the pricing at each tier applies to the quantity within that tier.

volume
Use volume-based tiering: the maximum quantity within a period determines the per-unit price for that period.


tiers
array of dictionaries
Each element represents a pricing tier. Cannot be set if unit_amount is provided.

Show child attributes

transform_quantity
nullable dictionary
Apply a transformation to the reported usage or set quantity before computing the amount billed.

Show child attributes

unit_amount
nullable string
The per-unit amount to be charged, represented as a decimal string in minor currency units with at most 12 decimal places. Cannot be set if tiers is provided.

Error Codes
404
license_fee_not_found
Returned when the provided license_fee ID cannot be found.

GET 
/v2/billing/license_fees/:id
Server-side language
cURL
curl https://api.stripe.com/v2/billing/license_fees/licf_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "active": true,
  "created": "2025-01-01T00:00:00.000Z",
  "currency": "usd",
  "display_name": "Monthly fee",
  "id": "licf_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "latest_version": "licfv_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "licensed_item": {
    "created": "2025-01-01T00:00:00.000Z",
    "display_name": "Monthly fee item",
    "id": "bli_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
    "lookup_key": "monthly-fee-item",
    "metadata": {
      "key": "value"
    },
    "object": "v2.billing.licensed_item",
    "unit_label": "per month",
    "livemode": true
  },
  "live_version": "licfv_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "lookup_key": "monthly-fee",
  "metadata": {
    "key": "value"
  },
  "object": "v2.billing.license_fee",
  "service_interval": "month",
  "service_interval_count": 1,
  "tax_behavior": "exclusive",
  "tiers": [],
  "unit_amount": "20.00",
  "livemode": true
}
Retrieve a License Fee Version v2
Ask about this section
Copy for LLM

View as Markdown
Retrieve a License Fee Version object.

Learn more about calling API v2 endpoints. 
Parameters

id
string
Required
The ID of the License Fee Version to retrieve.


license_fee_id
string
Required
The ID of the License Fee object.

Returns
Response attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.license_fee_version"
String representing the object’s type. Objects of the same type share the same value of the object field.


created
timestamp
Timestamp of when the object was created.


license_fee_id
string
The ID of the parent License Fee.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


tiering_mode
nullable enum
Defines whether the tiering price should be graduated or volume-based. In volume-based tiering, the maximum quantity within a period determines the per-unit price. In graduated tiering, the pricing changes as the quantity grows into new tiers. Can only be set if tiers is set.

Possible enum values
graduated
Use graduated tiering: the pricing at each tier applies to the quantity within that tier.

volume
Use volume-based tiering: the maximum quantity within a period determines the per-unit price for that period.


tiers
array of dictionaries
Each element represents a pricing tier. Cannot be set if unit_amount is provided.

Show child attributes

transform_quantity
nullable dictionary
Apply a transformation to the reported usage or set quantity before computing the amount billed.

Show child attributes

unit_amount
nullable string
The per-unit amount to be charged, represented as a decimal string in minor currency units with at most 12 decimal places. Cannot be set if tiers is provided.

Error Codes
404
license_fee_not_found
Returned when the provided license_fee ID cannot be found.

404
license_fee_version_not_found
Returned when the provided license_fee_version ID cannot be found.

GET 
/v2/billing/license_fees/:id/versions/:id
Server-side language
cURL
curl https://api.stripe.com/v2/billing/license_fees/licf_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy/versions/licfv_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "created": "2025-01-01T00:00:00.000Z",
  "id": "licfv_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "license_fee_id": "licf_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "object": "v2.billing.license_fee_version",
  "tiers": [],
  "unit_amount": "20.00",
  "livemode": true
}
List License Fees v2
Ask about this section
Copy for LLM

View as Markdown
List all License Fee objects.

Learn more about calling API v2 endpoints. 
Parameters

lookup_keys
array of strings
Required
Filter by lookup keys. You can specify up to 10 lookup keys.


licensed_item
string
Filter by licensed item.


limit
integer
Optionally set the maximum number of results per page. Defaults to 20.


page
string
A cursor for use in pagination.

Returns
Response attributes

data
array of dictionaries
List of License Fees.

Show child attributes

next_page_url
nullable string
The URL to get the next page of results, if there are any.


previous_page_url
nullable string
The URL to get the previous page of results, if there are any.

GET 
/v2/billing/license_fees
Server-side language
cURL
curl -G https://api.stripe.com/v2/billing/license_fees \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview" \
  -d "lookup_keys[0]"=monthly-fee
Response
{
  "data": [
    {
      "active": true,
      "created": "2025-01-01T00:00:00.000Z",
      "currency": "usd",
      "display_name": "Monthly fee",
      "id": "licf_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
      "latest_version": "licfv_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
      "licensed_item": {
        "created": "2025-01-01T00:00:00.000Z",
        "display_name": "Monthly fee item",
        "id": "bli_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
        "lookup_key": "monthly-fee-item",
        "metadata": {
          "key": "value"
        },
        "object": "v2.billing.licensed_item",
        "unit_label": "per month",
        "livemode": true
      },
      "live_version": "licfv_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
      "lookup_key": "monthly-fee",
      "metadata": {
        "key": "value"
      },
      "object": "v2.billing.license_fee",
      "service_interval": "month",
      "service_interval_count": 1,
      "tax_behavior": "exclusive",
      "tiers": [],
      "unit_amount": "20.00",
      "livemode": true
    }
  ],
  "next_page_url": null,
  "previous_page_url": null
}
List License Fee Versions v2
Ask about this section
Copy for LLM

View as Markdown
List all versions of a License Fee object.

Learn more about calling API v2 endpoints. 
Parameters

license_fee_id
string
Required
The ID of the License Fee to list versions for.


limit
integer
Optionally set the maximum number of results per page. Defaults to 20.


page
string
A cursor for use in pagination.

Returns
Response attributes

data
array of dictionaries
List of License Fee Versions.

Show child attributes

next_page_url
nullable string
The URL to get the next page of results, if there are any.


previous_page_url
nullable string
The URL to get the previous page of results, if there are any.

Error Codes
404
license_fee_not_found
Returned when the provided license_fee ID cannot be found.

GET 
/v2/billing/license_fees/:id/versions
Server-side language
cURL
curl https://api.stripe.com/v2/billing/license_fees/licf_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy/versions \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "data": [
    {
      "created": "2025-01-01T00:00:00.000Z",
      "id": "licfv_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
      "license_fee_id": "licf_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
      "object": "v2.billing.license_fee_version",
      "tiers": [],
      "unit_amount": "20.00",
      "livemode": true
    }
  ],
  "next_page_url": null,
  "previous_page_url": null
}
License Fee Version event types v2
Ask about this section
Copy for LLM

View as Markdown
This is a list of all public thin events we currently send for updates to License Fee Version, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

Event types
TypeFilter events by type
Type
Filter events
v2.billing.license_fee_version.created
Occurs when a License Fee Version is created.


Billing Intents v2
Ask about this section
Copy for LLM

View as Markdown
A Billing Intent represents a request to create, modify or cancel subscriptions.

Learn more about calling API v2 endpoints. 
Endpoints
POST
/v2/billing/intents
GET
/v2/billing/intents/:id
GET
/v2/billing/intents/:id/actions/:id
GET
/v2/billing/intents/:id/actions
GET
/v2/billing/intents
POST
/v2/billing/intents/:id/cancel
POST
/v2/billing/intents/:id/commit
POST
/v2/billing/intents/:id/release_reservation
POST
/v2/billing/intents/:id/reserve
The Intent object v2
Ask about this section
Copy for LLM

View as Markdown
Attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.intent"
String representing the object’s type. Objects of the same type share the same value of the object field.


amount_details
dictionary
Breakdown of the amount for this Billing Intent.

Show child attributes

cadence
nullable string
ID of an existing Cadence to use.


created
timestamp
Time at which the object was created.


currency
string
Three-letter ISO currency code, in lowercase. Must be a supported currency.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


status
enum
Current status of the Billing Intent.

Possible enum values
canceled
The Billing Intent is canceled.

committed
The Billing Intent is committed.

draft
The Billing Intent is in draft state.

reserved
The Billing Intent is reserved.


status_transitions
dictionary
Timestamps for status transitions of the Billing Intent.

Show child attributes
The Intent object
{
  "amount_details": {
    "currency": "usd",
    "discount": 0,
    "shipping": 0,
    "subtotal": 0,
    "tax": 0,
    "total": 0
  },
  "created": "2025-01-01T00:00:00.000Z",
  "currency": "usd",
  "effective_at": "current_billing_period_start",
  "id": "bilint_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "object": "v2.billing.billing_intent",
  "status": "draft",
  "status_transitions": {
    "canceled_at": null,
    "committed_at": null,
    "drafted_at": "2025-01-01T00:00:00.000Z",
    "reserved_at": null
  },
  "livemode": true,
  "cadence": "bc_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy"
}
The Intent Action object v2
Ask about this section
Copy for LLM

View as Markdown
Attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.intent_action"
String representing the object’s type. Objects of the same type share the same value of the object field.


created
timestamp
Time at which the object was created.


deactivate
nullable dictionary
Details for a deactivate action.

Show child attributes

livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


modify
nullable dictionary
Details for a modify action.

Show child attributes

subscribe
nullable dictionary
Details for a subscribe action.

Show child attributes

type
enum
Type of the Billing Intent Action.

Possible enum values
deactivate
Action to deactivate an existing subscription.

modify
Action to modify an existing subscription.

subscribe
Action to create a new subscription.

The Intent Action object
{
  "created": "2025-01-01T00:00:00.000Z",
  "id": "bilinti_61T9VNT6aGFjxfNPx16SBbsMNLSQJnWcho4VDz0fYVOq",
  "object": "v2.billing.intent_action",
  "type": "subscribe",
  "livemode": true,
  "subscribe": {
    "type": "pricing_plan_subscription_details",
    "pricing_plan_subscription_details": {
      "component_configurations": [],
      "metadata": {},
      "pricing_plan": "bpp_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
      "pricing_plan_version": "bppv_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
      "pricing_plan_subscription": "bpps_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy"
    }
  }
}
Create a billing intent v2
Ask about this section
Copy for LLM

View as Markdown
Create a Billing Intent.

Learn more about calling API v2 endpoints. 
Parameters

actions
array of dictionaries
Required
Actions to be performed by this Billing Intent.

Show child parameters

currency
string
Required
Three-letter ISO currency code, in lowercase. Must be a supported currency.


cadence
string
ID of an existing Cadence to use.

Returns
Response attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.intent"
String representing the object’s type. Objects of the same type share the same value of the object field.


amount_details
dictionary
Breakdown of the amount for this Billing Intent.

Show child attributes

cadence
nullable string
ID of an existing Cadence to use.


created
timestamp
Time at which the object was created.


currency
string
Three-letter ISO currency code, in lowercase. Must be a supported currency.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


status
enum
Current status of the Billing Intent.

Possible enum values
canceled
The Billing Intent is canceled.

committed
The Billing Intent is committed.

draft
The Billing Intent is in draft state.

reserved
The Billing Intent is reserved.


status_transitions
dictionary
Timestamps for status transitions of the Billing Intent.

Show child attributes
Error Codes
400
amount_too_large
Returned when the billing intent total amount due is greater than the maximum amount allowed.

400
amount_too_small
Returned when the billing intent total amount due is less than the minimum amount allowed.

400
billing_cadence_canceled
Returned when trying to cancel a billing cadence that has already been canceled.

400
billing_cadence_inactive
Returned when trying to create or update a billing intent with an inactive billing cadence.

400
cadence_currency_mismatch
Returned when trying to create a BillingIntent for a currency that is not supported by the billing cadence.

400
collect_at_invalid_for_v1_subscription
Returned when collect at is specified for a v1 subscription.

400
component_configuration_invalid
Returned when trying to create a billing intent action with a component configuration for an invalid pricing plan component.

400
concurrent_actions_not_allowed
Returned when trying to create a BillingIntent that involves multiple actions on the same object.

400
currency_mismatch
Returned when creating a rate card subscription for a billing cadence and the rate card currency does not match the billing cadence currency.

400
duplicate_actions_not_allowed
Returned when trying to create a BillingIntent with duplicate actions.

400
duplicate_component_configuration
Returned when trying to create a billing intent action with multiple component configurations for the same pricing plan component.

400
invalid_billing_cycle_dates
Returned by billing cadences when invalid dates for a billing cycle are set.

400
invalid_customer
Returned when creating or updating a cadence with a deleted customer.

400
invalid_discount_percent_off
Returned when trying to apply a discount with an invalid percent_off value.

400
invalid_effective_at_timestamp
Returned when the effective_at parameter is not a past timestamp.

400
invalid_modify_proration_behavior
Returned when the credit_proration_behavior and debit_proration_behavior are not equal for quantity changes during a modify action.

400
invalid_pricing_plan
Returned when trying to subscribe to a pricing plan that does not have any components on the version.

400
license_fee_currency_mismatch
Returned when creating a rate card subscription for a billing cadence and the rate card currency does not match the billing cadence currency.

400
license_fee_servicing_interval_exceeds_billing_interval
Returned when the license fee servicing interval exceeds the billing cadence cycle length.

400
manual_configuration_inactive
Returned when the ManualTaxConfiguration is inactive.

400
missing_discount_function
Returned when applying a discount without a discount function.

400
month_of_year_not_supported_for_interval_count
Returned by billing cadences when billing_cycle.month.month_of_year is used with an invalid interval_count.

400
partial_period_behavior_overlap
Returned when there is an overlap in partial period behavior override configurations.

400
price_currency_mismatch_with_billing_intent
Returned when the price currency does not match the billing intent currency.

400
price_interval_mismatch_billing_cadence_cycle_interval
Returned when the price interval is different than the billing cadence cycle interval.

400
pricing_plan_currency_mismatch
Returned when trying to create a BillingIntent for a currency that is not supported by the PricingPlan.

400
pricing_plan_inactive
Returned when trying to create or modify a subscription for an inactive pricing plan.

400
pricing_plan_subscription_already_exists
Returned when a user tries to create a pricing plan subscription for a billing cadence that has already subscribed to the same pricing plan.

400
rate_card_subscription_already_exists
Returned when a user tries to create a rate card subscription for a billing cadence that has already subscribed to the same rate card.

400
require_cadence
Returned when removing a discount without providing a cadence.

400
require_cadence_or_data
Returned when applying a discount without providing a cadence or cadence_data.

400
servicing_interval_exceeds_billing_interval
Returned when the rate card servicing interval exceeds the billing cadence cycle length.

400
too_many_active_pricing_plan_subscriptions
Returned when a user tries to create a pricing plan subscription for a billing cadence that has already reached the limit of active pricing plan subscriptions.

400
too_many_active_rate_card_subscriptions
Returned when a user tries to create a rate card subscription for a billing cadence that has already reached the limit of active subscriptions.

400
too_many_billing_intent_actions
Returned when trying to create a billing intent with too many billing intent actions.

400
unpriced_rate_card
Returned when no rates can be found for the given rate card ID and version.

404
bill_settings_not_found
Returned when the bill settings ID cannot be found.

404
bill_settings_version_not_found
Returned when the provided bill settings version ID cannot be found.

404
billing_cadence_not_found
Returned when the provided billing_cadence ID cannot be found.

404
collection_settings_not_found
Returned when the collection settings ID cannot be found.

404
collection_settings_version_not_found
Returned when the provided collection settings version ID cannot be found.

404
customer_not_found
Returned when the customer for the provided ID cannot be found.

404
discount_not_found
Returned when removing a non-existent discount, or when the discount is not found for the cadence.

404
manual_tax_configuration_not_found
Returned when no ManualTaxConfiguration object was found for the given ID.

404
price_not_found
Returned when the provided price ID cannot be found.

404
pricing_plan_component_not_found
Returned when the provided pricing_plan_component ID cannot be found.

404
pricing_plan_not_found
Returned when the provided pricing_plan ID cannot be found.

404
pricing_plan_subscription_not_found
Returned when a pricing plan subscription with the provided ID cannot be found.

404
pricing_plan_version_not_found
Returned when the provided pricing_plan_version ID cannot be found.

POST 
/v2/billing/intents
cURL
curl -X POST https://api.stripe.com/v2/billing/intents \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "cadence": "bc_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
    "currency": "usd",
    "actions": [
        {
            "type": "subscribe",
            "subscribe": {
                "type": "pricing_plan_subscription_details"
            }
        }
    ]
  }'
Response
{
  "amount_details": {
    "currency": "usd",
    "discount": 0,
    "shipping": 0,
    "subtotal": 2000,
    "tax": 200,
    "total": 2200
  },
  "created": "2025-01-01T00:00:00.000Z",
  "currency": "usd",
  "id": "bilint_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "object": "v2.billing.billing_intent",
  "status": "draft",
  "status_transitions": {
    "canceled_at": null,
    "committed_at": null,
    "drafted_at": "2025-01-01T00:00:00.000Z",
    "reserved_at": null
  },
  "livemode": true,
  "cadence": "bc_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy"
}
Retrieve a billing intent v2
Ask about this section
Copy for LLM

View as Markdown
Retrieve a Billing Intent.

Learn more about calling API v2 endpoints. 
Parameters

id
string
Required
The ID of the Billing Intent to retrieve.

Returns
Response attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.intent"
String representing the object’s type. Objects of the same type share the same value of the object field.


amount_details
dictionary
Breakdown of the amount for this Billing Intent.

Show child attributes

cadence
nullable string
ID of an existing Cadence to use.


created
timestamp
Time at which the object was created.


currency
string
Three-letter ISO currency code, in lowercase. Must be a supported currency.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


status
enum
Current status of the Billing Intent.

Possible enum values
canceled
The Billing Intent is canceled.

committed
The Billing Intent is committed.

draft
The Billing Intent is in draft state.

reserved
The Billing Intent is reserved.


status_transitions
dictionary
Timestamps for status transitions of the Billing Intent.

Show child attributes
Error Codes
404
billing_intent_not_found
Returned when billing intent is not found.

GET 
/v2/billing/intents/:id
Server-side language
cURL
curl https://api.stripe.com/v2/billing/intents/bilint_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "amount_details": {
    "currency": "usd",
    "discount": 0,
    "shipping": 0,
    "subtotal": 2000,
    "tax": 200,
    "total": 2200
  },
  "created": "2025-01-01T00:00:00.000Z",
  "currency": "usd",
  "id": "bilint_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "object": "v2.billing.billing_intent",
  "status": "draft",
  "status_transitions": {
    "canceled_at": null,
    "committed_at": null,
    "drafted_at": "2025-01-01T00:00:00.000Z",
    "reserved_at": null
  },
  "livemode": true,
  "cadence": "bc_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy"
}
Retrieve a billing intent action v2
Ask about this section
Copy for LLM

View as Markdown
Retrieve a Billing Intent Action.

Learn more about calling API v2 endpoints. 
Parameters

id
string
Required
ID of the Billing Intent Action to retrieve.


intent_id
string
Required
The ID of the Billing Intent the Billing Intent Action belongs to.

Returns
Response attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.intent_action"
String representing the object’s type. Objects of the same type share the same value of the object field.


created
timestamp
Time at which the object was created.


deactivate
nullable dictionary
Details for a deactivate action.

Show child attributes

livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


modify
nullable dictionary
Details for a modify action.

Show child attributes

subscribe
nullable dictionary
Details for a subscribe action.

Show child attributes

type
enum
Type of the Billing Intent Action.

Possible enum values
deactivate
Action to deactivate an existing subscription.

modify
Action to modify an existing subscription.

subscribe
Action to create a new subscription.

Error Codes
404
billing_intent_action_not_found
Returned when Billing Intent Action is not found.

404
billing_intent_not_found
Returned when billing intent is not found.

GET 
/v2/billing/intents/:id/actions/:id
cURL
curl https://api.stripe.com/v2/billing/intents/bilint_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy/actions/bilinti_61T9VNT6aGFjxfNPx16SBbsMNLSQJnWcho4VDz0fYVOq \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "created": "2025-01-01T00:00:00.000Z",
  "id": "bilinti_61T9VNT6aGFjxfNPx16SBbsMNLSQJnWcho4VDz0fYVOq",
  "object": "v2.billing.intent_action",
  "type": "subscribe",
  "livemode": true,
  "subscribe": {
    "type": "pricing_plan_subscription_details"
  }
}
List billing intent actions v2
Ask about this section
Copy for LLM

View as Markdown
List Billing Intent Actions.

Learn more about calling API v2 endpoints. 
Parameters

intent_id
string
Required
ID of the Billing Intent to list Billing Intent Actions for.


limit
integer
Optionally set the maximum number of results per page. Defaults to 10.


page
string
Opaque page token.

Returns
Response attributes

data
array of dictionaries
List of Billing Intent Actions.

Show child attributes

next_page_url
nullable string
The URL to get the next page of results, if there are any.


previous_page_url
nullable string
The URL to get the previous page of results, if there are any.

Error Codes
404
billing_intent_not_found
Returned when billing intent is not found.

GET 
/v2/billing/intents/:id/actions
cURL
curl https://api.stripe.com/v2/billing/intents/bilint_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy/actions \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "data": [
    {
      "created": "2025-01-01T00:00:00.000Z",
      "id": "bilinti_61T9VNT6aGFjxfNPx16SBbsMNLSQJnWcho4VDz0fYVOq",
      "object": "v2.billing.intent_action",
      "type": "subscribe",
      "livemode": true,
      "subscribe": {
        "type": "pricing_plan_subscription_details"
      }
    }
  ],
  "next_page_url": null,
  "previous_page_url": null
}
List billing intents v2
Ask about this section
Copy for LLM

View as Markdown
List Billing Intents.

Learn more about calling API v2 endpoints. 
Parameters

limit
integer
Optionally set the maximum number of results per page. Defaults to 10.


page
string
Opaque page token.

Returns
Response attributes

data
array of dictionaries
List of Billing Intent objects.

Show child attributes

next_page_url
nullable string
The URL to get the next page of results, if there are any.


previous_page_url
nullable string
The URL to get the previous page of results, if there are any.

GET 
/v2/billing/intents
Server-side language
cURL
curl https://api.stripe.com/v2/billing/intents \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "data": [
    {
      "amount_details": {
        "currency": "usd",
        "discount": 0,
        "shipping": 0,
        "subtotal": 2000,
        "tax": 200,
        "total": 2200
      },
      "created": "2025-01-01T00:00:00.000Z",
      "currency": "usd",
      "id": "bilint_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
      "object": "v2.billing.billing_intent",
      "status": "draft",
      "status_transitions": {
        "canceled_at": null,
        "committed_at": null,
        "drafted_at": "2025-01-01T00:00:00.000Z",
        "reserved_at": null
      },
      "livemode": true,
      "cadence": "bc_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy"
    }
  ],
  "next_page_url": null,
  "previous_page_url": null
}
Cancel a billing intent v2
Ask about this section
Copy for LLM

View as Markdown
Cancel a Billing Intent.

Learn more about calling API v2 endpoints. 
Parameters

id
string
Required
The ID of the Billing Intent to cancel.

Returns
Response attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.intent"
String representing the object’s type. Objects of the same type share the same value of the object field.


amount_details
dictionary
Breakdown of the amount for this Billing Intent.

Show child attributes

cadence
nullable string
ID of an existing Cadence to use.


created
timestamp
Time at which the object was created.


currency
string
Three-letter ISO currency code, in lowercase. Must be a supported currency.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


status
enum
Current status of the Billing Intent.

Possible enum values
canceled
The Billing Intent is canceled.

committed
The Billing Intent is committed.

draft
The Billing Intent is in draft state.

reserved
The Billing Intent is reserved.


status_transitions
dictionary
Timestamps for status transitions of the Billing Intent.

Show child attributes
Error Codes
400
invalid_status_for_cancel
Returned when billing intent is committed or canceled.

404
billing_intent_not_found
Returned when billing intent is not found.

POST 
/v2/billing/intents/:id/cancel
Server-side language
cURL
curl -X POST https://api.stripe.com/v2/billing/intents/bilint_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy/cancel \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "amount_details": {
    "currency": "usd",
    "discount": 0,
    "shipping": 0,
    "subtotal": 2000,
    "tax": 200,
    "total": 2200
  },
  "created": "2025-01-01T00:00:00.000Z",
  "currency": "usd",
  "id": "bilint_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "object": "v2.billing.billing_intent",
  "status": "canceled",
  "status_transitions": {
    "canceled_at": "2025-01-05T00:00:00.000Z",
    "committed_at": null,
    "drafted_at": "2025-01-01T00:00:00.000Z",
    "reserved_at": null
  },
  "livemode": true,
  "cadence": "bc_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy"
}
Commit a billing intent v2
Ask about this section
Copy for LLM

View as Markdown
Commit a Billing Intent.

Learn more about calling API v2 endpoints. 
Parameters

id
string
Required
The ID of the Billing Intent to commit.


payment_intent
string
ID of the PaymentIntent associated with this commit.

Returns
Response attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.intent"
String representing the object’s type. Objects of the same type share the same value of the object field.


amount_details
dictionary
Breakdown of the amount for this Billing Intent.

Show child attributes

cadence
nullable string
ID of an existing Cadence to use.


created
timestamp
Time at which the object was created.


currency
string
Three-letter ISO currency code, in lowercase. Must be a supported currency.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


status
enum
Current status of the Billing Intent.

Possible enum values
canceled
The Billing Intent is canceled.

committed
The Billing Intent is committed.

draft
The Billing Intent is in draft state.

reserved
The Billing Intent is reserved.


status_transitions
dictionary
Timestamps for status transitions of the Billing Intent.

Show child attributes
Error Codes
400
billing_cadence_inactive
Returned when trying to create or update a billing intent with an inactive billing cadence.

400
invalid_status_for_commit
Returned when trying to commit a billing intent and the status is not in reserved.

400
payment_intent_amount_invalid
Returned when the payment intent does not have an amount matching the billing intent’s total amount.

400
payment_intent_customer_invalid
Returned when the payment intent customer does not match the billing cadence payer.

400
payment_intent_status_invalid
Returned when the payment intent does not have a succeeded status.

400
payment_not_required
Returned when a payment intent is provided for a billing intent with a non-positive total amount.

400
payment_not_required_for_send_invoice
Returned when a payment intent is provided and the billing cadence has a send_invoice collection setting.

400
payment_required_to_commit
Returned when a payment intent is required to commit the billing intent.

400
pricing_plan_inactive
Returned when trying to create or modify a subscription for an inactive pricing plan.

400
pricing_plan_subscription_already_exists
Returned when a user tries to create a pricing plan subscription for a billing cadence that has already subscribed to the same pricing plan.

400
rate_card_subscription_already_exists
Returned when a user tries to create a rate card subscription for a billing cadence that has already subscribed to the same rate card.

400
too_many_active_pricing_plan_subscriptions
Returned when a user tries to create a pricing plan subscription for a billing cadence that has already reached the limit of active pricing plan subscriptions.

400
too_many_active_rate_card_subscriptions
Returned when a user tries to create a rate card subscription for a billing cadence that has already reached the limit of active subscriptions.

400
too_many_unused_credit_grants
Returned when trying to create new credit grants for a customer who already has too many unused credit grants.

404
billing_intent_not_found
Returned when billing intent is not found.

404
payment_intent_not_found
Returned when payment intent is not found.

404
payment_record_not_found
Returned when payment record is not found.

POST 
/v2/billing/intents/:id/commit
Server-side language
cURL
curl -X POST https://api.stripe.com/v2/billing/intents/bilint_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy/commit \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "amount_details": {
    "currency": "usd",
    "discount": 0,
    "shipping": 0,
    "subtotal": 2000,
    "tax": 200,
    "total": 2200
  },
  "created": "2025-01-01T00:00:00.000Z",
  "currency": "usd",
  "id": "bilint_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "object": "v2.billing.billing_intent",
  "status": "committed",
  "status_transitions": {
    "canceled_at": null,
    "committed_at": "2025-01-01T00:00:00.000Z",
    "drafted_at": "2025-01-01T00:00:00.000Z",
    "reserved_at": "2025-01-01T00:00:00.000Z"
  },
  "livemode": true,
  "cadence": "bc_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy"
}
Release a billing intent v2
Ask about this section
Copy for LLM

View as Markdown
Release a Billing Intent.

Learn more about calling API v2 endpoints. 
Parameters

id
string
Required
The ID of the Billing Intent to release.

Returns
Response attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.intent"
String representing the object’s type. Objects of the same type share the same value of the object field.


amount_details
dictionary
Breakdown of the amount for this Billing Intent.

Show child attributes

cadence
nullable string
ID of an existing Cadence to use.


created
timestamp
Time at which the object was created.


currency
string
Three-letter ISO currency code, in lowercase. Must be a supported currency.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


status
enum
Current status of the Billing Intent.

Possible enum values
canceled
The Billing Intent is canceled.

committed
The Billing Intent is committed.

draft
The Billing Intent is in draft state.

reserved
The Billing Intent is reserved.


status_transitions
dictionary
Timestamps for status transitions of the Billing Intent.

Show child attributes
Error Codes
400
invalid_status_for_release
Returned when billing intent is not reserved.

404
billing_intent_not_found
Returned when billing intent is not found.

POST 
/v2/billing/intents/:id/release_reservation
Server-side language
cURL
curl -X POST https://api.stripe.com/v2/billing/intents/bilint_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy/release_reservation \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "amount_details": {
    "currency": "usd",
    "discount": 0,
    "shipping": 0,
    "subtotal": 2000,
    "tax": 200,
    "total": 2200
  },
  "created": "2025-01-01T00:00:00.000Z",
  "currency": "usd",
  "id": "bilint_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "object": "v2.billing.billing_intent",
  "status": "draft",
  "status_transitions": {
    "canceled_at": null,
    "committed_at": null,
    "drafted_at": "2025-01-01T00:00:00.000Z",
    "reserved_at": null
  },
  "livemode": true,
  "cadence": "bc_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy"
}
Reserve a billing intent v2
Ask about this section
Copy for LLM

View as Markdown
Reserve a Billing Intent.

Learn more about calling API v2 endpoints. 
Parameters

id
string
Required
The ID of the Billing Intent to reserve.

Returns
Response attributes

id
string
Unique identifier for the object.


object
string, value is "v2.billing.intent"
String representing the object’s type. Objects of the same type share the same value of the object field.


amount_details
dictionary
Breakdown of the amount for this Billing Intent.

Show child attributes

cadence
nullable string
ID of an existing Cadence to use.


created
timestamp
Time at which the object was created.


currency
string
Three-letter ISO currency code, in lowercase. Must be a supported currency.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


status
enum
Current status of the Billing Intent.

Possible enum values
canceled
The Billing Intent is canceled.

committed
The Billing Intent is committed.

draft
The Billing Intent is in draft state.

reserved
The Billing Intent is reserved.


status_transitions
dictionary
Timestamps for status transitions of the Billing Intent.

Show child attributes
Error Codes
400
amount_too_large
Returned when the billing intent total amount due is greater than the maximum amount allowed.

400
amount_too_small
Returned when the billing intent total amount due is less than the minimum amount allowed.

400
invalid_status_for_reserve
Returned when trying to reserve a billing intent and the status is not in draft.

404
billing_intent_not_found
Returned when billing intent is not found.

POST 
/v2/billing/intents/:id/reserve
Server-side language
cURL
curl -X POST https://api.stripe.com/v2/billing/intents/bilint_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy/reserve \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "amount_details": {
    "currency": "usd",
    "discount": 0,
    "shipping": 0,
    "subtotal": 2000,
    "tax": 200,
    "total": 2200
  },
  "created": "2025-01-01T00:00:00.000Z",
  "currency": "usd",
  "id": "bilint_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy",
  "object": "v2.billing.billing_intent",
  "status": "reserved",
  "status_transitions": {
    "canceled_at": null,
    "committed_at": null,
    "drafted_at": "2025-01-01T00:00:00.000Z",
    "reserved_at": "2025-01-01T00:00:00.000Z"
  },
  "livemode": true,
  "cadence": "bc_61SbQ4ZVMJ2ESqq2416S40x4RVA8P2F2ShZStd6x6RCy"
}


Billing Settings v2
Ask about this section
Copy for LLM

View as Markdown
Billing Settings are the centralized location for configuring the various settings for billing related objects.

Learn more about calling API v2 endpoints. 
Endpoints
POST
/v2/billing/bill_settings
POST
/v2/billing/collection_settings
POST
/v2/billing/bill_settings/:id
POST
/v2/billing/collection_settings/:id
GET
/v2/billing/bill_settings/:id
GET
/v2/billing/bill_settings/:id/versions/:id
GET
/v2/billing/collection_settings/:id
GET
/v2/billing/collection_settings/:id/versions/:id
GET
/v2/billing/bill_settings
GET
/v2/billing/bill_settings/:id/versions
GET
/v2/billing/collection_settings
GET
/v2/billing/collection_settings/:id/versions
The Collection Setting object v2
Ask about this section
Copy for LLM

View as Markdown
Attributes

id
string
The ID of the CollectionSetting.


object
string, value is "v2.billing.collection_setting"
String representing the object’s type. Objects of the same type share the same value of the object field.


collection_method
nullable enum
Either automatic, or send_invoice. When charging automatically, Stripe will attempt to pay this bill at the end of the period using the payment method attached to the payer profile. When sending an invoice, Stripe will email your payer profile an invoice with payment instructions. Defaults to automatic.

Possible enum values
automatic
Automatically charge for collection.

send_invoice
Send invoice for collection.


created
timestamp
Timestamp of when the object was created.


display_name
nullable string
An optional field for adding a display name for the CollectionSetting object.


email_delivery
nullable dictionary
Email delivery settings.

Show child attributes

latest_version
string
The latest version of the current settings object. This will be Updated every time an attribute of the settings is updated.


live_version
string
The current live version of the settings object. This can be different from latest_version if settings are updated without setting live_version=‘latest’.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
A lookup key used to retrieve settings dynamically from a static string. This may be up to 200 characters.


payment_method_configuration
nullable string
The ID of the PaymentMethodConfiguration object, which controls which payment methods are displayed to your customers.


payment_method_options
nullable dictionary
Payment Method specific configuration stored on the object.

Show child attributes
The Collection Setting object
{
  "id": "bclset_test_61SIqALsEreXk4vb616S0Sp34rSQ5rdid9OCzVKXYQrI",
  "object": "v2.billing.collection_setting",
  "collection_method": "automatic",
  "created": "2025-01-01T10:00:00.000Z",
  "display_name": "Automatic tax settings",
  "latest_version": "bclsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum",
  "live_version": "bclsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum"
}
The Bill Setting object v2
Ask about this section
Copy for LLM

View as Markdown
Attributes

id
string
The ID of the BillSetting object.


object
string, value is "v2.billing.bill_setting"
String representing the object’s type. Objects of the same type share the same value of the object field.


calculation
nullable dictionary
Settings related to calculating a bill.

Show child attributes

created
timestamp
Timestamp of when the object was created.


display_name
nullable string
An optional field for adding a display name for the BillSetting object.


invoice
nullable dictionary
Settings related to invoice behavior.

Show child attributes

invoice_rendering_template
nullable string
The ID of the invoice rendering template to be used when generating invoices.


latest_version
string
The latest version of the current settings object. This will be Updated every time an attribute of the settings is updated.


live_version
string
The current live version of the settings object. This can be different from latest_version if settings are updated without setting live_version=‘latest’.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
A lookup key used to retrieve settings dynamically from a static string. This may be up to 200 characters.

The Bill Setting object
{
  "id": "bblset_test_61SIqALsEreXk4vb616S0Sp34rSQ5rdid9OCzVKXYQrI",
  "object": "v2.billing.bill_setting",
  "calculation": {
    "tax": {
      "type": "automatic"
    }
  },
  "created": "2025-01-01T10:00:00.000Z",
  "display_name": "Automatic tax settings",
  "latest_version": "bblsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum",
  "live_version": "bblsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum"
}
The Bill Setting Version object v2
Ask about this section
Copy for LLM

View as Markdown
Attributes

id
string
The ID of the BillSettingVersion object.


object
string, value is "v2.billing.bill_setting_version"
String representing the object’s type. Objects of the same type share the same value of the object field.


calculation
nullable dictionary
Settings related to calculating a bill.

Show child attributes

created
timestamp
Timestamp of when the object was created.


invoice
nullable dictionary
Settings related to invoice behavior.

Show child attributes

invoice_rendering_template
nullable string
The ID of the invoice rendering template to be used when generating invoices.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.

The Bill Setting Version object
{
  "calculation": {
    "tax": {
      "type": "automatic"
    }
  },
  "created": "2025-01-01T00:00:00.000Z",
  "id": "bblsetv_test_61T2gNXz4yci3XdEH16Sg5eV2tSQs27bdBltKwQGm4k4",
  "invoice": {
    "time_until_due": {
      "interval": "day",
      "interval_count": 1
    }
  },
  "invoice_rendering_template": "inrtem_test_1RYqt9H5wvQ9UC0Vtppz2bSj",
  "object": "v2.billing.bill_setting_version",
  "livemode": true
}
The Collection Setting Version object v2
Ask about this section
Copy for LLM

View as Markdown
Attributes

id
string
The ID of the CollectionSettingVersion object.


object
string, value is "v2.billing.collection_setting_version"
String representing the object’s type. Objects of the same type share the same value of the object field.


collection_method
nullable enum
Either automatic, or send_invoice. When charging automatically, Stripe will attempt to pay this bill at the end of the period using the payment method attached to the payer profile. When sending an invoice, Stripe will email your payer profile an invoice with payment instructions. Defaults to automatic.

Possible enum values
automatic
Automatically charge for collection.

send_invoice
Send invoice for collection.


created
timestamp
Timestamp of when the object was created.


email_delivery
nullable dictionary
Email delivery settings.

Show child attributes

livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


payment_method_configuration
nullable string
The ID of the PaymentMethodConfiguration object, which controls which payment methods are displayed to your customers.


payment_method_options
nullable dictionary
Payment Method specific configuration stored on the object.

Show child attributes
The Collection Setting Version object
{
  "collection_method": "automatic",
  "created": "2025-01-01T00:00:00.000Z",
  "id": "bclsetv_test_61T2gtFFCeOrTS7PB16Sg5eV2tSQs27bdBltKwQGm1No",
  "object": "v2.billing.collection_setting_version",
  "payment_method_configuration": "pmc_234",
  "payment_method_options": {
    "acss_debit": {
      "mandate_options": {
        "transaction_type": "business"
      },
      "verification_method": "automatic"
    },
    "bancontact": {
      "preferred_language": "de"
    },
    "card": {
      "mandate_options": {
        "amount": 1000,
        "amount_type": "maximum",
        "description": "Test mandate"
      },
      "network": "visa",
      "request_three_d_secure": "any"
    },
    "customer_balance": {
      "bank_transfer": {
        "eu_bank_transfer": {
          "country": "BE"
        },
        "type": "eu_bank_transfer"
      },
      "funding_type": "bank_transfer"
    },
    "konbini": {},
    "sepa_debit": {},
    "us_bank_account": {
      "financial_connections": {
        "filters": {
          "account_subcategories": [
            "checking"
          ]
        },
        "permissions": [
          "balances"
        ],
        "prefetch": [
          "balances"
        ]
      },
      "verification_method": "automatic"
    }
  },
  "livemode": true
}
Create a Bill Setting v2
Ask about this section
Copy for LLM

View as Markdown
Create a BillSetting object.

Learn more about calling API v2 endpoints. 
Parameters

calculation
dictionary
Settings related to calculating a bill.

Show child parameters

display_name
string
An optional customer-facing display name for the CollectionSetting object. Maximum length of 250 characters.


invoice
dictionary
Settings related to invoice behavior.

Show child parameters

invoice_rendering_template
string
The ID of the invoice rendering template to be used when generating invoices.


lookup_key
string
A lookup key used to retrieve settings dynamically from a static string. This may be up to 200 characters.

Returns
Response attributes

id
string
The ID of the BillSetting object.


object
string, value is "v2.billing.bill_setting"
String representing the object’s type. Objects of the same type share the same value of the object field.


calculation
nullable dictionary
Settings related to calculating a bill.

Show child attributes

created
timestamp
Timestamp of when the object was created.


display_name
nullable string
An optional field for adding a display name for the BillSetting object.


invoice
nullable dictionary
Settings related to invoice behavior.

Show child attributes

invoice_rendering_template
nullable string
The ID of the invoice rendering template to be used when generating invoices.


latest_version
string
The latest version of the current settings object. This will be Updated every time an attribute of the settings is updated.


live_version
string
The current live version of the settings object. This can be different from latest_version if settings are updated without setting live_version=‘latest’.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
A lookup key used to retrieve settings dynamically from a static string. This may be up to 200 characters.

Error Codes
400
automatic_tax_no_merchant_location
Returned when the merchant doesn’t have a valid origin address.

400
invalid_invoice_rendering_template_for_bill_setting
Returned when the invoice rendering template is archived.

400
invoice_rendering_template_not_found_for_bill_setting
Returned when the invoice rendering template cannot be found.

400
lookup_key_already_used_for_bill_setting
Returned when the lookup key is already used for a bill setting.

POST 
/v2/billing/bill_settings
cURL
curl -X POST https://api.stripe.com/v2/billing/bill_settings \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "Automatic tax settings",
    "calculation": {
        "tax": {
            "type": "automatic"
        }
    }
  }'
Response
{
  "id": "bblset_test_61SIqALsEreXk4vb616S0Sp34rSQ5rdid9OCzVKXYQrI",
  "object": "v2.billing.bill_setting",
  "calculation": {
    "tax": {
      "type": "automatic"
    }
  },
  "created": "2025-01-01T10:00:00.000Z",
  "display_name": "Automatic tax settings",
  "latest_version": "bblsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum",
  "live_version": "bblsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum",
  "livemode": true
}
Create a Collection Setting v2
Ask about this section
Copy for LLM

View as Markdown
Create a CollectionSetting object.

Learn more about calling API v2 endpoints. 
Parameters

collection_method
enum
Either automatic, or send_invoice. When charging automatically, Stripe will attempt to pay this bill at the end of the period using the payment method attached to the payer profile. When sending an invoice, Stripe will email your payer profile an invoice with payment instructions. Defaults to automatic.

Possible enum values
automatic
Automatically charge for collection.

send_invoice
Send invoice for collection.


display_name
string
An optional customer-facing display name for the CollectionSetting object. Maximum length of 250 characters.


email_delivery
dictionary
Email delivery setting.

Show child parameters

lookup_key
string
A lookup key used to retrieve settings dynamically from a static string. This may be up to 200 characters.


payment_method_configuration
string
The ID of the PaymentMethodConfiguration object, which controls which payment methods are displayed to your customers.


payment_method_options
dictionary
Payment Method specific configuration to be stored on the object.

Show child parameters
Returns
Response attributes

id
string
The ID of the CollectionSetting.


object
string, value is "v2.billing.collection_setting"
String representing the object’s type. Objects of the same type share the same value of the object field.


collection_method
nullable enum
Either automatic, or send_invoice. When charging automatically, Stripe will attempt to pay this bill at the end of the period using the payment method attached to the payer profile. When sending an invoice, Stripe will email your payer profile an invoice with payment instructions. Defaults to automatic.

Possible enum values
automatic
Automatically charge for collection.

send_invoice
Send invoice for collection.


created
timestamp
Timestamp of when the object was created.


display_name
nullable string
An optional field for adding a display name for the CollectionSetting object.


email_delivery
nullable dictionary
Email delivery settings.

Show child attributes

latest_version
string
The latest version of the current settings object. This will be Updated every time an attribute of the settings is updated.


live_version
string
The current live version of the settings object. This can be different from latest_version if settings are updated without setting live_version=‘latest’.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
A lookup key used to retrieve settings dynamically from a static string. This may be up to 200 characters.


payment_method_configuration
nullable string
The ID of the PaymentMethodConfiguration object, which controls which payment methods are displayed to your customers.


payment_method_options
nullable dictionary
Payment Method specific configuration stored on the object.

Show child attributes
Error Codes
400
email_delivery_incompatible_with_collection_method
Returned when the email delivery is incompatible with the collection method.

400
invalid_payment_method_configuration_for_collection_setting
Returned when the payment method configuration is not active.

400
lookup_key_already_used_for_collection_setting
Returned when the lookup key is already used for a collection setting.

400
payment_method_configuration_not_found_for_collection_setting
Returned when the payment method configuration cannot be found.

POST 
/v2/billing/collection_settings
cURL
curl -X POST https://api.stripe.com/v2/billing/collection_settings \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "collection_method": "automatic",
    "display_name": "Automatic collection settings"
  }'
Response
{
  "id": "bclset_test_61SIqALsEreXk4vb616S0Sp34rSQ5rdid9OCzVKXYQrI",
  "object": "v2.billing.collection_setting",
  "collection_method": "automatic",
  "created": "2025-01-01T10:00:00.000Z",
  "display_name": "Automatic tax settings",
  "latest_version": "bclsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum",
  "live_version": "bclsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum",
  "livemode": true
}
Update a Bill Setting v2
Ask about this section
Copy for LLM

View as Markdown
Update fields on an existing BillSetting object.

Learn more about calling API v2 endpoints. 
Parameters

id
string
Required
The ID of the BillSetting object to update.


calculation
dictionary
Settings related to calculating a bill.

Show child parameters

display_name
string
An optional customer-facing display name for the BillSetting object. To remove the display name, set it to an empty string in the request. Maximum length of 250 characters.


invoice
dictionary
Settings related to invoice behavior.

Show child parameters

invoice_rendering_template
string
The ID of the invoice rendering template to be used when generating invoices.


live_version
string
Optionally change the live version of the BillSetting. Providing live_version = "latest" will set the BillSetting’ live_version to its latest version.


lookup_key
string
A lookup key used to retrieve settings dynamically from a static string. This may be up to 200 characters.

Returns
Response attributes

id
string
The ID of the BillSetting object.


object
string, value is "v2.billing.bill_setting"
String representing the object’s type. Objects of the same type share the same value of the object field.


calculation
nullable dictionary
Settings related to calculating a bill.

Show child attributes

created
timestamp
Timestamp of when the object was created.


display_name
nullable string
An optional field for adding a display name for the BillSetting object.


invoice
nullable dictionary
Settings related to invoice behavior.

Show child attributes

invoice_rendering_template
nullable string
The ID of the invoice rendering template to be used when generating invoices.


latest_version
string
The latest version of the current settings object. This will be Updated every time an attribute of the settings is updated.


live_version
string
The current live version of the settings object. This can be different from latest_version if settings are updated without setting live_version=‘latest’.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
A lookup key used to retrieve settings dynamically from a static string. This may be up to 200 characters.

Error Codes
400
automatic_tax_no_merchant_location
Returned when the merchant doesn’t have a valid origin address.

400
invalid_invoice_rendering_template_for_bill_setting
Returned when the invoice rendering template is archived.

400
invoice_rendering_template_not_found_for_bill_setting
Returned when the invoice rendering template cannot be found.

400
lookup_key_already_used_for_bill_setting
Returned when the lookup key is already used for a bill setting.

404
bill_setting_not_found
Returned when the bill setting cannot be found.

POST 
/v2/billing/bill_settings/:id
cURL
curl -X POST https://api.stripe.com/v2/billing/bill_settings/bblset_test_61SIqALsEreXk4vb616S0Sp34rSQ5rdid9OCzVKXYQrI \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "New name"
  }'
Response
{
  "id": "bblset_test_61SIqALsEreXk4vb616S0Sp34rSQ5rdid9OCzVKXYQrI",
  "object": "v2.billing.bill_setting",
  "calculation": {
    "tax": {
      "type": "automatic"
    }
  },
  "created": "2025-01-01T10:00:00.000Z",
  "display_name": "New name",
  "latest_version": "bblsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum",
  "live_version": "bblsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum",
  "livemode": true
}
Update a Collection Setting v2
Ask about this section
Copy for LLM

View as Markdown
Update fields on an existing CollectionSetting.

Learn more about calling API v2 endpoints. 
Parameters

id
string
Required
The ID of the CollectionSetting.


collection_method
enum
Either automatic, or send_invoice. When charging automatically, Stripe will attempt to pay this bill at the end of the period using the payment method attached to the payer profile. When sending an invoice, Stripe will email your payer profile an invoice with payment instructions.

Possible enum values
automatic
Automatically charge for collection.

send_invoice
Send invoice for collection.


display_name
string
An optional customer-facing display name for the CollectionSetting object. To remove the display name, set it to an empty string in the request. Maximum length of 250 characters.


email_delivery
dictionary
Email delivery settings.

Show child parameters

live_version
string
Optionally change the live version of the CollectionSetting. Billing Cadences and other objects that refer to this CollectionSetting will use this version when no overrides are set. Providing live_version = "latest" will set the CollectionSetting’s live_version to its latest version.


lookup_key
string
A lookup key used to retrieve settings dynamically from a static string. This may be up to 200 characters.


payment_method_configuration
string
The ID of the PaymentMethodConfiguration object, which controls which payment methods are displayed to your customers.


payment_method_options
dictionary
Payment Method specific configuration to be stored on the object.

Show child parameters
Returns
Response attributes

id
string
The ID of the CollectionSetting.


object
string, value is "v2.billing.collection_setting"
String representing the object’s type. Objects of the same type share the same value of the object field.


collection_method
nullable enum
Either automatic, or send_invoice. When charging automatically, Stripe will attempt to pay this bill at the end of the period using the payment method attached to the payer profile. When sending an invoice, Stripe will email your payer profile an invoice with payment instructions. Defaults to automatic.

Possible enum values
automatic
Automatically charge for collection.

send_invoice
Send invoice for collection.


created
timestamp
Timestamp of when the object was created.


display_name
nullable string
An optional field for adding a display name for the CollectionSetting object.


email_delivery
nullable dictionary
Email delivery settings.

Show child attributes

latest_version
string
The latest version of the current settings object. This will be Updated every time an attribute of the settings is updated.


live_version
string
The current live version of the settings object. This can be different from latest_version if settings are updated without setting live_version=‘latest’.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
A lookup key used to retrieve settings dynamically from a static string. This may be up to 200 characters.


payment_method_configuration
nullable string
The ID of the PaymentMethodConfiguration object, which controls which payment methods are displayed to your customers.


payment_method_options
nullable dictionary
Payment Method specific configuration stored on the object.

Show child attributes
Error Codes
400
collection_method_incompatible_with_email_delivery
Returned when the collection method is incompatible with the email delivery.

400
email_delivery_incompatible_with_collection_method
Returned when the email delivery is incompatible with the collection method.

400
invalid_payment_method_configuration_for_collection_setting
Returned when the payment method configuration is not active.

400
lookup_key_already_used_for_collection_setting
Returned when the lookup key is already used for a collection setting.

400
payment_method_configuration_not_found_for_collection_setting
Returned when the payment method configuration cannot be found.

404
collection_setting_not_found
Returned when the collection setting cannot be found.

POST 
/v2/billing/collection_settings/:id
cURL
curl -X POST https://api.stripe.com/v2/billing/collection_settings/bclset_test_61SIqALsEreXk4vb616S0Sp34rSQ5rdid9OCzVKXYQrI \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "display_name": "New name",
    "collection_method": "send_invoice"
  }'
Response
{
  "id": "bclset_test_61SIqALsEreXk4vb616S0Sp34rSQ5rdid9OCzVKXYQrI",
  "object": "v2.billing.collection_setting",
  "collection_method": "send_invoice",
  "created": "2025-01-01T10:00:00.000Z",
  "display_name": "New name",
  "latest_version": "bclsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum",
  "live_version": "bclsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum",
  "livemode": true
}
Retrieve a Bill Setting v2
Ask about this section
Copy for LLM

View as Markdown
Retrieve a BillSetting object by ID.

Learn more about calling API v2 endpoints. 
Parameters

id
string
Required
The ID of the BillSetting object to retrieve.

Returns
Response attributes

id
string
The ID of the BillSetting object.


object
string, value is "v2.billing.bill_setting"
String representing the object’s type. Objects of the same type share the same value of the object field.


calculation
nullable dictionary
Settings related to calculating a bill.

Show child attributes

created
timestamp
Timestamp of when the object was created.


display_name
nullable string
An optional field for adding a display name for the BillSetting object.


invoice
nullable dictionary
Settings related to invoice behavior.

Show child attributes

invoice_rendering_template
nullable string
The ID of the invoice rendering template to be used when generating invoices.


latest_version
string
The latest version of the current settings object. This will be Updated every time an attribute of the settings is updated.


live_version
string
The current live version of the settings object. This can be different from latest_version if settings are updated without setting live_version=‘latest’.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
A lookup key used to retrieve settings dynamically from a static string. This may be up to 200 characters.

Error Codes
404
bill_setting_not_found
Returned when the bill setting cannot be found.

GET 
/v2/billing/bill_settings/:id
cURL
curl https://api.stripe.com/v2/billing/bill_settings/bblset_test_61SIqALsEreXk4vb616S0Sp34rSQ5rdid9OCzVKXYQrI \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "id": "bblset_test_61SIqALsEreXk4vb616S0Sp34rSQ5rdid9OCzVKXYQrI",
  "object": "v2.billing.bill_setting",
  "calculation": {
    "tax": {
      "type": "automatic"
    }
  },
  "created": "2025-01-01T10:00:00.000Z",
  "display_name": "Automatic tax settings",
  "latest_version": "bblsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum",
  "live_version": "bblsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum",
  "livemode": true
}
Retrieve a Bill Setting Version v2
Ask about this section
Copy for LLM

View as Markdown
Retrieve a BillSettingVersion by ID.

Learn more about calling API v2 endpoints. 
Parameters

bill_setting_id
string
Required
The ID of the BillSetting object to retrieve the version from.


id
string
Required
The ID of the BillSettingVersion object to retrieve.

Returns
Response attributes

id
string
The ID of the BillSettingVersion object.


object
string, value is "v2.billing.bill_setting_version"
String representing the object’s type. Objects of the same type share the same value of the object field.


calculation
nullable dictionary
Settings related to calculating a bill.

Show child attributes

created
timestamp
Timestamp of when the object was created.


invoice
nullable dictionary
Settings related to invoice behavior.

Show child attributes

invoice_rendering_template
nullable string
The ID of the invoice rendering template to be used when generating invoices.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.

Error Codes
404
bill_setting_not_found
Returned when the bill setting cannot be found.

404
bill_setting_version_not_found
Returned when the bill setting version cannot be found.

GET 
/v2/billing/bill_settings/:id/versions/:id
Server-side language
cURL
curl https://api.stripe.com/v2/billing/bill_settings/bblset_test_61T2gNXemFgqleYpd16Sg5eV2tSQs27bdBltKwQGm6qO/versions/bblsetv_test_61T2gNXz4yci3XdEH16Sg5eV2tSQs27bdBltKwQGm4k4 \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "calculation": {
    "tax": {
      "type": "automatic"
    }
  },
  "created": "2025-01-01T00:00:00.000Z",
  "id": "bblsetv_test_61T2gNXz4yci3XdEH16Sg5eV2tSQs27bdBltKwQGm4k4",
  "invoice": {
    "time_until_due": {
      "interval": "day",
      "interval_count": 1
    }
  },
  "invoice_rendering_template": "inrtem_test_1RYqt9H5wvQ9UC0Vtppz2bSj",
  "object": "v2.billing.bill_setting_version",
  "livemode": true
}
Retrieve a Collection Setting v2
Ask about this section
Copy for LLM

View as Markdown
Retrieve a CollectionSetting by ID.

Learn more about calling API v2 endpoints. 
Parameters

id
string
Required
The ID of the CollectionSetting.

Returns
Response attributes

id
string
The ID of the CollectionSetting.


object
string, value is "v2.billing.collection_setting"
String representing the object’s type. Objects of the same type share the same value of the object field.


collection_method
nullable enum
Either automatic, or send_invoice. When charging automatically, Stripe will attempt to pay this bill at the end of the period using the payment method attached to the payer profile. When sending an invoice, Stripe will email your payer profile an invoice with payment instructions. Defaults to automatic.

Possible enum values
automatic
Automatically charge for collection.

send_invoice
Send invoice for collection.


created
timestamp
Timestamp of when the object was created.


display_name
nullable string
An optional field for adding a display name for the CollectionSetting object.


email_delivery
nullable dictionary
Email delivery settings.

Show child attributes

latest_version
string
The latest version of the current settings object. This will be Updated every time an attribute of the settings is updated.


live_version
string
The current live version of the settings object. This can be different from latest_version if settings are updated without setting live_version=‘latest’.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
A lookup key used to retrieve settings dynamically from a static string. This may be up to 200 characters.


payment_method_configuration
nullable string
The ID of the PaymentMethodConfiguration object, which controls which payment methods are displayed to your customers.


payment_method_options
nullable dictionary
Payment Method specific configuration stored on the object.

Show child attributes
Error Codes
404
collection_setting_not_found
Returned when the collection setting cannot be found.

GET 
/v2/billing/collection_settings/:id
cURL
curl https://api.stripe.com/v2/billing/collection_settings/bclset_test_61SIqALsEreXk4vb616S0Sp34rSQ5rdid9OCzVKXYQrI \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "id": "bclset_test_61SIqALsEreXk4vb616S0Sp34rSQ5rdid9OCzVKXYQrI",
  "object": "v2.billing.collection_setting",
  "collection_method": "automatic",
  "created": "2025-01-01T10:00:00.000Z",
  "display_name": "Automatic tax settings",
  "latest_version": "bclsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum",
  "live_version": "bclsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum",
  "livemode": true
}
Retrieve a Collection Setting Version v2
Ask about this section
Copy for LLM

View as Markdown
Retrieve a CollectionSetting Version by ID.

Learn more about calling API v2 endpoints. 
Parameters

collection_setting_id
string
Required
The ID of the CollectionSetting that has the version.


id
string
Required
The ID of the CollectionSettingVersion.

Returns
Response attributes

id
string
The ID of the CollectionSettingVersion object.


object
string, value is "v2.billing.collection_setting_version"
String representing the object’s type. Objects of the same type share the same value of the object field.


collection_method
nullable enum
Either automatic, or send_invoice. When charging automatically, Stripe will attempt to pay this bill at the end of the period using the payment method attached to the payer profile. When sending an invoice, Stripe will email your payer profile an invoice with payment instructions. Defaults to automatic.

Possible enum values
automatic
Automatically charge for collection.

send_invoice
Send invoice for collection.


created
timestamp
Timestamp of when the object was created.


email_delivery
nullable dictionary
Email delivery settings.

Show child attributes

livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


payment_method_configuration
nullable string
The ID of the PaymentMethodConfiguration object, which controls which payment methods are displayed to your customers.


payment_method_options
nullable dictionary
Payment Method specific configuration stored on the object.

Show child attributes
Error Codes
404
collection_setting_not_found
Returned when the collection setting cannot be found.

404
collection_setting_version_not_found
Returned when the collection setting version cannot be found.

GET 
/v2/billing/collection_settings/:id/versions/:id
Server-side language
cURL
curl https://api.stripe.com/v2/billing/collection_settings/bclset_test_61T2gtFM6pBAo30oj16Sg5eV2tSQs27bdBltKwQGmSI4/versions/bclsetv_test_61T2gtFFCeOrTS7PB16Sg5eV2tSQs27bdBltKwQGm1No \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "collection_method": "automatic",
  "created": "2025-01-01T00:00:00.000Z",
  "id": "bclsetv_test_61T2gtFFCeOrTS7PB16Sg5eV2tSQs27bdBltKwQGm1No",
  "object": "v2.billing.collection_setting_version",
  "payment_method_configuration": "pmc_234",
  "payment_method_options": {
    "acss_debit": {
      "mandate_options": {
        "transaction_type": "business"
      },
      "verification_method": "automatic"
    },
    "bancontact": {
      "preferred_language": "de"
    },
    "card": {
      "mandate_options": {
        "amount": 1000,
        "amount_type": "maximum",
        "description": "Test mandate"
      },
      "network": "visa",
      "request_three_d_secure": "any"
    },
    "customer_balance": {
      "bank_transfer": {
        "eu_bank_transfer": {
          "country": "BE"
        },
        "type": "eu_bank_transfer"
      },
      "funding_type": "bank_transfer"
    },
    "konbini": {},
    "sepa_debit": {},
    "us_bank_account": {
      "financial_connections": {
        "filters": {
          "account_subcategories": [
            "checking"
          ]
        },
        "permissions": [
          "balances"
        ],
        "prefetch": [
          "balances"
        ]
      },
      "verification_method": "automatic"
    }
  },
  "livemode": true
}
List Bill Settings v2
Ask about this section
Copy for LLM

View as Markdown
List all BillSetting objects.

Learn more about calling API v2 endpoints. 
Parameters

limit
integer
Optionally set the maximum number of results per page. Defaults to 20.


lookup_keys
array of strings
Only return the settings with these lookup_keys, if any exist. You can specify up to 10 lookup_keys.


page
string
Opaque page token.

Returns
Response attributes

data
array of dictionaries
The list of retrieved Bill Settings.

Show child attributes

next_page_url
nullable string
The URL of the next page of results, if there is one.


previous_page_url
nullable string
The URL of the previous page of results, if there is one.

GET 
/v2/billing/bill_settings
cURL
curl https://api.stripe.com/v2/billing/bill_settings \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "data": [
    {
      "id": "bblset_test_61SIqALsEreXk4vb616S0Sp34rSQ5rdid9OCzVKXYQrI",
      "object": "v2.billing.bill_setting",
      "calculation": {
        "tax": {
          "type": "automatic"
        }
      },
      "created": "2025-01-01T10:00:00.000Z",
      "display_name": "Automatic tax settings",
      "latest_version": "bblsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum",
      "live_version": "bblsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum",
      "livemode": true
    }
  ]
}
List Bill Setting Versions v2
Ask about this section
Copy for LLM

View as Markdown
List all BillSettingVersions by BillSetting ID.

Learn more about calling API v2 endpoints. 
Parameters

bill_setting_id
string
Required
ID of the BillSettings to retrieve versions for.


limit
integer
Optionally set the maximum number of results per page. Defaults to 20.


page
string
Opaque page token.

Returns
Response attributes

data
array of dictionaries
The list of retrieved Bill Setting Versions.

Show child attributes

next_page_url
nullable string
The URL of the next page of results, if there is one.


previous_page_url
nullable string
The URL of the previous page of results, if there is one.

Error Codes
404
bill_setting_not_found
Returned when the bill setting cannot be found.

GET 
/v2/billing/bill_settings/:id/versions
Server-side language
cURL
curl https://api.stripe.com/v2/billing/bill_settings/bblset_test_61T2gNXemFgqleYpd16Sg5eV2tSQs27bdBltKwQGm6qO/versions \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "data": [
    {
      "calculation": {
        "tax": {
          "type": "automatic"
        }
      },
      "created": "2025-01-01T00:00:00.000Z",
      "id": "bblsetv_test_61T2gNXz4yci3XdEH16Sg5eV2tSQs27bdBltKwQGm4k4",
      "invoice": {
        "time_until_due": {
          "interval": "day",
          "interval_count": 1
        }
      },
      "invoice_rendering_template": "inrtem_test_1RYqt9H5wvQ9UC0Vtppz2bSj",
      "object": "v2.billing.bill_setting_version",
      "livemode": true
    }
  ],
  "next_page_url": null,
  "previous_page_url": null
}
List Collection Settings v2
Ask about this section
Copy for LLM

View as Markdown
List all CollectionSetting objects.

Learn more about calling API v2 endpoints. 
Parameters

limit
integer
Optionally set the maximum number of results per page. Defaults to 20.


lookup_keys
array of strings
Only return the settings with these lookup_keys, if any exist. You can specify up to 10 lookup_keys.


page
string
Opaque page token.

Returns
Response attributes

data
array of dictionaries
The list of retrieved CollectionSetting.

Show child attributes

next_page_url
nullable string
The URL of the next page of results, if there is one.


previous_page_url
nullable string
The URL of the previous page of results, if there is one.

GET 
/v2/billing/collection_settings
cURL
curl https://api.stripe.com/v2/billing/collection_settings \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "data": [
    {
      "id": "bclset_test_61SIqALsEreXk4vb616S0Sp34rSQ5rdid9OCzVKXYQrI",
      "object": "v2.billing.collection_setting",
      "collection_method": "automatic",
      "created": "2025-01-01T10:00:00.000Z",
      "display_name": "Automatic tax settings",
      "latest_version": "bclsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum",
      "live_version": "bclsetv_test_61SIqALNs1R6M7aU416S0Sp34rSQ5rdid9OCzVKXYIum",
      "livemode": true
    }
  ]
}
List Collection Setting Versions v2
Ask about this section
Copy for LLM

View as Markdown
List all CollectionSettingVersions by CollectionSetting ID.

Learn more about calling API v2 endpoints. 
Parameters

collection_setting_id
string
Required
ID of the CollectionSettings to retrieve versions for.


limit
integer
Optionally set the maximum number of results per page. Defaults to 20.


page
string
Opaque page token.

Returns
Response attributes

data
array of dictionaries
The list of retrieved CollectionSettingVersions.

Show child attributes

next_page_url
nullable string
The URL of the next page of results, if there is one.


previous_page_url
nullable string
The URL of the previous page of results, if there is one.

Error Codes
404
collection_setting_not_found
Returned when the collection setting cannot be found.

GET 
/v2/billing/collection_settings/:id/versions
Server-side language
cURL
curl https://api.stripe.com/v2/billing/collection_settings/bclset_test_61T2gtFM6pBAo30oj16Sg5eV2tSQs27bdBltKwQGmSI4/versions \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "data": [
    {
      "collection_method": "automatic",
      "created": "2025-01-01T00:00:00.000Z",
      "id": "bclsetv_test_61T2gtFFCeOrTS7PB16Sg5eV2tSQs27bdBltKwQGm1No",
      "object": "v2.billing.collection_setting_version",
      "payment_method_configuration": "pmc_234",
      "payment_method_options": {
        "acss_debit": {
          "mandate_options": {
            "transaction_type": "business"
          },
          "verification_method": "automatic"
        },
        "bancontact": {
          "preferred_language": "de"
        },
        "card": {
          "mandate_options": {
            "amount": 1000,
            "amount_type": "maximum",
            "description": "Test mandate"
          },
          "network": "visa",
          "request_three_d_secure": "any"
        },
        "customer_balance": {
          "bank_transfer": {
            "eu_bank_transfer": {
              "country": "BE"
            },
            "type": "eu_bank_transfer"
          },
          "funding_type": "bank_transfer"
        },
        "konbini": {},
        "sepa_debit": {},
        "us_bank_account": {
          "financial_connections": {
            "filters": {
              "account_subcategories": [
                "checking"
              ]
            },
            "permissions": [
              "balances"
            ],
            "prefetch": [
              "balances"
            ]
          },
          "verification_method": "automatic"
        }
      },
      "livemode": true
    }
  ],
  "next_page_url": null,
  "previous_page_url": null
}
BillSetting event types v2
Ask about this section
Copy for LLM

View as Markdown
This is a list of all public thin events we currently send for updates to BillSetting, which are continually evolving and expanding. The payload of thin events is unversioned. During processing, you must fetch the versioned event from the API or fetch the resource’s current state.

Event types
TypeFilter events by type
Type
Filter events
v2.billing.bill_setting.updated
This event occurs when a Bill Setting is updated.


Billing Profile v2
Ask about this section
Copy for LLM

View as Markdown
A Billing Profile is a representation of how a bill is paid, separating payment behavior from customer identity.

Learn more about calling API v2 endpoints. 
Endpoints
POST
/v2/billing/profiles
POST
/v2/billing/profiles/:id
GET
/v2/billing/profiles/:id
GET
/v2/billing/profiles
The Profile object v2
Ask about this section
Copy for LLM

View as Markdown
Attributes

id
string
The ID of the billing profile object.


object
string, value is "v2.billing.profile"
String representing the object’s type. Objects of the same type share the same value of the object field.


created
timestamp
Timestamp of when the object was created.


customer
nullable string
The ID of the customer object.


default_payment_method
nullable string
The ID of the payment method object.


display_name
nullable string
A customer-facing name for the billing profile. Maximum length of 250 characters.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
An internal key you can use to search for a particular billing profile. Maximum length of 200 characters.


metadata
nullable map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


status
enum
The current status of the billing profile.

Possible enum values
active
The billing profile is active.

inactive
The billing profile is inactive and cannot be used.

The Profile object
{
  "created": "2025-01-01T00:00:00.000Z",
  "customer": "cus_SM22QFjZh7DtOo",
  "default_payment_method": "pm_1RRJyOCZPkOPzJLWkaBPKr4J ",
  "display_name": "Display Name",
  "id": "bilp_61SahwKGATwuyXMY516SBbsMNLSQJnWcho4VDz0fYLKi",
  "lookup_key": "billing_profile_cus_SM22QFjZh7DtOo",
  "metadata": {
    "test": "data"
  },
  "object": "v2.billing.profile",
  "status": "active",
  "livemode": true
}
Create a billing profile v2
Ask about this section
Copy for LLM

View as Markdown
Create a BillingProfile object.

Learn more about calling API v2 endpoints. 
Parameters

customer
string
Required
The ID of the customer object.


default_payment_method
string
The ID of the payment method object.


display_name
string
A customer-facing name for the billing profile. Maximum length of 250 characters.


lookup_key
string
An internal key you can use to search for a particular billing profile. It must be unique among billing profiles for a given customer. Maximum length of 200 characters.


metadata
map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Returns
Response attributes

id
string
The ID of the billing profile object.


object
string, value is "v2.billing.profile"
String representing the object’s type. Objects of the same type share the same value of the object field.


created
timestamp
Timestamp of when the object was created.


customer
nullable string
The ID of the customer object.


default_payment_method
nullable string
The ID of the payment method object.


display_name
nullable string
A customer-facing name for the billing profile. Maximum length of 250 characters.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
An internal key you can use to search for a particular billing profile. Maximum length of 200 characters.


metadata
nullable map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


status
enum
The current status of the billing profile.

Possible enum values
active
The billing profile is active.

inactive
The billing profile is inactive and cannot be used.

Error Codes
400
customer_not_found_for_billing_profile
Returned when the customer for the provided ID cannot be found.

400
invalid_customer_for_billing_profile
Returned when associating a billing profile with a deleted customer.

400
lookup_key_already_exists_for_billing_profile
Returned when the Lookup Key already exists for another billing profile for this customer.

400
payment_method_customer_mismatch_for_billing_profile
Returned when the payment method belongs to a different customer.

400
payment_method_not_found_for_billing_profile
Returned when the payment method for the provided ID cannot be found.

POST 
/v2/billing/profiles
Server-side language
cURL
curl -X POST https://api.stripe.com/v2/billing/profiles \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "customer": "cus_123",
    "default_payment_method": "pm_123",
    "display_name": "Display Name",
    "lookup_key": "billing_profile_cus_123",
    "metadata": {
        "test": "data"
    }
  }'
Response
{
  "created": "2025-01-01T00:00:00.000Z",
  "customer": "cus_123",
  "default_payment_method": "pm_123",
  "display_name": "Display Name",
  "id": "bilp_123",
  "lookup_key": "billing_profile_cus_123",
  "metadata": {
    "test": "data"
  },
  "object": "v2.billing.profile",
  "status": "active",
  "livemode": true
}
Update a billing profile v2
Ask about this section
Copy for LLM

View as Markdown
Update a BillingProfile object.

Learn more about calling API v2 endpoints. 
Parameters

id
string
Required
The ID of the billing profile to update.


default_payment_method
string
The ID of the payment method object.


display_name
string
A customer-facing name for the billing profile. Maximum length of 250 characters. To remove the display_name from the object, set it to null in the request.


lookup_key
string
An internal key you can use to search for a particular billing profile. It must be unique among billing profiles for a given customer. Maximum length of 200 characters. To remove the lookup_key from the object, set it to null in the request.


metadata
map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

Returns
Response attributes

id
string
The ID of the billing profile object.


object
string, value is "v2.billing.profile"
String representing the object’s type. Objects of the same type share the same value of the object field.


created
timestamp
Timestamp of when the object was created.


customer
nullable string
The ID of the customer object.


default_payment_method
nullable string
The ID of the payment method object.


display_name
nullable string
A customer-facing name for the billing profile. Maximum length of 250 characters.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
An internal key you can use to search for a particular billing profile. Maximum length of 200 characters.


metadata
nullable map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


status
enum
The current status of the billing profile.

Possible enum values
active
The billing profile is active.

inactive
The billing profile is inactive and cannot be used.

Error Codes
400
lookup_key_already_exists_for_billing_profile
Returned when the Lookup Key already exists for another billing profile for this customer.

400
payment_method_customer_mismatch_for_billing_profile
Returned when the payment method belongs to a different customer.

400
payment_method_not_found_for_billing_profile
Returned when the payment method for the provided ID cannot be found.

404
billing_profile_not_found
Returned when the Billing Profile for the provided ID cannot be found.

POST 
/v2/billing/profiles/:id
Server-side language
cURL
curl -X POST https://api.stripe.com/v2/billing/profiles/bilp_123 \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --json '{
    "lookup_key": "business_profile_cus_123",
    "display_name": "Business Profile"
  }'
Response
{
  "created": "2025-01-01T00:00:00.000Z",
  "customer": "cus_123",
  "default_payment_method": "pm_123",
  "display_name": "Business Profile",
  "id": "bilp_123",
  "lookup_key": "business_profile_cus_123",
  "metadata": {
    "test": "data"
  },
  "object": "v2.billing.profile",
  "status": "active",
  "livemode": true
}
Retrieve a billing profile v2
Ask about this section
Copy for LLM

View as Markdown
Retrieve a BillingProfile object.

Learn more about calling API v2 endpoints. 
Parameters

id
string
Required
The ID of the billing profile to Retrieve.

Returns
Response attributes

id
string
The ID of the billing profile object.


object
string, value is "v2.billing.profile"
String representing the object’s type. Objects of the same type share the same value of the object field.


created
timestamp
Timestamp of when the object was created.


customer
nullable string
The ID of the customer object.


default_payment_method
nullable string
The ID of the payment method object.


display_name
nullable string
A customer-facing name for the billing profile. Maximum length of 250 characters.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


lookup_key
nullable string
An internal key you can use to search for a particular billing profile. Maximum length of 200 characters.


metadata
nullable map
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


status
enum
The current status of the billing profile.

Possible enum values
active
The billing profile is active.

inactive
The billing profile is inactive and cannot be used.

Error Codes
404
billing_profile_not_found
Returned when the Billing Profile for the provided ID cannot be found.

GET 
/v2/billing/profiles/:id
Server-side language
cURL
curl https://api.stripe.com/v2/billing/profiles/bilp_123 \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "created": "2025-01-01T00:00:00.000Z",
  "customer": "cus_123",
  "default_payment_method": "pm_123",
  "display_name": "Display Name",
  "id": "bilp_123",
  "lookup_key": "billing_profile_cus_123",
  "metadata": {
    "test": "data"
  },
  "object": "v2.billing.profile",
  "status": "active",
  "livemode": true
}
List billing profiles v2
Ask about this section
Copy for LLM

View as Markdown
List Billing Profiles.

Learn more about calling API v2 endpoints. 
Parameters

lookup_keys
array of strings
Required
Filter billing profiles by lookup keys. Mutually exclusive with customer and default_payment_method. You can specify up to 10 lookup_keys.


customer
string
Filter billing profiles by a customer. Mutually exclusive with lookup_keys and default_payment_method.


default_payment_method
string
Filter billing profiles by a default payment method. Mutually exclusive with customer and lookup_keys.


limit
integer
Optionally set the maximum number of results per page. Defaults to 10.


page
string
Opaque page token.


status
enum
Filter billing profiles by status. Can be combined with all other filters. If not provided, all billing profiles will be returned.

Possible enum values
active
The billing profile is active.

inactive
The billing profile is inactive and cannot be used.

Returns
Response attributes

data
array of dictionaries
The retrieved Profile objects.

Show child attributes

next_page_url
nullable string
The URL of the next page of results, if there is one.


previous_page_url
nullable string
The URL of the previous page of results, if there is one.

Error Codes
400
customer_not_found_for_billing_profile
Returned when the customer for the provided ID cannot be found.

400
payment_method_not_found_for_billing_profile
Returned when the payment method for the provided ID cannot be found.

GET 
/v2/billing/profiles
cURL
curl -G https://api.stripe.com/v2/billing/profiles \
  -H "Authorization: Bearer sk_123" \
  -H "Stripe-Version: 2025-12-15.preview" \
  -d default_payment_method=pm_123
Response
{
  "data": [
    {
      "created": "2025-01-01T00:00:00.000Z",
      "customer": "cus_123",
      "default_payment_method": "pm_123",
      "display_name": "Display Name",
      "id": "bilp_123",
      "lookup_key": "billing_profile_cus_123",
      "metadata": {
        "test": "data"
      },
      "object": "v2.billing.profile",
      "status": "active",
      "livemode": true
    }
  ]
}

Customer Portal Session 
Ask about this section
Copy for LLM

View as Markdown
The Billing customer portal is a Stripe-hosted UI for subscription and billing management.

A portal configuration describes the functionality and features that you want to provide to your customers through the portal.

A portal session describes the instantiation of the customer portal for a particular customer. By visiting the session’s URL, the customer can manage their subscriptions and billing details. For security reasons, sessions are short-lived and will expire if the customer does not visit the URL. Create sessions on-demand when customers intend to manage their subscriptions and billing details.

Related guide: Customer management

Endpoints
POST
/v1/billing_portal/sessions
The Customer Portal Session object 
Ask about this section
Copy for LLM

View as Markdown
Attributes

id
string
Unique identifier for the object.


object
string
String representing the object’s type. Objects of the same type share the same value.


configuration
string
Expandable
The configuration used by this session, describing the features available.


created
timestamp
Time at which the object was created. Measured in seconds since the Unix epoch.


customer
string
The ID of the customer for this session.


customer_account
nullable string
The ID of the account for this session.


flow
nullable dictionary
Information about a specific flow for the customer to go through. See the docs to learn more about using customer portal deep links and flows.

Show child attributes

livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


locale
nullable enum
The IETF language tag of the locale Customer Portal is displayed in. If blank or auto, the customer’s preferred_locales or browser’s locale is used.


on_behalf_of
nullable string
Connect only
The account for which the session was created on behalf of. When specified, only subscriptions and invoices with this on_behalf_of account appear in the portal. For more information, see the docs. Use the Accounts API to modify the on_behalf_of account’s branding settings, which the portal displays.


return_url
nullable string
The URL to redirect customers to when they click on the portal’s link to return to your website.


url
string
The short-lived URL of the session that gives customers access to the customer portal.

The Customer Portal Session object
{
  "id": "bps_1MrSjzLkdIwHu7ixex0IvU9b",
  "object": "billing_portal.session",
  "configuration": "bpc_1MAhNDLkdIwHu7ixckACO1Jq",
  "created": 1680210639,
  "customer": "cus_NciAYcXfLnqBoz",
  "flow": null,
  "livemode": false,
  "locale": null,
  "on_behalf_of": null,
  "return_url": "https://example.com/account",
  "url": "https://billing.stripe.com/p/session/test_YWNjdF8xTTJKVGtMa2RJd0h1N2l4LF9OY2lBYjJXcHY4a2NPck96UjBEbFVYRnU5bjlwVUF50100BUtQs3bl"
}
Create a portal session 
Ask about this section
Copy for LLM

View as Markdown
Creates a session of the customer portal.

Parameters

configuration
string
The ID of an existing configuration to use for this session, describing its functionality and features. If not specified, the session uses the default configuration.


customer
string
The ID of an existing customer.


customer_account
string
The ID of an existing account.


flow_data
dictionary
Information about a specific flow for the customer to go through. See the docs to learn more about using customer portal deep links and flows.

Show child parameters

locale
enum
The IETF language tag of the locale customer portal is displayed in. If blank or auto, the customer’s preferred_locales or browser’s locale is used.


on_behalf_of
string
Connect only
The on_behalf_of account to use for this session. When specified, only subscriptions and invoices with this on_behalf_of account appear in the portal. For more information, see the docs. Use the Accounts API to modify the on_behalf_of account’s branding settings, which the portal displays.


return_url
string
The default URL to redirect customers to when they click on the portal’s link to return to your website.

Returns
Returns a portal session object.


Customer Portal Configuration 
Ask about this section
Copy for LLM

View as Markdown
A portal configuration describes the functionality and behavior you embed in a portal session. Related guide: Configure the customer portal.

Endpoints
POST
/v1/billing_portal/configurations
POST
/v1/billing_portal/configurations/:id
GET
/v1/billing_portal/configurations/:id
GET
/v1/billing_portal/configurations
The Customer portal configuration object 
Ask about this section
Copy for LLM

View as Markdown
Attributes

id
string
Unique identifier for the object.


object
string
String representing the object’s type. Objects of the same type share the same value.


active
boolean
Whether the configuration is active and can be used to create portal sessions.


application
nullable string
Expandable
Connect only
ID of the Connect Application that created the configuration.


business_profile
dictionary
The business information shown to customers in the portal.

Show child attributes

created
timestamp
Time at which the object was created. Measured in seconds since the Unix epoch.


default_return_url
nullable string
The default URL to redirect customers to when they click on the portal’s link to return to your website. This can be overriden when creating the session.


features
dictionary
Information about the features available in the portal.

Show child attributes

is_default
boolean
Whether the configuration is the default. If true, this configuration can be managed in the Dashboard and portal sessions will use this configuration unless it is overriden when creating the session.


livemode
boolean
Has the value true if the object exists in live mode or the value false if the object exists in test mode.


login_page
dictionary
The hosted login page for this configuration. Learn more about the portal login page in our integration docs.

Show child attributes

metadata
nullable dictionary
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format.


name
nullable string
The name of the configuration.


updated
timestamp
Time at which the object was last updated. Measured in seconds since the Unix epoch.

The Customer portal configuration object
{
  "id": "bpc_1MrnZsLkdIwHu7ixNiQL1xPM",
  "object": "billing_portal.configuration",
  "active": true,
  "application": null,
  "business_profile": {
    "headline": null,
    "privacy_policy_url": null,
    "terms_of_service_url": null
  },
  "created": 1680290736,
  "default_return_url": null,
  "features": {
    "customer_update": {
      "allowed_updates": [
        "email",
        "tax_id"
      ],
      "enabled": true
    },
    "invoice_history": {
      "enabled": true
    },
    "payment_method_update": {
      "enabled": false
    },
    "subscription_cancel": {
      "cancellation_reason": {
        "enabled": false,
        "options": [
          "too_expensive",
          "missing_features",
          "switched_service",
          "unused",
          "other"
        ]
      },
      "enabled": false,
      "mode": "at_period_end",
      "proration_behavior": "none"
    },
    "subscription_update": {
      "default_allowed_updates": [],
      "enabled": false,
      "proration_behavior": "none"
    }
  },
  "is_default": false,
  "livemode": false,
  "login_page": {
    "enabled": false,
    "url": null
  },
  "metadata": {},
  "updated": 1680290736
}
Create a portal configuration 
Ask about this section
Copy for LLM

View as Markdown
Creates a configuration that describes the functionality and behavior of a PortalSession

Parameters

features
dictionary
Required
Information about the features available in the portal.

Show child parameters

business_profile
dictionary
The business information shown to customers in the portal.

Show child parameters

default_return_url
string
The default URL to redirect customers to when they click on the portal’s link to return to your website. This can be overriden when creating the session.


login_page
dictionary
The hosted login page for this configuration. Learn more about the portal login page in our integration docs.

Show child parameters

metadata
dictionary
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.


name
string
The name of the configuration.

The maximum length is 256 characters.

Returns
Returns a portal configuration object.

POST 
/v1/billing_portal/configurations
Server-side language
cURL
curl https://api.stripe.com/v1/billing_portal/configurations \
  -u "sk_123:" \
  -H "Stripe-Version: 2025-12-15.preview" \
  -d "features[customer_update][allowed_updates][]"=email \
  -d "features[customer_update][allowed_updates][]"=tax_id \
  -d "features[customer_update][enabled]"=true \
  -d "features[invoice_history][enabled]"=true
Response
{
  "id": "bpc_1MrnZsLkdIwHu7ixNiQL1xPM",
  "object": "billing_portal.configuration",
  "active": true,
  "application": null,
  "business_profile": {
    "headline": null,
    "privacy_policy_url": null,
    "terms_of_service_url": null
  },
  "created": 1680290736,
  "default_return_url": null,
  "features": {
    "customer_update": {
      "allowed_updates": [
        "email",
        "tax_id"
      ],
      "enabled": true
    },
    "invoice_history": {
      "enabled": true
    },
    "payment_method_update": {
      "enabled": false
    },
    "subscription_cancel": {
      "cancellation_reason": {
        "enabled": false,
        "options": [
          "too_expensive",
          "missing_features",
          "switched_service",
          "unused",
          "other"
        ]
      },
      "enabled": false,
      "mode": "at_period_end",
      "proration_behavior": "none"
    },
    "subscription_update": {
      "default_allowed_updates": [],
      "enabled": false,
      "proration_behavior": "none"
    }
  },
  "is_default": false,
  "livemode": false,
  "login_page": {
    "enabled": false,
    "url": null
  },
  "metadata": {},
  "updated": 1680290736
}
Update a portal configuration 
Ask about this section
Copy for LLM

View as Markdown
Updates a configuration that describes the functionality of the customer portal.

Parameters

active
boolean
Whether the configuration is active and can be used to create portal sessions.


business_profile
dictionary
The business information shown to customers in the portal.

Show child parameters

default_return_url
string
The default URL to redirect customers to when they click on the portal’s link to return to your website. This can be overriden when creating the session.


features
dictionary
Information about the features available in the portal.

Show child parameters

login_page
dictionary
The hosted login page for this configuration. Learn more about the portal login page in our integration docs.

Show child parameters

metadata
dictionary
Set of key-value pairs that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to metadata.


name
string
The name of the configuration.

The maximum length is 256 characters.

Returns
Returns a portal configuration object.

POST 
/v1/billing_portal/configurations/:id
Server-side language
cURL
curl https://api.stripe.com/v1/billing_portal/configurations/bpc_1MrnZsLkdIwHu7ixNiQL1xPM \
  -u "sk_123:" \
  -H "Stripe-Version: 2025-12-15.preview" \
  --data-urlencode "business_profile[privacy_policy_url]"="https://example.com/new_privacy_url" \
  --data-urlencode "business_profile[terms_of_service_url]"="https://example.com/new_terms_of_service_url"
Response
{
  "id": "bpc_1MrnZsLkdIwHu7ixNiQL1xPM",
  "object": "billing_portal.configuration",
  "active": true,
  "application": null,
  "business_profile": {
    "headline": null,
    "privacy_policy_url": "https://example.com/new_privacy_url",
    "terms_of_service_url": "https://example.com/new_terms_of_service_url"
  },
  "created": 1680290736,
  "default_return_url": null,
  "features": {
    "customer_update": {
      "allowed_updates": [
        "email",
        "tax_id"
      ],
      "enabled": true
    },
    "invoice_history": {
      "enabled": true
    },
    "payment_method_update": {
      "enabled": false
    },
    "subscription_cancel": {
      "cancellation_reason": {
        "enabled": false,
        "options": [
          "too_expensive",
          "missing_features",
          "switched_service",
          "unused",
          "other"
        ]
      },
      "enabled": false,
      "mode": "at_period_end",
      "proration_behavior": "none"
    },
    "subscription_update": {
      "default_allowed_updates": [],
      "enabled": false,
      "proration_behavior": "none"
    }
  },
  "is_default": false,
  "livemode": false,
  "login_page": {
    "enabled": false,
    "url": null
  },
  "metadata": {},
  "updated": 1688593779
}
Retrieve a portal configuration 
Ask about this section
Copy for LLM

View as Markdown
Retrieves a configuration that describes the functionality of the customer portal.

Parameters
No parameters.

Returns
Returns a portal configuration object.

GET 
/v1/billing_portal/configurations/:id
Server-side language
cURL
curl https://api.stripe.com/v1/billing_portal/configurations/bpc_1MrnZsLkdIwHu7ixNiQL1xPM \
  -u "sk_123:" \
  -H "Stripe-Version: 2025-12-15.preview"
Response
{
  "id": "bpc_1MrnZsLkdIwHu7ixNiQL1xPM",
  "object": "billing_portal.configuration",
  "active": true,
  "application": null,
  "business_profile": {
    "headline": null,
    "privacy_policy_url": null,
    "terms_of_service_url": null
  },
  "created": 1680290736,
  "default_return_url": null,
  "features": {
    "customer_update": {
      "allowed_updates": [
        "email",
        "tax_id"
      ],
      "enabled": true
    },
    "invoice_history": {
      "enabled": true
    },
    "payment_method_update": {
      "enabled": false
    },
    "subscription_cancel": {
      "cancellation_reason": {
        "enabled": false,
        "options": [
          "too_expensive",
          "missing_features",
          "switched_service",
          "unused",
          "other"
        ]
      },
      "enabled": false,
      "mode": "at_period_end",
      "proration_behavior": "none"
    },
    "subscription_update": {
      "default_allowed_updates": [],
      "enabled": false,
      "proration_behavior": "none"
    }
  },
  "is_default": false,
  "livemode": false,
  "login_page": {
    "enabled": false,
    "url": null
  },
  "metadata": {},
  "updated": 1680290736
}
List portal configurations 
Ask about this section
Copy for LLM

View as Markdown
Returns a list of configurations that describe the functionality of the customer portal.

Parameters

active
boolean
Only return configurations that are active or inactive (e.g., pass true to only list active configurations).


is_default
boolean
Only return the default or non-default configurations (e.g., pass true to only list the default configuration).

More parameters
Expand all

ending_before
string

limit
integer

starting_after
string
Returns
Returns a list of portal configuration objects.

GET 
/v1/billing_portal/configurations
Server-side language
cURL
curl -G https://api.stripe.com/v1/billing_portal/configurations \
  -u "sk_123:" \
  -H "Stripe-Version: 2025-12-15.preview" \
  -d limit=3
Response
{
  "object": "list",
  "url": "/v1/billing_portal/configurations",
  "has_more": false,
  "data": [
    {
      "id": "bpc_1MrnZsLkdIwHu7ixNiQL1xPM",
      "object": "billing_portal.configuration",
      "active": true,
      "application": null,
      "business_profile": {
        "headline": null,
        "privacy_policy_url": null,
        "terms_of_service_url": null
      },
      "created": 1680290736,
      "default_return_url": null,
      "features": {
        "customer_update": {
          "allowed_updates": [
            "email",
            "tax_id"
          ],
          "enabled": true
        },
        "invoice_history": {
          "enabled": true
        },
        "payment_method_update": {
          "enabled": false
        },
        "subscription_cancel": {
          "cancellation_reason": {
            "enabled": false,
            "options": [
              "too_expensive",
              "missing_features",
              "switched_service",
              "unused",
              "other"
            ]
          },
          "enabled": false,
          "mode": "at_period_end",
          "proration_behavior": "none"
        },
        "subscription_update": {
          "default_allowed_updates": [],
          "enabled": false,
          "proration_behavior": "none"
        }
      },
      "is_default": false,
      "livemode": false,
      "login_page": {
        "enabled": false,
        "url": null
      },
      "metadata": {},
      "updated": 1680290736
    }
  ]
}

# Create a Custom Pricing Unit

Create a Custom Pricing Unit object.

## Parameters

- `display_name` (string, required)
  Description that customers will see in the invoice line item. Maximum length of 10 characters.

- `lookup_key` (string, optional)
  An internal key you can use to search for a particular custom pricing unit item. Must be unique among items. Maximum length of 200 characters.

- `metadata` (map, optional)
  Set of [key-value pairs](https://docs.stripe.com/docs/api/metadata.md) that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

## Returns

## Response attributes

- `id` (string)
  Unique identifier for the object.

- `object` (string, value is "v2.billing.custom_pricing_unit")
  String representing the object’s type. Objects of the same type share the same value of the object field.

- `active` (boolean)
  Whether the custom pricing unit is active.

- `created` (timestamp)
  Timestamp of when the object was created.

- `display_name` (string)
  Description that customers will see in the invoice line item. Maximum length of 10 characters.

- `livemode` (boolean)
  Has the value `true` if the object exists in live mode or the value `false` if the object exists in test mode.

- `lookup_key` (string, nullable)
  An internal key you can use to search for a particular Custom Pricing Unit. Maximum length of 200 characters.

- `metadata` (map, nullable)
  Set of [key-value pairs](https://docs.stripe.com/docs/api/metadata.md) that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

## Error Codes

| HTTP status code | Code                    | Description                                                                     |
| ---------------- | ----------------------- | ------------------------------------------------------------------------------- |
| 400              | lookup_key_already_used | Returned when another object of the same type already has the given lookup key. |

```curl
curl -X POST https://api.stripe.com/v2/billing/custom_pricing_units \
  -H "Authorization: Bearer <<YOUR_SECRET_KEY>>" \
  -H "Stripe-Version: 2026-01-28.preview" \
  --json '{
    "display_name": "Sample Custom Pricing Unit",
    "lookup_key": "Unit #1",
    "metadata": {
        "key": "value"
    }
  }'
```

### Response

```json
{
  "active": true,
  "created": "2025-01-01T00:00:00.000Z",
  "display_name": "Unit #1",
  "id": "cpu_61T4sQA90ELFdWUhl16Ss95I3tSQSib3S1PC0IDCSFCS",
  "lookup_key": "my-custom-pricing-unit-1",
  "metadata": {
    "key": "value"
  },
  "object": "v2.billing.custom_pricing_unit",
  "livemode": true
}
```

# The Custom Pricing Unit object

## Attributes

- `id` (string)
  Unique identifier for the object.

- `object` (string, value is "v2.billing.custom_pricing_unit")
  String representing the object’s type. Objects of the same type share the same value of the object field.

- `active` (boolean)
  Whether the custom pricing unit is active.

- `created` (timestamp)
  Timestamp of when the object was created.

- `display_name` (string)
  Description that customers will see in the invoice line item. Maximum length of 10 characters.

- `livemode` (boolean)
  Has the value `true` if the object exists in live mode or the value `false` if the object exists in test mode.

- `lookup_key` (string, nullable)
  An internal key you can use to search for a particular Custom Pricing Unit. Maximum length of 200 characters.

- `metadata` (map, nullable)
  Set of [key-value pairs](https://docs.stripe.com/docs/api/metadata.md) that you can attach to an object. This can be useful for storing additional information about the object in a structured format.

### The Custom Pricing Unit object

```json
{
  "created": "2025-01-01T00:00:00.000Z",
  "display_name": "Unit #1",
  "id": "cpu_61T4sQA90ELFdWUhl16Ss95I3tSQSib3S1PC0IDCSFCS",
  "lookup_key": "my-custom-pricing-unit-1",
  "metadata": {},
  "object": "v2.billing.custom_pricing_unit",
  "livemode": true
}
```