import socket
from datetime import datetime, time
from uuid import uuid4
import streamlit as st

from datos.clientes import clientes
from datos.movimientos import MOVIMIENTOS
from datos.escenarios import ESCENARIOS_SEGURIDAD

# ==========================================================
# DISPOSITIVO
# ==========================================================

def obtener_dispositivo_local():
    """
    Obtiene el nombre del equipo donde se ejecuta la
    aplicación.

    En ejecución local corresponde normalmente al equipo
    utilizado para la demostración.
    """

    try:

        nombre = socket.gethostname()

        if nombre:
            return nombre

    except Exception:
        pass

    return "Equipo-local"


# ==========================================================
# HORA
# ==========================================================
def obtener_hora_actual():
    """
    Obtiene la hora actual del equipo donde se ejecuta
    BankShield Expert.

    En la demostración local corresponde a la hora
    del computador que ejecuta Streamlit.
    """

    ahora = datetime.now()

    return time(
        ahora.hour,
        ahora.minute
    )

def hora_a_decimal(hora):
    """
    Convierte datetime.time a número decimal.

    Ejemplos:
        14:00 -> 14.0
        14:30 -> 14.5
        23:15 -> 23.25
    """

    return (
        hora.hour
        +
        hora.minute / 60
    )


# ==========================================================
# MOVIMIENTOS
# ==========================================================

def mostrar_movimientos(codigo_cliente):
    """
    Muestra los movimientos históricos y las operaciones
    realizadas durante la sesión actual.
    """

    movimientos = st.session_state.get(
        "movimientos_sesion",
        MOVIMIENTOS
    ).get(
        codigo_cliente,
        []
    )

    for movimiento in movimientos:

        estado = movimiento.get(
            "estado"
        )

        monto = movimiento.get(
            "monto",
            0
        )

        monto_operacion = movimiento.get(
            "monto_operacion",
            abs(monto)
        )

        with st.container(
            border=True
        ):

            izquierda, derecha = st.columns(
                [2.8, 1.2]
            )

            with izquierda:

                st.markdown(
                    f"**{movimiento['descripcion']}**"
                )

                texto_secundario = (
                    f"{movimiento['fecha']} · "
                    f"{movimiento['tipo']}"
                )

                if estado:

                    texto_secundario += (
                        f" · {estado}"
                    )

                st.caption(
                    texto_secundario
                )

            with derecha:

                # ==================================================
                # APROBADA
                # ==================================================

                if estado == "Aprobada":

                    st.markdown(
                        (
                            '<div class="movement-negative">'
                            f'-${monto_operacion:,.2f}'
                            '</div>'
                        ),
                        unsafe_allow_html=True
                    )

                # ==================================================
                # PENDIENTE
                # ==================================================

                elif estado == "Pendiente de verificación":

                    st.markdown(
                        f"**${monto_operacion:,.2f}**"
                    )

                    st.caption(
                        "Pendiente"
                    )

                # ==================================================
                # EN REVISIÓN
                # ==================================================

                elif estado == "En revisión":

                    st.markdown(
                        f"**${monto_operacion:,.2f}**"
                    )

                    st.caption(
                        "En revisión"
                    )

                # ==================================================
                # BLOQUEADA
                # ==================================================

                elif estado == "Bloqueada":

                    st.markdown(
                        f"**${monto_operacion:,.2f}**"
                    )

                    st.caption(
                        "Bloqueada"
                    )

                # ==================================================
                # MOVIMIENTOS HISTÓRICOS
                # ==================================================

                else:

                    if monto >= 0:

                        st.markdown(
                            (
                                '<div class="movement-positive">'
                                f'+${monto:,.2f}'
                                '</div>'
                            ),
                            unsafe_allow_html=True
                        )

                    else:

                        st.markdown(
                            (
                                '<div class="movement-negative">'
                                f'-${abs(monto):,.2f}'
                                '</div>'
                            ),
                            unsafe_allow_html=True
                        )
                        
# ==========================================================
# PERFIL DEL CLIENTE
# ==========================================================

def mostrar_perfil(cliente):

    st.markdown(
        '<div class="section-title">'
        'Perfil habitual de la cuenta'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Monto promedio",
            f"${cliente['monto_promedio']:,.2f}"
        )

    with col2:

        ubicaciones = ", ".join(
            cliente["ubicaciones_habituales"]
        )

        st.metric(
            "Ubicación habitual",
            ubicaciones
        )

    with col3:

        st.metric(
            "Operaciones por hora",
            (
                f"{cliente['transacciones_hora_min']}"
                f"–"
                f"{cliente['transacciones_hora_max']}"
            )
        )
    st.caption(
        "Estos valores representan el comportamiento "
        "histórico simulado de la cuenta."
    )

# ==========================================================
# FORMULARIO DE TRANSFERENCIA
# ==========================================================

def formulario_transferencia(
    codigo_cliente,
    cliente,
    saldo_actual,
    dispositivo_detectado,
    dispositivo_reconocido,
    ubicacion_detectada,
    hora_detectada,
    datos_seguridad,
    modo_analisis
):

    st.markdown(
        '<div class="section-title">'
        'Nueva transferencia'
        '</div>',
        unsafe_allow_html=True
    )

    # ======================================================
    # CONTENEDOR VISUAL
    # ======================================================

    with st.container(
        border=True
    ):

        # ==================================================
        # FILA 1
        # BENEFICIARIO | MONTO
        # ==================================================

        col1, col2 = st.columns(
            2,
            gap="medium"
        )

        with col1:

            opciones_beneficiario = (
                cliente["beneficiarios_habituales"]
                +
                ["Nuevo beneficiario"]
            )

            beneficiario_opcion = st.selectbox(
                "Beneficiario",
                opciones_beneficiario,
                key=(
                    f"beneficiario_"
                    f"{codigo_cliente}"
                ),
                help=(
                    "Seleccione un beneficiario habitual "
                    "o agregue uno nuevo."
                )
            )

        with col2:

            monto = st.number_input(
                "Monto de la transferencia",
                min_value=0.00,
                max_value=float(
                    saldo_actual
                ),
                value=0.00,
                step=10.00,
                format="%.2f",
                key=(
                    f"monto_"
                    f"{codigo_cliente}"
                ),
                help=(
                    "Ingrese el valor que desea transferir."
                )
            )

        # ==================================================
        # NUEVO BENEFICIARIO
        # ==================================================

        if beneficiario_opcion == "Nuevo beneficiario":

            st.markdown(
                "**Datos del nuevo beneficiario**"
            )

            beneficiario = st.text_input(
                "Nombre del nuevo beneficiario",
                placeholder="Ej. Juan Pérez",
                key=(
                    f"nuevo_beneficiario_"
                    f"{codigo_cliente}"
                )
            )

        else:

            beneficiario = beneficiario_opcion

        # ==================================================
        # FILA 2
        # UBICACIÓN | DISPOSITIVO
        # ==================================================

        col3, col4 = st.columns(
            2,
            gap="medium"
        )

        with col3:

            st.text_input(
                "Ubicación detectada",
                value=ubicacion_detectada,
                disabled=True,
                key=(
                    f"ubicacion_detectada_"
                    f"{codigo_cliente}"
                ),
                help=(
                    "Se obtiene automáticamente del "
                    "contexto de la sesión. En esta "
                    "simulación puede configurarse desde "
                    "el panel lateral."
                )
            )

        with col4:

            st.text_input(
                "Dispositivo detectado",
                value=dispositivo_detectado,
                disabled=True,
                key=(
                    f"dispositivo_detectado_"
                    f"{codigo_cliente}"
                ),
                help=(
                    "Se obtiene automáticamente del "
                    "entorno donde se ejecuta la aplicación."
                )
            )

        # ==================================================
        # FILA 3
        # HORA | CONCEPTO
        # ==================================================

        col5, col6 = st.columns(
            2,
            gap="medium"
        )

        with col5:

            st.text_input(
                "Hora detectada",
                value=hora_detectada.strftime(
                    "%H:%M"
                ),
                disabled=True,
                key=(
                    f"hora_detectada_"
                    f"{codigo_cliente}"
                ),
                help=(
                    "La hora se registra automáticamente. "
                    "Puede simularse una hora diferente "
                    "desde el panel de demostración."
                )
            )

        with col6:

            concepto = st.text_input(
                "Concepto de la transferencia",
                placeholder="Ej. Pago de servicios",
                key=(
                    f"concepto_"
                    f"{codigo_cliente}"
                ),
                help=(
                    "Descripción opcional de la operación."
                )
            )

        # ==================================================
        # INFORMACIÓN
        # ==================================================

        st.divider()

        st.caption(
            "Antes de procesar la operación, BankShield Expert "
            "realizará una evaluación de seguridad mediante "
            "su sistema experto basado en reglas."
        )

        # ==================================================
        # BOTÓN
        # ==================================================

        enviar = st.button(
            "Continuar con la transferencia",
            use_container_width=True,
            type="primary",
            key=(
                f"continuar_transferencia_"
                f"{codigo_cliente}"
            )
        )

    # ======================================================
    # VALIDACIONES
    # ======================================================

    if enviar:

        errores = []

        if monto <= 0:

            errores.append(
                "El monto debe ser mayor que cero."
            )

        if (
            beneficiario_opcion
            == "Nuevo beneficiario"
            and not beneficiario.strip()
        ):

            errores.append(
                "Debe ingresar el nombre del nuevo beneficiario."
            )

        if monto > saldo_actual:

            errores.append(
                "El saldo disponible es insuficiente."
            )

        if errores:

            for error in errores:

                st.error(
                    error
                )

            return

        # ==================================================
        # TRANSACCIÓN
        # ==================================================

        transaccion = {
            "id_transaccion":
                f"TRX-{uuid4().hex[:8].upper()}",

            "fecha_registro":
                datetime.now().strftime(
                    "%d/%m/%Y"
                ),

            "fecha_hora_registro":
                datetime.now().strftime(
                    "%d/%m/%Y %H:%M:%S"
                ),

            "cliente_id":
                codigo_cliente,

            "monto":
                float(monto),

            "saldo_disponible":
                float(saldo_actual),

            "ubicacion":
                ubicacion_detectada,

            "hora":
                hora_a_decimal(
                    hora_detectada
                ),

            "hora_texto":
                hora_detectada.strftime(
                    "%H:%M"
                ),

            "dispositivo":
                dispositivo_detectado,

            "dispositivo_reconocido":
                dispositivo_reconocido,

            "beneficiario":
                beneficiario.strip(),

            "concepto":
                concepto.strip()
        }

        # ==================================================
        # DATOS INTERNOS DEL SISTEMA BANCARIO
        # ==================================================

        transaccion.update(
            datos_seguridad
        )


        # ==================================================
        # AJUSTES DERIVADOS DE LA OPERACIÓN ACTUAL
        # ==================================================

        # Si el dispositivo no está registrado, también
        # consideramos que existe una nueva sesión reciente.
        if not dispositivo_reconocido:

            transaccion[
                "sesion_nueva_reciente"
            ] = True


        # Si se acaba de ingresar un nuevo beneficiario,
        # lo consideramos recientemente registrado.
        if beneficiario_opcion == "Nuevo beneficiario":

            transaccion[
                "beneficiario_registrado_recientemente"
            ] = True


        # ==================================================
        # DETERMINAR SI LA OPERACIÓN SE PARECE AL PATRÓN
        # HABITUAL DEL CLIENTE
        # ==================================================

        hora_decimal = hora_a_decimal(
            hora_detectada
        )

        horario_habitual = (
            cliente["hora_inicio"]
            <= hora_decimal
            <= cliente["hora_fin"]
        )

        ubicacion_habitual = (
            ubicacion_detectada
            in cliente["ubicaciones_habituales"]
        )

        beneficiario_habitual = (
            beneficiario.strip()
            in cliente["beneficiarios_habituales"]
        )

        monto_compatible = (
            float(monto)
            <= cliente["monto_promedio"] * 2
        )

        contexto_compatible = all(
            [
                dispositivo_reconocido,
                ubicacion_habitual,
                horario_habitual,
                beneficiario_habitual,
                monto_compatible
            ]
        )

        # Solo puede considerarse similar si tanto el
        # historial simulado como la operación actual
        # son compatibles.
        transaccion[
            "operaciones_similares"
        ] = (
            bool(
                transaccion.get(
                    "operaciones_similares",
                    False
                )
            )
            and contexto_compatible
        )


        # ==================================================
        # MODO DE ANÁLISIS
        # ==================================================

        transaccion[
            "modo_analisis"
        ] = modo_analisis

        # ==================================================
        # PREPARAR SISTEMA EXPERTO
        # ==================================================

        st.session_state[
            "transaccion_pendiente"
        ] = transaccion

        st.session_state[
            "respuestas_experto"
        ] = {}

        st.session_state[
            "verificacion_actual"
        ] = 0

        st.session_state[
            "pantalla"
        ] = "evaluacion"

        st.rerun()
        
# ==========================================================
# BANCA
# ==========================================================

def mostrar_banca():

    # ======================================================
    # CABECERA
    # ======================================================

    st.html(
        """
        <div class="bank-header">
            <div class="bank-brand">BANKSHIELD</div>
            <div class="bank-subtitle">
                Banca Digital · Protección inteligente de transacciones
            </div>
        </div>
        """
    )

    st.caption(
        "Entorno académico de simulación. "
        "Todos los clientes y datos son ficticios."
    )

    # ======================================================
    # CLIENTE
    # ======================================================

    codigo_cliente = st.selectbox(
        "Cliente de demostración",
        options=list(
            clientes.keys()
        ),
        format_func=lambda codigo:
            clientes[codigo]["nombre"]
    )

    cliente = clientes[
        codigo_cliente
    ]

    saldo_actual = st.session_state[
        "saldos_sesion"
    ][codigo_cliente]

    # ======================================================
    # RESULTADO DE LA ÚLTIMA OPERACIÓN
    # ======================================================

    ultima_evaluacion = st.session_state.get(
        "ultima_evaluacion"
    )

    if ultima_evaluacion:

        ultima_transaccion = ultima_evaluacion[
            "transaccion"
        ]

        ultimo_resultado = ultima_evaluacion[
            "resultado"
        ]

        # Solo mostramos la operación correspondiente
        # al cliente actualmente seleccionado.
        if (
            ultima_transaccion.get(
                "cliente_id"
            )
            == codigo_cliente
        ):

            ultimo_nivel = ultimo_resultado[
                "nivel_riesgo"
            ]

            st.markdown(
                "### Estado de la última operación"
            )

            if ultimo_nivel == "riesgo_bajo":

                st.success(
                    f"TRANSFERENCIA APROBADA · "
                    f"${ultima_transaccion['monto']:,.2f} "
                    f"a {ultima_transaccion['beneficiario']}."
                )

            elif ultimo_nivel == "riesgo_moderado":

                st.warning(
                    "VERIFICACIÓN ADICIONAL REQUERIDA · "
                    f"La transferencia de "
                    f"${ultima_transaccion['monto']:,.2f} "
                    "permanece pendiente."
                )

            elif ultimo_nivel == "riesgo_alto":

                st.warning(
                    "OPERACIÓN EN REVISIÓN · "
                    f"La transferencia de "
                    f"${ultima_transaccion['monto']:,.2f} "
                    "ha sido retenida temporalmente."
                )

            elif ultimo_nivel == "riesgo_critico":

                st.error(
                    "OPERACIÓN BLOQUEADA · "
                    f"La transferencia de "
                    f"${ultima_transaccion['monto']:,.2f} "
                    "no fue procesada debido a la evaluación "
                    "de seguridad."
                )

            st.write("")

    st.session_state[
        "cliente_actual"
    ] = codigo_cliente

    # ======================================================
    # DISPOSITIVO DETECTADO
    # ======================================================

    dispositivo_detectado = (
        obtener_dispositivo_local()
    )

    # ======================================================
    # PANEL DE CONTROL DE LA SIMULACIÓN
    # ======================================================

    with st.sidebar:

        st.title(
            "Panel de demostración"
        )

        st.caption(
            "Estos controles existen únicamente para "
            "simular diferentes escenarios del sistema experto."
        )

        st.divider()

        if st.button(
            "Historial de evaluaciones",
            use_container_width=True
        ):

            st.session_state[
                "pantalla"
            ] = "historial"

            st.rerun()

        # ======================================================
        # DISPOSITIVO
        # ======================================================

        st.subheader(
            "Dispositivo"
        )

        st.caption(
            "Equipo detectado automáticamente"
        )

        st.code(
            dispositivo_detectado,
            language=None
        )

        dispositivo_reconocido = st.toggle(
            "Dispositivo registrado",
            value=True,
            key=(
                f"dispositivo_reconocido_"
                f"{codigo_cliente}"
            ),
            help=(
                "Activado: el banco reconoce el equipo. "
                "Desactivado: se considera un dispositivo nuevo."
            )
        )

        if dispositivo_reconocido:

            st.success(
                "Dispositivo conocido"
            )

        else:

            st.warning(
                "Dispositivo no reconocido"
            )

        # ======================================================
        # UBICACIÓN
        # ======================================================

        st.divider()

        st.subheader(
            "Ubicación de la sesión"
        )

        st.caption(
            "En una aplicación real esta información sería "
            "obtenida automáticamente. Aquí se simula para "
            "probar diferentes escenarios."
        )

        ciudades_demo = [
            "Riobamba",
            "Quito",
            "Guayaquil",
            "Cuenca",
            "Ambato",
            "Loja",
            "Manta"
        ]

        # Primero colocamos las ubicaciones habituales
        # del cliente.
        opciones_ubicacion = []

        for ciudad in (
            cliente["ubicaciones_habituales"]
            +
            ciudades_demo
        ):

            if ciudad not in opciones_ubicacion:
                opciones_ubicacion.append(
                    ciudad
                )

        ubicacion_detectada = st.selectbox(
            "Ubicación simulada",
            opciones_ubicacion,
            key=(
                f"ubicacion_demo_"
                f"{codigo_cliente}"
            ),
            help=(
                "Este control pertenece al entorno de "
                "demostración y no a la banca del cliente."
            )
        )

        if ubicacion_detectada in cliente[
            "ubicaciones_habituales"
        ]:

            st.success(
                "Ubicación habitual"
            )

        else:

            st.warning(
                "Ubicación no habitual"
            )

        # ======================================================
        # HORA DE LA SESIÓN
        # ======================================================

        st.divider()

        st.subheader(
            "Hora de la sesión"
        )

        hora_actual = obtener_hora_actual()

        st.caption(
            "La hora se registra automáticamente. "
            "Para fines de demostración puede simularse "
            "un horario diferente."
        )

        simular_hora = st.toggle(
            "Simular una hora diferente",
            value=False,
            key=(
                f"simular_hora_"
                f"{codigo_cliente}"
            )
        )

        if simular_hora:

            hora_detectada = st.time_input(
                "Hora simulada",
                value=hora_actual,
                key=(
                    f"hora_demo_"
                    f"{codigo_cliente}"
                )
            )

        else:

            hora_detectada = hora_actual

            st.code(
                hora_detectada.strftime("%H:%M"),
                language=None
            )

        # ======================================================
        # CONTEXTO INTERNO DE SEGURIDAD
        # ======================================================

        st.divider()

        st.subheader(
            "Contexto de seguridad"
        )

        st.caption(
            "Simula la información obtenida de los "
            "registros internos del sistema bancario."
        )

        escenario_id = st.selectbox(
            "Escenario interno",
            options=list(
                ESCENARIOS_SEGURIDAD.keys()
            ),
            format_func=lambda codigo:
                ESCENARIOS_SEGURIDAD[codigo]["nombre"],
            key=(
                f"escenario_seguridad_"
                f"{codigo_cliente}"
            )
        )

        escenario = ESCENARIOS_SEGURIDAD[
            escenario_id
        ]

        datos_seguridad = dict(
            escenario["datos"]
        )

        st.info(
            escenario[
                "descripcion"
            ]
        )


        # ======================================================
        # MODO DE EJECUCIÓN
        # ======================================================

        st.divider()

        st.subheader(
            "Modo de evaluación"
        )

        modo_analisis = st.radio(
            "Seleccionar modo",
            options=[
                "guiado",
                "automatico"
            ],
            format_func=lambda modo:
                (
                    "Demostración guiada · 10 verificaciones"
                    if modo == "guiado"
                    else "Análisis automático"
                ),
            key=(
                f"modo_analisis_"
                f"{codigo_cliente}"
            )
        )

        if modo_analisis == "guiado":

            st.caption(
                "Un analista confirmará 10 variables "
                "antes de ejecutar la inferencia."
            )

        else:

            st.caption(
                "La banca enviará automáticamente los "
                "datos al motor de inferencia."
            )
        
        # ------------------------------------------------------
        # COMPARACIÓN CON EL PERFIL HABITUAL
        # ------------------------------------------------------

        hora_decimal = hora_a_decimal(
            hora_detectada
        )

        if (
            cliente["hora_inicio"]
            <= hora_decimal
            <= cliente["hora_fin"]
        ):

            st.success(
                "Horario habitual"
            )

        else:

            st.warning(
                "Horario no habitual"
            )

        # ======================================================
        # ACLARACIÓN
        # ======================================================

        st.divider()

        st.caption(
            "Este panel no representa controles disponibles "
            "para un cliente real. Sirve únicamente para "
            "demostrar el comportamiento del sistema experto."
        )
    # ======================================================
    # RESUMEN DE CUENTA
    # ======================================================

    izquierda, derecha = st.columns(
        [1.15, 1],
        gap="large"
    )

    with izquierda:

        st.html(
    f"""
    <div class="balance-card">
        <div class="balance-label">
            Saldo disponible
        </div>

        <div class="balance-value">
            ${saldo_actual:,.2f}
        </div>

        <div class="account-number">
            CUENTA {cliente["cuenta"]}
        </div>

        <div style="
            margin-top:15px;
            font-size:13px;
            opacity:0.8;
            color:white;
        ">
            Cuenta de ahorros
        </div>
    </div>
    """
)

    with derecha:

        st.html(
    f"""
    <div class="bank-card" style="min-height:190px;">
        <div class="profile-small">
            TITULAR
        </div>

        <div class="profile-title">
            {cliente["nombre"]}
        </div>

        <br>

        <span class="badge-safe">
            PERFIL ACTIVO
        </span>

        <div style="
            margin-top:24px;
            color:#637083;
            font-size:13px;
        ">
            BankShield comparará la nueva operación
            con el comportamiento habitual de este cliente.
        </div>
    </div>
    """
)

    # ======================================================
    # PERFIL
    # ======================================================

    mostrar_perfil(
        cliente
    )

    # ======================================================
    # TRANSFERENCIA + MOVIMIENTOS
    # ======================================================

    columna_transferencia, columna_movimientos = (
        st.columns(
            [1.25, 0.75],
            gap="large"
        )
    )

    with columna_transferencia:
        formulario_transferencia(
            codigo_cliente,
            cliente,
            saldo_actual,
            dispositivo_detectado,
            dispositivo_reconocido,
            ubicacion_detectada,
            hora_detectada,
            datos_seguridad,
            modo_analisis
        )

    with columna_movimientos:

        st.markdown(
            '<div class="section-title">'
            'Movimientos recientes'
            '</div>',
            unsafe_allow_html=True
        )

        mostrar_movimientos(
            codigo_cliente
        )