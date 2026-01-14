import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from PIL import Image

# 1. FORZAR TEMA CLARO Y CONFIGURACIÓN
st.set_page_config(page_title="Terminal Logística –lic. Albert Guacaran", layout="wide")

# CSS para matar el fondo negro y poner todo blanco/gris profesional
st.markdown("""
    <style>
    /* Forzar fondo blanco */
    .stApp { background-color: #FFFFFF; }
    /* Estilo para métricas */
    [data-testid="stMetricValue"] { color: #1E3A8A !important; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #4B5563 !important; }
    /* Estilo de tablas */
    .stDataFrame { border: 1px solid #E5E7EB; }
    /* Encabezado */
    h1 { color: #111827; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# 2. COLOCAR TU LOGO
try:
    # Cambia 'mi_logo.png' por el nombre real de tu archivo subido
    logo = Image.open('logo_de_albert.png') 
    st.image(logo, width=200)
except:
    st.warning("⚠️ Sube tu archivo 'mi_logo.png' a GitHub para verlo aquí.")

# 3. TÍTULO Y PRESENTACIÓN
st.title("🏛️ Sistema de Inteligencia Portuaria")
st.markdown(f"**Consultor Senior:** Lic. Albert Guacaran | *Comercio Exterior & Data Analytics*")
st.write("---")

# 4. CARGA DE DATOS
def cargar_datos():
    conn = sqlite3.connect('reconstruccion_vzla.db')
    df = pd.read_sql_query("SELECT * FROM logistica_exportacion", conn)
    conn.close()
    return df

try:
    df = cargar_datos()

    # MÉTRICAS PRINCIPALES
    m1, m2, m3 = st.columns(3)
    total_bbls = df["capacidad_barriles"].sum()
    valor_fob = total_bbls * 75
    
    m1.metric("Volumen Total Declarado", f"{total_bbls:,} BBLS")
    m2.metric("Valoración FOB (USD)", f"$ {valor_fob:,.2f}")
    m3.metric("Estatus Operativo", "ACTIVO", delta="Normal")

    st.write("##")

    # GRÁFICOS
    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(df, values='capacidad_barriles', names='destino', title="Cuota por Mercado")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.bar(df, x='buque_nombre', y='capacidad_barriles', title="Capacidad por Unidad", color_discrete_sequence=['#1E3A8A'])
        st.plotly_chart(fig2, use_container_width=True)

    # TABLA
    st.subheader("📋 Manifiestos de Carga y Aduana")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("Error en la conexión de datos.")

# PIE DE PÁGINA LEGAL
st.markdown("---")
st.caption("Desarrollado bajo normativa de la Ley Orgánica de Aduanas de Venezuela | © 2026 Albert Guacaran")
