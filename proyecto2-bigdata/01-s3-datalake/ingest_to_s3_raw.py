import boto3
import os
import argparse
from datetime import datetime

S3_BUCKET = "openaq-datalake"
S3_RAW_PREFIX = "raw/openaq/csv/"

def upload_to_s3(csv_path: str, profile: str = None):
    session = boto3.Session(profile_name=profile) if profile else boto3.Session()
    s3 = session.client("s3")

    filename = os.path.basename(csv_path)
    date_str = datetime.utcnow().strftime("%Y/%m/%d")
    s3_key = f"{S3_RAW_PREFIX}{date_str}/{filename}"

    try:
        s3.upload_file(csv_path, S3_BUCKET, s3_key)
        print(f"OK -> s3://{S3_BUCKET}/{s3_key}")
    except Exception as e:
        print(f"ERROR: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sube CSV de OpenAQ a S3 raw/")
    parser.add_argument("csv_path", help="Ruta al archivo CSV")
    parser.add_argument("--profile", help="Perfil AWS CLI", default=None)
    args = parser.parse_args()
    upload_to_s3(args.csv_path, args.profile)
