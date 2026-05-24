-- Crea la base de datos en AWS Glue Data Catalog (si no existe)
CREATE DATABASE IF NOT EXISTS openaq_db;

-- Tabla sobre datos trusted/ en Parquet (creada por Crawler o manual)
CREATE EXTERNAL TABLE IF NOT EXISTS openaq_db.trusted_measurements (
    location_id   INT,
    location_name STRING,
    parameter     STRING,
    value         DOUBLE,
    unit          STRING,
    timezone      STRING,
    latitude      DOUBLE,
    longitude     DOUBLE,
    owner_name    STRING,
    provider      STRING,
    datetime_utc  TIMESTAMP,
    datetime_local TIMESTAMP
)
PARTITIONED BY (dt STRING)
STORED AS PARQUET
LOCATION 's3://openaq-datalake/trusted/openaq/'
TBLPROPERTIES ('parquet.compression'='SNAPPY');

-- Reparar tablas para detectar particiones
MSCK REPAIR TABLE openaq_db.trusted_measurements;

-- Vista previa
SELECT * FROM openaq_db.trusted_measurements LIMIT 10;

-- Conteo por parámetro
SELECT parameter, COUNT(*) AS cnt
FROM openaq_db.trusted_measurements
GROUP BY parameter;
