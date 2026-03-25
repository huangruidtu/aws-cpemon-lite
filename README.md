# aws-cpemon-lite
A lightweight AWS-native MVP for CPE telemetry ingestion, observability, and alerting.

# AWS CPEmon Lite

A lightweight AWS-native MVP inspired by a CPE monitoring scenario.

## Goal

This project demonstrates a minimal end-to-end telemetry pipeline using managed AWS services. The focus is on simplicity, low operational overhead, and cost-conscious cloud design.

## Planned scope

- Simulated device telemetry generation
- Cloud ingestion endpoint
- Backend processing
- Persistent telemetry storage
- Basic observability and alerting
- Documentation and demo walkthrough

## Planned AWS services

- API Gateway
- AWS Lambda
- DynamoDB
- CloudWatch Logs / Metrics / Alarms
- SNS (optional)

## Project structure

```text
docs/       Documentation, architecture notes, diagrams
infra/      Infrastructure as code
simulator/  Python-based device simulator
src/        Backend or helper code
