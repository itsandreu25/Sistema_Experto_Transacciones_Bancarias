# ==========================================================
# BATERÍA DE PRUEBAS
# BankShield Expert
# ==========================================================
#
# Este archivo permite comprobar que el sistema experto
# diferencia correctamente distintos escenarios de riesgo.
# ==========================================================

from datos.clientes import clientes
from experto.hechos import generar_hechos_iniciales
from experto.inferencia import (
    motor_inferencia,
    obtener_nombre_riesgo,
    obtener_accion_recomendada
)


# ==========================================================
# CASOS DE PRUEBA
# ==========================================================

casos_prueba = [

    # ======================================================
    # CASO 1 - OPERACIÓN NORMAL
    # ======================================================

    {
        "nombre": "CASO 1 - Operación normal de Ana",
        "cliente": "C001",
        "riesgo_esperado": "riesgo_bajo",

        "transaccion": {
            "monto": 120.00,
            "ubicacion": "Riobamba",
            "hora": 14.0,
            "dispositivo": "Samsung Galaxy S24",
            "beneficiario": "Maria Torres",

            "transacciones_ultima_hora": 1,
            "intentos_fallidos": 0,

            "credenciales_modificadas": False,
            "sesion_nueva_reciente": False,

            "autenticacion_reforzada": "correcta",

            "multiples_beneficiarios": False,

            "sesiones_geograficamente_incompatibles": False,

            "operaciones_similares": True
        }
    },


    # ======================================================
    # CASO 2 - RIESGO MODERADO
    # ======================================================

    {
        "nombre": "CASO 2 - Acceso atípico de Ana",
        "cliente": "C001",
        "riesgo_esperado": "riesgo_moderado",

        "transaccion": {
            "monto": 600.00,

            "ubicacion": "Quito",

            "hora": 18.0,

            "dispositivo": "Pixel-Desconocido",

            # Utilizamos un beneficiario conocido para que
            # no se combinen demasiadas anomalías.
            "beneficiario": "Daniel Lopez",

            "transacciones_ultima_hora": 1,

            "intentos_fallidos": 0,

            "credenciales_modificadas": False,

            "sesion_nueva_reciente": False,

            "autenticacion_reforzada": "correcta",

            "multiples_beneficiarios": False,

            "sesiones_geograficamente_incompatibles": False,

            "operaciones_similares": True
        }
    },


    # ======================================================
    # CASO 3 - RIESGO ALTO
    # ======================================================

    {
        "nombre": "CASO 3 - Posible toma de cuenta de Carlos",
        "cliente": "C002",
        "riesgo_esperado": "riesgo_alto",

        "transaccion": {
            "monto": 3000.00,

            # Ubicación habitual
            "ubicacion": "Quito",

            "hora": 15.0,

            # Dispositivo conocido
            "dispositivo": "iPhone-Carlos",

            # Beneficiario nuevo
            "beneficiario": "Inversiones Delta",

            "transacciones_ultima_hora": 2,

            "intentos_fallidos": 1,

            # Elementos que permiten inferir una posible
            # toma de cuenta.
            "credenciales_modificadas": True,

            "sesion_nueva_reciente": True,

            "autenticacion_reforzada": "fallida",

            "multiples_beneficiarios": False,

            "sesiones_geograficamente_incompatibles": False,

            "operaciones_similares": False
        }
    },


    # ======================================================
    # CASO 4 - RIESGO CRÍTICO
    # ======================================================

    {
        "nombre": "CASO 4 - Operación crítica de Laura",
        "cliente": "C003",
        "riesgo_esperado": "riesgo_critico",

        "transaccion": {
            "monto": 1400.00,

            "ubicacion": "Guayaquil",

            "hora": 3.0,

            "dispositivo": "iPhone-Desconocido",

            "beneficiario": "Cuenta Externa XYZ",

            "transacciones_ultima_hora": 6,

            "intentos_fallidos": 5,

            "credenciales_modificadas": True,

            "sesion_nueva_reciente": True,

            "autenticacion_reforzada": "fallida",

            "multiples_beneficiarios": True,

            "sesiones_geograficamente_incompatibles": True,

            "operaciones_similares": False
        }
    },


    # ======================================================
    # CASO 5
    # MONTO ALTO EN TÉRMINOS ABSOLUTOS,
    # PERO NORMAL PARA EL PERFIL DEL CLIENTE
    # ======================================================

    {
        "nombre":
            "CASO 5 - Transferencia habitual de Miguel",

        "cliente": "C004",

        "riesgo_esperado": "riesgo_bajo",

        "transaccion": {
            "monto": 4000.00,

            "ubicacion": "Guayaquil",

            "hora": 22.0,

            "dispositivo": "Laptop-Empresa",

            "beneficiario": "Distribuidora Sierra",

            "transacciones_ultima_hora": 5,

            "intentos_fallidos": 0,

            "credenciales_modificadas": False,

            "sesion_nueva_reciente": False,

            "autenticacion_reforzada": "correcta",

            "multiples_beneficiarios": False,

            "sesiones_geograficamente_incompatibles": False,

            "operaciones_similares": True
        }
    }
]


# ==========================================================
# FUNCIÓN PARA EJECUTAR UNA PRUEBA
# ==========================================================

def ejecutar_prueba(caso, numero):

    cliente = clientes[
        caso["cliente"]
    ]

    transaccion = caso[
        "transaccion"
    ]

    esperado = caso[
        "riesgo_esperado"
    ]

    # ------------------------------------------------------
    # Generar hechos iniciales
    # ------------------------------------------------------

    hechos, detalles = generar_hechos_iniciales(
        cliente,
        transaccion
    )

    # ------------------------------------------------------
    # Ejecutar motor de inferencia
    # ------------------------------------------------------

    resultado = motor_inferencia(
        hechos
    )

    obtenido = resultado[
        "nivel_riesgo"
    ]

    # ------------------------------------------------------
    # Comparación
    # ------------------------------------------------------

    correcto = esperado == obtenido

    print("\n" + "=" * 75)

    print(
        f"PRUEBA {numero}"
    )

    print(
        caso["nombre"]
    )

    print("=" * 75)

    print(
        f"Cliente: {cliente['nombre']}"
    )

    print(
        f"Monto: ${transaccion['monto']:.2f}"
    )

    print(
        f"Monto promedio habitual: "
        f"${cliente['monto_promedio']:.2f}"
    )

    print(
        f"Veces respecto al promedio: "
        f"{detalles['monto']['veces_promedio']}"
    )

    print(
        f"Ubicación: "
        f"{transaccion['ubicacion']}"
    )

    print(
        f"Dispositivo: "
        f"{transaccion['dispositivo']}"
    )

    print(
        f"Beneficiario: "
        f"{transaccion['beneficiario']}"
    )

    print("\nRESULTADO")

    print(
        f"Esperado: "
        f"{obtener_nombre_riesgo(esperado)}"
    )

    print(
        f"Obtenido: "
        f"{obtener_nombre_riesgo(obtenido)}"
    )

    if correcto:

        print(
            "\n[OK] PRUEBA SUPERADA"
        )

    else:

        print(
            "\n[ERROR] EL RESULTADO NO COINCIDE"
        )

        print(
            "\nHechos iniciales:"
        )

        for hecho in sorted(
            resultado["hechos_iniciales"]
        ):
            print(
                f"   - {hecho}"
            )

        print(
            "\nHechos inferidos:"
        )

        for hecho in sorted(
            resultado["hechos_inferidos"]
        ):
            print(
                f"   - {hecho}"
            )

    print(
        f"\nReglas activadas: "
        f"{len(resultado['reglas_activadas'])}"
    )

    print(
        f"Iteraciones: "
        f"{resultado['iteraciones']}"
    )

    print(
        "\nAcción:"
    )

    print(
        obtener_accion_recomendada(
            obtenido
        )
    )

    return correcto


# ==========================================================
# EJECUCIÓN DE TODA LA BATERÍA
# ==========================================================

print("\n")
print("=" * 75)
print("BANKSHIELD EXPERT")
print("BATERÍA DE PRUEBAS DEL SISTEMA EXPERTO")
print("=" * 75)


resultados = []

for numero, caso in enumerate(
    casos_prueba,
    start=1
):

    resultado = ejecutar_prueba(
        caso,
        numero
    )

    resultados.append(
        resultado
    )


# ==========================================================
# RESUMEN FINAL
# ==========================================================

total = len(
    resultados
)

correctas = sum(
    resultados
)

incorrectas = total - correctas


print("\n")
print("=" * 75)
print("RESUMEN DE PRUEBAS")
print("=" * 75)

print(
    f"Total de pruebas: {total}"
)

print(
    f"Pruebas superadas: {correctas}"
)

print(
    f"Pruebas fallidas: {incorrectas}"
)


if incorrectas == 0:

    print(
        "\nTODAS LAS PRUEBAS FUERON SUPERADAS."
    )

    print(
        "El motor de inferencia está diferenciando "
        "correctamente los escenarios definidos."
    )

else:

    print(
        "\nEXISTEN PRUEBAS QUE REQUIEREN REVISIÓN."
    )

    print(
        "Revise los hechos y las reglas mostradas "
        "en los casos fallidos."
    )

print("=" * 75)