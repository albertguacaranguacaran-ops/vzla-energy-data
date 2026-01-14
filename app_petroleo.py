import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from PIL import Image

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Terminal Logística - Albert Guacaran", layout="wide")

# 2. EL "SUPER CSS" PARA ARREGLAR VISIBILIDAD (Fondo blanco, Letras Negras)
st.markdown("""
    <style>
    /* Forzar fondo blanco en toda la app */
    .stApp { background-color: #FFFFFF !important; }
    
    /* Forzar que TODO el texto sea NEGRO profundo */
    .stApp, .stMarkdown, p, span, label, .stMetric, div { color: #000000 !important; }
    
    /* Forzar títulos a azul marino muy oscuro */
    h1, h2, h3, h4 { color: #001f3f !important; font-family: 'Arial', sans-serif; font-weight: bold; }
    
    /* Estilo para las métricas (Números grandes) */
    [data-testid="stMetricValue"] { color: #000000 !important; font-weight: 800 !important; font-size: 35px !important; }
    [data-testid="stMetricLabel"] { color: #333333 !important; font-weight: bold !important; }
    
    /* Quitar el fondo negro de los gráficos de Plotly que se ve en tu imagen */
    .js-plotly-plot .plotly .main-svg { background: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. CARGA DE LOGO
try:
    # Asegúrate de que el nombre coincida con tu archivo subido a GitHub
    logo = Image.open('logo.png') 
    st.image(logo, width=200)
except:
    st.info("💡 Sube tu logo como 'logo.png' en GitHub para que aparezca aquí.")

# 4. TÍTULOS VISIBLES
st.title("🏛️ Sistema de Inteligencia Portuaria")
st.markdown(f"**Consultor Senior Responsable:** Lic. Albert Guacaran | *Comercio Exterior & Data Analytics*")
st.write("---")

# 5. CARGA DE DATOS
def cargar_datos():
    try:
        conn = sqlite3.connect('reconstruccion_vzla.db')
        df = pd.read_sql_query("SELECT * FROM logistica_exportacion", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

df = cargar_datos()

if not df.empty:
    # MÉTRICAS
    m1, m2, m3 = st.columns(3)
    total_bbls = df["capacidad_barriles"].sum()
    valor_fob = total_bbls * 75
    
    m1.metric("Volumen Total (BBLS)", f"{total_bbls:,}")
    m2.metric("Valoración FOB Est. (USD)", f"$ {valor_fob:,.2f}")
    m3.metric("Estatus de Red", "OPERATIVO")

    st.write("##")

    # GRÁFICOS (Forzando tema claro en los gráficos)
    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(df, values='capacidad_barriles', names='destino', title="Distribución por Mercado")
        fig.update_layout(template="plotly_white", paper_bgcolor='rgba(0,0,0,0)', font=dict(color="black"))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.bar(df, x='buque_nombre', y='capacidad_barriles', title="Capacidad por Buque")
        fig2.update_layout(template="plotly_white", paper_bgcolor='rgba(0,0,0,0)', font=dict(color="black"))
        st.plotly_chart(fig2, use_container_width=True)

    # TABLA
    st.subheader("📋 Registro Maestro de Operaciones")
    st.dataframe(df, use_container_width=True)

else:
    st.error("Error: No se encontró la base de datos 'reconstruccion_vzla.db'.")

st.write("---")
st.caption("© 2026 Desarrollado por Albert Guacaran | Cumplimiento Ley Orgánica de Aduanas")
