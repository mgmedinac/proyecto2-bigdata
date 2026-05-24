# Punto 1 - Caso de Estudio

## Problema

Monitoreo de calidad del aire usando datos del sensor AirGradient ubicado en el Colegio Bolívar, Cali, Colombia. Los datos provienen de la plataforma OpenAQ y contienen mediciones horarias de partículas (PM1, PM2.5, um003), temperatura y humedad relativa.

## Dataset

- **Fuente:** OpenAQ API pública
- **Estación:** Colegio Bolívar, Cali, Colombia (`location_id: 3163445`)
- **Sensor:** AirGradient — Propietario: Juan Carlos
- **Ubicación:** lat 3.3404, lon -76.5459 — Timezone: America/Bogota
- **Parámetros:** pm1, pm25, relativehumidity, temperature, um003
- **Registros:** 104 mediciones horarias (≈21 por parámetro)

## Preguntas de Negocio

1. **¿Cuáles son las horas del día con mayor concentración de PM2.5?**
   - Permite identificar patrones horarios de contaminación para tomar medidas preventivas.

2. **¿Existe correlación entre temperatura y niveles de PM2.5?**
   - Determina si condiciones térmicas influyen en la concentración de partículas.

3. **¿Los niveles de PM2.5 superan el límite OMS de 15 µg/m³?**
   - Evalúa el cumplimiento de la guía de calidad del aire de la Organización Mundial de la Salud.

4. **¿Cómo varía la calidad del aire entre día y noche?**
   - Compara los niveles de contaminación en periodos diurnos (06-17) vs nocturnos (18-05).

5. **¿Hay correlación entre humedad relativa y conteo de partículas um003?**
   - Explora la relación entre humedad ambiental y partículas ultrafinas.
