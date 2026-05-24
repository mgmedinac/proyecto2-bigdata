# Punto 6 - Consultas SQL

## 6.1 Amazon Athena

Ejecutar `athena_queries.sql` desde la consola de Athena.

Las consultas incluyen:
- PM2.5 por hora del día
- Correlación temperatura vs PM2.5
- Superación del límite OMS (15 µg/m³)
- Comparación día vs noche
- Correlación humedad vs um003

## 6.2 EMR/Hive

Ejecutar `hive_queries.sql` en una sesión de Hive sobre EMR.

```bash
hive -f hive_queries.sql
```

## 6.3 SparkSQL

Las mismas consultas analíticas están implementadas en PySpark en el **Punto 7** (`sparksql_analysis.py`), donde se pueden ejecutar como SparkSQL.
