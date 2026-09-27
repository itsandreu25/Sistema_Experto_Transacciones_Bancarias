# ==========================================================
# GENERACIÓN DE HECHOS INICIALES
# Sistema experto para detección de posibles fraudes
# ==========================================================




def validar_transaccion(transaccion):
    """Valida los campos mínimos antes de generar hechos."""
    requeridos = {
        "monto",
        "ubicacion",
        "hora",
        "dispositivo",
        "beneficiario",
        "transacciones_ultima_hora",
        "intentos_fallidos",
    }
    faltantes = sorted(requeridos - set(transaccion))
    if faltantes:
        raise ValueError(
            "Faltan campos requeridos en la transacción: " + ", ".join(faltantes)
        )

    if float(transaccion["monto"]) <= 0:
        raise ValueError("El monto de la transacción debe ser mayor que cero.")

    hora = float(transaccion["hora"])
    if not 0 <= hora < 24:
        raise ValueError("La hora debe estar en el intervalo [0, 24).")

    if int(transaccion["transacciones_ultima_hora"]) < 0:
        raise ValueError("La frecuencia de transacciones no puede ser negativa.")

    if int(transaccion["intentos_fallidos"]) < 0:
        raise ValueError("Los intentos fallidos no pueden ser negativos.")

    if not str(transaccion["ubicacion"]).strip():
        raise ValueError("La ubicación no puede estar vacía.")
    if not str(transaccion["dispositivo"]).strip():
        raise ValueError("El dispositivo no puede estar vacío.")
    if not str(transaccion["beneficiario"]).strip():
        raise ValueError("El beneficiario no puede estar vacío.")

    autenticacion = transaccion.get("autenticacion_reforzada", "correcta")
    if autenticacion not in {"correcta", "fallida", "no_aplica"}:
        raise ValueError("Resultado de autenticación reforzada no válido.")

def normalizar_texto(texto):
    """
    Convierte un texto a minúsculas y elimina espacios
    innecesarios para facilitar las comparaciones.
    """
    return str(texto).strip().lower()


def analizar_monto(cliente, transaccion, hechos, detalles):
    """
    Compara el monto actual con el monto promedio habitual
    del cliente.
    """

    monto = float(transaccion["monto"])
    promedio = float(cliente["monto_promedio"])

    if promedio <= 0:
        razon = 0
    else:
        razon = monto / promedio

    detalles["monto"] = {
        "actual": monto,
        "promedio": promedio,
        "veces_promedio": round(razon, 2)
    }

    # Umbrales académicos para la simulación
    if razon <= 2:
        hechos.add("monto_habitual")

    elif razon <= 5:
        hechos.add("monto_elevado")

    else:
        hechos.add("monto_muy_inusual")


def analizar_dispositivo(cliente, transaccion, hechos, detalles):
    """
    Determina si el dispositivo utilizado está reconocido.

    Si la transacción contiene el campo
    'dispositivo_reconocido', se utiliza dicho metadato.

    Esto simula el comportamiento de un sistema bancario real,
    donde el reconocimiento del dispositivo no depende solamente
    de su nombre visible, sino de identificadores registrados.

    Si el campo no existe, se mantiene la comparación tradicional
    contra los dispositivos almacenados en el perfil.
    """

    dispositivo_actual = normalizar_texto(
        transaccion["dispositivo"]
    )

    # ======================================================
    # OPCIÓN 1
    # El sistema bancario ya conoce si el dispositivo
    # está registrado.
    # ======================================================

    if "dispositivo_reconocido" in transaccion:

        conocido = bool(
            transaccion["dispositivo_reconocido"]
        )

    # ======================================================
    # OPCIÓN 2
    # Compatibilidad con las pruebas anteriores.
    # ======================================================

    else:

        dispositivos_conocidos = [
            normalizar_texto(dispositivo)
            for dispositivo
            in cliente["dispositivos_conocidos"]
        ]

        conocido = (
            dispositivo_actual
            in dispositivos_conocidos
        )

    # ======================================================
    # GENERAR HECHO
    # ======================================================

    if conocido:

        hechos.add(
            "dispositivo_conocido"
        )

    else:

        hechos.add(
            "dispositivo_nuevo"
        )

    detalles["dispositivo"] = {

        "actual":
            transaccion["dispositivo"],

        "conocido":
            conocido
    }

def analizar_ubicacion(cliente, transaccion, hechos, detalles):
    """
    Determina si la operación proviene de una ubicación
    habitual para el cliente.
    """

    ubicacion_actual = normalizar_texto(
        transaccion["ubicacion"]
    )

    ubicaciones_habituales = [
        normalizar_texto(ubicacion)
        for ubicacion in cliente["ubicaciones_habituales"]
    ]

    if ubicacion_actual in ubicaciones_habituales:
        hechos.add("ubicacion_habitual")
        habitual = True
    else:
        hechos.add("ubicacion_nueva")
        habitual = False

    detalles["ubicacion"] = {
        "actual": transaccion["ubicacion"],
        "habitual": habitual
    }


def analizar_horario(cliente, transaccion, hechos, detalles):
    """
    Determina si la transacción se realizó dentro del horario
    habitual del cliente.

    La hora se representa como un número decimal.
    Ejemplos:
        8.0  = 08:00
        14.5 = 14:30
        22.25 = 22:15
    """

    hora = float(transaccion["hora"])

    inicio = float(cliente["hora_inicio"])
    fin = float(cliente["hora_fin"])

    if inicio <= hora <= fin:
        hechos.add("horario_habitual")
        habitual = True
    else:
        hechos.add("horario_inusual")
        habitual = False

    detalles["horario"] = {
        "hora": hora,
        "inicio_habitual": inicio,
        "fin_habitual": fin,
        "habitual": habitual
    }


def analizar_beneficiario(cliente, transaccion, hechos, detalles):
    """
    Determina si el beneficiario ya pertenece al conjunto
    habitual de destinatarios del cliente.
    """

    beneficiario_actual = normalizar_texto(
        transaccion["beneficiario"]
    )

    beneficiarios_habituales = [
        normalizar_texto(beneficiario)
        for beneficiario in cliente["beneficiarios_habituales"]
    ]

    if beneficiario_actual in beneficiarios_habituales:
        hechos.add("beneficiario_conocido")
        conocido = True
    else:
        hechos.add("beneficiario_nuevo")
        conocido = False

    detalles["beneficiario"] = {
        "actual": transaccion["beneficiario"],
        "conocido": conocido
    }


def analizar_frecuencia(cliente, transaccion, hechos, detalles):
    """
    Compara el número de operaciones realizadas en la última
    hora con la frecuencia habitual del cliente.
    """

    cantidad = int(transaccion["transacciones_ultima_hora"])

    max_habitual = int(
        cliente["transacciones_hora_max"]
    )

    if cantidad <= max_habitual:
        hechos.add("frecuencia_normal")
        nivel = "normal"

    elif cantidad <= max_habitual * 2:
        hechos.add("frecuencia_elevada")
        nivel = "elevada"

    else:
        hechos.add("frecuencia_muy_alta")
        nivel = "muy alta"

    detalles["frecuencia"] = {
        "transacciones_ultima_hora": cantidad,
        "maximo_habitual": max_habitual,
        "nivel": nivel
    }


def analizar_intentos_fallidos(transaccion, hechos, detalles):
    """
    Clasifica la cantidad de intentos fallidos de
    autenticación.
    """

    intentos = int(transaccion["intentos_fallidos"])

    if intentos == 0:
        hechos.add("autenticacion_normal")
        nivel = "normal"

    elif intentos <= 2:
        hechos.add("algunos_intentos_fallidos")
        nivel = "advertencia"

    else:
        hechos.add("multiples_intentos_fallidos")
        nivel = "sospechoso"

    detalles["intentos_fallidos"] = {
        "cantidad": intentos,
        "nivel": nivel
    }


def analizar_saldo(cliente, transaccion, hechos, detalles):
    """
    Analiza qué porcentaje del saldo disponible representa
    la transacción.
    """

    monto = float(transaccion["monto"])
    saldo = float(
        transaccion.get("saldo_disponible", cliente["saldo"])
    )

    if saldo <= 0:
        porcentaje = 0
    else:
        porcentaje = (monto / saldo) * 100

    if porcentaje >= 80:
        hechos.add("porcentaje_saldo_muy_alto")

    elif porcentaje >= 50:
        hechos.add("porcentaje_saldo_alto")

    else:
        hechos.add("porcentaje_saldo_normal")

    detalles["saldo"] = {
        "saldo_disponible": saldo,
        "monto": monto,
        "porcentaje_utilizado": round(porcentaje, 2)
    }


def analizar_factores_adicionales(transaccion, hechos, detalles):
    """
    Procesa la información complementaria obtenida durante
    las 10 verificaciones del sistema experto.
    """

    # ======================================================
    # P03 - Cambio reciente de credenciales
    # ======================================================

    if transaccion.get("credenciales_modificadas", False):
        hechos.add("credenciales_modificadas")
    else:
        hechos.add("credenciales_sin_cambios")


    # ======================================================
    # P04 - Nueva sesión reciente
    # ======================================================

    if transaccion.get("sesion_nueva_reciente", False):
        hechos.add("sesion_nueva_reciente")
    else:
        hechos.add("sin_sesion_nueva_reciente")


    # ======================================================
    # P05 - Autenticación adicional
    # ======================================================

    autenticacion = transaccion.get(
        "autenticacion_reforzada",
        "correcta"
    )

    if autenticacion == "correcta":

        hechos.add(
            "autenticacion_reforzada_correcta"
        )

    elif autenticacion == "fallida":

        hechos.add(
            "autenticacion_reforzada_fallida"
        )

    elif autenticacion == "no_aplica":

        hechos.add(
            "autenticacion_reforzada_no_aplica"
        )


    # ======================================================
    # P06 - Múltiples beneficiarios
    # ======================================================

    if transaccion.get(
        "multiples_beneficiarios",
        False
    ):

        hechos.add(
            "multiples_beneficiarios"
        )

    else:

        hechos.add(
            "beneficiarios_sin_variacion"
        )


    # ======================================================
    # P07 - Incompatibilidad geográfica
    # ======================================================

    if transaccion.get(
        "sesiones_geograficamente_incompatibles",
        False
    ):

        hechos.add(
            "sesiones_geograficamente_incompatibles"
        )

    else:

        hechos.add(
            "sin_incompatibilidad_geografica"
        )


    # ======================================================
    # P08 - Operaciones similares
    # ======================================================

    if transaccion.get(
        "operaciones_similares",
        False
    ):

        hechos.add(
            "patron_conocido"
        )

    else:

        hechos.add(
            "patron_no_habitual"
        )


    # ======================================================
    # P09 - Beneficiario agregado recientemente
    # ======================================================

    if transaccion.get(
        "beneficiario_registrado_recientemente",
        False
    ):

        hechos.add(
            "beneficiario_registrado_recientemente"
        )

    else:

        hechos.add(
            "beneficiario_no_registrado_recientemente"
        )


    # ======================================================
    # P10 - Cambio reciente en límite de transferencias
    # ======================================================

    if transaccion.get(
        "limite_transferencia_modificado",
        False
    ):

        hechos.add(
            "limite_transferencia_modificado"
        )

    else:

        hechos.add(
            "limite_transferencia_sin_cambios"
        )


    # ======================================================
    # DETALLES
    # ======================================================

    detalles["factores_adicionales"] = {

        "credenciales_modificadas":
            transaccion.get(
                "credenciales_modificadas",
                False
            ),

        "sesion_nueva_reciente":
            transaccion.get(
                "sesion_nueva_reciente",
                False
            ),

        "autenticacion_reforzada":
            autenticacion,

        "multiples_beneficiarios":
            transaccion.get(
                "multiples_beneficiarios",
                False
            ),

        "sesiones_geograficamente_incompatibles":
            transaccion.get(
                "sesiones_geograficamente_incompatibles",
                False
            ),

        "operaciones_similares":
            transaccion.get(
                "operaciones_similares",
                False
            ),

        "beneficiario_registrado_recientemente":
            transaccion.get(
                "beneficiario_registrado_recientemente",
                False
            ),

        "limite_transferencia_modificado":
            transaccion.get(
                "limite_transferencia_modificado",
                False
            )
    }

def generar_hechos_iniciales(cliente, transaccion):
    """
    Función principal.

    Recibe:
        - un cliente
        - una transacción

    Devuelve:
        - conjunto de hechos iniciales
        - detalles del análisis realizado
    """

    validar_transaccion(transaccion)

    hechos = set()
    detalles = {}

    analizar_monto(
        cliente,
        transaccion,
        hechos,
        detalles
    )

    analizar_dispositivo(
        cliente,
        transaccion,
        hechos,
        detalles
    )

    analizar_ubicacion(
        cliente,
        transaccion,
        hechos,
        detalles
    )

    analizar_horario(
        cliente,
        transaccion,
        hechos,
        detalles
    )

    analizar_beneficiario(
        cliente,
        transaccion,
        hechos,
        detalles
    )

    analizar_frecuencia(
        cliente,
        transaccion,
        hechos,
        detalles
    )

    analizar_intentos_fallidos(
        transaccion,
        hechos,
        detalles
    )

    analizar_saldo(
        cliente,
        transaccion,
        hechos,
        detalles
    )

    analizar_factores_adicionales(
        transaccion,
        hechos,
        detalles
    )

    return hechos, detalles