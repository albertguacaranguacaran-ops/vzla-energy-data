import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os
from fpdf import FPDF
import base64
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Terminal Logística - Albert Guacaran", layout="wide")

# --- 2. CSS MAESTRO (TARJETAS + ESTILOS) ---
st.markdown("""
    <style>
    /* 1. FONDO BLANCO GENERAL */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #F8F9FA !important; /* Un gris muy muy claro para que las tarjetas blancas resalten */
    }
    
    /* 2. TEXTOS GENERALES EN NEGRO */
    h1, h2, h3, p, span, div, label {
        color: #000000 !important;
        font-family: 'Arial', sans-serif !important;
    }

    /* --- 3. ¡AQUÍ ESTÁN LAS TARJETAS (CARDS) DE MÉTRICAS! --- */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important; /* Fondo blanco de la tarjeta */
        border: 1px solid #D1D5DB !important; /* Borde gris suave */
        padding: 20px !important;              /* Espacio interno */
        border-radius: 10px !important;        /* Bordes redondeados */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important; /* Sombra suave 3D */
        border-left: 8px solid #1E3A8A !important; /* Tira AZUL PETRÓLEO a la izquierda */
        text-align: center !important;
    }
    
    /* Ajuste de los números dentro de la tarjeta */
    [data-testid="stMetricValue"] {
        color: #1E3A8A !important; /* Azul corporativo */
        font-size: 32px !important;
        font-weight: 800 !important;
    }
    
    /* Ajuste del título pequeño (label) dentro de la tarjeta */
    [data-testid="stMetricLabel"] {
        color: #4B5563 !important; /* Gris oscuro */
        font-size: 16px !important;
        font-weight: bold !important;
    }

    /* --- 4. SIDEBAR CON IMAGEN PETROLERA --- */
    [data-testid="stSidebar"] {
        background-image: url('https://img.freepik.com/free-photo/oil-refinery-plant-at-sunset_1150-10932.jpg');
        background-size: cover;
        background-position: center;
    }
    [data-testid="stSidebar"]::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(255, 255, 255, 0.90); /* Capa blanca para leer letras */
        z-index: 0;
    }
    [data-testid="stSidebar"] > div:nth-child(1) { position: relative; z-index: 1; }

    /* --- 5. MENÚ DESPLEGABLE (FIX NEGRO) --- */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #000000 !important;
        color: #000000 !important;
    }
    ul[data-baseweb="menu"] { background-color: #FFFFFF !important; }
    li[data-baseweb="option"] { color: #000000 !important; background-color: #FFFFFF !important; }
    li[data-baseweb="option"]:hover { background-color: #E5E7EB !important; color: #1E3A8A !important; }
    svg { fill: #000000 !important; }

    /* --- 6. BOTÓN PDF ROJO --- */
    div.stDownloadButton > button {
        background-color: #D32F2F !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        width: 100%;
    }
    div.stDownloadButton > button:hover { background-color: #B71C1C !important; }

    /* --- 7. ESTILO TABLA --- */
    .stDataFrame { border: 1px solid #D1D5DB !important; background-color: white !important;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONFIGURACIÓN Y DATOS ---
DB_NAME = 'reconstruccion_vzla.db'
LOGO_FILENAME = 'logo_de_albert.png'

@st.cache_data(ttl=3600)
def cargar_datos():
    # Datos simulados para garantizar que funcione al copiar y pegar
    data = {
        'buque_nombre': ['MV Liberty', 'Oil Star', 'Caribbean Queen', 'Orinoco Spirit', 'Atlantic Voyager'],
        'destino': ['Rotterdam, Netherlands', 'Louisiana, USA', 'Houston, USA', 'Louisiana, USA', 'Rotterdam, Netherlands'],
        'capacidad_barriles': [500000, 1000000, 500000, 1000000, 2100000],
        'fecha_salida': ['2026-01-29', '2026-01-15', '2026-01-24', '2026-01-26', '2026-01-25'],
        'estatus': ['Pendiente Revisión', 'Pendiente Revisión', 'Pendiente Revisión', 'Pendiente Revisión', 'Programado']
    }
    return pd.DataFrame(data)

df_raw = cargar_datos()

# --- 4. FUNCIÓN PDF ---
class PDF(FPDF):
    def header(self):
        if os.path.exists(LOGO_FILENAME):
            try: self.image(LOGO_FILENAME, 10, 8, 33)
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

# --- 6. CUERPO DASHBOARD ---
if not df_raw.empty:
    
    # SIDEBAR
    st.sidebar.title("🛠️ Panel de Control")
    st.sidebar.markdown("### Filtros Operativos")
    lista_destinos = ["Todos"] + list(df_raw['destino'].unique())
    filtro_destino = st.sidebar.selectbox("Seleccionar Destino:", lista_destinos)
    
    if filtro_destino != "Todos":
        df = df_raw[df_raw['destino'] == filtro_destino]
    else:
        df = df_raw
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👨‍💻 Sobre el Autor")
    st.sidebar.info("Albert Guacaran\n\nLicenciado en Comercio Internacional & Data Developer.")

    # --- AQUÍ ESTÁN LAS MÉTRICAS CON ESTILO DE TARJETA ---
    # Usamos st.columns para distribuirlas horizontalmente
    m1, m2, m3, m4 = st.columns(4)
    
    total_bbls = df["capacidad_barriles"].sum()
    valor_fob = total_bbls * 75
    n_buques = df["buque_nombre"].nunique()
    
    # El CSS inyectado arriba convertirá esto automáticamente en tarjetas
    m1.metric("Volumen Total (BBLS)", f"{total_bbls:,.0f}")
    m2.metric("Valoración FOB (USD)", f"$ {valor_fob:,.0f}")
    m3.metric("Buques Activos", f"{n_buques}")
    m4.metric("Estado de Red", "OPERATIVO", delta="100%")

    st.write("##")

    # GRÁFICOS
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

    # TABLA Y PDF
    st.markdown("### 📋 Registro Maestro de Operaciones")
    col_tabla, col_descarga = st.columns([4, 1])
    with col_tabla:
        st.dataframe(df, use_container_width=True, hide_index=True)
    with col_descarga:
        st.write("##")
        try:
            pdf_bytes = generar_pdf_bytes(df)
            st.download_button(label="📄 Descargar PDF", data=pdf_bytes, file_name="Reporte_Albert.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"Error PDF: {e}")

else:
    st.error("⚠️ No hay datos cargados.")

st.write("---")
st.caption("© 2026 Desarrollado por Albert Guacaran.")
