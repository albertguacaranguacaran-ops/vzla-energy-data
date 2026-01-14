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

# CSS MEJORADO PARA CORREGIR EL MENÚ NEGRO
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
        width: 100%;
    }

    /* --- CORRECCIÓN CRÍTICA DE MENÚS DESPLEGABLES (EL CUADRO NEGRO) --- */
    
    /* 1. La caja del selector cuando está cerrada */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #D1D5DB !important;
    }
    
    /* 2. La lista desplegable (la que se veía negra) */
    ul[data-baseweb="menu"] {
        background-color: #FFFFFF !important;
    }
    
    /* 3. Las opciones individuales dentro de la lista */
    li[data-baseweb="option"] {
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }
    
    /* 4. Color al pasar el mouse por encima (Hover) */
    li[data-baseweb="option"]:hover {
        background-color: #E5E7EB !important;
        color: #1E3A8A !important;
    }

    /* 5. Asegurar que el texto dentro del select sea negro */
    div[data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
    }
    
    /* 6. Icono de flecha del dropdown */
    svg {
        fill: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTIÓN DE BASE DE DATOS ---
DB_NAME = 'reconstruccion_vzla.db'
LOGO_FILENAME = 'logo_de_albert.png'

def inicializar_db_si_no_existe():
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
        st.error(f"Error DB: {e}")
        return pd.DataFrame()

df_raw = cargar_datos()

# --- 4. SISTEMA PDF ROBUSTO ---
class PDF(FPDF):
    def header(self):
        if os.path.exists(LOGO_FILENAME):
            try:
                self.image(LOGO_FILENAME, 10, 8, 33)
            except: pass
        self.set_font('Arial', 'B', 15)
        self.cell(80) 
        self.cell(30, 10, 'Reporte de Operaciones', 0, 0, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()} - Albert Guacaran', 0, 0, 'C')

def clean_text(text):
    if text is None: return ""
    return str(text).encode('latin-1', 'replace').decode('latin-1')

def generar_pdf_bytes(df_export):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    fecha = datetime.now().strftime('%Y-%m-%d')
    pdf.cell(200, 10, txt=clean_text(f"Fecha: {fecha}"), ln=True)
    pdf.cell(200, 10, txt=clean_text("Logística y Comercio Exterior"), ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 10)
    cols = ["Buque", "Destino", "Capacidad", "Salida", "Estatus"]
    anchos = [40, 35, 30, 30, 40]
    for i, col in enumerate(cols):
        pdf.cell(anchos[i], 10, clean_text(col), 1)
    pdf.ln()
    
    pdf.set_font("Arial", size=9)
    for index, row in df_export.iterrows():
        try:
            pdf.cell(anchos[0], 10, clean_text(row['buque_nombre']), 1)
            pdf.cell(anchos[1], 10, clean_text(row['destino']), 1)
            pdf.cell(anchos[2], 10, clean_text(f"{row['capacidad_barriles']:,}"), 1)
            pdf.cell(anchos[3], 10, clean_text(row['fecha_salida']), 1)
            pdf.cell(anchos[4], 10, clean_text(row['estatus']), 1)
            pdf.ln()
        except: continue
    return pdf.output(dest='S').encode('latin-1', 'replace')

# --- 5. ENCABEZADO ---
col_logo, col_titulo = st.columns([1, 5])
with col_logo:
    try:
        img = Image.open(LOGO_FILENAME)
        st.image(img, use_container_width=True)
    except:
        st.markdown("## ⚓")

with col_titulo:
    st.title("Sistema de Inteligencia Portuaria")
    st.markdown("### Dashboard Ejecutivo de Logística y Exportación")
    st.markdown("**Desarrollado por:** Lic. Albert Guacaran | **Tecnología:** Python + SQL + Streamlit")

st.write("---")

# --- 6. INTERFAZ ---
if not df_raw.empty:
    
    # SIDEBAR
    st.sidebar.title("🛠️ Panel de Control")
    st.sidebar.markdown("**Filtros Operativos**") # Markdown en lugar de subheader para controlar color
    
    lista_destinos = ["Todos"] + list(df_raw['destino'].unique())
    # El CSS arriba se encarga de pintar esto de blanco
    filtro_destino = st.sidebar.selectbox("Seleccionar Destino:", lista_destinos)
    
    if filtro_destino != "Todos":
        df = df_raw[df_raw['destino'] == filtro_destino]
    else:
        df = df_raw
        
    st.sidebar.markdown("---")
    st.sidebar.info(
        """
        **Albert Guacaran**
        *Licenciado en Comercio Internacional & Data Developer.*
        """
    )

    # METRICAS
    m1, m2, m3, m4 = st.columns(4)
    total_bbls = df["capacidad_barriles"].sum()
    valor_fob = total_bbls * 75 
    n_buques = df["buque_nombre"].nunique()
    
    m1.metric("Volumen Total (BBLS)", f"{total_bbls:,.0f}")
    m2.metric("Valoración FOB (USD)", f"$ {valor_fob:,.0f}")
    m3.metric("Buques Activos", f"{n_buques}")
    m4.metric("Estado de Red", "OPERATIVO", delta="100%")

    st.write("##")

    # GRÁFICOS (TEXTO NEGRO)
    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(df, values='capacidad_barriles', names='destino', 
                     title="Distribución Geográfica",
                     color_discrete_sequence=px.colors.qualitative.Bold, hole=0.4)
        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', 
                          font_color="black", title_font_color="black",
                          legend=dict(font=dict(color="black")))
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        df_sorted = df.sort_values(by="capacidad_barriles", ascending=True)
        fig2 = px.bar(df_sorted, x='capacidad_barriles', y='buque_nombre', 
                      title="Capacidad por Buque", orientation='h', text_auto='.2s',
                      color_discrete_sequence=['#1E3A8A'])
        fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white', 
                           font_color="black", title_font_color="black",
                           xaxis=dict(title_font=dict(color="black"), tickfont=dict(color="black")),
                           yaxis=dict(title_font=dict(color="black"), tickfont=dict(color="black")))
        st.plotly_chart(fig2, use_container_width=True)

    # TABLA
    st.markdown("### 📋 Registro Maestro")
    col_tabla, col_descarga = st.columns([4, 1])
    with col_tabla:
        st.dataframe(df, use_container_width=True, hide_index=True,
                     column_config={"capacidad_barriles": st.column_config.NumberColumn("Capacidad", format="%d")})
    
    with col_descarga:
        st.write("##")
        try:
            pdf_bytes = generar_pdf_bytes(df)
            st.download_button("📄 Descargar PDF", data=pdf_bytes, file_name="Reporte_Albert.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"Error PDF: {e}")

else:
    st.error("⚠️ Sin datos.")

st.write("---")
st.caption("© 2026 Desarrollado por Albert Guacaran.")
