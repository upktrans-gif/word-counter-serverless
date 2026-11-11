import json
from datetime import datetime, timezone

def lambda_handler(event, context):
    try:
        body_raw = event.get("body")
        if not body_raw:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Тіло запиту не може бути порожнім"}, ensure_ascii=False),
            }

        body = json.loads(body_raw) if isinstance(body_raw, str) else body_raw

        if "message" not in body or not isinstance(body["message"], str):
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Поле 'message' є обов'язковим і має бути рядком"}, ensure_ascii=False),
            }

        words = body["message"].strip().split()
        response_payload = {
            "word_count": len(words),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response_payload, ensure_ascii=False),
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Некоректний формат JSON"}, ensure_ascii=False),
        }
