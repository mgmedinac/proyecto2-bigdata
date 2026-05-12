"""
PySpark - Análisis Descriptivo de Calidad del Aire (OpenAQ)
Versión local: lee CSV directo en vez de S3 Parquet
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, stddev, min, max, count, hour, col, when, round
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "openaq_location_3163445_measurments.csv")

spark = SparkSession.builder.appName("openaq-descriptive-analysis-local").getOrCreate()

df = (
    spark.read.format("csv")
    .option("header", True)
    .option("inferSchema", True)
    .option("quote", '"')
    .option("escape", '"')
    .load(CSV_PATH)
)

df = df.withColumn("value", col("value").cast("double"))

print("=" * 60)
print("ESQUEMA DEL DATAFRAME")
print("=" * 60)
df.printSchema()

# --- Estadísticas descriptivas por parámetro ---
print("\n" + "=" * 60)
print("ESTADÍSTICAS DESCRIPTIVAS POR PARÁMETRO")
print("=" * 60)
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
print("\n" + "=" * 60)
print("PM2.5 PROMEDIO POR HORA DEL DÍA")
print("=" * 60)
pm25_hour = (
    df.filter(col("parameter") == "pm25")
    .withColumn("hour", hour(col("datetimeLocal")))
    .groupBy("hour")
    .agg(
        round(avg("value"), 2).alias("avg_pm25"),
        round(max("value"), 2).alias("max_pm25"),
        round(min("value"), 2).alias("min_pm25"),
    )
    .orderBy("hour")
)
pm25_hour.show(24)
print("Hora con mayor PM2.5 promedio:")
best_row = pm25_hour.orderBy(col("avg_pm25").desc()).first()
print(f"  -> Hora {best_row['hour']}:00 con {best_row['avg_pm25']} µg/m³")

# --- Día vs Noche (PM2.5) ---
print("\n" + "=" * 60)
print("DÍA vs NOCHE - PM2.5")
print("=" * 60)
day_night = (
    df.filter(col("parameter") == "pm25")
    .withColumn(
        "period",
        when((hour(col("datetimeLocal")) >= 6) & (hour(col("datetimeLocal")) <= 17), "DIA (06-17)")
        .otherwise("NOCHE (18-05)"),
    )
    .groupBy("period")
    .agg(
        round(avg("value"), 2).alias("avg_pm25"),
        round(max("value"), 2).alias("max_pm25"),
        round(min("value"), 2).alias("min_pm25"),
        count("*").alias("samples"),
    )
)
day_night.show()

# --- Superación OMS (PM2.5 > 15) ---
print("\n" + "=" * 60)
print("LÍMITE OMS (15 µg/m³) - SUPERACIÓN")
print("=" * 60)
total_pm25 = df.filter(col("parameter") == "pm25").count()
exceed_oms = df.filter((col("parameter") == "pm25") & (col("value") > 15)).count()
pct = round(exceed_oms * 100 / total_pm25, 1) if total_pm25 > 0 else 0
print(f"Total muestras PM2.5:       {total_pm25}")
print(f"Superan límite OMS (15):   {exceed_oms}")
print(f"Porcentaje de superación:  {pct}%")

# --- Correlación temperatura vs PM2.5 ---
print("\n" + "=" * 60)
print("CORRELACIÓN TEMPERATURA vs PM2.5")
print("=" * 60)
temp_df = df.filter(col("parameter") == "temperature").select(
    col("datetimeLocal").alias("dt"), col("value").alias("temp")
)
pm25_df = df.filter(col("parameter") == "pm25").select(
    col("datetimeLocal").alias("dt"), col("value").alias("pm25")
)
corr_df = temp_df.join(pm25_df, "dt").select("temp", "pm25")
corr_val = corr_df.stat.corr("temp", "pm25")
print(f"Coeficiente de correlación de Pearson: {corr_val:.4f}")
if abs(corr_val) >= 0.7:
    print("Interpretación: Correlación fuerte")
elif abs(corr_val) >= 0.5:
    print("Interpretación: Correlación moderada")
else:
    print("Interpretación: Correlación débil")

# --- Correlación humedad vs um003 ---
print("\n" + "=" * 60)
print("CORRELACIÓN HUMEDAD vs um003")
print("=" * 60)
hum_df = df.filter(col("parameter") == "relativehumidity").select(
    col("datetimeLocal").alias("dt"), col("value").alias("humidity")
)
um003_df = df.filter(col("parameter") == "um003").select(
    col("datetimeLocal").alias("dt"), col("value").alias("um003")
)
corr_hum = hum_df.join(um003_df, "dt").select("humidity", "um003")
corr_val_hum = corr_hum.stat.corr("humidity", "um003")
print(f"Coeficiente de correlación de Pearson: {corr_val_hum:.4f}")
if abs(corr_val_hum) >= 0.7:
    print("Interpretación: Correlación fuerte")
elif abs(corr_val_hum) >= 0.5:
    print("Interpretación: Correlación moderada")
else:
    print("Interpretación: Correlación débil")

spark.stop()
