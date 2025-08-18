# lambda_function.py
# Thin HTTP wrapper for API Gateway -> Lambda

import json
from resume_matcher import generate_match_report

def lambda_handler(event, context):
    try:
        body = event.get("body")
        if isinstance(body, str):
            data = json.loads(body)
        elif isinstance(body, dict):
            data = body
        else:
            data = {}

        jd_text = data.get("jd_text", "")
        resume_text = data.get("resume_text", "")

        if not jd_text or not resume_text:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"  # CORS
                },
                "body": json.dumps({"error": "Both jd_text and resume_text are required"})
            }

        report = generate_match_report(jd_text, resume_text)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"  # CORS
            },
            "body": json.dumps(report, ensure_ascii=False)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }
