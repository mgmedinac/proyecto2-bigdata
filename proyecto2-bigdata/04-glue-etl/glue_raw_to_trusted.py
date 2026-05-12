import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, to_timestamp, when, regexp_replace, round

glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session
job = Job(glueContext)
args = getResolvedOptions(sys.argv, ["JOB_NAME"])
job.init(args["JOB_NAME"], args)

# --- Leer desde S3 raw/ ---
raw_df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={
        "paths": ["s3://openaq-datalake/raw/openaq/csv/"],
        "recurse": True,
    },
    format="csv",
    format_options={
        "withHeader": True,
        "separator": ",",
        "quoteChar": '"',
    },
).toDF()

# --- Limpieza ---
cleaned = (
    raw_df
    .withColumn("location_id", col("location_id").cast("int"))
    .withColumn("value", col("value").cast("double"))
    .withColumn("latitude", col("latitude").cast("double"))
    .withColumn("longitude", col("longitude").cast("double"))
    .withColumn("datetime_utc", to_timestamp(regexp_replace(col("datetimeUtc"), "Z$", ""), "yyyy-MM-dd'T'HH:mm:ss"))
    .withColumn("datetime_local", to_timestamp(col("datetimeLocal"), "yyyy-MM-dd'T'HH:mm:ssXXX"))
    .withColumn("parameter", when(col("parameter") == "pm25", "pm25")
                           .when(col("parameter") == "pm1", "pm1")
                           .when(col("parameter") == "temperature", "temperature")
                           .when(col("parameter") == "relativehumidity", "relative_humidity")
                           .when(col("parameter") == "um003", "um003")
                           .otherwise(col("parameter")))
    .drop("datetimeUtc", "datetimeLocal", "country_iso", "isMobile", "isMonitor")
)

cleaned = cleaned.withColumn("value", round(col("value"), 1))

# --- Escribir a S3 trusted/ en Parquet ---
trusted_path = "s3://openaq-datalake/trusted/openaq/"
cleaned.write.mode("overwrite").partitionBy("parameter").parquet(trusted_path)

job.commit()
print(f"ETL completado. {cleaned.count()} registros escritos en {trusted_path}")
