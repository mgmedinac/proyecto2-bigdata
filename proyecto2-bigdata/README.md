# Proyecto 2 - Big Data (ST0263) | Universidad EAFIT

**Monitoreo de Calidad del Aire con OpenAQ en AWS**

---

## Dataset

- **Fuente:** [OpenAQ](https://openaq.org) - API pública
- **Estación:** Colegio Bolívar, Cali, Colombia (`location_id: 3163445`)
- **Sensor:** AirGradient — Propietario: **Juan Carlos**
- **Coordenadas:** `lat 3.3404, lon -76.5459` — Timezone: `America/Bogota`
- **Parámetros:** `pm1`, `pm25`, `relativehumidity`, `temperature`, `um003`
- **Registros:** 104 mediciones horarias (21 por parámetro)

## Preguntas de Negocio

1. ¿Cuáles son las horas del día con mayor concentración de PM2.5?
2. ¿Existe correlación entre temperatura y niveles de PM2.5?
3. ¿Los niveles de PM2.5 superan el límite OMS (15 µg/m³)?
4. ¿Cómo varía la calidad del aire entre día y noche?
5. ¿Hay correlación entre humedad relativa y conteo de partículas um003?

## Arquitectura AWS

```
┌──────────────┐     ┌────────────────┐     ┌─────────────────┐
│   EC2        │────▶│   S3 Datalake  │────▶│   Glue / Spark  │
│ CSVs hist.   │     │ raw/trusted/   │     │ raw → trusted   │
└──────────────┘     └────────────────┘     └─────────────────┘
                           │                        │
                           ▼                        ▼
                    ┌──────────────┐     ┌─────────────────┐
                    │   RDS        │     │ Glue Crawler    │
                    │   MariaDB    │     │ + EMR / Hive    │
                    │   metadatos  │     │ Data Catalog    │
                    └──────────────┘     └─────────────────┘
                           │                        │
                           ▼                        ▼
                    ┌──────────────┐     ┌─────────────────┐
                    │   Athena     │     │   PySpark       │
                    │   SQL anal.  │     │ análisis desc.  │
                    └──────────────┘     └─────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Streamlit   │
                    │  + API GW    │
                    │  visualiz.   │
                    └──────────────┘
```

## Estructura del Repositorio

```
proyecto2-bigdata/
├── 01-s3-datalake/        # Ingesta a S3 (raw/) + setup buckets
├── 02-rds-database/       # Esquema MariaDB (metadata)
├── 03-ec2-storage/        # Configuración EC2 (CSVs históricos)
├── 04-glue-etl/           # Glue ETL: raw → trusted (Parquet)
├── 05-glue-crawler-emr/   # Glue Crawler + Hive catalog
├── 06-athena-analytics/   # Queries Athena (5 preguntas negocio)
├── 07-pyspark-analytics/  # Análisis descriptivo con PySpark
├── 08-streamlit-app/      # Dashboard Streamlit + API Gateway
├── openaq_location_3163445_measurments.csv   # Dataset original
└── README.md              # Este archivo
```

## Stack Tecnológico

| Componente         | Servicio AWS     | Propósito                         |
|--------------------|------------------|-----------------------------------|
| Almacenamiento     | S3               | Datalake por zonas (raw/trusted/refined) |
| Base de datos      | RDS MariaDB      | Metadatos de estaciones/sensores  |
| Cómputo            | EC2              | Almacenamiento CSVs históricos    |
| ETL                | AWS Glue + Spark | Limpieza y transformación         |
| Catalogación       | Glue Crawler     | Catálogo de datos                 |
| Consultas          | Athena           | SQL analítico sobre S3            |
| Procesamiento      | EMR + Hive/PySpark | Análisis descriptivo           |
| Visualización      | Streamlit        | Dashboard interactivo             |

## Instrucciones de Despliegue

### 1. Ingesta a S3

```bash
cd 01-s3-datalake
chmod +x s3_setup.sh
./s3_setup.sh openaq-datalake

pip install boto3
python ingest_to_s3_raw.py ../openaq_location_3163445_measurments.csv
```

### 2. Base de Datos (RDS MariaDB)

```sql
SOURCE 02-rds-database/schema.sql;
```

### 3. ETL con Glue

Subir `04-glue-etl/glue_raw_to_trusted.py` a AWS Glue Jobs y ejecutar.

### 4. Consultas Athena

Ejecutar las queries en `06-athena-analytics/queries_business.sql` desde la consola Athena.

### 5. Dashboard Streamlit

```bash
cd 08-streamlit-app
pip install -r requirements.txt
streamlit run app.py
```

## Resultados Esperados

- Identificación de horas pico de contaminación por PM2.5
- Correlaciones entre variables ambientales (temp, humedad, partículas)
- Porcentaje de tiempo que se supera la norma OMS
- Comparación día/noche de calidad del aire
- Dashboard interactivo con visualizaciones

---

**Curso:** ST0263 - Tópicos en Telemática II (Big Data)
**Universidad:** EAFIT, Medellín
**Año:** 2026
