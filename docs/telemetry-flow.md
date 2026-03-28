# Telemetry Flow

## Purpose

This document describes the end-to-end telemetry path in AWS CPEmon Lite.

The flow is intentionally lightweight, but it still reflects a realistic cloud telemetry design with ingestion, processing, storage, observability, and alerting.

## End-to-end flow

The main telemetry path is:

**Simulator → API Gateway → Lambda**

After receiving telemetry, the ingestion Lambda performs the following actions:

1. Validates the incoming payload
2. Writes processing logs to CloudWatch Logs
3. Derives a lightweight health state
4. Publishes custom telemetry and health metrics to CloudWatch Metrics
5. Stores the raw telemetry payload in S3
6. Stores structured telemetry records in DynamoDB

In addition to the ingestion path, a scheduled heartbeat-check Lambda scans the DynamoDB telemetry history table, derives the latest `last_seen` value per device, counts stale devices, and publishes the fleet-level metric:

- `FleetMissingHeartbeatCount`

The detection and notification path is:

**CloudWatch Metrics → CloudWatch Alarms → SNS**

## Example telemetry payload

A simulated device sends a payload similar to the following:

```json
{
  "device_id": "cpe-001",
  "last_seen": "2026-03-26T10:00:00Z",
  "cpu_usage": 82,
  "memory_usage": 68,
  "temperature": 71,
  "wan_status": "up"
}
```

## Lambda responsibilities

The Lambda function is intentionally small and focused.

### Validation

It checks whether the payload contains the required fields and whether the values are in a reasonable format.

## CloudWatch logging behavior

The Lambda function writes both default runtime logs and lightweight application-level logs to CloudWatch Logs.

Default Lambda runtime logs include:
- INIT_START
- START RequestId
- END RequestId
- REPORT RequestId

In addition, the function now emits application logs during successful processing so that the telemetry flow can be traced more clearly. These logs cover:
- payload receipt
- validation success
- derived health state
- CloudWatch metric publication
- DynamoDB write completion
- S3 archival completion
- final successful processing outcome

This approach keeps the logging model simple while making CloudWatch Logs the first troubleshooting layer for the MVP.

### Metrics

The ingestion Lambda publishes per-device supporting metrics such as:

* `DeviceTelemetryReceived`
* `WanDown`
* `CpuUsage`
* `MemoryUsage`
* `Temperature`
* `HealthWarning`
* `HealthCritical`

It also publishes the fleet-level aggregate metric:

* `FleetWanDownCount`

The heartbeat-check Lambda publishes the second fleet-level primary metric:

* `FleetMissingHeartbeatCount`

### Raw archive

It stores the original payload in S3 for history, retention, and possible future analytics.

Example S3 layout:

```text
s3://aws-cpemon-lite-raw/device_id=cpe-001/date=2026-03-26/telemetry-001.json
```

### Structured telemetry persistence

Structured telemetry records are written to DynamoDB for operational lookup and recent history queries.

Example logical item shape:

```json
{
  "device_id": "cpe-001",
  "last_seen": "2026-03-26T10:00:00Z",
  "cpu_usage": 82,
  "memory_usage": 68,
  "temperature": 71,
  "wan_status": "up",
  "health_state": "warning",
  "ingested_at": "2026-03-26T10:00:05Z"
}
```

## Why S3 and DynamoDB are both used

The design separates storage by access pattern:

* S3 stores raw telemetry cheaply for retention and future analysis
* DynamoDB stores the latest device state for fast operational lookup

This makes the MVP more realistic than using a single backend for both use cases.

## Detection and alerting

CloudWatch Alarms evaluate fleet-level custom metrics and trigger SNS notifications when thresholds are crossed.

The two primary operational signals are:

* `FleetWanDownCount`
* `FleetMissingHeartbeatCount`

Supporting per-device metrics remain available for drill-down and investigation rather than primary alerting.

## Operational visibility

The platform also includes a lightweight CloudWatch Dashboard to provide a simple operational view of telemetry volume, abnormal signals, and Lambda health.

