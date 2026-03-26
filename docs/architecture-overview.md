# Architecture Overview

## Overview
AWS CPEmon Lite is a lightweight AWS-native telemetry monitoring MVP inspired by a cloud-based CPE monitoring scenario.

The goal of this project is to simulate a simple but realistic telemetry path from devices into AWS while keeping the design minimal, cost-aware, and easy to explain in interviews. The architecture favors managed AWS services to reduce operational overhead and avoid unnecessary platform complexity.

## Architecture goals
The MVP is designed around the following principles:

- managed-first design
- minimal operational overhead
- cost-aware architecture
- production-minded but lightweight
- simple service boundaries
- easy to explain and evolve

## High-level architecture
The core telemetry path is:

**Simulator → API Gateway → Lambda**

Lambda then performs the following responsibilities:

- validate telemetry payloads
- write processing logs to CloudWatch Logs
- publish custom metrics to CloudWatch Metrics
- store raw telemetry in S3
- update latest device state in DynamoDB

The detection and notification path is:

**CloudWatch Metrics → CloudWatch Alarms → SNS**

Supporting operational and governance capabilities include:

- IAM for least-privilege access control
- CloudWatch Dashboard for operational visibility
- Parameter Store for externalized secrets/configuration
- CloudTrail for auditability awareness
- Cost Explorer and AWS Budgets for lightweight cost visibility

## Core AWS services
The MVP uses the following AWS managed services:

- API Gateway
- Lambda
- S3
- DynamoDB
- CloudWatch Logs
- CloudWatch Metrics
- CloudWatch Alarms
- CloudWatch Dashboard
- SNS
- IAM
- Systems Manager Parameter Store
- CloudTrail
- Cost Explorer
- AWS Budgets

## Why this architecture
This architecture intentionally stays small and focused. It is not meant to reproduce a full production-scale monitoring platform. Instead, it demonstrates the most important platform engineering ideas in a simple and interview-ready form:

- telemetry ingestion
- event-driven processing
- storage split by access pattern
- observability
- alerting
- lightweight security controls
- cost awareness

## Future evolution
If the platform needed to scale further, the next possible evolution areas could include:

- SQS for asynchronous buffering
- Timestream for longer-term time-series querying
- WAF for stronger public endpoint protection
- Cognito for user authentication if a portal is added
- ECS or EKS if the processing layer outgrows Lambda
- Glue and Athena for historical analytics over archived telemetry
