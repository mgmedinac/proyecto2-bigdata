# Punto 2 - Fuentes de Datos

## RDS MariaDB

Base de datos relacional en AWS RDS para metadatos de estaciones y mediciones.

```sql
SOURCE mariadb_schema.sql;
```

Crea la base de datos `openaq_metadata` con las tablas `stations` y `measurements`.

## EC2 - Logs de Sensores

Script Python que simula la generación de logs de sensores en una instancia EC2:

```bash
python ec2_logs_generator.py --output /data/openaq/historical --hours 48
```

## URL - OpenAQ API

Los datos reales provienen de la API pública de OpenAQ: https://openaq.org

El dataset original usado en el proyecto está en `openaq_location_3163445_measurments.csv`.
