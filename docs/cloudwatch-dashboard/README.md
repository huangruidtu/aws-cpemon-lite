# CloudWatch Dashboard

## Purpose

This directory stores the CloudWatch dashboard definition for AWS CPEmon Lite.

The dashboard is kept in the repository as a configuration artifact so that the operational view can be versioned, reviewed, and recreated if needed.

## Dashboard file

- `aws-cpemon-lite-operations-dashboard.json`

## Dashboard intent

The dashboard provides a lightweight operational view of the MVP and is organized around three layers:

### 1. Fleet-level primary operational signals
These widgets show the main fleet-level monitoring signals:

- `FleetWanDownCount`
- `FleetMissingHeartbeatCount`

These two metrics act as the primary operational signals for the MVP.

### 2. Lambda operational health
These widgets show the AWS-managed Lambda service metrics for:

- ingestion Lambda invocations
- ingestion Lambda errors
- heartbeat-check Lambda invocations
- heartbeat-check Lambda errors

These metrics help interpret fleet-level signal changes together with the health of the underlying Lambda execution paths.

### 3. Per-device drill-down
The dashboard also includes device-level supporting metrics driven by a `deviceId` dashboard variable.

The following per-device metrics are shown:

- `WanDown`
- `CpuUsage`
- `MemoryUsage`
- `Temperature`

These are supporting investigation signals rather than primary alerting signals.

## Why the dashboard definition is stored in the repository

The dashboard is stored in the repository for the same reason as IAM policy files and design documents:

- reproducibility
- version control
- easier review
- easier recovery or recreation
- alignment between implementation and documentation

## Notes

The dashboard is intentionally lightweight and MVP-focused.

It prioritizes:

- fleet-level visibility first
- Lambda execution health second
- device-level investigation support third

It does not try to become a full custom device lookup UI.
