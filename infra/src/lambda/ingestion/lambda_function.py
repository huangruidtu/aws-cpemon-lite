import json
import os
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError


dynamodb = boto3.resource("dynamodb")
s3_client = boto3.client("s3")
cloudwatch_client = boto3.client("cloudwatch")

TABLE_NAME = os.environ["DYNAMODB_TABLE_NAME"]
RAW_PAYLOAD_BUCKET = os.environ["RAW_PAYLOAD_BUCKET"]
CW_METRIC_NAMESPACE = os.environ["CW_METRIC_NAMESPACE"]

table = dynamodb.Table(TABLE_NAME)


def build_response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "body": json.dumps(body)
    }


def parse_event_body(event: dict) -> dict:
    body = event.get("body")

    if body is None:
        raise ValueError("Missing request body")

    if isinstance(body, str):
        return json.loads(body)

    if isinstance(body, dict):
        return body

    raise ValueError("Unsupported body format")


def validate_payload(payload: dict) -> None:
    required_fields = [
        "device_id",
        "last_seen",
        "cpu_usage",
        "memory_usage",
        "temperature",
        "wan_status"
    ]

    for field in required_fields:
        if field not in payload:
            raise ValueError(f"Missing required field: {field}")

    if payload["wan_status"] not in ["up", "down"]:
        raise ValueError("wan_status must be either 'up' or 'down'")

    if not isinstance(payload["cpu_usage"], (int, float)):
        raise ValueError("cpu_usage must be a number")

    if not isinstance(payload["memory_usage"], (int, float)):
        raise ValueError("memory_usage must be a number")

    if not isinstance(payload["temperature"], (int, float)):
        raise ValueError("temperature must be a number")


def derive_health_state(payload: dict) -> str:
    wan_status = payload["wan_status"]
    cpu_usage = payload["cpu_usage"]
    memory_usage = payload["memory_usage"]
    temperature = payload["temperature"]

    if temperature > 85:
        return "critical"

    if wan_status == "down" or cpu_usage > 90 or memory_usage > 90:
        return "warning"

    return "ok"


def publish_metrics(payload: dict, health_state: str) -> None:
    device_id = payload["device_id"]
    wan_down = 1 if payload["wan_status"] == "down" else 0
    health_warning = 1 if health_state == "warning" else 0
    health_critical = 1 if health_state == "critical" else 0

    cloudwatch_client.put_metric_data(
        Namespace=CW_METRIC_NAMESPACE,
        MetricData=[
            {
                "MetricName": "DeviceTelemetryReceived",
                "Dimensions": [
                    {"Name": "device_id", "Value": device_id}
                ],
                "Value": 1,
                "Unit": "Count"
            },
            {
                "MetricName": "WanDown",
                "Dimensions": [
                    {"Name": "device_id", "Value": device_id}
                ],
                "Value": wan_down,
                "Unit": "Count"
            },
            {
                "MetricName": "CpuUsage",
                "Dimensions": [
                    {"Name": "device_id", "Value": device_id}
                ],
                "Value": payload["cpu_usage"],
                "Unit": "Percent"
            },
            {
                "MetricName": "MemoryUsage",
                "Dimensions": [
                    {"Name": "device_id", "Value": device_id}
                ],
                "Value": payload["memory_usage"],
                "Unit": "Percent"
            },
            {
                "MetricName": "Temperature",
                "Dimensions": [
                    {"Name": "device_id", "Value": device_id}
                ],
                "Value": payload["temperature"],
                "Unit": "None"
            },
            {
                "MetricName": "HealthWarning",
                "Dimensions": [
                    {"Name": "device_id", "Value": device_id}
                ],
                "Value": health_warning,
                "Unit": "Count"
            },
            {
                "MetricName": "HealthCritical",
                "Dimensions": [
                    {"Name": "device_id", "Value": device_id}
                ],
                "Value": health_critical,
                "Unit": "Count"
            }
        ]
    )


def write_to_dynamodb(payload: dict, health_state: str) -> None:
    ingested_at = datetime.now(timezone.utc).isoformat()

    item = {
        "device_id": payload["device_id"],
        "last_seen": payload["last_seen"],
        "cpu_usage": payload["cpu_usage"],
        "memory_usage": payload["memory_usage"],
        "temperature": payload["temperature"],
        "wan_status": payload["wan_status"],
        "health_state": health_state,
        "ingested_at": ingested_at
    }

    table.put_item(Item=item)


def archive_raw_payload(payload: dict) -> None:
    device_id = payload["device_id"]
    last_seen = payload["last_seen"]
    safe_last_seen = last_seen.replace(":", "-")
    object_key = f"raw/{device_id}/{safe_last_seen}.json"

    s3_client.put_object(
        Bucket=RAW_PAYLOAD_BUCKET,
        Key=object_key,
        Body=json.dumps(payload).encode("utf-8"),
        ContentType="application/json"
    )


def lambda_handler(event, context):
    try:
        payload = parse_event_body(event)
        validate_payload(payload)

        health_state = derive_health_state(payload)

        publish_metrics(payload, health_state)
        write_to_dynamodb(payload, health_state)
        archive_raw_payload(payload)

        return build_response(
            200,
            {
                "message": "Telemetry processed successfully",
                "device_id": payload["device_id"],
                "health_state": health_state
            }
        )

    except ValueError as exc:
        print(f"Validation error: {str(exc)}")
        return build_response(
            400,
            {
                "message": "Invalid telemetry payload",
                "error": str(exc)
            }
        )

    except ClientError as exc:
        print(f"AWS service error: {str(exc)}")
        return build_response(
            500,
            {
                "message": "Failed to process telemetry",
                "error": "AWS service operation failed"
            }
        )

    except Exception as exc:
        print(f"Unexpected error: {str(exc)}")
        return build_response(
            500,
            {
                "message": "Unexpected server error",
                "error": str(exc)
            }
        )
