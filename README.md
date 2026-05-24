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
├── README.md                                # Guía general de arquitectura
├── .gitignore                               # Configurado (sin .DS_Store)
├── punto-1-caso-de-estudio/                 # Definición del problema y preguntas de negocio
├── punto-2-fuentes-de-datos/                # RDS MariaDB, EC2, URL (dataset)
├── punto-3-ingesta-datalake/                # Ingesta automática a S3 (raw/trusted/refined)
├── punto-4-procesamiento-spark-glue/        # Glue ETL + Spark (raw → trusted)
├── punto-5-catalogacion-glue-hive/          # Glue Crawler + Hive catalogación
├── punto-6-consultas-sql/                   # Athena + Hive + SparkSQL queries
├── punto-7-analisis-pyspark/               # Análisis descriptivo con PySpark
└── punto-8-visualizacion-api/              # Streamlit dashboard + Lambda API
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
cd punto-3-ingesta-datalake
chmod +x ingest.sh
./ingest.sh openaq-datalake

pip install boto3
python ingest_all_sources.py ../punto-2-fuentes-de-datos/openaq_location_3163445_measurments.csv
```

### 2. Base de Datos (RDS MariaDB)

```sql
SOURCE punto-2-fuentes-de-datos/mariadb_schema.sql;
```

### 3. ETL con Glue

Subir `punto-4-procesamiento-spark-glue/pyspark_process.py` a AWS Glue Jobs y ejecutar.

### 4. Consultas Athena

Ejecutar las queries en `punto-6-consultas-sql/athena_queries.sql` desde la consola Athena.

### 5. Dashboard Streamlit

```bash
cd punto-8-visualizacion-api
pip install -r requirements.txt
streamlit run streamlit_app.py
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
