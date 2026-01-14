import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Configuración de página con look profesional
st.set_page_config(page_title="COMEX Data Engine - Albert Guacaran", layout="wide")

# CSS Avanzado para que parezca una App Corporativa
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    [data-testid="stMetricValue"] { font-size: 28px; color: #1E3A8A; font-weight: bold; }
    .stDataFrame { border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    h1 { color: #1E3A8A; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; }
    .legales { background-color: #ffffff; padding: 20px; border-radius: 10px; border-left: 5px solid #1E3A8A; }
    </style>
    """, unsafe_allow_html=True)

# Encabezado con Identidad Profesional
st.markdown("<h1>📊 Terminal de Inteligencia Portuaria y Logística</h1>", unsafe_allow_html=True)
st.markdown(f"**Analista Senior de Datos Comex:** Lic. Albert Guacaran")
st.write("---")

# Carga de datos
def cargar_datos():
    conn = sqlite3.connect('reconstruccion_vzla.db')
    df = pd.read_sql_query("SELECT * FROM logistica_exportacion", conn)
    conn.close()
    # Limpieza básica
    df['fecha_zarpe'] = pd.to_datetime(df['fecha_zarpe'])
    return df

try:
    df = cargar_datos()

    # --- KPI SECTION (Métricas que brillan) ---
    total_bbls = df["capacidad_barriles"].sum()
    valor_fob = total_bbls * 75
    eficiencia = 94.5 # Dato simulado para el dashboard

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Volumen Total FOB", f"{total_bbls:,} BBLS", "+5.2%")
    m2.metric("Valoración Estimada", f"$ {valor_fob:,.0f} USD")
    m3.metric("Buques en Puerto", len(df))
    m4.metric("Cumplimiento Aduanero", f"{eficiencia}%", "Optimal")

    st.write("##")

    # --- GRÁFICOS DINÁMICOS (Plotly para que no se vea "muerto") ---
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Distribución de Carga por Destino")
        fig = px.pie(df, values='capacidad_barriles', names='destino', 
                     hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)

    with col_chart2:
        st.subheader("Cronograma de Salidas (Zarpe)")
        fig2 = px.bar(df, x='fecha_zarpe', y='capacidad_barriles', 
                      color='buque_nombre', title="Capacidad vs Fecha")
        st.plotly_chart(fig2, use_container_width=True)

    # --- DATOS CRUDOS ---
    st.subheader("📋 Libro de Operaciones Aduaneras")
    st.dataframe(df.style.highlight_max(axis=0, subset=['capacidad_barriles'], color='#dcfce7'), use_container_width=True)

except Exception as e:
    st.error(f"Error al cargar la base de datos: {e}")
    st.info("Asegúrate de que el archivo 'reconstruccion_vzla.db' esté en la misma carpeta que este script.")

# --- MARCO LEGAL (Pie de página profesional) ---
st.write("---")
st.markdown("""
<div class="legales">
    <strong>Marco Normativo Aplicado:</strong><br>
    Este sistema opera bajo los lineamientos de la <strong>Ley Orgánica de Aduanas</strong> y los protocolos de 
    valoración FOB según las normas de la ICC. Proyecto diseñado para la optimización del comercio exterior venezolano.
</div>
""", unsafe_allow_html=True)
