# Design Decisions

## Purpose
This document records the main architecture decisions behind AWS CPEmon Lite.

The goal is to explain why the MVP was intentionally designed to stay simple, low-maintenance, and cost-aware, while still looking realistic enough for technical discussions and interviews.

## 1. Managed-first architecture
The MVP uses AWS managed services instead of self-managed infrastructure wherever possible.

### Decision
Use API Gateway, Lambda, S3, DynamoDB, CloudWatch, SNS, IAM, Parameter Store, and related native AWS services as the foundation of the platform.

### Reasoning
This reduces operational burden, shortens implementation time, and aligns with the goal of building a cloud-native MVP with minimal maintenance.

### Trade-off
The design is less flexible than a larger container-based or event-stream-based platform, but much simpler to deliver and explain.

## 2. Event-driven processing over always-on services
The telemetry pipeline is built as an event-driven flow instead of running backend services continuously.

### Decision
Use API Gateway as the ingestion endpoint and Lambda as the processing layer.

### Reasoning
This fits lightweight telemetry ingestion well and avoids operating EC2 or container-based APIs for a small MVP.

### Trade-off
If workload complexity or sustained traffic grows significantly, ECS, EKS, or queue-based buffering could become more appropriate.

## 3. Split storage by access pattern
The design uses separate storage systems for historical archive and current operational state.

### Decision
Use S3 for raw telemetry archive and DynamoDB for latest device state.

### Reasoning
S3 is cost-effective and durable for raw payload retention, while DynamoDB is efficient for fast key-based latest-state lookup.

### Trade-off
Two storage backends are slightly more complex than one, but they reflect realistic access patterns much better.

## 4. Keep observability native and lightweight
Observability is kept inside CloudWatch rather than introducing a larger external stack.

### Decision
Use CloudWatch Logs, CloudWatch Metrics, CloudWatch Alarms, and CloudWatch Dashboard.

### Reasoning
This keeps the MVP simple, AWS-native, and operationally light while still covering the main observability layers.

### Trade-off
The observability stack is less feature-rich than Prometheus/Grafana or ELK-based solutions, but it is a better fit for the current scope.

## 5. Keep alerting simple
The first version uses a lightweight notification path.

### Decision
Use SNS for alert notifications.

### Reasoning
SNS is easy to integrate with CloudWatch Alarms and is enough for basic email-based alert delivery.

### Trade-off
This does not include advanced routing, deduplication, suppression, or incident workflow management.

## 6. Security should be explicit but low-cost
The MVP includes practical security controls without turning the project into a full security platform.

### Decision
Use HTTPS-only ingress, least-privilege IAM, encrypted storage, restricted S3 access, externalized secrets, and auditability awareness.

### Reasoning
These controls add strong engineering value at relatively low implementation cost.

### Trade-off
The design does not yet include WAF tuning, Cognito, mTLS, GuardDuty, Security Hub, or enterprise-grade compliance controls.

## 7. Cost awareness should be visible
Cost-aware design is treated as an explicit part of the architecture rather than a hidden assumption.

### Decision
Use Cost Explorer for service-level cost visibility and AWS Budgets for simple monthly budget guardrails.

### Reasoning
This helps reinforce the project’s cloud cost awareness without adding custom cost tooling.

### Trade-off
The MVP does not include advanced FinOps automation, tagging governance, or automated shutdown controls.

## 8. Keep future evolution open, but do not build it now
The architecture should be extensible, but the MVP should stay focused.

### Decision
Do not include Kinesis, ECS, EKS, Step Functions, OpenSearch, Timestream, Glue, WAF, or Cognito in the first version.

### Reasoning
These services can be valid later, but they would add complexity beyond the needs of this lightweight telemetry MVP.

### Trade-off
The first version is intentionally not a full production platform. It is a minimal production-minded foundation.
