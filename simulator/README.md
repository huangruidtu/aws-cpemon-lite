# Device Simulator

A lightweight Python-based simulator for generating and sending sample telemetry payloads to the AWS CPEmon Lite ingestion endpoint.

## Requirements
- Python 3
- requests
- python-dotenv

## Configuration
Create a `.env` file from `.env.example` and set:

- `INGESTION_URL`
- `DEVICE_ID`
- `SEND_INTERVAL`

## Run
```bash
python simulator.py
