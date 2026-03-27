ACR-20 — Telemetry storage design and implementation
Overview

This task implemented the telemetry storage layer for the AWS CPEmon Lite MVP.

The ingestion Lambda now performs three key responsibilities after receiving a valid telemetry payload:

publishes lightweight operational metrics
stores structured telemetry records in DynamoDB
archives the original raw payload in S3

This creates a simple but realistic telemetry processing pattern that is easy to explain and extend.

Hot, warm, and cold paths

The telemetry handling model is intentionally divided into three paths.

Hot path

Handled by Lambda.

Responsibilities:

parse and validate incoming payloads
derive a lightweight health_state
publish CloudWatch custom metrics
perform immediate per-event evaluation

This path is focused on immediate processing.

Warm path

Handled by DynamoDB.

Responsibilities:

store structured telemetry records
support latest-state lookup
support recent telemetry history queries
provide a low-latency operational query path

This path is meant for queryable recent state, not long-term archival.

Cold path

Handled by S3.

Responsibilities:

archive the raw original payload
preserve traceability
support debugging and future replay possibilities

This path is intended for retention and evidence, not operational queries.

Why DynamoDB and S3 are both needed

DynamoDB and S3 serve different purposes.

DynamoDB

Used for structured operational records:

latest state
recent history
queryable telemetry
S3

Used for raw payload retention:

archival
traceability
debugging
replay potential

Even if some data overlaps, the responsibilities are different.

Service availability vs. device liveness

The telemetry scenario in this MVP focuses primarily on household broadband service availability, not only on whether the gateway device is still powered on.

Because of that, the signals are interpreted as follows:

Primary service-availability signal
wan_status
Supporting device-liveness signal
last_seen
Supporting health indicators
cpu_usage
memory_usage
temperature

This distinction is important for both implementation and interview explanation.

Field semantics
wan_status

Represents upstream WAN connectivity, not simple device power state.

up means the gateway can reach the external network normally
down means the gateway may still be alive, but household broadband service is degraded or unavailable
last_seen

Represents when telemetry was last seen from the device side.

This helps identify whether the device is still reporting at all.

health_state

A derived summary field computed by Lambda for simplified downstream interpretation.

Current simplified values:

ok
warning
critical
Threshold and alerting rationale

Different telemetry signals should not be treated in the same way.

Immediate reaction candidates

Critical conditions may justify single-event handling, such as dangerously high temperature.

Sustained warning candidates

CPU and memory usage are better interpreted as sustained signals rather than immediate hard-failure triggers, because short spikes can happen naturally.

Service degradation signals

Persistent WAN-down states are meaningful because they directly affect broadband service availability.

This logic shaped the CloudWatch metrics that were added during this task and will be extended further in later alarm/SNS work.

Implemented AWS resources
Lambda
aws-cpemon-lite-ingestion
DynamoDB table
aws-cpemon-lite-telemetry
S3 bucket
aws-cpemon-lite-raw-payloads-hr
CloudWatch metric namespace
AWS/CPEmonLite/Telemetry
DynamoDB item model

Example logical item shape:

{
  "device_id": "cpe-001",
  "last_seen": "2026-03-27T11:00:00Z",
  "cpu_usage": 45,
  "memory_usage": 50,
  "temperature": 60,
  "wan_status": "up",
  "health_state": "ok",
  "ingested_at": "2026-03-27T18:24:31+00:00"
}
S3 object layout

Raw payloads are archived under:

raw/<device_id>/<last_seen>.json

Example:

raw/cpe-001/2026-03-27T11-00-00Z.json
Implementation outcome

The task was verified successfully:

processed telemetry records were written into DynamoDB
raw payloads were archived into S3
the ingestion storage path is functioning correctly
