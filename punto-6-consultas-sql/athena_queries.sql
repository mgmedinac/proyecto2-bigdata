-- =====================================================
--  Consultas Athena para las 5 preguntas de negocio
--  Base de datos: openaq_db
--  Tabla: trusted_measurements
-- =====================================================

-- 1. ¿Cuáles son las horas del día con mayor concentración de PM2.5?
SELECT
    HOUR(datetime_local) AS hora,
    ROUND(AVG(value), 1) AS pm25_promedio,
    MAX(value) AS pm25_maximo,
    MIN(value) AS pm25_minimo,
    COUNT(*) AS muestras
FROM openaq_db.trusted_measurements
WHERE parameter = 'pm25'
GROUP BY HOUR(datetime_local)
ORDER BY pm25_promedio DESC;

-- 2. ¿Existe correlación entre temperatura y niveles de PM2.5?
SELECT
    t.datetime_local,
    t.value AS temperatura,
    p.value AS pm25
FROM openaq_db.trusted_measurements t
JOIN openaq_db.trusted_measurements p
    ON t.datetime_local = p.datetime_local
    AND t.location_id = p.location_id
WHERE t.parameter = 'temperature'
  AND p.parameter = 'pm25'
ORDER BY t.datetime_local;

-- 3. ¿Los niveles de PM2.5 superan el límite OMS de 15 µg/m³?
SELECT
    COUNT(*) AS total_muestras,
    SUM(CASE WHEN value > 15 THEN 1 ELSE 0 END) AS superan_oms,
    ROUND(SUM(CASE WHEN value > 15 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS porcentaje_supera
FROM openaq_db.trusted_measurements
WHERE parameter = 'pm25';

-- 4. ¿Cómo varía la calidad del aire entre noche y día?
SELECT
    CASE
        WHEN HOUR(datetime_local) BETWEEN 6 AND 17 THEN 'DIA (06-17)'
        ELSE 'NOCHE (18-05)'
    END AS periodo,
    parameter,
    ROUND(AVG(value), 1) AS valor_promedio,
    MAX(value) AS maximo,
    MIN(value) AS minimo,
    COUNT(*) AS muestras
FROM openaq_db.trusted_measurements
WHERE parameter IN ('pm25', 'pm1')
GROUP BY
    CASE
        WHEN HOUR(datetime_local) BETWEEN 6 AND 17 THEN 'DIA (06-17)'
        ELSE 'NOCHE (18-05)'
    END,
    parameter
ORDER BY parameter, periodo;

-- 5. ¿Hay correlación entre humedad relativa y conteo de um003?
SELECT
    h.datetime_local,
    h.value AS humedad_relativa,
    u.value AS particulas_um003
FROM openaq_db.trusted_measurements h
JOIN openaq_db.trusted_measurements u
    ON h.datetime_local = u.datetime_local
    AND h.location_id = u.location_id
WHERE h.parameter = 'relative_humidity'
  AND u.parameter = 'um003'
ORDER BY h.datetime_local;
