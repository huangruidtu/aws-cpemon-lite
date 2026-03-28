import json
import os
from datetime import datetime, timedelta, timezone

import boto3


dynamodb = boto3.resource("dynamodb")
cloudwatch_client = boto3.client("cloudwatch")

TABLE_NAME = os.environ["DYNAMODB_TABLE_NAME"]
CW_METRIC_NAMESPACE = os.environ["CW_METRIC_NAMESPACE"]
HEARTBEAT_STALE_MINUTES = int(os.environ.get("HEARTBEAT_STALE_MINUTES", "10"))

table = dynamodb.Table(TABLE_NAME)


def publish_missing_heartbeat_metric(stale_count: int) -> None:
    cloudwatch_client.put_metric_data(
        Namespace=CW_METRIC_NAMESPACE,
        MetricData=[
            {
                "MetricName": "FleetMissingHeartbeatCount",
                "Value": stale_count,
                "Unit": "Count"
            }
        ]
    )

    print(f"Published FleetMissingHeartbeatCount={stale_count}")


def build_response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    now = datetime.now(timezone.utc)
    stale_threshold = now - timedelta(minutes=HEARTBEAT_STALE_MINUTES)

    print(
        f"Starting heartbeat check with stale threshold "
        f"{stale_threshold.isoformat()}"
    )

    latest_last_seen_by_device = {}
    scan_kwargs = {}
    scanned_items = 0

    while True:
        response = table.scan(**scan_kwargs)
        items = response.get("Items", [])
        scanned_items += len(items)

        for item in items:
            device_id = item.get("device_id")
            last_seen = item.get("last_seen")

            if not device_id or not last_seen:
                continue

            try:
                last_seen_dt = datetime.fromisoformat(last_seen.replace("Z", "+00:00"))
            except ValueError:
                print(
                    f"Skipping invalid last_seen format for device_id={device_id}: "
                    f"{last_seen}"
                )
                continue

            current_latest = latest_last_seen_by_device.get(device_id)

            if current_latest is None or last_seen_dt > current_latest:
                latest_last_seen_by_device[device_id] = last_seen_dt

        last_evaluated_key = response.get("LastEvaluatedKey")
        if not last_evaluated_key:
            break

        scan_kwargs["ExclusiveStartKey"] = last_evaluated_key

    stale_count = 0

    for device_id, latest_last_seen in latest_last_seen_by_device.items():
        if latest_last_seen < stale_threshold:
            stale_count += 1
            print(
                f"Device marked stale: device_id={device_id}, "
                f"last_seen={latest_last_seen.isoformat()}"
            )

    print(
        f"Heartbeat check completed. scanned_items={scanned_items}, "
        f"unique_devices={len(latest_last_seen_by_device)}, "
        f"stale_devices={stale_count}"
    )

    publish_missing_heartbeat_metric(stale_count)

    return build_response(
        200,
        {
            "message": "Heartbeat check completed",
            "stale_devices": stale_count,
            "unique_devices": len(latest_last_seen_by_device),
            "stale_threshold": stale_threshold.isoformat()
        }
    )
