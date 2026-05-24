# Punto 5 - Catalogación con Glue y Hive

## AWS Glue Crawler

Configurar un Crawler que apunte a `s3://openaq-datalake/trusted/openaq/` para catalogar automáticamente las tablas en AWS Glue Data Catalog.

### Comando CLI
```bash
aws glue create-crawler \
    --name openaq-trusted-crawler \
    --role arn:aws:iam::ACCOUNT:role/AWSGlueServiceRole \
    --database-name openaq_db \
    --targets '{"S3Targets":[{"Path":"s3://openaq-datalake/trusted/openaq/"}]}'

aws glue start-crawler --name openaq-trusted-crawler
```

## Hive DDL

El archivo `hive_tables.sql` contiene la definición manual de la tabla externa:

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS openaq_db.trusted_measurements (
    location_id INT, location_name STRING, parameter STRING,
    value DOUBLE, unit STRING, timezone STRING,
    latitude DOUBLE, longitude DOUBLE,
    owner_name STRING, provider STRING,
    datetime_utc TIMESTAMP, datetime_local TIMESTAMP
)
PARTITIONED BY (dt STRING)
STORED AS PARQUET
LOCATION 's3://openaq-datalake/trusted/openaq/'
TBLPROPERTIES ('parquet.compression'='SNAPPY');

MSCK REPAIR TABLE openaq_db.trusted_measurements;
```
