#!/bin/bash
# Configuración de EC2 para almacenamiento de CSVs históricos
# 1. Conectarse por SSH y ejecutar:

echo "=== Configuración EC2 - Almacenamiento CSVs Históricos ==="

# Variables (reemplazar con valores reales)
BUCKET_NAME="openaq-datalake"
LOCAL_DIR="/data/openaq/historical"

# Crear directorio
sudo mkdir -p "$LOCAL_DIR"
sudo chown -R "$(whoami):$(whoami)" "$LOCAL_DIR"

# Descargar CSVs desde S3 raw/
echo "Descargando datos históricos desde S3..."
aws s3 sync "s3://${BUCKET_NAME}/raw/" "$LOCAL_DIR/raw/"

# Programar descarga periódica con cron (cada 6 horas)
CRON_JOB="0 */6 * * * aws s3 sync s3://${BUCKET_NAME}/raw/ ${LOCAL_DIR}/raw/ >> /var/log/openaq-sync.log 2>&1"
(crontab -l 2>/dev/null | grep -v "openaq-sync"; echo "$CRON_JOB") | crontab -

echo "EC2 listo. Datos en: $LOCAL_DIR"
echo "Cron cada 6h: activado."
