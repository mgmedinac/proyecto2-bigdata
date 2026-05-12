#!/bin/bash
# Crear buckets S3 para datalake por zonas
# Uso: ./s3_setup.sh <bucket-name-prefix>

PREFIX=${1:-openaq-datalake}

echo "Creando buckets S3 para datalake..."

aws s3 mb "s3://${PREFIX}" --region us-east-1

aws s3api put-bucket-lifecycle-configuration \
    --bucket "${PREFIX}" \
    --lifecycle-configuration '{
        "Rules": [
            {"Id": "expire-old-logs", "Status": "Enabled", "Prefix": "logs/", "Expiration": {"Days": 90}}
        ]
    }'

echo "OK. Estructura de zonas (raw/, trusted/, refined/):"
aws s3api put-object --bucket "${PREFIX}" --key "raw/"
aws s3api put-object --bucket "${PREFIX}" --key "trusted/"
aws s3api put-object --bucket "${PREFIX}" --key "refined/"

echo "Buckets listos:"
echo "  s3://${PREFIX}/raw/"
echo "  s3://${PREFIX}/trusted/"
echo "  s3://${PREFIX}/refined/"
