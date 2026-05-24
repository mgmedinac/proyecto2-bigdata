# Punto 4 - Procesamiento con Spark y AWS Glue

## Descripción

Job de AWS Glue que transforma datos desde la zona `raw/` (CSV) hacia la zona `trusted/` (Parquet) en S3.

## Transformaciones

- Casting de tipos (int, double, timestamp)
- Parseo de fechas (`datetimeUtc`, `datetimeLocal`)
- Normalización de nombres de parámetros
- Eliminación de columnas innecesarias
- Redondeo de valores a 1 decimal
- Escritura en formato Parquet particionado por `parameter`

## Ejecución

### AWS Glue
1. Subir `pyspark_process.py` a AWS Glue Jobs
2. Configurar job con Spark 3.x + Glue 4.0
3. Ejecutar

### Local (pruebas)
```bash
pip install pyspark
python pyspark_process.py
```
