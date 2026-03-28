# ACR-21 — SNS integration and end-to-end alert validation

## Overview
This task extended the AWS CPEmon Lite MVP from telemetry storage into an end-to-end alerting and notification flow.

The validated monitoring path is:

**Telemetry payload → Lambda → CloudWatch custom metrics → CloudWatch Alarm → SNS email**

This task also preserved the previously implemented storage flow:

**Telemetry payload → Lambda → DynamoDB + S3**

---

## Alerting model

The alerting design now has two layers:

### 1. Sample per-device alarm
A per-device alarm is retained only for validation purposes.

- Alarm: `aws-cpemon-lite-wan-down-sample-alarm`
- Metric: `WanDown`
- Dimension: `device_id`

This alarm exists to validate the technical path from metric publication to CloudWatch alarm evaluation and SNS notification delivery.

It is **not** the primary production-style alerting model.

### 2. Fleet-level aggregate alarm
A fleet-level aggregate alarm is used as the primary service-availability alarm.

- Alarm: `aws-cpemon-lite-fleet-wan-down-alarm`
- Metric: `FleetWanDownCount`
- Dimension: none

This alarm reflects the higher-value monitoring question:

**Are multiple devices experiencing WAN-down conditions within a short time window?**

---

## Why the fleet-level alarm is primary
For broadband and telecom-style monitoring, the key concern is not isolated single-device degradation, but whether a broader service issue is developing across a device population.

Because of that:

- per-device alarms are useful for sample-path validation
- fleet-level aggregate alarms are more useful for service-level monitoring
- per-device drill-down is better handled by querying DynamoDB-backed telemetry records

---

## Metric design

### Per-device metric
`WanDown`

Used for:
- sample validation
- metric/alarm/SNS path testing
- single-device demonstrations

### Fleet-level aggregate metric
`FleetWanDownCount`

Used for:
- service degradation monitoring
- aggregate WAN-down event counting
- primary fleet alarming

The aggregate metric is published without `device_id` dimension so that all WAN-down events contribute to one shared time series.

---

## Notification path
SNS topic:
- `aws-cpemon-lite-alerts`

Notification target:
- confirmed email subscription

Both the sample alarm and the fleet-level alarm publish to this SNS topic.

---

## Validation outcome
The following were verified successfully:

- per-device alarm entered `ALARM`
- SNS email notification was delivered for the sample alarm
- fleet-level aggregate metric appeared in CloudWatch
- fleet-level alarm entered `ALARM`
- SNS email notification was delivered for the fleet-level alarm

This confirms that the MVP now supports both telemetry persistence and end-to-end alert delivery.

---

## Final status of alarms

### Validation-only alarm
- `aws-cpemon-lite-wan-down-sample-alarm`

Status:
- retained
- validation-only
- not the primary monitoring signal

### Primary fleet alarm
- `aws-cpemon-lite-fleet-wan-down-alarm`

Status:
- active
- primary WAN-down service availability alarm

---

## Follow-up monitoring evolution

After the initial WAN-down alerting path was validated, the monitoring model was extended to include a second fleet-level primary operational signal:

- `FleetMissingHeartbeatCount`

This signal is published by a scheduled heartbeat-check Lambda that evaluates stale `last_seen` values from the DynamoDB telemetry history table.

With this addition, the primary fleet-level monitoring model now covers both:

- aggregate WAN-down conditions
- aggregate missing-heartbeat or stale-telemetry conditions

## Current alarm model after monitoring refinement

The alerting model was later refined after the dashboard and missing-heartbeat monitoring path were added.

### Removed validation-only sample alarm
The per-device sample alarm was removed after the technical metric-to-alarm-to-SNS path had been validated.

Removed alarm:
- `aws-cpemon-lite-wan-down-sample-alarm`

Reason:
- it was only needed for technical path validation
- it was not part of the intended primary operational monitoring model
- the fleet-level monitoring model became the preferred steady-state design

### Active primary fleet alarm
The WAN-down fleet alarm remains active as the primary service-availability alarm.

- Alarm: `aws-cpemon-lite-fleet-wan-down-alarm`
- Metric: `FleetWanDownCount`
- Status: active

### Defined but disabled missing-heartbeat alarm
A second fleet-level primary alarm was added for missing-heartbeat detection.

- Alarm: `aws-cpemon-lite-fleet-missing-heartbeat-alarm`
- Metric: `FleetMissingHeartbeatCount`

Status:
- created
- alarm logic validated
- alarm actions intentionally disabled in the current test environment

Reason:
The simulator is not intended to run continuously in the test environment, so leaving alarm actions enabled would generate noisy email notifications. The alarm definition is retained because it reflects the intended production-style monitoring model.
