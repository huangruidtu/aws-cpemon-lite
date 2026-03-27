import json
import os
import random
import time
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv


load_dotenv()


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


INGESTION_URL = get_env("INGESTION_URL")
DEVICE_ID = get_env("DEVICE_ID", "cpe-001")
SEND_INTERVAL = int(get_env("SEND_INTERVAL", "10"))


def generate_payload(device_id: str) -> dict:
    return {
        "device_id": device_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cpu_usage": round(random.uniform(5.0, 85.0), 2),
        "memory_usage": round(random.uniform(10.0, 90.0), 2),
        "connection_status": random.choice(["online", "degraded"]),
        "firmware_version": "1.0.3",
        "temperature": round(random.uniform(35.0, 65.0), 2),
    }


def send_payload(url: str, payload: dict) -> None:
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"[INFO] Sent payload: {json.dumps(payload)}")
        print(f"[INFO] Response: {response.status_code} {response.text}")
    except requests.RequestException as exc:
        print(f"[ERROR] Failed to send payload: {exc}")


def main() -> None:
    print("[INFO] Starting device simulator...")
    print(f"[INFO] Device ID: {DEVICE_ID}")
    print(f"[INFO] Ingestion URL: {INGESTION_URL}")
    print(f"[INFO] Send interval: {SEND_INTERVAL}s")

    while True:
        payload = generate_payload(DEVICE_ID)
        send_payload(INGESTION_URL, payload)
        time.sleep(SEND_INTERVAL)


if __name__ == "__main__":
    main()
