import json
import boto3
import csv
from io import StringIO

S3_BUCKET = "openaq-datalake"
S3_KEY = "trusted/openaq/"

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    params = event.get("queryStringParameters", {}) or {}
    parameter = params.get("parameter", "pm25")

    try:
        response = s3.get_object(Bucket=S3_BUCKET, Key=f"{S3_KEY}parameter={parameter}/")
        content = response["Body"].read().decode("utf-8")
        reader = csv.DictReader(StringIO(content))
        data = [row for row in reader]
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"parameter": parameter, "count": len(data), "data": data}, default=str),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
