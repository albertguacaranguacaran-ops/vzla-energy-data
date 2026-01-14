import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from PIL import Image

# 1. CONFIGURACIÓN Y FORZADO DE TEMA CLARO
st.set_page_config(page_title="Terminal Logística - Albert Guacaran", layout="wide")

# CSS para asegurar visibilidad total (Letras oscuras sobre fondo blanco)
st.markdown("""
    <style>
    /* Fondo de la aplicación */
    .stApp { background-color: #FFFFFF !important; }
    
    /* Forzar color de TODO el texto base a gris muy oscuro/negro */
    .stApp, .stMarkdown, p, span, label { color: #1F2937 !important; }
    
    /* Títulos principales en azul marino */
    h1, h2, h3 { color: #1E3A8A !important; font-family: 'Inter', sans-serif; }
    
    /* Métricas (Números grandes) */
    [data-testid="stMetricValue"] { color: #1E3A8A !important; font-weight: bold; font-size: 32px; }
    [data-testid="stMetricLabel"] { color: #4B5563 !important; font-size: 16px; }
    
    /* Estilo para la tabla de datos */
    .stDataFrame { border: 1px solid #E5E7EB; background-color: #FFFFFF; }
    
    /* Línea divisoria */
    hr { border: 0; border-top: 1px solid #E5E7EB; }
    </style>
    """, unsafe_allow_html=True)

# 2. CARGA DE LOGO (Asegúrate de que el nombre coincida con tu archivo en GitHub)
try:
    # Cambia 'nombre_de_tu_logo.png' por el nombre real que subiste
    logo = Image.open('logo.png') 
    st.image(logo, width=180)
except:
    st.info("💡 Para mostrar tu logo, súbelo a GitHub con el nombre 'logo.png'")

# 3. ENCABEZADO PROFESIONAL
st.title("🏛️ Terminal Virtual de Exportación de Hidrocarburos")
st.markdown(f"**Consultor Senior Responsable:** Lic. Albert Guacaran | *Comercio Exterior & Data Analytics*")
st.write("---")

# 4. FUNCIÓN DE DATOS
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
    # MÉTRICAS CON ALTO CONTRASTE
    m1, m2, m3 = st.columns(3)
    total_bbls = df["capacidad_barriles"].sum()
    valor_fob = total_bbls * 75
    
    m1.metric("Volumen Total (BBLS)", f"{total_bbls:,}")
    m2.metric("Valoración FOB Est. (USD)", f"$ {valor_fob:,.2f}")
    m3.metric("Estatus de Red", "OPERATIVO")

    st.write("##")

    # GRÁFICOS VISIBLES
    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(df, values='capacidad_barriles', names='destino', 
                     title="Distribución por Mercado Destino",
                     color_discrete_sequence=px.colors.qualitative.Prism)
        fig.update_layout(paper_bgcolor='white', font=dict(color="#1F2937"))
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        fig2 = px.bar(df, x='buque_nombre', y='capacidad_barriles', 
                      title="Capacidad por Buque",
                      color_discrete_sequence=['#1E3A8A'])
        fig2.update_layout(paper_bgcolor='white', plot_bgcolor='white', font=dict(color="#1F2937"))
        st.plotly_chart(fig2, use_container_width=True)

    # TABLA
    st.subheader("📋 Registro Maestro de Operaciones Aduaneras")
    st.dataframe(df, use_container_width=True)

else:
    st.error("No se pudo leer la base de datos. Verifica el archivo .db en GitHub.")

# PIE DE PÁGINA
st.write("---")
st.markdown("⚖️ *Operación bajo normativa de la Ley Orgánica de Aduanas de Venezuela.*")
st.caption(f"© 2026 Desarrollado por Albert Guacaran")
