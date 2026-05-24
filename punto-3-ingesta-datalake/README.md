# Punto 3 - Ingesta al Datalake (S3)

## Estructura del Bucket S3

```
s3://openaq-datalake/
├── raw/          # Datos sin procesar (CSV original)
├── trusted/      # Datos limpios en Parquet
└── refined/      # Datos agregados para análisis
```

## Scripts

### ingest.sh
Configura el bucket S3 y las zonas del datalake:

```bash
chmod +x ingest.sh
./ingest.sh openaq-datalake
```

### ingest_all_sources.py
Sube datos al bucket S3 en la zona raw/:

```bash
pip install boto3
python ingest_all_sources.py openaq_location_3163445_measurments.csv
```

## Automatización

La ingesta puede programarse con cron en EC2 para ejecución periódica.
