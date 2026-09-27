"""Funciones puras para reconstruir la explicación de una inferencia."""


def construir_cadena_principal(resultado):
    """Reconstruye las reglas directamente relacionadas con el riesgo final.

    Se recorre el grafo de dependencias hacia atrás, desde la conclusión final
    hasta los hechos que no fueron producidos por otras reglas activadas.
    """
    reglas = resultado.get("reglas_activadas", [])
    objetivo = resultado.get("nivel_riesgo")
    if not reglas or not objetivo:
        return []

    productores = {}
    for indice, regla in enumerate(reglas):
        productores.setdefault(regla["conclusion"], []).append((indice, regla))

    cadena = []
    reglas_visitadas = set()
    hechos_visitados = set()

    def recorrer(hecho):
        if hecho in hechos_visitados:
            return
        hechos_visitados.add(hecho)

        candidatos = productores.get(hecho, [])
        if not candidatos:
            return

        indice, regla = candidatos[-1]
        if regla["id"] in reglas_visitadas:
            return

        for antecedente in regla["antecedentes"]:
            recorrer(antecedente)

        reglas_visitadas.add(regla["id"])
        cadena.append((indice, regla))

    recorrer(objetivo)
    cadena.sort(key=lambda elemento: elemento[0])
    return [regla for _, regla in cadena]


def calcular_capas_logicas(cadena):
    """Agrupa una cadena de reglas por profundidad de dependencia lógica."""
    if not cadena:
        return {}

    productores = {regla["conclusion"]: regla for regla in cadena}
    profundidades = {}
    en_calculo = set()

    def calcular_profundidad(regla):
        regla_id = regla["id"]
        if regla_id in profundidades:
            return profundidades[regla_id]
        if regla_id in en_calculo:
            raise ValueError("Se detectó un ciclo en la cadena de inferencia.")

        en_calculo.add(regla_id)
        dependencias = []
        for antecedente in regla["antecedentes"]:
            regla_productora = productores.get(antecedente)
            if regla_productora is not None:
                dependencias.append(calcular_profundidad(regla_productora))

        profundidad = max(dependencias) + 1 if dependencias else 1
        profundidades[regla_id] = profundidad
        en_calculo.remove(regla_id)
        return profundidad

    capas = {}
    for regla in cadena:
        capa = calcular_profundidad(regla)
        capas.setdefault(capa, []).append(regla)
    return capas
