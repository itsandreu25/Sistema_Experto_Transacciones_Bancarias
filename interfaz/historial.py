import streamlit as st

from datos.clientes import clientes
from experto.inferencia import obtener_nombre_riesgo
from interfaz.razonamiento import mostrar_cadena_inferencia
from interfaz.utilidades import humanizar_hecho, nombre_modo

# ==========================================================
# UTILIDADES
# ==========================================================

def mostrar_detalle_evaluacion(registro):

    transaccion = registro[
        "transaccion"
    ]

    resultado = registro[
        "resultado"
    ]

    cliente = clientes[
        registro["cliente_id"]
    ]

    st.divider()

    st.subheader(
        "Detalle de la evaluación"
    )

    st.caption(
        f"Identificador: {registro['id']}"
    )

    # ======================================================
    # DATOS PRINCIPALES
    # ======================================================

    col1, col2, col3, col4 = st.columns(
        4
    )

    with col1:

        st.metric(
            "Cliente",
            cliente["nombre"]
        )

    with col2:

        st.metric(
            "Monto",
            f"${registro['monto']:,.2f}"
        )

    with col3:

        st.metric(
            "Riesgo",
            obtener_nombre_riesgo(
                registro["riesgo"]
            )
        )

    with col4:

        st.metric(
            "Reglas",
            registro[
                "reglas_activadas"
            ]
        )

    # ======================================================
    # TRANSACCIÓN
    # ======================================================

    st.markdown(
        "### Información de la transacción"
    )

    izquierda, derecha = st.columns(2)

    with izquierda:

        st.write(
            f"**Beneficiario:** "
            f"{transaccion['beneficiario']}"
        )

        st.write(
            f"**Estado:** "
            f"{registro['estado']}"
        )

        st.write(
            f"**Modo:** "
            f"{nombre_modo(registro['modo'])}"
        )

    with derecha:

        st.write(
            f"**Ubicación:** "
            f"{transaccion['ubicacion']}"
        )

        st.write(
            f"**Dispositivo:** "
            f"{transaccion['dispositivo']}"
        )

        st.write(
            f"**Hora:** "
            f"{transaccion['hora_texto']}"
        )

    # ======================================================
    # RAZONAMIENTO
    # ======================================================

    st.markdown(
        "### Razonamiento del sistema experto"
    )

    tab0, tab1, tab2, tab3 = st.tabs(
        [
            "Cadena principal",
            "Hechos iniciales",
            "Hechos inferidos",
            "Reglas activadas"
        ]
    )

    # ------------------------------------------------------
    # CADENA PRINCIPAL
    # ------------------------------------------------------

    with tab0:

        mostrar_cadena_inferencia(
            resultado
        )

    # ------------------------------------------------------
    # HECHOS INICIALES
    # ------------------------------------------------------

    with tab1:

        for hecho in sorted(
            resultado[
                "hechos_iniciales"
            ]
        ):

            st.write(
                f"• {humanizar_hecho(hecho)}"
            )

    # ------------------------------------------------------
    # HECHOS INFERIDOS
    # ------------------------------------------------------

    with tab2:

        hechos_inferidos = resultado[
            "hechos_inferidos"
        ]

        if hechos_inferidos:

            for hecho in sorted(
                hechos_inferidos
            ):

                st.write(
                    f"• {humanizar_hecho(hecho)}"
                )

        else:

            st.caption(
                "No se generaron hechos inferidos."
            )

    # ------------------------------------------------------
    # REGLAS
    # ------------------------------------------------------

    with tab3:

        reglas = resultado[
            "reglas_activadas"
        ]

        if not reglas:

            st.caption(
                "No se activaron reglas."
            )

        for regla in reglas:

            with st.container(
                border=True
            ):

                st.markdown(
                    f"**{regla['id']} · "
                    f"Nivel {regla['nivel']} · "
                    f"Ciclo {regla['iteracion']}**"
                )

                st.write(
                    "**Condiciones:**"
                )

                for condicion in regla[
                    "antecedentes"
                ]:

                    st.write(
                        f"• "
                        f"{humanizar_hecho(condicion)}"
                    )

                st.write(
                    "**Conclusión:** "
                    f"{humanizar_hecho(regla['conclusion'])}"
                )

                st.caption(
                    regla[
                        "descripcion"
                    ]
                )


# ==========================================================
# PANTALLA PRINCIPAL
# ==========================================================

def mostrar_historial():

    st.html(
        """
        <div class="bank-header">
            <div class="bank-brand">
                BANKSHIELD EXPERT
            </div>

            <div class="bank-subtitle">
                Historial de evaluaciones de seguridad
            </div>
        </div>
        """
    )

    historial = st.session_state.get(
        "historial_evaluaciones",
        []
    )

    # ======================================================
    # SIN REGISTROS
    # ======================================================

    if not historial:

        st.info(
            "Todavía no existen evaluaciones registradas "
            "durante esta sesión."
        )

        if st.button(
            "Volver a la banca"
        ):

            st.session_state[
                "pantalla"
            ] = "banca"

            st.rerun()

        return

    # ======================================================
    # RESUMEN
    # ======================================================

    st.subheader(
        "Evaluaciones realizadas"
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        st.metric(
            "Total",
            len(historial)
        )

    with col2:

        bloqueadas = sum(
            1
            for registro in historial
            if registro[
                "estado"
            ] == "Bloqueada"
        )

        st.metric(
            "Bloqueadas",
            bloqueadas
        )

    with col3:

        aprobadas = sum(
            1
            for registro in historial
            if registro[
                "estado"
            ] == "Aprobada"
        )

        st.metric(
            "Aprobadas",
            aprobadas
        )

    # ======================================================
    # TABLA
    # ======================================================

    filas = []

    for registro in historial:

        cliente = clientes[
            registro["cliente_id"]
        ]

        filas.append(
            {
                "ID":
                    registro["id"],

                "Fecha":
                    registro["fecha"],

                "Cliente":
                    cliente["nombre"],

                "Beneficiario":
                    registro["beneficiario"],

                "Monto":
                    f"${registro['monto']:,.2f}",

                "Riesgo":
                    obtener_nombre_riesgo(
                        registro["riesgo"]
                    ),

                "Estado":
                    registro["estado"],

                "Reglas":
                    registro[
                        "reglas_activadas"
                    ],

                "Modo":
                    nombre_modo(
                        registro["modo"]
                    )
            }
        )

    st.dataframe(
        filas,
        use_container_width=True,
        hide_index=True
    )

    # ======================================================
    # SELECCIONAR EVALUACIÓN
    # ======================================================

    st.subheader(
        "Consultar una evaluación"
    )

    ids = [
        registro["id"]
        for registro in historial
    ]

    id_seleccionado = st.selectbox(
        "Seleccione una operación",
        ids,
        format_func=lambda identificador: next(
            (
                f"{registro['id']} · "
                f"{clientes[registro['cliente_id']]['nombre']} · "
                f"${registro['monto']:,.2f} · "
                f"{obtener_nombre_riesgo(registro['riesgo'])}"
                for registro in historial
                if registro["id"] == identificador
            ),
            identificador
        )
    )
    registro_seleccionado = next(
        registro
        for registro in historial
        if registro["id"] == id_seleccionado
    )

    mostrar_detalle_evaluacion(
        registro_seleccionado
    )

    st.divider()

    # ======================================================
    # VOLVER
    # ======================================================

    if st.button(
        "Volver a la banca",
        use_container_width=True
    ):

        st.session_state[
            "pantalla"
        ] = "banca"

        st.rerun()