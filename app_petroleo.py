import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from PIL import Image
import os

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS ---
st.set_page_config(page_title="Terminal Logística - Lic. Albert Guacaran", layout="wide")

# CSS para forzar Tema Claro (High Contrast)
st.markdown("""
    <style>
    /* Fondo Blanco Total */
    .stApp { background-color: #FFFFFF !important; }
    
    /* Títulos en Negro Puro */
    h1 { color: #000000 !important; font-family: 'Helvetica', sans-serif; font-weight: 900 !important; }
    h2, h3 { color: #111827 !important; font-weight: 700 !important; }
    
    /* Texto general en Negro */
    .stMarkdown, p, span, label, div { color: #000000 !important; font-weight: 500 !important; }
    
    /* Métricas (Números grandes en Azul Marino) */
    [data-testid="stMetricValue"] { color: #1E3A8A !important; font-weight: 800 !important; font-size: 38px !important; }
    [data-testid="stMetricLabel"] { color: #374151 !important; font-weight: bold !important; font-size: 18px !important; }
    
    /* Tablas y Sidebar */
    .stDataFrame { background-color: #FFFFFF !important; border: 1px solid #D1D5DB !important; }
    [data-testid="stSidebar"] { background-color: #F3F4F6 !important; border-right: 1px solid #E5E7EB; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTIÓN DE BASE DE DATOS (AUTO-GENERACIÓN PARA PRUEBAS) ---
DB_NAME = 'reconstruccion_vzla.db'

def inicializar_db_si_no_existe():
    """Crea una DB dummy si no existe para que el dashboard no de error al arrancar."""
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS logistica_exportacion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                buque_nombre TEXT,
                destino TEXT,
                capacidad_barriles INTEGER,
                fecha_salida TEXT,
                estatus TEXT
            )
        ''')
        # Datos semilla de prueba
        datos_prueba = [
            ('Buque Libertador', 'China', 2000000, '2026-01-15', 'En Tránsito'),
            ('Buque Jose Leonardo', 'India', 1500000, '2026-01-18', 'Cargando'),
            ('Buque Miranda', 'EE.UU', 1800000, '2026-01-20', 'Programado'),
            ('Buque Sucre', 'Brasil', 900000, '2026-01-22', 'En Mantenimiento'),
            ('Buque Urdaneta', 'China', 2100000, '2026-01-25', 'Programado')
        ]
        c.executemany('INSERT INTO logistica_exportacion (buque_nombre, destino, capacidad_barriles, fecha_salida, estatus) VALUES (?,?,?,?,?)', datos_prueba)
        conn.commit()
        conn.close()

# Ejecutamos la verificación de la DB al inicio
inicializar_db_si_no_existe()

# --- 3. CARGA DE DATOS (CON CACHÉ) ---
@st.cache_data(ttl=3600)
def cargar_datos():
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM logistica_exportacion", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return pd.DataFrame()

df_raw = cargar_datos()

# --- 4. ENCABEZADO ---
col_logo, col_titulo = st.columns([1, 5])

with col_logo:
    try:
        # Intenta cargar logo, si falla usa un icono
        img = Image.open('logo_de_albert.png')
        st.image(img, use_container_width=True)
    except:
        st.markdown("# ⚓") # Icono fallback

with col_titulo:
    st.title("Sistema de Inteligencia Portuaria")
    st.markdown("### Consultor Responsable Senior: Lic. Albert Guacaran")
    st.markdown("**Sector:** Comercio Exterior y Análisis de Datos | **Ciclo:** 2026")

st.write("---")

# --- 5. INTERFAZ PRINCIPAL ---
if not df_raw.empty:
    
    # --- BARRA LATERAL (FILTROS) ---
    st.sidebar.title("🛠️ Panel de Control")
    st.sidebar.markdown("Filtros operativos para análisis detallado.")
    
    # Filtro por Destino
    lista_destinos = ["Todos"] + list(df_raw['destino'].unique())
    filtro_destino = st.sidebar.selectbox("Seleccionar Destino:", lista_destinos)
    
    # Aplicar Filtro
    if filtro_destino != "Todos":
        df = df_raw[df_raw['destino'] == filtro_destino]
    else:
        df = df_raw

    # --- DASHBOARD DE MÉTRICAS (KPIs) ---
    m1, m2, m3, m4 = st.columns(4)
    
    total_bbls = df["capacidad_barriles"].sum()
    valor_fob = total_bbls * 75 # Precio estimado por barril
    n_buques = df["buque_nombre"].nunique()
    
    m1.metric("Volumen Total (BBLS)", f"{total_bbls:,.0f}")
    m2.metric("Valoración FOB (USD)", f"$ {valor_fob:,.0f}")
    m3.metric("Buques Activos", f"{n_buques}")
    m4.metric("Estado de Red", "OPERATIVO", delta="100%", delta_color="normal")

    st.write("##")

    # --- GRÁFICOS ---
    c1, c2 = st.columns(2)
    
    with c1:
        # Gráfico de Pastel mejorado
        fig = px.pie(df, values='capacidad_barriles', names='destino', 
                     title="Distribución Geográfica de Carga",
                     color_discrete_sequence=px.colors.qualitative.Bold,
                     hole=0.4) # Estilo Donut
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color="black", size=14))
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        # Gráfico de Barras ordenado
        df_sorted = df.sort_values(by="capacidad_barriles", ascending=True)
        fig2 = px.bar(df_sorted, x='capacidad_barriles', y='buque_nombre', 
                      title="Capacidad de Carga por Buque",
                      orientation='h', # Barras horizontales para mejor lectura de nombres
                      text_auto='.2s',
                      color_discrete_sequence=['#1E3A8A'])
        fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color="black", size=14))
        st.plotly_chart(fig2, use_container_width=True)

    # --- TABLA DE DATOS ---
    st.markdown("### 📋 Registro Maestro de Operaciones")
    st.dataframe(
        df, 
        use_container_width=True,
        hide_index=True,
        column_config={
            "capacidad_barriles": st.column_config.NumberColumn(
                "Capacidad (BBLS)",
                format="%d"
            ),
            "valor_fob": st.column_config.NumberColumn(
                "Valor Estimado ($)",
                format="$%d"
            )
        }
    )

else:
    st.error("⚠️ Error Crítico: No hay datos disponibles en el sistema.")

# --- PIE DE PÁGINA ---
st.write("---")
c_foot1, c_foot2 = st.columns([3,1])
with c_foot1:
    st.markdown("⚖️ *Reporte generado bajo los lineamientos de la Ley Orgánica de Aduanas.*")
    st.caption(f"© 2026 Desarrollado por Albert Guacaran para el sector energético.")
with c_foot2:
    st.caption("v.2.1.0 - Stable")
