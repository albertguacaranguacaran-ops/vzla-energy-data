import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from PIL import Image

# 1. FORZAR TEMA CLARO Y CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Terminal Logística - Albert Guacaran", layout="wide")

# 2. CSS PARA VISIBILIDAD TOTAL (Contraste Máximo)
st.markdown("""
    <style>
    /* Fondo Blanco Total */
    .stApp { background-color: #FFFFFF !important; }
    
    /* Títulos en Negro Puro para que sean visibles */
    h1 { color: #000000 !important; font-family: 'Helvetica', sans-serif; font-weight: 900 !important; }
    h2, h3 { color: #111827 !important; font-weight: 700 !important; }
    
    /* Texto de párrafos y etiquetas en Negro */
    .stMarkdown, p, span, label { color: #000000 !important; font-weight: 500 !important; }
    
    /* Métricas (Números grandes en Azul Marino) */
    [data-testid="stMetricValue"] { color: #1E3A8A !important; font-weight: 800 !important; font-size: 38px !important; }
    [data-testid="stMetricLabel"] { color: #374151 !important; font-weight: bold !important; font-size: 18px !important; }
    
    /* Ajuste para que la tabla no se vea negra si el navegador está en modo oscuro */
    .stDataFrame { background-color: #FFFFFF !important; border: 1px solid #D1D5DB !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. ENCABEZADO: LOGO Y TÍTULO
col_logo, col_titulo = st.columns([1, 4])

with col_logo:
    try:
        # Asegúrate de que el archivo se llame exactamente logo.png en GitHub
        img = Image.open('logo.png')
        st.image(img, use_container_width=True)
    except:
        st.write("📌 [Logo]")

with col_titulo:
    st.title("Sistema de Inteligencia Portuaria")
    st.markdown("### Consultor Responsable Senior: Lic. Albert Guacaran")
    st.write("Sector: Comercio Exterior y Análisis de Datos")

st.write("---")

# 4. CARGA DE DATOS
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
    # 5. DASHBOARD DE MÉTRICAS
    m1, m2, m3 = st.columns(3)
    total_bbls = df["capacidad_barriles"].sum()
    valor_fob = total_bbls * 75
    
    m1.metric("Volumen Total (BBLS)", f"{total_bbls:,}")
    m2.metric("Valoración FOB Est. (USD)", f"$ {valor_fob:,.2f}")
    m3.metric("Estado de Red", "OPERATIVO")

    st.write("##")

    # 6. GRÁFICOS CON COLORES PROFESIONALES
    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(df, values='capacidad_barriles', names='destino', 
                     title="Distribución Geográfica de Carga",
                     color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color="black", size=14))
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        fig2 = px.bar(df, x='buque_nombre', y='capacidad_barriles', 
                      title="Capacidad de Carga por Buque",
                      color_discrete_sequence=['#1E3A8A'])
        fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color="black", size=14))
        st.plotly_chart(fig2, use_container_width=True)

    # 7. TABLA DE DATOS
    st.markdown("### 📋 Registro Maestro de Operaciones")
    st.dataframe(df, use_container_width=True)

else:
    st.error("⚠️ Error: No se pudo conectar con la base de datos 'reconstruccion_vzla.db'.")

# PIE DE PÁGINA
st.write("---")
st.markdown("⚖️ *Reporte generado bajo los lineamientos de la Ley Orgánica de Aduanas.*")
st.caption(f"© 2026 Desarrollado por Albert Guacaran para el sector energético.")
