import streamlit as st


def aplicar_estilos():

    st.markdown(
        """
<style>

/* =========================================================
   GENERAL
========================================================= */

.stApp {
    background:
        radial-gradient(
            circle at top right,
            rgba(30, 64, 175, 0.07),
            transparent 30%
        ),
        #f5f7fb;
}

.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}


/* =========================================================
   TEXTO DE STREAMLIT
========================================================= */

p {
    color: #172033;
}

[data-testid="stWidgetLabel"] p {
    color: #172033 !important;
    font-weight: 650 !important;
}

[data-testid="stMetricLabel"] {
    color: #667085 !important;
}

[data-testid="stMetricValue"] {
    color: #172033 !important;
}

[data-testid="stCaptionContainer"] p {
    color: #697586 !important;
}


/* =========================================================
   CABECERA
========================================================= */

.bank-header {
    background: linear-gradient(
        120deg,
        #071c3b 0%,
        #0a3268 55%,
        #0e4d92 100%
    );

    padding: 28px 32px;
    border-radius: 20px;
    color: white;

    margin-bottom: 24px;

    box-shadow:
        0 10px 30px rgba(7, 28, 59, 0.18);
}

.bank-brand {
    font-size: 30px;
    font-weight: 800;
    letter-spacing: 0.5px;
    color: white;
}

.bank-subtitle {
    opacity: 0.85;
    font-size: 14px;
    color: white;
    margin-top: 4px;
}


/* =========================================================
   TARJETAS
========================================================= */

.bank-card {
    background: white;

    padding: 22px;

    border-radius: 17px;

    border:
        1px solid #e4e9f0;

    box-shadow:
        0 5px 18px rgba(20, 35, 60, 0.06);

    margin-bottom: 15px;
}


.balance-card {
    background:
        linear-gradient(
            135deg,
            #0a3268,
            #155da3
        );

    color: white;

    padding: 27px;

    border-radius: 20px;

    box-shadow:
        0 12px 30px rgba(10, 50, 104, 0.22);

    min-height: 190px;
}


.balance-label {
    font-size: 14px;
    opacity: 0.82;
    color: white;
}


.balance-value {
    font-size: 38px;
    font-weight: 800;

    margin-top: 5px;
    margin-bottom: 25px;

    color: white;
}


.account-number {
    font-size: 15px;
    letter-spacing: 2px;
    opacity: 0.92;
    color: white;
}


/* =========================================================
   PERFIL
========================================================= */

.profile-title {
    font-size: 22px;
    font-weight: 750;
    color: #132238;
}

.profile-small {
    color: #697586;
    font-size: 13px;
}


.badge-safe {
    display: inline-block;

    padding: 6px 12px;

    background: #e8f8f0;

    color: #087f5b;

    border-radius: 20px;

    font-size: 12px;
    font-weight: 700;
}


.badge-device {
    display: inline-block;

    padding: 6px 12px;

    background: #eaf2ff;

    color: #1558a6;

    border-radius: 20px;

    font-size: 12px;
    font-weight: 700;
}


.section-title {
    color: #132238;

    font-size: 23px;
    font-weight: 800;

    margin-top: 15px;
    margin-bottom: 15px;
}


/* =========================================================
   MOVIMIENTOS
========================================================= */

.movement-positive {
    color: #087f5b;
    font-weight: 800;
    font-size: 16px;
}

.movement-negative {
    color: #c92a2a;
    font-weight: 800;
    font-size: 16px;
}


/* =========================================================
   FORMULARIOS
========================================================= */

div[data-testid="stForm"] {
    background: white;

    border:
        1px solid #e1e7ef;

    padding: 24px;

    border-radius: 18px;

    box-shadow:
        0 6px 20px rgba(20, 35, 60, 0.05);
}


/* =========================================================
   BOTONES
========================================================= */

div[data-testid="stFormSubmitButton"] button,
div[data-testid="stButton"] button {

    background: #0a3268 !important;

    color: #ffffff !important;

    border: 1px solid #0a3268 !important;

    border-radius: 10px !important;

    font-weight: 700 !important;

    min-height: 46px !important;
}


/* Fuerza también el texto interno del botón a blanco */

div[data-testid="stFormSubmitButton"] button *,
div[data-testid="stButton"] button * {

    color: #ffffff !important;
}


/* Hover */

div[data-testid="stFormSubmitButton"] button:hover,
div[data-testid="stButton"] button:hover {

    background: #0e4d92 !important;

    border-color: #0e4d92 !important;

    color: #ffffff !important;
}


div[data-testid="stFormSubmitButton"] button:hover *,
div[data-testid="stButton"] button:hover * {

    color: #ffffff !important;
}


/* =========================================================
   MÉTRICAS
========================================================= */

div[data-testid="stMetric"] {

    background: white;

    border:
        1px solid #e5eaf1;

    padding: 14px;

    border-radius: 14px;
}

/* =========================================================
   PANEL LATERAL DE DEMOSTRACIÓN
========================================================= */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #111827 0%,
            #172033 100%
        ) !important;
}


/* Títulos */

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}


/* Texto general */

section[data-testid="stSidebar"]
[data-testid="stMarkdownContainer"] p {
    color: #dbe4f0 !important;
}


/* Etiquetas de controles */

section[data-testid="stSidebar"]
[data-testid="stWidgetLabel"] p {
    color: #f8fafc !important;
    font-weight: 650 !important;
}


/* Texto pequeño */

section[data-testid="stSidebar"]
[data-testid="stCaptionContainer"] p {
    color: #aebccc !important;
}


/* Separadores */

section[data-testid="stSidebar"] hr {
    border-color: #334155 !important;
}


/* Inputs y selectores */

section[data-testid="stSidebar"]
div[data-baseweb="select"] > div {

    background: #202938 !important;

    color: #ffffff !important;

    border-color: #3b4658 !important;
}


/* Texto dentro de inputs */

section[data-testid="stSidebar"] input {
    color: #ffffff !important;
}


/* Código - nombre del equipo */

section[data-testid="stSidebar"]
[data-testid="stCode"] {

    background: #0f172a !important;

    border-radius: 8px !important;
}


/* Toggle */

section[data-testid="stSidebar"]
[data-testid="stToggle"] p {

    color: #f8fafc !important;
}

/* =========================================================
   TÍTULOS DEL CONTENIDO PRINCIPAL
========================================================= */

h1,
h2,
h3,
h4 {
    color: #172033 !important;
}


/* El sidebar conserva títulos blancos */

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4 {
    color: #ffffff !important;
}

/* =========================================================
   DESPLEGABLES / EXPANDERS DEL CONTENIDO PRINCIPAL
========================================================= */

div[data-testid="stExpander"] details {
    background: #ffffff !important;
    border: 1px solid #dfe5ec !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}


/* Cabecera cerrada */

div[data-testid="stExpander"] details summary {
    background: #ffffff !important;
    color: #172033 !important;
    padding: 13px 16px !important;
}


/* Texto del título */

div[data-testid="stExpander"] details summary p {
    color: #172033 !important;
    font-weight: 650 !important;
}


/* Flecha */

div[data-testid="stExpander"] details summary svg {
    color: #172033 !important;
    fill: #172033 !important;
}


/* Cuando está abierto */

div[data-testid="stExpander"] details[open] summary {
    background: #f8fafc !important;
    border-bottom: 1px solid #e5eaf0 !important;
}


/* Contenido */

div[data-testid="stExpander"] details > div {
    background: #ffffff !important;
    color: #172033 !important;
}


/* =========================================================
   AJUSTES FINALES DE LEGIBILIDAD Y RESPONSIVIDAD
========================================================= */

[data-testid="stMetricValue"] {
    font-size: clamp(1.45rem, 2.5vw, 2.25rem) !important;
    line-height: 1.15 !important;
    white-space: normal !important;
    overflow-wrap: anywhere !important;
}

div[data-testid="stMetric"] {
    min-height: 108px;
}

input:disabled,
textarea:disabled {
    color: #d7dfeb !important;
    -webkit-text-fill-color: #d7dfeb !important;
    opacity: 1 !important;
}

section[data-testid="stSidebar"] {
    min-width: 285px !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #e5eaf1;
    border-radius: 12px;
    overflow: hidden;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.35rem;
    flex-wrap: wrap;
}

.stTabs [data-baseweb="tab"] {
    color: #334155 !important;
    font-weight: 600;
}

@media (max-width: 900px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .bank-header {
        padding: 22px 24px;
        border-radius: 16px;
    }

    .bank-brand {
        font-size: 25px;
    }

    .balance-value {
        font-size: 31px;
    }
}

</style>
        """,
        unsafe_allow_html=True
    )