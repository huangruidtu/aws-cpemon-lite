# Cost Visibility

## Purpose
This document describes the lightweight cost visibility approach for AWS CPEmon Lite.

The MVP is intentionally small, but cost awareness is still treated as an important part of good cloud platform design.

## Goal
The goal is not to build a full FinOps solution. The goal is to make the MVP cost-aware in a simple, practical, and explainable way.

## Current MVP approach

The current MVP uses two lightweight AWS-native capabilities:

- **AWS Cost Explorer**
- **AWS Budgets**

These are used as supporting operational capabilities rather than part of the telemetry processing path.

## AWS Cost Explorer

### Current usage
Cost Explorer is used mainly for **service-level cost visibility**.

The current MVP reviews cost and usage with a simple view such as:

- group by **Service**
- review recent time ranges such as month-to-date or recent weeks
- use the result as a lightweight way to understand which AWS services are contributing to project cost

### Why this is enough for the MVP
The current project footprint is small and the visible spend is very low.

At this stage, the main value of Cost Explorer is not detailed cost optimization, but lightweight visibility into:

- whether the project is generating spend at all
- which AWS services are contributing to spend
- whether architecture changes are introducing unexpected cost

## AWS Budgets

### Current usage
AWS Budgets is used as a lightweight monthly budget guardrail.

The current MVP uses a very small budget threshold because the project is a lightweight interview-oriented implementation rather than a continuously running production platform.

### Why this is enough for the MVP
The purpose of the budget is to provide a simple early warning if the small project starts generating more spend than expected.

This helps demonstrate that cost-aware design is not only about architecture choices, but also about having a basic operational guardrail in place.

## Why this fits the MVP

This approach is intentionally lightweight:

- no custom cost dashboard required
- no extra infrastructure required
- very little implementation effort
- easy to explain in documentation and interviews

It supports the broader project principle that cloud architecture should not only work technically, but should also remain aware of operational cost.

## MVP decision rationale

For the current MVP, the chosen cost model is intentionally simple:

- service-level visibility in Cost Explorer
- a lightweight budget guardrail in AWS Budgets

This is sufficient because:

- the project has a very small footprint
- the number of services is limited
- there is no multi-team or multi-environment cost-governance requirement
- the main goal is awareness and guardrails rather than detailed financial optimization

## Larger-scale platform direction

At larger scale, a service-level view alone would not be enough.

A larger production-scale platform would typically require deeper cost analysis and more structured budget monitoring, such as:

- cost breakdown by **service**
- cost breakdown by **region**
- cost breakdown by **usage type**
- cost breakdown by **linked account**
- cost breakdown by **tag** or **cost category**
- separate budgets for **production**, **staging**, and **development**
- possibly separate budgets for teams, applications, or business units
- stronger use of forecast-based alerts

This means the current MVP cost setup is intentionally appropriate for its scale, while larger systems would require a more advanced cost-monitoring model.

## Expected value

The current cost-visibility baseline helps answer practical questions such as:

- which services are currently generating spend
- whether the MVP is still operating within its intended budget range
- whether new architecture changes are increasing cost unexpectedly
- how cost visibility might evolve if the platform grows significantly

## Out of scope

The MVP does not currently include:

- advanced FinOps automation
- automated shutdown actions
- full cost allocation tagging strategy
- custom cost reporting pipeline
- layered budget model across teams or environments

These can be explored later if the project grows.
