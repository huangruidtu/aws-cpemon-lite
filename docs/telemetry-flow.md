# Telemetry Flow

## Purpose

This document describes the end-to-end telemetry path in AWS CPEmon Lite.

The flow is intentionally lightweight, but it still reflects a realistic cloud telemetry design with ingestion, processing, storage, observability, and alerting.

## End-to-end flow

The main telemetry path is:

**Simulator → API Gateway → Lambda**

After receiving telemetry, Lambda performs the following actions:

1. Validates the incoming payload
2. Writes processing logs to CloudWatch Logs
3. Publishes custom health and telemetry metrics to CloudWatch Metrics
4. Stores the raw telemetry payload in S3
5. Updates the latest device state in DynamoDB

The detection and notification path is:

**CloudWatch Metrics → CloudWatch Alarms → SNS**

## Example telemetry payload

A simulated device sends a payload similar to the following:

```json
{
  "device_id": "cpe-001",
  "timestamp": "2026-03-26T10:00:00Z",
  "cpu_usage": 82,
  "memory_usage": 68,
  "temperature": 71,
  "wan_status": "up",
  "packet_loss": 0.5
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

It publishes custom metrics such as:

* `TelemetryReceivedCount`
* `HighCpuDeviceCount`
* `WanDownDeviceCount`
* `HighTemperatureDeviceCount`

### Raw archive

It stores the original payload in S3 for history, retention, and possible future analytics.

Example S3 layout:

```text
s3://aws-cpemon-lite-raw/device_id=cpe-001/date=2026-03-26/telemetry-001.json
```

### Latest state update

It updates the most recent known device state in DynamoDB.

Example logical item shape:

```json
{
  "device_id": "cpe-001",
  "last_seen": "2026-03-26T10:00:00Z",
  "cpu_usage": 82,
  "memory_usage": 68,
  "temperature": 71,
  "wan_status": "up",
  "health_state": "warning"
}
```

## Why S3 and DynamoDB are both used

The design separates storage by access pattern:

* S3 stores raw telemetry cheaply for retention and future analysis
* DynamoDB stores the latest device state for fast operational lookup

This makes the MVP more realistic than using a single backend for both use cases.

## Detection and alerting

CloudWatch Alarms evaluate custom metrics and trigger SNS notifications when thresholds are crossed.

Example detection ideas:

* No telemetry received for a defined period
* WAN down signal detected
* High CPU count above threshold
* Lambda error count increased unexpectedly

## Operational visibility

The platform also includes a lightweight CloudWatch Dashboard to provide a simple operational view of telemetry volume, abnormal signals, and Lambda health.

