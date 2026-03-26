# Cost Visibility

## Purpose
This document describes the lightweight cost visibility approach for AWS CPEmon Lite.

The MVP is intentionally small, but cost awareness is still treated as an important part of good cloud platform design.

## Goal
The goal is not to build a full FinOps solution. The goal is to make the MVP cost-aware in a simple and practical way.

## Selected AWS services

### AWS Cost Explorer
Used for service-level cost visibility and spend inspection.

#### Why
Cost Explorer provides a simple way to understand which AWS services are contributing to the project’s spend and how usage trends change over time.

### AWS Budgets
Used for lightweight monthly budget guardrails and notifications.

#### Why
AWS Budgets makes it easy to set a basic spending threshold for the MVP and notify the operator when actual or forecasted spend approaches that limit.

## Why this fits the MVP
This approach is intentionally lightweight:

- no custom cost dashboard required
- no extra infrastructure required
- very little implementation effort
- easy to explain in documentation and interviews

It supports the broader project principle that cloud architecture should not only work technically, but should also remain aware of operational cost.

## Example cost guardrail
A simple example budget policy for the MVP could be:

- define a small monthly budget
- alert at 50% usage
- alert again at 80% usage
- trigger a final alert at 100%

## Expected usage
Cost visibility is treated as a supporting operational capability rather than part of the telemetry data path.

It helps answer basic questions such as:

- which services are generating the current cost
- whether the MVP is still operating within its intended budget range
- whether architecture changes are increasing cost unexpectedly

## Out of scope
The MVP does not currently include:

- advanced FinOps automation
- automated shutdown actions
- full cost allocation tagging strategy
- custom cost reporting pipeline

These can be explored later if the project grows.
