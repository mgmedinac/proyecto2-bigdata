# Punto 7 - Análisis Descriptivo con PySpark

## Archivos

### sparksql_analysis.py
Script para ejecutar en AWS EMR o AWS Glue Jobs. Lee desde S3 trusted/ (Parquet) y genera:
- Estadísticas descriptivas por parámetro (count, mean, stddev, min, max)
- PM2.5 promedio por hora del día
- Comparación día vs noche
- Porcentaje de superación del límite OMS

```bash
spark-submit sparksql_analysis.py
```

### descriptive_analysis_local.py
Versión extendida para ejecución local. Lee el CSV directamente e incluye:
- Correlación de Pearson (temperatura vs PM2.5)
- Correlación de Pearson (humedad vs um003)
- Interpretación de correlación (débil/moderada/fuerte)

```bash
pip install pyspark
python descriptive_analysis_local.py
```
