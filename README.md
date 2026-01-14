# ⚓ Sistema de Inteligencia Portuaria & Logística

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b)
![SQL](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

> **Solución BI desarrollada para la optimización, seguimiento y auditoría de operaciones de exportación de crudo y derivados.**

---

## 📖 Descripción del Proyecto

Este proyecto es una aplicación de **Business Intelligence (BI)** full-stack diseñada para transformar datos operativos crudos en dashboards ejecutivos de alta precisión. 

El sistema simula un entorno real de **Comercio Exterior**, permitiendo a gerentes y auditores visualizar métricas críticas como volumen de barriles (BBLS), valoración FOB, estatus de buques y tiempos de zarpe, garantizando la toma de decisiones basada en datos.

### 🎯 Objetivo Profesional
Demostrar la convergencia entre el conocimiento experto en **Logística Aduanera/Comercio Internacional** y el desarrollo de software con **Python & SQL**.

---

## 🚀 Características Principales

* **📊 Dashboard Ejecutivo Interactivo:** Visualización de KPIs en tiempo real (Volumen Total, Valoración Financiera, Flota Activa).
* **🌍 Análisis Geoespacial:** Distribución de carga por destino internacional (China, India, EE.UU., etc.) mediante gráficos interactivos de Plotly.
* **🛡️ UI/UX de Alto Contraste:** Interfaz optimizada con CSS personalizado que garantiza legibilidad perfecta (Fondo Blanco / Texto Negro) independientemente de la configuración del dispositivo del usuario.
* **📄 Generación de Reportes PDF:** Módulo automatizado con `FPDF` que genera documentos formales de auditoría, procesando caracteres especiales y adjuntando marca corporativa.
* **💾 Gestión de Datos Autónoma:** Sistema de autogeneración de base de datos SQLite. Si no detecta la DB, la crea y puebla con data semilla automáticamente (Ideal para portabilidad).
* **🔍 Filtros Operativos:** Segmentación dinámica de la data por destino o estatus aduanero.

---

## 🛠️ Tecnologías Utilizadas

| Categoría | Tecnologías | Uso en el Proyecto |
| :--- | :--- | :--- |
| **Lenguaje** | ![Python](https://img.shields.io/badge/-Python-000?&logo=python) | Lógica de backend y cálculos financieros. |
| **Frontend** | ![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?&logo=streamlit) | Interfaz de usuario y componentes web. |
| **Data Viz** | ![Plotly](https://img.shields.io/badge/-Plotly-3F4F75?&logo=plotly) | Gráficos de pastel y barras interactivos. |
| **Database** | ![SQLite](https://img.shields.io/badge/-SQLite-003B57?&logo=sqlite) | Almacenamiento persistente de operaciones. |
| **Reporting** | `FPDF` | Motor de generación de reportes PDF. |
| **Data Ops** | `Pandas` | Manipulación y limpieza de DataFrames. |

---

## 💻 Instalación y Ejecución Local

Sigue estos pasos para clonar y ejecutar el sistema en tu máquina:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/albertguacaranguacaran-ops/vzla-energy-data.git](https://github.com/albertguacaranguacaran-ops/vzla-energy-data.git)
    cd vzla-energy-data
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar la aplicación:**
    ```bash
    streamlit run app.py
    ```

*El sistema creará automáticamente la base de datos `reconstruccion_vzla.db` en la primera ejecución.*

---

## 📂 Estructura del Proyecto

```text
├── app.py                  # Código fuente principal (Lógica + UI)
├── requirements.txt        # Dependencias para despliegue en nube
├── logo_de_albert.png      # Activos de marca personal
├── reconstruccion_vzla.db  # Base de datos (Autogenerada)
└── README.md               # Documentación



<img width="1920" height="1002" alt="image" src="https://github.com/user-attachments/assets/bc3efff3-9501-4f68-a565-76a4fd801e22" />
