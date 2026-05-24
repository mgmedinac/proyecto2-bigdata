# Punto 8 - Visualización y API

## Streamlit Dashboard

Aplicación interactiva para visualizar los datos de calidad del aire.

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Visualizaciones
1. PM2.5 por hora del día (línea)
2. Correlación temperatura vs PM2.5 (dispersión + OLS)
3. Superación del límite OMS (pastel)
4. Comparación día vs noche (barras)
5. Correlación humedad vs um003 (dispersión + OLS)
6. Serie temporal completa (líneas múltiples)

## AWS Lambda + API Gateway

`lambda_function.py` expone los datos del datalake a través de una API REST.

### Despliegue
1. Crear función Lambda con `lambda_function.py`
2. Configurar API Gateway (REST API) con un endpoint GET
3. Parámetro opcional: `?parameter=pm25`

### Ejemplo
```
GET https://api-gateway-url/prod?parameter=pm25
```

## API Gateway

Endpoints:
- `GET /` - Devuelve datos del parámetro especificado
