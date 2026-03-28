# Heartbeat Check Lambda

## Purpose

This Lambda evaluates missing-heartbeat conditions at fleet level for AWS CPEmon Lite.

It scans the existing DynamoDB telemetry history table, derives the latest `last_seen` value per device, counts devices whose latest heartbeat is older than the configured threshold, and publishes the fleet-level CloudWatch custom metric:

- `FleetMissingHeartbeatCount`

This metric acts as a primary operational signal alongside:

- `FleetWanDownCount`

## Why this Lambda exists

The ingestion Lambda can publish `FleetWanDownCount` when WAN-down telemetry is received, but missing-heartbeat detection is different.

A device that stops sending telemetry does not trigger the ingestion path at all, so a separate scheduled check is needed.

For the MVP, this is implemented with:

- an EventBridge schedule running every 10 minutes
- heartbeat-check Lambda
- DynamoDB telemetry history table
- CloudWatch custom metric publication

## Inputs

This Lambda does not require a request body.

It reads from DynamoDB using the telemetry history table.
The Lambda can be invoked manually with an empty JSON event (`{}`) for validation, but its normal operating path is automatic scheduled invocation from EventBridge.

## Environment variables

- `DYNAMODB_TABLE_NAME`
- `CW_METRIC_NAMESPACE`
- `HEARTBEAT_STALE_MINUTES`

## Metric published

- `FleetMissingHeartbeatCount`

This metric is published without `device_id` dimension because it is intended to represent a fleet-level operational signal.

## Logging

The Lambda writes lightweight application logs to CloudWatch Logs, including:

- heartbeat check start
- stale threshold used
- stale device detection
- scan summary
- metric publication result

## MVP trade-off

For this MVP, missing-heartbeat detection is implemented by scheduled polling against DynamoDB `last_seen` values.

This is simple and suitable for small scale, but it is intentionally documented as an MVP trade-off. At larger scale, the architecture would likely evolve toward event-driven device presence or lifecycle handling rather than table polling.
