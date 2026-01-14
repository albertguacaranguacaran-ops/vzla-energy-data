import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from PIL import Image
import os
from fpdf import FPDF
import base64
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS ---
st.set_page_config(page_title="Terminal Logística - Albert Guacaran", layout="wide")

# CSS para forzar Tema Claro (High Contrast) y mantener tu diseño responsivo
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
    
    /* Botones */
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        border-radius: 5px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTIÓN DE BASE DE DATOS (AUTO-GENERACIÓN) ---
DB_NAME = 'reconstruccion_vzla.db'
LOGO_FILENAME = 'logo_de_albert.png'

def inicializar_db_si_no_existe():
    """Crea una DB dummy si no existe para portabilidad del portafolio."""
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
            ('Orinoco Spirit', 'China', 2000000, '2026-01-15', 'En Tránsito'),
            ('Oil Star', 'India', 1500000, '2026-01-18', 'Cargando'),
            ('Caribbean Queen', 'EE.UU', 1800000, '2026-01-20', 'Programado'),
            ('MV Liberty', 'Brasil', 900000, '2026-01-22', 'En Mantenimiento'),
            ('Atlantic Voyager', 'Rotterdam', 2100000, '2026-01-25', 'Programado')
        ]
        c.executemany('INSERT INTO logistica_exportacion (buque_nombre, destino, capacidad_barriles, fecha_salida, estatus) VALUES (?,?,?,?,?)', datos_prueba)
        conn.commit()
        conn.close()

inicializar_db_si_no_existe()

# --- 3. CARGA DE DATOS ---
@st.cache_data(ttl=3600)
def cargar_datos():
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM logistica_exportacion", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error de conexión con DB: {e}")
        return pd.DataFrame()

df_raw = cargar_datos()

# --- 4. FUNCIÓN PARA GENERAR PDF ---
class PDF(FPDF):
    def header(self):
        # Logo
        if os.path.exists(LOGO_FILENAME):
            self.image(LOGO_FILENAME, 10, 8, 33)
        self.set_font('Arial', 'B', 15)
        # Mover a la derecha
        self.cell(80)
        # Título
        self.cell(30, 10, 'Reporte de Operaciones Portuarias', 0, 0, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()} - Gen. por Albert Guacaran System', 0, 0, 'C')

def generar_pdf_bytes(df_export):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Información General
    pdf.cell(200, 10, txt=f"Fecha de Emisión: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align='L')
    pdf.cell(200, 10, txt="Departamento: Logística y Comercio Exterior", ln=True, align='L')
    pdf.ln(10)
    
    # Encabezados de Tabla
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(40, 10, "Buque", 1)
    pdf.cell(30, 10, "Destino", 1)
    pdf.cell(40, 10, "Capacidad (BBLS)", 1)
    pdf.cell(35, 10, "Fecha Salida", 1)
    pdf.cell(35, 10, "Estatus", 1)
    pdf.ln()
    
    # Datos de Tabla
    pdf.set_font("Arial", size=10)
    for index, row in df_export.iterrows():
        pdf.cell(40, 10, str(row['buque_nombre']), 1)
        pdf.cell(30, 10, str(row['destino']), 1)
        pdf.cell(40, 10, f"{row['capacidad_barriles']:,}", 1)
        pdf.cell(35, 10, str(row['fecha_salida']), 1)
        pdf.cell(35, 10, str(row['estatus']), 1)
        pdf.ln()
        
    return pdf.output(dest='S').encode('latin-1')

# --- 5. ENCABEZADO ---
col_logo, col_titulo = st.columns([1, 5])

with col_logo:
    try:
        # AQUÍ CARGA TU LOGO PERSONAL
        img = Image.open(LOGO_FILENAME)
        st.image(img, use_container_width=True)
    except:
        st.markdown("# ⚓")
        st.caption("Falta logo_de_albert.png")

with col_titulo:
    st.title("Sistema de Inteligencia Portuaria")
    st.markdown("### Dashboard Ejecutivo de Logística y Exportación")
    st.markdown("**Desarrollado por:** Lic. Albert Guacaran | **Tecnología:** Python + SQL + Streamlit")

st.write("---")

# --- 6. INTERFAZ PRINCIPAL ---
if not df_raw.empty:
    
    # --- SIDEBAR & FILTROS ---
    st.sidebar.title("🛠️ Panel de Control")
    st.sidebar.subheader("Filtros Operativos")
    lista_destinos = ["Todos"] + list(df_raw['destino'].unique())
    filtro_destino = st.sidebar.selectbox("Seleccionar Destino:", lista_destinos)
    
    if filtro_destino != "Todos":
        df = df_raw[df_raw['destino'] == filtro_destino]
    else:
        df = df_raw
        
    # Perfil Autor
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👨‍💻 Sobre el Autor")
    st.sidebar.info(
        """
        **Albert Guacaran**
        
        *Licenciado en Comercio Internacional & Data Developer.*
        
        Experto en visualización de datos logísticos y desarrollo de soluciones BI.
        """
    )

    # --- MÉTRICAS KPI ---
    m1, m2, m3, m4 = st.columns(4)
    total_bbls = df["capacidad_barriles"].sum()
    valor_fob = total_bbls * 75 
    n_buques = df["buque_nombre"].nunique()
    
    m1.metric("Volumen Total (BBLS)", f"{total_bbls:,.0f}")
    m2.metric("Valoración FOB (USD)", f"$ {valor_fob:,.0f}")
    m3.metric("Buques Activos", f"{n_buques}")
    m4.metric("Estado de Red", "OPERATIVO", delta="100%")

    st.write("##")

    # --- GRÁFICOS (NEGRO PURO PARA LEGIBILIDAD) ---
    c1, c2 = st.columns(2)
    
    with c1:
        fig = px.pie(df, values='capacidad_barriles', names='destino', 
                     title="Distribución Geográfica de Carga",
                     color_discrete_sequence=px.colors.qualitative.Bold, hole=0.4)
        fig.update_layout(
            plot_bgcolor='white', paper_bgcolor='white', 
            font_color="black", title_font_color="black",
            legend=dict(font=dict(color="black"))
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        df_sorted = df.sort_values(by="capacidad_barriles", ascending=True)
        fig2 = px.bar(df_sorted, x='capacidad_barriles', y='buque_nombre', 
                      title="Capacidad de Carga por Buque",
                      orientation='h', text_auto='.2s',
                      color_discrete_sequence=['#1E3A8A'])
        fig2.update_layout(
            plot_bgcolor='white', paper_bgcolor='white', 
            font_color="black", title_font_color="black",
            xaxis=dict(title_font=dict(color="black"), tickfont=dict(color="black"), showgrid=True, gridcolor='#E5E7EB'),
            yaxis=dict(title_font=dict(color="black"), tickfont=dict(color="black"))
        )
        st.plotly_chart(fig2, use_container_width=True)

    # --- TABLA Y EXPORTACIÓN ---
    st.markdown("### 📋 Registro Maestro de Operaciones")
    
    col_tabla, col_descarga = st.columns([4, 1])
    
    with col_tabla:
        st.dataframe(
            df, 
            use_container_width=True,
            hide_index=True,
            column_config={
                "capacidad_barriles": st.column_config.NumberColumn("Capacidad (BBLS)", format="%d"),
            }
        )

    with col_descarga:
        st.write("##") # Espacio para alinear
        # BOTÓN DE DESCARGA PDF
        try:
            pdf_bytes = generar_pdf_bytes(df)
            st.download_button(
                label="📄 Descargar PDF",
                data=pdf_bytes,
                file_name="Reporte_Logistica_AlbertGuacaran.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.warning("Instala 'fpdf' para habilitar PDF.")

else:
    st.error("⚠️ Error Crítico: No hay datos disponibles.")

# --- PIE DE PÁGINA ---
st.write("---")
c_foot1, c_foot2 = st.columns([3,1])
with c_foot1:
    st.markdown("⚖️ *Reporte generado bajo normativas internacionales.*")
    st.caption(f"© 2026 Desarrollado por Albert Guacaran.")
with c_foot2:
    st.caption("v.3.2 - PDF Export Enabled")
