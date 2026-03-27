# AWS CPEmon Lite

A lightweight AWS-native MVP for CPE telemetry ingestion, observability, alerting, and cost-aware cloud design.

## Goal

AWS CPEmon Lite is a lightweight AWS-native MVP inspired by a CPE monitoring scenario.

The project demonstrates a minimal end-to-end telemetry pipeline built with managed AWS services. The design focuses on:

* simplicity
* low operational overhead
* cost-aware cloud design
* production-minded but lightweight architecture
* interview-ready explainability

This project is not intended to reproduce a full production-scale monitoring platform. Instead, it is designed to show the core ideas of cloud-native telemetry ingestion, event-driven processing, observability, alerting, basic security controls, and lightweight cost visibility.

## Architecture principles

This project follows a few simple architecture principles:

* managed-first
* minimal operational overhead
* cost-aware design
* production-minded but lightweight
* simple service boundaries
* easy to explain and evolve

## High-level architecture

The core telemetry path is:

**Simulator → API Gateway → Lambda**

After receiving telemetry, Lambda performs the following actions:

* validates telemetry payloads
* writes processing logs to CloudWatch Logs
* publishes custom metrics to CloudWatch Metrics
* stores raw telemetry in S3
* stores structured telemetry records in DynamoDB for recent history and operational lookup

The detection and notification path is:

**CloudWatch Metrics → CloudWatch Alarms → SNS**

Supporting platform capabilities include:

* IAM for least-privilege access control
* CloudWatch Dashboard for operational visibility
* Systems Manager Parameter Store for externalized secrets/configuration
* CloudTrail for auditability awareness
* Cost Explorer and AWS Budgets for lightweight cost visibility

## Planned scope

The MVP scope includes:

* simulated device telemetry generation
* managed cloud ingestion endpoint
* event-driven backend processing
* raw telemetry archival
* structured telemetry storage for recent history and operational lookup
* basic observability and alerting
* lightweight security baseline
* lightweight cost visibility
* documentation and demo walkthrough

## Selected AWS services

The MVP uses the following AWS managed services:

* API Gateway
* AWS Lambda
* Amazon S3
* Amazon DynamoDB
* CloudWatch Logs
* CloudWatch Metrics
* CloudWatch Alarms
* CloudWatch Dashboard
* Amazon SNS
* AWS IAM
* AWS Systems Manager Parameter Store
* AWS CloudTrail
* AWS Cost Explorer
* AWS Budgets

## Why these services

The service selection is intentionally simple.

* **API Gateway** provides a managed HTTPS ingestion endpoint
* **Lambda** provides lightweight event-driven processing
* **S3** stores raw telemetry cheaply and durably
* **DynamoDB** stores structured telemetry records for fast operational lookup and recent history queries
* **CloudWatch** provides native logs, metrics, alarms, and dashboard visibility
* **SNS** provides simple alert delivery
* **IAM** provides least-privilege access control
* **Parameter Store** keeps configuration and secrets outside code
* **CloudTrail** adds auditability awareness
* **Cost Explorer and AWS Budgets** reinforce cost-aware operation

The goal is to stay focused on a minimal but realistic AWS-native monitoring architecture rather than building a larger enterprise platform in the first version.

## Telemetry flow

A simulated device sends telemetry payloads to API Gateway. Lambda processes the payload and then:

1. validates the data
2. derives a lightweight health state
3. publishes custom metrics to CloudWatch Metrics
4. archives raw telemetry in S3
5. stores structured telemetry records in DynamoDB

The telemetry handling model is intentionally divided into three paths:

* **Hot path**: Lambda validates incoming payloads, derives a lightweight health state, and publishes CloudWatch custom metrics.
* **Warm path**: DynamoDB stores structured telemetry records for operational lookup and recent history queries.
* **Cold path**: S3 archives raw payloads for traceability, debugging, and future replay possibilities.

This MVP focuses primarily on **household broadband service availability**, not only on whether the device is powered on.

Because of that:

* `wan_status` is treated as a primary service-availability signal
* `last_seen` is treated as a supporting device-liveness signal
* `cpu_usage`, `memory_usage`, and `temperature` are treated as supporting health indicators

Example telemetry payload:

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

Current custom metrics include:

* `DeviceTelemetryReceived`
* `WanDown`
* `CpuUsage`
* `MemoryUsage`
* `Temperature`
* `HealthWarning`
* `HealthCritical`

## Alerting and notification flow

The monitoring flow now supports both a validation-only per-device alarm and a primary fleet-level aggregate alarm.

### Validation-only sample alarm
A per-device alarm is retained for technical path validation:

- **Alarm**: `aws-cpemon-lite-wan-down-sample-alarm`
- **Metric**: `WanDown`
- **Dimension**: `device_id`

This alarm is used only to validate the path from Lambda-published metrics to CloudWatch alarm evaluation and SNS email delivery.

### Primary fleet-level alarm
The main WAN-down alerting signal is fleet-level:

- **Alarm**: `aws-cpemon-lite-fleet-wan-down-alarm`
- **Metric**: `FleetWanDownCount`

This aggregate metric is published without `device_id`, allowing multiple WAN-down events to contribute to one shared time series. This better reflects broadband service-availability monitoring, where broad impact matters more than isolated single-device failures.

### Notification target
Both alarms publish to:

- **SNS topic**: `aws-cpemon-lite-alerts`

with a confirmed email subscription for alert delivery.

### Monitoring intent
This project prioritizes **service availability monitoring** over pure device liveness.  
That means:

- fleet-level WAN-down aggregation is the primary alerting signal
- DynamoDB-backed telemetry remains the main path for per-device drill-down and operational investigation

## Security baseline

The MVP includes a lightweight but explicit security baseline:

* HTTPS-only ingestion
* least-privilege IAM roles
* S3 encryption enabled
* S3 Block Public Access enabled
* DynamoDB encryption at rest
* secrets/config kept outside source code where needed
* CloudTrail for auditability awareness
* CloudWatch alarms for operational failure visibility

The project does not try to implement a full enterprise-grade security stack in the first version. The focus is on practical, low-cost controls that fit a lightweight MVP.

## Cost awareness

The MVP keeps the architecture small and managed-first to reduce unnecessary operational and cost overhead.

Cost visibility is included as a supporting operational capability:

* **Cost Explorer** for service-level cost visibility
* **AWS Budgets** for lightweight monthly budget guardrails

This helps reinforce that cloud architecture should not only work technically, but should also remain aware of operational cost.

## Project structure

```text
docs/       Documentation, architecture notes, security notes, cost visibility
infra/      Infrastructure as code
simulator/  Python-based device simulator
src/        Backend or helper code
```

## Documentation

The repository includes lightweight documentation intended for both implementation clarity and interview preparation:

* `docs/architecture-overview.md`
* `docs/design-decisions.md`
* `docs/telemetry-flow.md`
* `docs/security-baseline.md`
* `docs/cost-visibility.md`

## Design decisions

The architecture is intentionally shaped by a few core decisions:

* use managed services instead of self-managed infrastructure
* use event-driven processing instead of always-on services
* split storage by access pattern
* keep observability native and lightweight
* keep alerting simple
* keep security explicit but low-cost
* make cost awareness visible
* leave room for future evolution without building it now

## Out of scope for version 1

The following services and capabilities are intentionally excluded from the first version:

* Kinesis
* ECS / EKS
* Step Functions
* OpenSearch
* Timestream
* Glue / Athena
* WAF
* Cognito
* advanced FinOps automation
* enterprise-grade security controls

These may be reasonable future improvements, but they are beyond the intended scope of this lightweight MVP.

## Future evolution

Possible future improvements include:

* SQS for asynchronous buffering
* Timestream for longer-term telemetry trend queries
* WAF for stronger public endpoint protection
* Cognito for user authentication if a portal is added
* ECS or EKS if the processing layer outgrows Lambda
* Glue and Athena for historical analytics over archived telemetry
* Slack integration for alerts
* stronger device authentication

## Interview positioning

This project is designed to be easy to explain in an interview setting.

It demonstrates:

* cloud-native telemetry ingestion
* event-driven AWS processing
* storage design based on access pattern
* basic observability and alerting
* practical security awareness
* lightweight cost-aware cloud thinking

## Status

This project is currently being implemented as a lightweight MVP with iterative documentation, architecture refinement, and demo-oriented design.

