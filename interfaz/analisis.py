import streamlit as st

from datos.clientes import clientes

from experto.preguntas import (
    VERIFICACIONES,
    cantidad_verificaciones
)

from experto.hechos import (
    generar_hechos_iniciales
)

from experto.inferencia import (
    motor_inferencia,
    obtener_nombre_riesgo,
    obtener_accion_recomendada,
    generar_explicacion
)

from experto.operaciones import registrar_operacion_en_estado

from interfaz.razonamiento import (
    mostrar_cadena_inferencia
)
from interfaz.utilidades import humanizar_hecho

# ==========================================================
# CONTROLES DE VERIFICACIÓN
# ==========================================================

def formatear_valor(pregunta, valor):
    """
    Convierte un valor interno en una representación
    comprensible para el analista.
    """

    tipo = pregunta[
        "tipo"
    ]

    if tipo == "si_no":

        return (
            "Sí"
            if valor
            else "No"
        )

    if tipo == "numero":

        unidad = pregunta.get(
            "unidad",
            ""
        )

        return (
            f"{valor} {unidad}"
        ).strip()

    if tipo == "opciones":

        etiquetas = pregunta.get(
            "etiquetas",
            {}
        )

        return etiquetas.get(
            valor,
            str(valor)
        )

    return str(
        valor
    )


def mostrar_control_verificacion(
    pregunta,
    transaccion
):
    """
    Muestra el dato detectado automáticamente.

    El analista puede confirmarlo directamente o,
    excepcionalmente, corregirlo antes de continuar.
    """

    campo = pregunta[
        "campo"
    ]

    respuestas = st.session_state.get(
        "respuestas_experto",
        {}
    )

    valor = respuestas.get(
        campo,
        transaccion.get(
            campo
        )
    )

    # ------------------------------------------------------
    # FUENTE
    # ------------------------------------------------------

    st.caption(
        f"Fuente: {pregunta['fuente']}"
    )

    # ------------------------------------------------------
    # DATO REGISTRADO
    # ------------------------------------------------------

    st.metric(
        "Dato registrado",
        formatear_valor(
            pregunta,
            valor
        )
    )

    # ------------------------------------------------------
    # CORRECCIÓN OPCIONAL
    # ------------------------------------------------------

    corregir = st.toggle(
        "Corregir este dato antes de confirmarlo",
        value=False,
        key=(
            f"corregir_"
            f"{pregunta['id']}"
        )
    )

    if not corregir:

        return valor

    st.caption(
        "Utilice esta opción únicamente para "
        "simular una corrección realizada por el analista."
    )

    tipo = pregunta[
        "tipo"
    ]

    # ------------------------------------------------------
    # NUMÉRICO
    # ------------------------------------------------------

    if tipo == "numero":

        return int(
            st.number_input(
                "Valor corregido",
                min_value=0,
                value=int(
                    valor or 0
                ),
                step=1,
                key=(
                    f"valor_corregido_"
                    f"{pregunta['id']}"
                )
            )
        )

    # ------------------------------------------------------
    # SÍ / NO
    # ------------------------------------------------------

    if tipo == "si_no":

        respuesta = st.radio(
            "Valor corregido",
            [
                "Sí",
                "No"
            ],
            index=(
                0
                if valor
                else 1
            ),
            horizontal=True,
            key=(
                f"valor_corregido_"
                f"{pregunta['id']}"
            )
        )

        return respuesta == "Sí"

    # ------------------------------------------------------
    # OPCIONES
    # ------------------------------------------------------

    if tipo == "opciones":

        opciones = pregunta[
            "opciones"
        ]

        etiquetas = pregunta.get(
            "etiquetas",
            {}
        )

        visibles = [
            etiquetas.get(
                opcion,
                opcion
            )
            for opcion in opciones
        ]

        indice = (
            opciones.index(
                valor
            )
            if valor in opciones
            else 0
        )

        seleccion = st.radio(
            "Valor corregido",
            visibles,
            index=indice,
            key=(
                f"valor_corregido_"
                f"{pregunta['id']}"
            )
        )

        return opciones[
            visibles.index(
                seleccion
            )
        ]

    return valor

# ==========================================================
# FINALIZAR EVALUACIÓN
# ==========================================================
def registrar_operacion(transaccion, resultado):
    """Registra en el estado de sesión el efecto de la evaluación."""
    return registrar_operacion_en_estado(
        transaccion=transaccion,
        resultado=resultado,
        saldos=st.session_state["saldos_sesion"],
        movimientos=st.session_state["movimientos_sesion"],
        historial=st.session_state["historial_evaluaciones"],
        registradas=st.session_state["transacciones_registradas"],
    )

def finalizar_evaluacion():
    """
    Une los datos de la transferencia con las respuestas
    confirmadas por el analista y ejecuta el sistema experto completo.
    """

    transaccion = dict(
        st.session_state[
            "transaccion_pendiente"
        ]
    )

    respuestas = st.session_state[
        "respuestas_experto"
    ]

    # Agregamos las respuestas del sistema experto
    # a los datos de la transacción.
    transaccion.update(
        respuestas
    )

    codigo_cliente = transaccion[
        "cliente_id"
    ]

    cliente = clientes[
        codigo_cliente
    ]

    # ======================================================
    # GENERAR HECHOS
    # ======================================================

    hechos_iniciales, detalles = (
        generar_hechos_iniciales(
            cliente,
            transaccion
        )
    )

    # ======================================================
    # EJECUTAR MOTOR DE INFERENCIA
    # ======================================================

    resultado = motor_inferencia(
        hechos_iniciales
    )

    registrar_operacion(
        transaccion,
        resultado
    )

    # ======================================================
    # GUARDAR RESULTADO COMPLETO
    # ======================================================

    st.session_state[
        "transaccion_analizada"
    ] = transaccion

    st.session_state[
        "hechos_iniciales_resultado"
    ] = hechos_iniciales

    st.session_state[
        "detalles_analisis"
    ] = detalles

    st.session_state[
        "resultado_inferencia"
    ] = resultado

    st.session_state[
        "ultima_evaluacion"
    ] = {
        "transaccion": transaccion,
        "resultado": resultado
    }

    st.session_state[
        "pantalla"
    ] = "resultado"

    st.rerun()


# ==========================================================
# SIDEBAR DURANTE EL ANÁLISIS
# ==========================================================

def mostrar_sidebar_evaluacion(
    cliente,
    transaccion,
    actual,
    total
):

    with st.sidebar:

        st.title(
            "Evaluación de seguridad"
        )

        st.caption(
            "Sistema experto basado en reglas"
        )

        st.divider()

        st.write(
            f"**Cliente:** "
            f"{cliente['nombre']}"
        )

        st.write(
            f"**Cuenta:** "
            f"{cliente['cuenta']}"
        )

        st.write(
            f"**Monto:** "
            f"${transaccion['monto']:,.2f}"
        )

        st.write(
            f"**Beneficiario:** "
            f"{transaccion['beneficiario']}"
        )

        st.write(
            f"**Ubicación:** "
            f"{transaccion['ubicacion']}"
        )

        st.write(
            f"**Dispositivo:** "
            f"{transaccion['dispositivo']}"
        )

        st.divider()

        st.write(
            f"Verificación **{actual} de {total}**"
        )

        st.progress(
            actual / total
        )

        st.caption(
            "El motor de inferencia se ejecutará "
            "únicamente después de confirmar "
            "las 10 verificaciones."
        )


# ==========================================================
# PANTALLA DE EVALUACIÓN
# ==========================================================

def mostrar_evaluacion():

    # ======================================================
    # VALIDAR TRANSACCIÓN
    # ======================================================

    transaccion = st.session_state.get(
        "transaccion_pendiente"
    )

    if not transaccion:

        st.warning(
            "No existe una transacción pendiente."
        )

        if st.button(
            "Regresar a la banca"
        ):

            st.session_state[
                "pantalla"
            ] = "banca"

            st.rerun()

        return

    codigo_cliente = transaccion[
        "cliente_id"
    ]

    cliente = clientes[
        codigo_cliente
    ]

    # ======================================================
    # MODO AUTOMÁTICO
    # ======================================================

    if transaccion.get(
        "modo_analisis"
    ) == "automatico":

        for item in VERIFICACIONES:

            campo = item[
                "campo"
            ]

            st.session_state[
                "respuestas_experto"
            ][campo] = transaccion.get(
                campo
            )

        finalizar_evaluacion()

        return

    # ======================================================
    # VERIFICACIÓN ACTUAL
    # ======================================================

    indice = st.session_state.get(
        "verificacion_actual",
        0
    )

    total = cantidad_verificaciones()

    if indice >= total:

        finalizar_evaluacion()
        return

    pregunta = VERIFICACIONES[
        indice
    ]

    numero_actual = indice + 1

    # ======================================================
    # SIDEBAR
    # ======================================================

    mostrar_sidebar_evaluacion(
        cliente,
        transaccion,
        numero_actual,
        total
    )

    # ======================================================
    # CABECERA
    # ======================================================

    st.html(
        """
        <div class="bank-header">
            <div class="bank-brand">
                BANKSHIELD EXPERT
            </div>

            <div class="bank-subtitle">
                Evaluación inteligente de seguridad
            </div>
        </div>
        """
    )

    # ======================================================
    # RESUMEN
    # ======================================================

    st.subheader(
        "Evaluación de la transacción"
    )

    st.caption(
        "Revise y confirme los datos obtenidos de los "
        "registros internos. El motor de inferencia se "
        "ejecutará después de completar las 10 verificaciones."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Monto",
            f"${transaccion['monto']:,.2f}"
        )

    with col2:

        st.metric(
            "Beneficiario",
            transaccion[
                "beneficiario"
            ]
        )

    with col3:

        st.metric(
            "Hora",
            transaccion[
                "hora_texto"
            ]
        )

    st.write("")

    # ======================================================
    # PROGRESO
    # ======================================================

    st.write(
        f"**Verificación {numero_actual} de {total}**"
    )

    st.progress(
        numero_actual / total
    )

    # ======================================================
    # TARJETA DE VERIFICACIÓN
    # ======================================================

    with st.container(
        border=True
    ):

        st.markdown(
            f"### {pregunta['titulo']}"
        )

        st.write(
            pregunta[
                "descripcion"
            ]
        )

        respuesta = mostrar_control_verificacion(
            pregunta,
            transaccion
        )

    st.write("")

    # ======================================================
    # NAVEGACIÓN
    # ======================================================

    izquierda, centro, derecha = st.columns(
        [1, 2, 1]
    )

    # ------------------------------------------------------
    # ANTERIOR
    # ------------------------------------------------------

    with izquierda:

        if indice > 0:

            if st.button(
                "Anterior",
                use_container_width=True
            ):

                st.session_state[
                    "verificacion_actual"
                ] = indice - 1

                st.rerun()

    # ------------------------------------------------------
    # CANCELAR
    # ------------------------------------------------------

    with centro:

        if st.button(
            "Cancelar evaluación",
            use_container_width=True
        ):

            st.session_state[
                "pantalla"
            ] = "banca"

            st.session_state[
                "transaccion_pendiente"
            ] = None

            st.session_state[
                "respuestas_experto"
            ] = {}

            st.session_state[
                "verificacion_actual"
            ] = 0

            st.rerun()

    # ------------------------------------------------------
    # SIGUIENTE
    # ------------------------------------------------------

    with derecha:

        texto_boton = (
            "Iniciar inferencia"
            if numero_actual == total
            else "Confirmar"
        )

        if st.button(
            texto_boton,
            use_container_width=True,
            type="primary"
        ):

            st.session_state[
                "respuestas_experto"
            ][
                pregunta["campo"]
            ] = respuesta

            if numero_actual == total:

                finalizar_evaluacion()

            else:

                st.session_state[
                    "verificacion_actual"
                ] = indice + 1

                st.rerun()

# ==========================================================
# RESULTADO FINAL
# ==========================================================

def mostrar_resultado():
    """
    Presenta el resultado final de la evaluación
    de seguridad de la transacción.
    """

    resultado = st.session_state.get(
        "resultado_inferencia"
    )

    transaccion = st.session_state.get(
        "transaccion_analizada"
    )

    if not resultado or not transaccion:

        st.warning(
            "No existe un análisis disponible."
        )

        if st.button(
            "Regresar a la banca"
        ):

            st.session_state[
                "pantalla"
            ] = "banca"

            st.rerun()

        return

    # ======================================================
    # DATOS PRINCIPALES
    # ======================================================

    nivel = resultado[
        "nivel_riesgo"
    ]

    nombre_riesgo = obtener_nombre_riesgo(
        nivel
    )

    modo = transaccion.get(
        "modo_analisis",
        "guiado"
    )

    # ======================================================
    # CABECERA
    # ======================================================

    st.html(
        """
        <div class="bank-header">
            <div class="bank-brand">
                BANKSHIELD EXPERT
            </div>

            <div class="bank-subtitle">
                Resultado de la evaluación de seguridad
            </div>
        </div>
        """
    )

    st.subheader(
        "Evaluación final de la operación"
    )

    # ======================================================
    # MÉTRICAS
    # ======================================================

    col1, col2, col3, col4 = st.columns(
        4
    )

    with col1:

        st.metric(
            "Monto analizado",
            f"${transaccion['monto']:,.2f}"
        )

    with col2:

        st.metric(
            "Nivel de riesgo",
            nombre_riesgo
        )

    with col3:

        st.metric(
            "Reglas activadas",
            len(
                resultado[
                    "reglas_activadas"
                ]
            )
        )

    with col4:

        if modo == "guiado":

            st.metric(
                "Verificaciones",
                "10 / 10"
            )

        else:

            st.metric(
                "Modo",
                "Automático"
            )

    st.caption(
        f"Ciclos realizados por el motor de inferencia: "
        f"{resultado['iteraciones']}."
    )

    st.divider()

    # ======================================================
    # RESPUESTA BANCARIA SEGÚN EL RIESGO
    # ======================================================

    if nivel == "riesgo_bajo":

        st.success(
            "TRANSFERENCIA APROBADA\n\n"
            "La operación coincide con el comportamiento "
            "esperado de la cuenta y puede continuar."
        )

        estado_operacion = "Aprobada"

    elif nivel == "riesgo_moderado":

        st.warning(
            "VERIFICACIÓN ADICIONAL REQUERIDA\n\n"
            "La operación presenta algunas características "
            "inusuales. Se recomienda verificar la identidad "
            "del titular antes de procesarla."
        )

        estado_operacion = "Pendiente de verificación"

    elif nivel == "riesgo_alto":

        st.warning(
            "OPERACIÓN RETENIDA TEMPORALMENTE\n\n"
            "Se detectaron varios indicadores de comportamiento "
            "atípico. La transferencia requiere revisión antes "
            "de ser procesada."
        )

        estado_operacion = "En revisión"

    elif nivel == "riesgo_critico":

        st.error(
            "OPERACIÓN BLOQUEADA POR SEGURIDAD\n\n"
            "Se detectó una combinación de indicadores de "
            "riesgo que requiere impedir temporalmente el "
            "procesamiento de la transferencia y realizar "
            "una revisión de seguridad."
        )

        estado_operacion = "Bloqueada"

    else:

        st.info(
            "OPERACIÓN EN REVISIÓN\n\n"
            "La información disponible no permite establecer "
            "un nivel de riesgo definitivo."
        )

        estado_operacion = "En revisión"

    # ======================================================
    # RESUMEN DE LA OPERACIÓN
    # ======================================================

    st.subheader(
        "Resumen de la transacción"
    )

    col5, col6 = st.columns(2)

    with col5:

        st.write(
            f"**Beneficiario:** "
            f"{transaccion['beneficiario']}"
        )

        st.write(
            f"**Monto:** "
            f"${transaccion['monto']:,.2f}"
        )

        st.write(
            f"**Estado:** "
            f"{estado_operacion}"
        )

    with col6:

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
    # EXPLICACIÓN
    # ======================================================

    st.subheader(
        "Conclusión del sistema experto"
    )

    st.info(
        generar_explicacion(
            resultado
        )
    )

    # ======================================================
    # RAZONAMIENTO
    # ======================================================

    with st.expander(
        "Ver razonamiento del sistema experto"
    ):

        pestaña0, pestaña1, pestaña2, pestaña3 = st.tabs(
            [
                "Cadena principal",
                "Hechos iniciales",
                "Hechos inferidos",
                "Reglas activadas"
            ]
        )

        # --------------------------------------------------
        # CADENA PRINCIPAL
        # --------------------------------------------------

        with pestaña0:

            mostrar_cadena_inferencia(
                resultado
            )

        # --------------------------------------------------
        # HECHOS INICIALES
        # --------------------------------------------------

        with pestaña1:

            for hecho in sorted(
                resultado[
                    "hechos_iniciales"
                ]
            ):

                st.write(
                    f"• {humanizar_hecho(hecho)}"
                )

        # --------------------------------------------------
        # HECHOS INFERIDOS
        # --------------------------------------------------

        with pestaña2:

            if resultado[
                "hechos_inferidos"
            ]:

                for hecho in sorted(
                    resultado[
                        "hechos_inferidos"
                    ]
                ):

                    st.write(
                        f"• {humanizar_hecho(hecho)}"
                    )

            else:

                st.caption(
                    "No se generaron hechos adicionales."
                )

        # --------------------------------------------------
        # REGLAS
        # --------------------------------------------------

        with pestaña3:

            if resultado[
                "reglas_activadas"
            ]:

                for regla in resultado[
                    "reglas_activadas"
                ]:

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

                        for antecedente in regla[
                            "antecedentes"
                        ]:

                            st.write(
                                f"• "
                                f"{humanizar_hecho(antecedente)}"
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

            else:

                st.caption(
                    "No se activaron reglas."
                )

    # ======================================================
    # ACCIÓN RECOMENDADA
    # ======================================================

    st.subheader(
        "Acción del sistema"
    )

    st.write(
        obtener_accion_recomendada(
            nivel
        )
    )

    st.divider()

    # ======================================================
    # BOTONES
    # ======================================================

    columna1, columna2 = st.columns(2)

    with columna1:

        if st.button(
            "Volver a la banca",
            use_container_width=True
        ):

            st.session_state[
                "pantalla"
            ] = "banca"

            st.rerun()

    with columna2:

        if st.button(
            "Nueva simulación",
            use_container_width=True
        ):

            st.session_state[
                "pantalla"
            ] = "banca"

            st.session_state[
                "transaccion_pendiente"
            ] = None

            st.session_state[
                "transaccion_analizada"
            ] = None

            st.session_state[
                "resultado_inferencia"
            ] = None

            st.session_state[
                "respuestas_experto"
            ] = {}

            st.session_state[
                "verificacion_actual"
            ] = 0

            st.session_state[
                "ultima_evaluacion"
            ] = None

            st.rerun()