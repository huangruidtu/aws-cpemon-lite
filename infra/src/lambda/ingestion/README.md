# Ingestion Lambda

This directory contains the first version of the AWS Lambda handler used by the API Gateway ingestion endpoint for the AWS CPEmon Lite MVP.

## Files
- `lambda_function.py`: Lambda handler for receiving telemetry requests
- `test_event.json`: Simple Lambda test event used during initial validation

## Notes
This first version only validates that the request body exists, logs the payload, and returns a success response. More advanced validation, normalization, and persistence logic will be added in later subtasks.
