"""
PySpark - Análisis Descriptivo de Calidad del Aire (OpenAQ)
Lee desde S3 trusted/ (Parquet) y genera estadísticas descriptivas.
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, stddev, min, max, count, hour, col, when, round

spark = SparkSession.builder.appName("openaq-descriptive-analysis").getOrCreate()

trusted_path = "s3://openaq-datalake/trusted/openaq/"
df = spark.read.parquet(trusted_path)
df.printSchema()

# --- Estadísticas descriptivas por parámetro ---
stats = (
    df.groupBy("parameter")
    .agg(
        count("*").alias("count"),
        round(avg("value"), 2).alias("mean"),
        round(stddev("value"), 2).alias("stddev"),
        round(min("value"), 2).alias("min"),
        round(max("value"), 2).alias("max"),
    )
    .orderBy("parameter")
)
stats.show(truncate=False)

# --- PM2.5 por hora ---
pm25_hour = (
    df.filter(col("parameter") == "pm25")
    .withColumn("hour", hour("datetime_local"))
    .groupBy("hour")
    .agg(
        round(avg("value"), 2).alias("avg_pm25"),
        round(max("value"), 2).alias("max_pm25"),
        round(min("value"), 2).alias("min_pm25"),
    )
    .orderBy("hour")
)
pm25_hour.show(24)

# --- Día vs Noche (PM2.5) ---
day_night = (
    df.filter(col("parameter") == "pm25")
    .withColumn(
        "period",
        when((hour("datetime_local") >= 6) & (hour("datetime_local") <= 17), "DIA")
        .otherwise("NOCHE"),
    )
    .groupBy("period")
    .agg(
        round(avg("value"), 2).alias("avg_pm25"),
        round(max("value"), 2).alias("max_pm25"),
        count("*").alias("samples"),
    )
)
day_night.show()

# --- Superación OMS (PM2.5 > 15) ---
total_pm25 = df.filter(col("parameter") == "pm25").count()
exceed_oms = df.filter((col("parameter") == "pm25") & (col("value") > 15)).count()
pct = round(exceed_oms * 100 / total_pm25, 1) if total_pm25 > 0 else 0
print(f"\n--- Límite OMS (15 µg/m³) ---")
print(f"Total muestras PM2.5: {total_pm25}")
print(f"Superan OMS: {exceed_oms} ({pct}%)")

spark.stop()
