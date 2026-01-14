import streamlit as st
import sqlite3
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Vzla Energy Dashboard", layout="wide")

st.title("📊 Monitor de Logística y Exportación Petrolera")
st.markdown("### Reconstrucción Estratégica 2026 - Albert Guacaran")

# Conexión a la base de datos que creamos
def cargar_datos():
    conn = sqlite3.connect('reconstruccion_vzla.db')
    df = pd.read_sql_query("SELECT * FROM logistica_exportacion", conn)
    conn.close()
    return df

df_logistica = cargar_datos()

# --- BARRA LATERAL (Filtros de Comercio Internacional) ---
st.sidebar.header("Filtros de Operación")
destino_selected = st.sidebar.multiselect(
    "Seleccione Destino:",
    options=df_logistica["destino"].unique(),
    default=df_logistica["destino"].unique()
)

# Filtrar datos
df_filtrado = df_logistica[df_logistica["destino"].isin(destino_selected)]

# --- INDICADORES CLAVE (KPIs) ---
col1, col2, col3 = st.columns(3)
total_barriles = df_filtrado["capacidad_barriles"].sum()
valor_total = total_barriles * 75 # Precio WTI proyectado

col1.metric("Total Barriles a Exportar", f"{total_barriles:,} bbls")
col2.metric("Valor Estimado de Carga", f"$ {valor_total:,.2f}")
col3.metric("Buques en Operación", len(df_filtrado))

# --- GRÁFICOS ---
st.write("---")
st.subheader("Distribución de Carga por Buque y Destino")
st.bar_chart(df_filtrado.set_index("buque_nombre")["capacidad_barriles"])

# --- TABLA DE DATOS INTERACTIVA ---
st.subheader("Detalle de Logística de Aduana")
st.dataframe(df_filtrado, use_container_width=True)

st.info("Este dashboard automatiza la lectura de la base de datos SQLite y proyecta flujos de caja basados en capacidad de transporte.")