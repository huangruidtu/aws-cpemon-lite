import json
from datetime import datetime, timezone


REQUIRED_FIELDS = [
    "device_id",
    "timestamp",
    "cpu_usage",
    "memory_usage",
    "connection_status",
    "firmware_version",
    "temperature",
]

ALLOWED_CONNECTION_STATUS = {"online", "degraded", "offline"}


def build_response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
    }


def parse_body(event: dict) -> dict:
    body = event.get("body")

    if body is None:
        raise ValueError("Missing request body")

    if isinstance(body, str):
        return json.loads(body)

    if isinstance(body, dict):
        return body

    raise ValueError("Unsupported request body format")


def validate_payload(payload: dict) -> None:
    for field in REQUIRED_FIELDS:
        if field not in payload:
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(payload["device_id"], str) or not payload["device_id"].strip():
        raise ValueError("device_id must be a non-empty string")

    if not isinstance(payload["timestamp"], str) or not payload["timestamp"].strip():
        raise ValueError("timestamp must be a non-empty string")

    if not isinstance(payload["firmware_version"], str) or not payload["firmware_version"].strip():
        raise ValueError("firmware_version must be a non-empty string")

    if payload["connection_status"] not in ALLOWED_CONNECTION_STATUS:
        raise ValueError("connection_status must be one of: online, degraded, offline")

    try:
        cpu_usage = float(payload["cpu_usage"])
    except (TypeError, ValueError):
        raise ValueError("cpu_usage must be a number")

    try:
        memory_usage = float(payload["memory_usage"])
    except (TypeError, ValueError):
        raise ValueError("memory_usage must be a number")

    try:
        temperature = float(payload["temperature"])
    except (TypeError, ValueError):
        raise ValueError("temperature must be a number")

    if not 0 <= cpu_usage <= 100:
        raise ValueError("cpu_usage must be between 0 and 100")

    if not 0 <= memory_usage <= 100:
        raise ValueError("memory_usage must be between 0 and 100")

    if not -50 <= temperature <= 150:
        raise ValueError("temperature must be between -50 and 150")


def normalize_payload(payload: dict) -> dict:
    return {
        "device_id": payload["device_id"].strip(),
        "event_timestamp": payload["timestamp"],
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "cpu_usage": float(payload["cpu_usage"]),
        "memory_usage": float(payload["memory_usage"]),
        "connection_status": payload["connection_status"],
        "firmware_version": payload["firmware_version"].strip(),
        "temperature": float(payload["temperature"]),
    }


def lambda_handler(event, context):
    try:
        payload = parse_body(event)
        print("Received raw payload:")
        print(json.dumps(payload))

        validate_payload(payload)

        normalized_record = normalize_payload(payload)
        print("Validated and normalized record:")
        print(json.dumps(normalized_record))

        return build_response(
            200,
            {
                "message": "Telemetry processed successfully",
                "record": normalized_record,
            },
        )

    except ValueError as exc:
        print(f"Validation error: {exc}")
        return build_response(
            400,
            {
                "message": "Invalid telemetry payload",
                "error": str(exc),
            },
        )

    except json.JSONDecodeError as exc:
        print(f"JSON parsing error: {exc}")
        return build_response(
            400,
            {
                "message": "Request body is not valid JSON",
                "error": str(exc),
            },
        )

    except Exception as exc:
        print(f"Unexpected error: {exc}")
        return build_response(
            500,
            {
                "message": "Internal server error",
            },
        )
