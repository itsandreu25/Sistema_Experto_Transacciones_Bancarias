"""Lógica de registro de operaciones de BankShield Expert.

Este módulo no depende de Streamlit. Mantiene separada la lógica bancaria
simulada de la interfaz para que pueda probarse de forma automática.
"""

from copy import deepcopy


ESTADOS_POR_RIESGO = {
    "riesgo_bajo": "Aprobada",
    "riesgo_moderado": "Pendiente de verificación",
    "riesgo_alto": "En revisión",
    "riesgo_critico": "Bloqueada",
    "riesgo_no_determinado": "En revisión",
}


def obtener_estado_operacion(nivel_riesgo):
    """Devuelve el estado bancario simulado para un nivel de riesgo."""
    return ESTADOS_POR_RIESGO.get(nivel_riesgo, "En revisión")


def registrar_operacion_en_estado(
    transaccion,
    resultado,
    saldos,
    movimientos,
    historial,
    registradas,
):
    """Registra una operación sobre estructuras de estado mutables.

    Solo las operaciones de riesgo bajo se consideran procesadas y descuentan
    saldo. Las demás quedan registradas con su estado, sin afectar el saldo.

    Retorna ``True`` si la operación se registró y ``False`` si ya había sido
    registrada previamente.
    """

    id_transaccion = transaccion["id_transaccion"]
    if id_transaccion in registradas:
        return False

    codigo_cliente = transaccion["cliente_id"]
    nivel = resultado["nivel_riesgo"]
    monto = float(transaccion["monto"])
    estado = obtener_estado_operacion(nivel)

    if codigo_cliente not in saldos:
        raise KeyError(f"Cliente sin saldo de sesión: {codigo_cliente}")
    if codigo_cliente not in movimientos:
        movimientos[codigo_cliente] = []

    saldo_antes = float(saldos[codigo_cliente])
    saldo_despues = saldo_antes

    if nivel == "riesgo_bajo":
        if monto > saldo_antes:
            raise ValueError("Saldo insuficiente para registrar la operación aprobada.")
        saldo_despues = saldo_antes - monto
        saldos[codigo_cliente] = saldo_despues

    movimiento = {
        "fecha": transaccion["fecha_registro"],
        "descripcion": transaccion["beneficiario"],
        "tipo": "Transferencia",
        "monto_operacion": monto,
        "monto": -monto if nivel == "riesgo_bajo" else 0.0,
        "estado": estado,
        "id_transaccion": id_transaccion,
    }
    movimientos[codigo_cliente].insert(0, movimiento)

    historial.insert(
        0,
        {
            "id": id_transaccion,
            "fecha": transaccion["fecha_hora_registro"],
            "cliente_id": codigo_cliente,
            "beneficiario": transaccion["beneficiario"],
            "monto": monto,
            "riesgo": nivel,
            "estado": estado,
            "modo": transaccion.get("modo_analisis", "guiado"),
            "reglas_activadas": len(resultado["reglas_activadas"]),
            "saldo_antes": saldo_antes,
            "saldo_despues": saldo_despues,
            "transaccion": deepcopy(transaccion),
            "resultado": deepcopy(resultado),
        },
    )

    registradas.add(id_transaccion)
    return True
