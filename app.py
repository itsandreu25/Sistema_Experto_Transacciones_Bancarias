from copy import deepcopy

import streamlit as st

from datos.clientes import clientes
from datos.movimientos import MOVIMIENTOS
from interfaz.analisis import mostrar_evaluacion, mostrar_resultado
from interfaz.banca import mostrar_banca
from interfaz.estilos import aplicar_estilos
from interfaz.historial import mostrar_historial


st.set_page_config(
    page_title="BankShield Expert",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

aplicar_estilos()

# Estado de navegación y evaluación.
st.session_state.setdefault("pantalla", "banca")
st.session_state.setdefault("transaccion_pendiente", None)
st.session_state.setdefault("respuestas_experto", {})
st.session_state.setdefault("verificacion_actual", 0)
st.session_state.setdefault("resultado_inferencia", None)
st.session_state.setdefault("transaccion_analizada", None)
st.session_state.setdefault("ultima_evaluacion", None)

# Estado bancario dinámico de la sesión.
if "saldos_sesion" not in st.session_state:
    st.session_state["saldos_sesion"] = {
        codigo: cliente["saldo"] for codigo, cliente in clientes.items()
    }

if "movimientos_sesion" not in st.session_state:
    st.session_state["movimientos_sesion"] = deepcopy(MOVIMIENTOS)

st.session_state.setdefault("historial_evaluaciones", [])
st.session_state.setdefault("transacciones_registradas", set())


pantalla = st.session_state["pantalla"]

if pantalla == "banca":
    mostrar_banca()
elif pantalla == "evaluacion":
    mostrar_evaluacion()
elif pantalla == "resultado":
    mostrar_resultado()
elif pantalla == "historial":
    mostrar_historial()
else:
    st.session_state["pantalla"] = "banca"
    st.rerun()
