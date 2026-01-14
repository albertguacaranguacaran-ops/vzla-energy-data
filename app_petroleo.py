import streamlit as st
import sqlite3
import pandas as pd

# Configuración con tema claro y profesional
st.set_page_config(page_title="Sistema de Gestión Comex - Albert Guacaran", layout="wide")

# Estilo CSS para forzar limpieza visual (Blanco y Gris Profesional)
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .stMetric { background-color: #F8F9FA; border: 1px solid #DEE2E6; padding: 15px; border-radius: 5px; }
    h1, h2, h3 { color: #212529; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# Encabezado Corporativo
st.title("🏛️ Terminal Virtual de Exportación de Hidrocarburos")
st.markdown(f"**Consultor Responsable:** Lic. Albert Guacaran | *Especialista en Comercio Internacional*")
st.write("---")

# Función de datos
def cargar_datos():
    conn = sqlite3.connect('reconstruccion_vzla.db')
    df = pd.read_sql_query("SELECT * FROM logistica_exportacion", conn)
    conn.close()
    return df

df = cargar_datos()

# --- MARCO LEGAL VENEZOLANO (El toque de nivel) ---
with st.expander("⚖️ Fundamentos Legales de la Operación"):
    st.write("""
    Esta plataforma integra los controles dispuestos en:
    * **Ley Orgánica de Aduanas:** Validación de manifiestos y potestad aduanera.
    * **Ley Orgánica de Hidrocarburos:** Control de volúmenes de extracción y exportación.
    * **Convenio Cambiario N° 1:** Registro de divisas por exportación no tradicional/petrolera.
    """)

# --- PANEL DE CONTROL ---
col1, col2, col3 = st.columns(3)
total_bbls = df["capacidad_barriles"].sum()
valor_usd = total_bbls * 75

with col1:
    st.metric("Volumen Total Declarado", f"{total_bbls:,} BBLS")
with col2:
    st.metric("Valor FOB Estimado", f"$ {valor_usd:,.2f}")
with col3:
    st.metric("Estatus de Buques", "Operativos")

# --- VISUALIZACIÓN ---
st.subheader("📊 Análisis de Tráfico Marítimo")
st.bar_chart(df.set_index("buque_nombre")["capacidad_barriles"])

# --- TABLA TÉCNICA ---
st.subheader("📋 Registro de Operaciones Aduaneras")
st.dataframe(df, use_container_width=True)

st.caption("© 2026 - Sistema Desarrollado por Albert Guacaran para la optimización del Comercio Exterior.")
