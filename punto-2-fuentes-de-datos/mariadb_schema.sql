-- Esquema MariaDB para metadatos de estaciones y sensores
-- Base de datos: openaq_metadata

CREATE DATABASE IF NOT EXISTS openaq_metadata;
USE openaq_metadata;

CREATE TABLE IF NOT EXISTS stations (
    location_id       INT PRIMARY KEY,
    location_name     VARCHAR(255) NOT NULL,
    latitude          DECIMAL(10,6) NOT NULL,
    longitude         DECIMAL(10,6) NOT NULL,
    timezone          VARCHAR(64),
    country_iso       CHAR(2),
    owner_name        VARCHAR(255),
    provider          VARCHAR(64),
    is_mobile         BOOLEAN DEFAULT FALSE,
    is_monitor        BOOLEAN DEFAULT FALSE,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS measurements (
    id                BIGINT AUTO_INCREMENT PRIMARY KEY,
    location_id       INT NOT NULL,
    parameter         VARCHAR(32) NOT NULL,
    value             DECIMAL(10,2) NOT NULL,
    unit              VARCHAR(16),
    datetime_utc      DATETIME NOT NULL,
    datetime_local    DATETIME NOT NULL,
    ingested_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (location_id) REFERENCES stations(location_id)
);

CREATE INDEX idx_measurements_loc_param ON measurements(location_id, parameter);
CREATE INDEX idx_measurements_dt ON measurements(datetime_utc);

INSERT INTO stations (location_id, location_name, latitude, longitude, timezone, owner_name, provider)
VALUES (3163445, 'Colegio Bolivar', 3.340499, -76.545985, 'America/Bogota', 'Juan Carlos', 'AirGradient');
