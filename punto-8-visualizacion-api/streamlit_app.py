import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="OpenAQ - Calidad del Aire", layout="wide")
st.title("🌬️ Monitoreo de Calidad del Aire - Colegio Bolívar, Cali")
st.markdown("**Fuente:** OpenAQ | **Sensor:** AirGradient | **Propietario:** Juan Carlos")

DATA_PATH = "openaq_location_3163445_measurments.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["datetimeUtc", "datetimeLocal"])
    df["hour"] = df["datetimeLocal"].dt.hour
    df["period"] = df["hour"].apply(lambda h: "DÍA (6-17)" if 6 <= h <= 17 else "NOCHE (18-5)")
    return df

df = load_data()

pm25 = df[df["parameter"] == "pm25"].copy()
pm1 = df[df["parameter"] == "pm1"].copy()
temp = df[df["parameter"] == "temperature"].copy()
hum = df[df["parameter"] == "relativehumidity"].copy()
um003 = df[df["parameter"] == "um003"].copy()

# --- MÉTRICAS CLAVE ---
avg_pm25 = pm25["value"].mean()
max_pm25 = pm25["value"].max()
pct_exceed = (pm25["value"] > 15).mean() * 100
avg_temp = temp["value"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("PM2.5 Promedio", f"{avg_pm25:.1f} µg/m³", delta=None)
col2.metric("PM2.5 Máximo", f"{max_pm25:.1f} µg/m³")
col3.metric("Supera OMS 15 µg/m³", f"{pct_exceed:.1f}%")
col4.metric("Temp. Promedio", f"{avg_temp:.1f} °C")

# --- 1. PM2.5 por hora ---
st.subheader("1. Concentración de PM2.5 por Hora del Día")
hourly = pm25.groupby("hour")["value"].agg(["mean", "max", "min"]).reset_index()
fig1 = px.line(hourly, x="hour", y="mean", error_y=None, markers=True,
               labels={"hour": "Hora del día", "mean": "PM2.5 promedio (µg/m³)"})
fig1.add_scatter(x=hourly["hour"], y=hourly["max"], mode="lines+markers",
                 name="Máximo", line=dict(dash="dash"))
fig1.add_scatter(x=hourly["hour"], y=hourly["min"], mode="lines+markers",
                 name="Mínimo", line=dict(dash="dot"))
fig1.add_hline(y=15, line_dash="dash", line_color="red", annotation_text="Límite OMS")
st.plotly_chart(fig1, width='stretch')

# --- 2. Temperatura vs PM2.5 ---
st.subheader("2. Correlación: Temperatura vs PM2.5")
merged = temp[["datetimeLocal", "value"]].rename(columns={"value": "temperature"})
merged = merged.merge(pm25[["datetimeLocal", "value"]].rename(columns={"value": "pm25"}), on="datetimeLocal")
fig2 = px.scatter(merged, x="temperature", y="pm25", trendline="ols",
                  labels={"temperature": "Temperatura (°C)", "pm25": "PM2.5 (µg/m³)"})
st.plotly_chart(fig2, width='stretch')

# --- 3. Límite OMS ---
st.subheader("3. Superación del Límite OMS (15 µg/m³)")
oms_counts = pm25["value"].apply(lambda v: "Supera OMS" if v > 15 else "Dentro del límite").value_counts()
fig3 = px.pie(values=oms_counts.values, names=oms_counts.index,
              color_discrete_sequence=["#ef553b", "#00cc96"])
st.plotly_chart(fig3, width='stretch')

# --- 4. Día vs Noche ---
st.subheader("4. Calidad del Aire: Día vs Noche")
day_night = pm25.groupby("period")["value"].agg(["mean", "max", "min"]).reset_index()
fig4 = px.bar(day_night, x="period", y="mean", error_y=None,
              labels={"period": "", "mean": "PM2.5 (µg/m³)"},
              color="period", text_auto=".1f")
fig4.add_hline(y=15, line_dash="dash", line_color="red", annotation_text="Límite OMS")
st.plotly_chart(fig4, width='stretch')

# --- 5. Humedad vs um003 ---
st.subheader("5. Correlación: Humedad Relativa vs Partículas um003")
merged_h = hum[["datetimeLocal", "value"]].rename(columns={"value": "humidity"})
merged_h = merged_h.merge(um003[["datetimeLocal", "value"]].rename(columns={"value": "um003"}), on="datetimeLocal")
fig5 = px.scatter(merged_h, x="humidity", y="um003", trendline="ols",
                  labels={"humidity": "Humedad Relativa (%)", "um003": "Partículas um003 (part/cm³)"})
st.plotly_chart(fig5, width='stretch')

# --- Serie temporal completa ---
st.subheader("Serie Temporal Completa")
all_params = df[df["parameter"].isin(["pm25", "pm1", "temperature"])]
fig6 = px.line(all_params, x="datetimeLocal", y="value", color="parameter", markers=True,
               labels={"datetimeLocal": "Fecha/Hora", "value": "Valor"})
st.plotly_chart(fig6, width='stretch')

st.caption(f"Datos actualizados: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
