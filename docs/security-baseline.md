# Security Baseline

## Purpose
This document describes the lightweight security baseline for AWS CPEmon Lite.

The project is not intended to be a full security showcase, but it should still demonstrate sound cloud engineering habits and production-minded security thinking.

## Security goals
The security baseline is designed to be:

- practical
- low-cost
- easy to implement
- easy to explain
- appropriate for a lightweight MVP

## 1. HTTPS-only ingestion
Telemetry ingestion is exposed through API Gateway over HTTPS only.

### Why
This ensures that telemetry data is encrypted in transit and avoids insecure plaintext submission.

## 2. Least-privilege IAM
Service-to-service access is controlled with narrow IAM roles and permissions.

### Examples
- Lambda can write only to the required S3 bucket
- Lambda can update only the required DynamoDB table
- Lambda can write logs and metrics only as needed
- CloudWatch Alarms can notify only the required SNS topic

### Why
Least-privilege access reduces accidental over-permissioning and improves the platform’s security posture.

## 3. Encrypted storage
Stored operational data should not be left unprotected.

### Controls
- S3 encryption enabled
- DynamoDB encryption at rest enabled

### Why
Even in a lightweight monitoring platform, archived telemetry and device state should be protected at rest.

## 4. S3 Block Public Access
The telemetry archive bucket should not be exposed publicly.

### Controls
- Block Public Access enabled
- no public bucket policy
- access limited to intended service roles

### Why
Raw telemetry is operational data and should remain private.

## 5. Secrets kept outside source code
Any secret-like value or operational configuration should be externalized.

### Examples
- shared secret
- Slack webhook endpoint
- configurable thresholds

### AWS service
Systems Manager Parameter Store is the natural next step for stronger externalized secret/config handling, but the current MVP keeps active runtime configuration intentionally lightweight.

### Why
Sensitive values should not be hardcoded into application code or Git history.

## 6. Auditability awareness
Control-plane actions should be auditable.

### AWS service
Use CloudTrail Event history for lightweight AWS API activity visibility in the current MVP.

### Current scope
The current MVP relies on the default CloudTrail Event history view, which is sufficient for lightweight auditability awareness of recent management events.

This is used to review control-plane changes such as:
- Lambda creation and updates
- CloudWatch alarm creation, deletion, and alarm-action changes
- dashboard updates
- IAM-related configuration changes

### Why
This improves operational governance and reinforces production-minded design without introducing a dedicated long-term audit trail at this stage.

## 7. Failure visibility as part of operational security
Some security-relevant situations first appear as operational anomalies.

### Examples
- unexpected telemetry drop
- repeated Lambda processing failures
- abnormal ingestion errors

### Controls
Use CloudWatch Metrics and Alarms to detect these conditions early.

## Out of scope for version 1
The following are intentionally excluded from the first version:

- WAF tuning
- Cognito
- mTLS
- GuardDuty
- Security Hub
- AWS Config compliance rules
- multi-account security baseline

These may be valid future improvements, but they are beyond the intended scope of this MVP.
