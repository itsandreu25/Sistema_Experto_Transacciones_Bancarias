import unittest

from experto.operaciones import registrar_operacion_en_estado


def transaccion(id_transaccion="TRX-TEST", monto=120.0):
    return {
        "id_transaccion": id_transaccion,
        "cliente_id": "C001",
        "beneficiario": "Maria Torres",
        "monto": monto,
        "fecha_registro": "26/09/2026",
        "fecha_hora_registro": "26/09/2026 18:00:00",
        "modo_analisis": "automatico",
    }


def resultado(riesgo):
    return {"nivel_riesgo": riesgo, "reglas_activadas": [{"id": "RX"}]}


class TestRegistroOperaciones(unittest.TestCase):
    def preparar(self):
        return {"C001": 4850.0}, {"C001": []}, [], set()

    def test_bajo_descuenta_saldo(self):
        saldos, movimientos, historial, registradas = self.preparar()
        ok = registrar_operacion_en_estado(
            transaccion(), resultado("riesgo_bajo"), saldos, movimientos, historial, registradas
        )
        self.assertTrue(ok)
        self.assertEqual(saldos["C001"], 4730.0)
        self.assertEqual(movimientos["C001"][0]["estado"], "Aprobada")
        self.assertEqual(movimientos["C001"][0]["monto"], -120.0)

    def test_moderado_no_descuenta(self):
        saldos, movimientos, historial, registradas = self.preparar()
        registrar_operacion_en_estado(
            transaccion(), resultado("riesgo_moderado"), saldos, movimientos, historial, registradas
        )
        self.assertEqual(saldos["C001"], 4850.0)
        self.assertEqual(movimientos["C001"][0]["estado"], "Pendiente de verificación")

    def test_alto_no_descuenta(self):
        saldos, movimientos, historial, registradas = self.preparar()
        registrar_operacion_en_estado(
            transaccion(), resultado("riesgo_alto"), saldos, movimientos, historial, registradas
        )
        self.assertEqual(saldos["C001"], 4850.0)
        self.assertEqual(movimientos["C001"][0]["estado"], "En revisión")

    def test_critico_no_descuenta(self):
        saldos, movimientos, historial, registradas = self.preparar()
        registrar_operacion_en_estado(
            transaccion(), resultado("riesgo_critico"), saldos, movimientos, historial, registradas
        )
        self.assertEqual(saldos["C001"], 4850.0)
        self.assertEqual(movimientos["C001"][0]["estado"], "Bloqueada")

    def test_no_registra_dos_veces(self):
        saldos, movimientos, historial, registradas = self.preparar()
        t = transaccion()
        r = resultado("riesgo_bajo")
        self.assertTrue(registrar_operacion_en_estado(t, r, saldos, movimientos, historial, registradas))
        self.assertFalse(registrar_operacion_en_estado(t, r, saldos, movimientos, historial, registradas))
        self.assertEqual(saldos["C001"], 4730.0)
        self.assertEqual(len(movimientos["C001"]), 1)
        self.assertEqual(len(historial), 1)


if __name__ == "__main__":
    unittest.main()
