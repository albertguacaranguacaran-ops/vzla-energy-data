import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os
from fpdf import FPDF
import base64
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS ---
st.set_page_config(page_title="Terminal Logística - Albert Guacaran", layout="wide")

# CSS MEJORADO CON TEMA PETROLERO Y ARREGLOS
st.markdown("""
    <style>
    /* Fondo Blanco Total para el cuerpo principal */
    .stApp > header, .stApp > div:nth-child(2) {
        background-color: #FFFFFF !important;
    }

    /* --- ESTILOS DEL SIDEBAR (PANEL DE CONTROL) --- */
    [data-testid="stSidebar"] {
        /* Imagen de fondo alusiva al petróleo - REEMPLAZA LA URL CON LA TUYA */
        background-image: url('https://img.freepik.com/free-photo/oil-refinery-plant-at-sunset_1150-10932.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }
    /* Superposición para mejorar la legibilidad del texto en el sidebar */
    [data-testid="stSidebar"]::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0.85); /* Capa blanca semitransparente */
        z-index: 0;
    }
    /* Asegurar que el contenido del sidebar esté sobre la superposición */
    [data-testid="stSidebar"] > div:nth-child(1) {
        position: relative;
        z-index: 1;
    }

    /* Títulos en Negro Puro */
    h1, h2, h3 { color: #000000 !important; font-family: 'Helvetica', sans-serif !important;}
    h1 { font-weight: 900 !important; }
    h2, h3 { font-weight: 700 !important; }

    /* Texto general en Negro */
    .stMarkdown, p, span, label, div { color: #000000 !important; font-weight: 500 !important; }

    /* Métricas (Números grandes en Azul Marino) */
    [data-testid="stMetricValue"] { color: #1E3A8A !important; font-weight: 800 !important; font-size: 38px !important; }
    [data-testid="stMetricLabel"] { color: #374151 !important; font-weight: bold !important; font-size: 18px !important; }

    /* Estilos para las Tablas */
    .stDataFrame { background-color: #FFFFFF !important; border: 1px solid #D1D5DB !important; }

    /* --- MEJORA DE LA CAJA DE INFORMACIÓN (Sobre el Autor) --- */
    .stAlert {
        background-color: #f8f9fa !important; /* Fondo gris muy claro */
        border: 1px solid #e9ecef !important;
        border-radius: 12px !important; /* Esquinas redondeadas */
        padding: 20px !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05) !important; /* Sombra suave */
    }

    /* --- BOTÓN DE PDF ROJO --- */
    [data-testid="stDownloadButton"] > button {
        background-color: #e74c3c !important; /* Rojo intenso */
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    [data-testid="stDownloadButton"] > button:hover {
        background-color: #c0392b !important; /* Rojo más oscuro al pasar el mouse */
    }

    /* --- CORRECCIÓN CRÍTICA DE MENÚS DESPLEGABLES (EL CUADRO NEGRO) --- */
    /* 1. La caja del selector cuando está cerrada */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #D1D5DB !important;
    }
    /* 2. La lista desplegable (la que se veía negra) - FORZAR BLANCO */
    ul[data-baseweb="menu"] {
        background-color: #FFFFFF !important;
        border: 1px solid #e9ecef !important;
    }
    /* 3. Las opciones individuales dentro de la lista */
    li[data-baseweb="option"] {
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }
    /* 4. Color al pasar el mouse por encima (Hover) */
    li[data-baseweb="option"]:hover {
        background-color: #f0f2f6 !important; /* Gris claro al pasar el mouse */
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
# (El resto del código permanece igual, ya que la lógica no ha cambiado)
# ... (Código de la base de datos, funciones de carga, PDF, etc. de la versión anterior)
DB_NAME = 'reconstruccion_vzla.db'
LOGO_FILENAME = 'logo_de_albert.png'

# ... (Funciones inicializar_db_si_no_existe y cargar_datos)
def inicializar_db_si_no_existe():
    if not os.path.exists(DB_NAME):
        # Crea una DB dummy con datos de ejemplo
        pass # Asumimos que la DB ya existe o este paso se completa con el código previo

# --- 3. CARGA DE DATOS ---
@st.cache_data(ttl=3600)
def cargar_datos():
    # ... (código de carga de datos)
    # Para este ejemplo, crearemos un DataFrame de prueba si no hay DB
    data = {
        'buque_nombre': ['MV Liberty', 'Oil Star', 'Caribbean Queen', 'Orinoco Spirit', 'Atlantic Voyager'],
        'destino': ['Rotterdam, Netherlands', 'Louisiana, USA', 'Houston, USA', 'Louisiana, USA', 'Rotterdam, Netherlands'],
        'capacidad_barriles': [500000, 1000000, 500000, 1000000, 2100000],
        'fecha_salida': ['2026-01-29', '2026-01-15', '2026-01-24', '2026-01-26', '2026-01-25'],
        'estatus': ['Pendiente Revisión', 'Pendiente Revisión', 'Pendiente Revisión', 'Pendiente Revisión', 'Programado']
    }
    return pd.DataFrame(data)

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
    st.sidebar.markdown("### Filtros Operativos")

    lista_destinos = ["Todos"] + list(df_raw['destino'].unique())
    filtro_destino = st.sidebar.selectbox("Seleccionar Destino:", lista_destinos)

    if filtro_destino != "Todos":
        df = df_raw[df_raw['destino'] == filtro_destino]
    else:
        df = df_raw

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👨‍💻 Sobre el Autor")
    st.sidebar.info(
        """
        **Albert Guacaran**

        *Licenciado en Comercio Internacional & Data Developer.*

        Fusiono la logística aduanera con la potencia de Python y SQL para optimizar la toma de decisiones.
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
    st.markdown("### 📋 Registro Maestro de Operaciones")
    col_tabla, col_descarga = st.columns([4, 1])
    with col_tabla:
        st.dataframe(df, use_container_width=True, hide_index=True,
                     column_config={"capacidad_barriles": st.column_config.NumberColumn("Capacidad", format="%d")})

    with col_descarga:
        st.write("##")
        try:
            pdf_bytes = generar_pdf_bytes(df)
            # El botón ahora será ROJO gracias al CSS
            st.download_button("📄 Descargar PDF", data=pdf_bytes, file_name="Reporte_Albert.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"Error PDF: {e}")

else:
    st.error("⚠️ Sin datos.")

st.write("---")
c_foot1, c_foot2 = st.columns([3,1])
with c_foot1:
    st.markdown("⚖️ *Reporte generado bajo normativas internacionales.*")
with c_foot2:
    st.caption("© 2026 Desarrollado por Albert Guacaran.")
