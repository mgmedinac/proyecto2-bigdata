.mode csv
.import openaq_location_3163445_measurments.csv measurements_raw

-- Create cleaned view (no header row in data)
CREATE TABLE measurements AS
SELECT location_id, location_name, parameter,
       CAST(value AS REAL) AS value, unit,
       datetimeUtc, datetimeLocal, timezone,
       CAST(latitude AS REAL) AS latitude,
       CAST(longitude AS REAL) AS longitude,
       owner_name, provider
FROM measurements_raw
WHERE location_id != 'location_id';

-- 1. Horas con mayor PM2.5
.print '========================================'
.print '1. HORAS CON MAYOR CONCENTRACIÓN PM2.5'
.print '========================================'
SELECT HOUR(datetimeLocal) AS hora,
       ROUND(AVG(value), 1) AS pm25_promedio,
       ROUND(MAX(value), 1) AS pm25_maximo,
       ROUND(MIN(value), 1) AS pm25_minimo,
       COUNT(*) AS muestras
FROM measurements
WHERE parameter = 'pm25'
GROUP BY hora
ORDER BY pm25_promedio DESC;

-- 2. Correlación temperatura vs PM2.5
.print ''
.print '========================================'
.print '2. TEMPERATURA vs PM2.5'
.print '========================================'
SELECT t.datetimeLocal,
       ROUND(t.value, 1) AS temperatura,
       ROUND(p.value, 1) AS pm25
FROM measurements t
JOIN measurements p ON t.datetimeLocal = p.datetimeLocal
WHERE t.parameter = 'temperature'
  AND p.parameter = 'pm25'
ORDER BY t.datetimeLocal;

-- 3. Superación límite OMS
.print ''
.print '========================================'
.print '3. SUPERACIÓN LÍMITE OMS (15 µg/m³)'
.print '========================================'
SELECT COUNT(*) AS total_muestras,
       SUM(CASE WHEN CAST(value AS REAL) > 15 THEN 1 ELSE 0 END) AS superan_oms,
       ROUND(SUM(CASE WHEN CAST(value AS REAL) > 15 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS porcentaje_supera
FROM measurements
WHERE parameter = 'pm25';

-- 4. Día vs Noche
.print ''
.print '========================================'
.print '4. DÍA vs NOCHE - PM2.5 y PM1'
.print '========================================'
SELECT
    CASE WHEN CAST(STRFTIME('%H', datetimeLocal) AS INTEGER) BETWEEN 6 AND 17 THEN 'DIA (06-17)'
         ELSE 'NOCHE (18-05)'
    END AS periodo,
    parameter,
    ROUND(AVG(CAST(value AS REAL)), 1) AS valor_promedio,
    ROUND(MAX(CAST(value AS REAL)), 1) AS maximo,
    ROUND(MIN(CAST(value AS REAL)), 1) AS minimo,
    COUNT(*) AS muestras
FROM measurements
WHERE parameter IN ('pm25', 'pm1')
GROUP BY periodo, parameter
ORDER BY parameter, periodo;

-- 5. Humedad vs um003
.print ''
.print '========================================'
.print '5. HUMEDAD RELATIVA vs um003'
.print '========================================'
SELECT h.datetimeLocal,
       ROUND(h.value, 1) AS humedad_relativa,
       ROUND(u.value, 0) AS particulas_um003
FROM measurements h
JOIN measurements u ON h.datetimeLocal = u.datetimeLocal
WHERE h.parameter = 'relativehumidity'
  AND u.parameter = 'um003'
ORDER BY h.datetimeLocal;
