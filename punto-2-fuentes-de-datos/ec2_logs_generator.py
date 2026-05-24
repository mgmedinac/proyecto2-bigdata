import csv
import os
import random
from datetime import datetime, timedelta

LOCAL_DIR = "/data/openaq/historical"
PARAMETERS = {
    "pm25": {"unit": "µg/m³", "min": 5, "max": 50},
    "pm1": {"unit": "µg/m³", "min": 1, "max": 20},
    "temperature": {"unit": "°C", "min": 18, "max": 35},
    "relativehumidity": {"unit": "%", "min": 40, "max": 90},
    "um003": {"unit": "part/cm³", "min": 100, "max": 2000},
}

def generate_reading(base_time: datetime, location_id: int) -> dict:
    for param, spec in PARAMETERS.items():
        value = round(random.uniform(spec["min"], spec["max"]), 1)
        yield {
            "location_id": location_id,
            "location_name": "Colegio Bolivar",
            "parameter": param,
            "value": value,
            "unit": spec["unit"],
            "datetimeUtc": base_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "datetimeLocal": base_time.strftime("%Y-%m-%dT%H:%M:%S-05:00"),
            "timezone": "America/Bogota",
            "latitude": 3.340499,
            "longitude": -76.545985,
            "owner_name": "Juan Carlos",
            "provider": "AirGradient",
        }

def generate_csv(output_dir: str, hours: int = 48):
    os.makedirs(output_dir, exist_ok=True)
    now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    fieldnames = [
        "location_id", "location_name", "parameter", "value", "unit",
        "datetimeUtc", "datetimeLocal", "timezone",
        "latitude", "longitude", "owner_name", "provider",
    ]
    filename = f"openaq_simulated_{now.strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for h in range(hours):
            ts = now - timedelta(hours=h)
            for reading in generate_reading(ts, location_id=3163445):
                writer.writerow(reading)
    print(f"CSV generado: {filepath} ({hours * len(PARAMETERS)} registros)")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Genera logs simulados de sensores OpenAQ")
    parser.add_argument("--output", default=LOCAL_DIR)
    parser.add_argument("--hours", type=int, default=48)
    args = parser.parse_args()
    generate_csv(args.output, args.hours)
