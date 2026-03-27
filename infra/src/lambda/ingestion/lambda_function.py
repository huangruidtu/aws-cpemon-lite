import json


def lambda_handler(event, context):
    try:
        body = event.get("body")

        if body is None:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Missing request body"})
            }

        print("Received telemetry payload:")
        print(body)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Telemetry received successfully"
            })
        }

    except Exception as exc:
        print(f"Error processing request: {exc}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal server error"
            })
        }
