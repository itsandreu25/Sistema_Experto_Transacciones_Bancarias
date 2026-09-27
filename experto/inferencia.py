# ==========================================================
# MOTOR DE INFERENCIA
# Sistema experto para detección de posibles fraudes
# ==========================================================
#
# El motor utiliza encadenamiento hacia adelante.
#
# Proceso:
# 1. Recibe los hechos iniciales.
# 2. Revisa todas las reglas.
# 3. Si todos los antecedentes de una regla están presentes,
#    la regla se activa.
# 4. La conclusión se agrega como un nuevo hecho.
# 5. El proceso se repite hasta que ninguna regla genere
#    hechos nuevos.
# ==========================================================

from experto.reglas import reglas, RIESGOS_FINALES


def motor_inferencia(hechos_iniciales):
    """
    Ejecuta encadenamiento hacia adelante.

    Parámetros:
        hechos_iniciales:
            Conjunto de hechos obtenidos antes de comenzar
            la inferencia.

    Retorna:
        Un diccionario con:
            - hechos_iniciales
            - hechos_finales
            - hechos_inferidos
            - reglas_activadas
            - nivel_riesgo
            - riesgo_codigo
            - iteraciones
    """

    # Copiamos los hechos iniciales para no modificar
    # directamente el conjunto original.
    hechos = set(hechos_iniciales)

    # Guardaremos las reglas que ya fueron activadas.
    reglas_activadas_ids = set()

    # Aquí almacenaremos información completa de cada
    # inferencia realizada.
    traza = []

    # Número de vueltas completas realizadas por el motor.
    iteraciones = 0

    # Mientras se produzca al menos un nuevo hecho,
    # continuaremos revisando las reglas.
    hubo_cambio = True

    while hubo_cambio:

        hubo_cambio = False
        iteraciones += 1

        for regla in reglas:

            regla_id = regla["id"]

            # Si la regla ya fue utilizada, no necesitamos
            # volver a activarla.
            if regla_id in reglas_activadas_ids:
                continue

            antecedentes = set(regla["si"])
            conclusion = regla["entonces"]

            # La regla se activa solamente si TODOS sus
            # antecedentes están presentes.
            if antecedentes.issubset(hechos):

                reglas_activadas_ids.add(regla_id)

                conclusion_nueva = conclusion not in hechos

                # Registramos la regla aunque otra regla haya
                # producido previamente la misma conclusión.
                traza.append({
                    "id": regla["id"],
                    "nivel": regla["nivel"],
                    "antecedentes": list(regla["si"]),
                    "conclusion": conclusion,
                    "descripcion": regla["descripcion"],
                    "nuevo_hecho": conclusion_nueva,
                    "iteracion": iteraciones
                })

                # Solo existe cambio lógico si aparece un
                # hecho que todavía no conocíamos.
                if conclusion_nueva:
                    hechos.add(conclusion)
                    hubo_cambio = True

    # ======================================================
    # HECHOS INFERIDOS
    # ======================================================

    hechos_inferidos = hechos.difference(
        set(hechos_iniciales)
    )

    # ======================================================
    # NIVEL FINAL DE RIESGO
    # ======================================================

    nivel_riesgo, riesgo_codigo = determinar_riesgo(
        hechos
    )

    return {
        "hechos_iniciales": set(hechos_iniciales),
        "hechos_finales": hechos,
        "hechos_inferidos": hechos_inferidos,
        "reglas_activadas": traza,
        "nivel_riesgo": nivel_riesgo,
        "riesgo_codigo": riesgo_codigo,
        "iteraciones": iteraciones
    }


def determinar_riesgo(hechos):
    """
    Busca todos los niveles de riesgo inferidos y devuelve
    el de mayor severidad.

    Ejemplo:
        Si aparecen:
            riesgo_moderado
            riesgo_alto
            riesgo_critico

        el resultado final será riesgo_critico.
    """

    riesgos_detectados = []

    for riesgo, valor in RIESGOS_FINALES.items():
        if riesgo in hechos:
            riesgos_detectados.append(
                (valor, riesgo)
            )

    if not riesgos_detectados:
        return "riesgo_no_determinado", 0

    # Seleccionamos el riesgo con mayor valor.
    valor_maximo, riesgo_final = max(
        riesgos_detectados,
        key=lambda elemento: elemento[0]
    )

    return riesgo_final, valor_maximo


def obtener_nombre_riesgo(nivel_riesgo):
    """
    Convierte el nombre interno del riesgo a una etiqueta
    adecuada para mostrar al usuario.
    """

    nombres = {
        "riesgo_bajo": "BAJO",
        "riesgo_moderado": "MODERADO",
        "riesgo_alto": "ALTO",
        "riesgo_critico": "CRÍTICO",
        "riesgo_no_determinado": "NO DETERMINADO"
    }

    return nombres.get(
        nivel_riesgo,
        "NO DETERMINADO"
    )


def obtener_accion_recomendada(nivel_riesgo):
    """
    Devuelve una acción simulada según el nivel de riesgo.

    Estas acciones forman parte del proyecto académico y no
    representan políticas reales de una institución bancaria.
    """

    acciones = {
        "riesgo_bajo":
            "Autorizar la operación.",

        "riesgo_moderado":
            "Solicitar una verificación adicional antes "
            "de continuar con la operación.",

        "riesgo_alto":
            "Retener temporalmente la operación y solicitar "
            "confirmación del titular.",

        "riesgo_critico":
            "Bloquear temporalmente la operación y generar "
            "una alerta de seguridad para revisión.",

        "riesgo_no_determinado":
            "Enviar la operación a revisión manual debido "
            "a que no existe evidencia suficiente para "
            "determinar un nivel de riesgo."
    }

    return acciones.get(
        nivel_riesgo,
        acciones["riesgo_no_determinado"]
    )


def obtener_riesgos_detectados(hechos):
    """
    Retorna todos los niveles de riesgo que fueron inferidos
    durante el razonamiento.
    """

    riesgos = []

    for riesgo, valor in RIESGOS_FINALES.items():
        if riesgo in hechos:
            riesgos.append(
                {
                    "riesgo": riesgo,
                    "valor": valor,
                    "nombre": obtener_nombre_riesgo(riesgo)
                }
            )

    riesgos.sort(
        key=lambda elemento: elemento["valor"]
    )

    return riesgos


def generar_explicacion(resultado):
    """
    Genera una explicación sencilla de por qué el sistema
    llegó al resultado obtenido.
    """

    nivel = resultado["nivel_riesgo"]

    reglas_activadas = resultado["reglas_activadas"]

    # Buscamos las reglas que produjeron específicamente
    # hechos relacionados con riesgo.
    reglas_riesgo = [
        regla
        for regla in reglas_activadas
        if regla["conclusion"].startswith("riesgo_")
    ]

    if nivel == "riesgo_no_determinado":
        return (
            "El sistema encontró información sobre la operación, "
            "pero las reglas activadas no fueron suficientes para "
            "establecer un nivel de riesgo definitivo."
        )

    # Buscamos la regla que produjo el riesgo final.
    regla_final = None

    for regla in reversed(reglas_riesgo):
        if regla["conclusion"] == nivel:
            regla_final = regla
            break

    if regla_final is None:
        return (
            f"El sistema determinó un nivel de "
            f"{obtener_nombre_riesgo(nivel)}."
        )

    return (
        f"El sistema determinó un nivel de riesgo "
        f"{obtener_nombre_riesgo(nivel)} porque se activó "
        f"la regla {regla_final['id']}: "
        f"{regla_final['descripcion']}"
    )