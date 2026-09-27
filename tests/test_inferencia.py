import unittest

from datos.clientes import clientes
from experto.hechos import generar_hechos_iniciales
from experto.inferencia import motor_inferencia


def analizar(codigo_cliente, transaccion):
    hechos, _ = generar_hechos_iniciales(clientes[codigo_cliente], transaccion)
    return hechos, motor_inferencia(hechos)


class TestMotorInferencia(unittest.TestCase):
    def test_caso_bajo(self):
        t = {
            "monto": 120.0,
            "saldo_disponible": 4850.0,
            "ubicacion": "Riobamba",
            "hora": 14.0,
            "dispositivo": "equipo",
            "dispositivo_reconocido": True,
            "beneficiario": "Maria Torres",
            "transacciones_ultima_hora": 1,
            "intentos_fallidos": 0,
            "credenciales_modificadas": False,
            "sesion_nueva_reciente": False,
            "autenticacion_reforzada": "correcta",
            "multiples_beneficiarios": False,
            "sesiones_geograficamente_incompatibles": False,
            "operaciones_similares": True,
            "beneficiario_registrado_recientemente": False,
            "limite_transferencia_modificado": False,
        }
        _, r = analizar("C001", t)
        self.assertEqual(r["nivel_riesgo"], "riesgo_bajo")
        self.assertIn("R36", {x["id"] for x in r["reglas_activadas"]})

    def test_caso_moderado(self):
        t = {
            "monto": 600.0,
            "saldo_disponible": 4850.0,
            "ubicacion": "Quito",
            "hora": 18.0,
            "dispositivo": "equipo",
            "dispositivo_reconocido": False,
            "beneficiario": "Daniel Lopez",
            "transacciones_ultima_hora": 1,
            "intentos_fallidos": 0,
            "credenciales_modificadas": False,
            "sesion_nueva_reciente": True,
            "autenticacion_reforzada": "correcta",
            "multiples_beneficiarios": False,
            "sesiones_geograficamente_incompatibles": False,
            "operaciones_similares": False,
            "beneficiario_registrado_recientemente": False,
            "limite_transferencia_modificado": False,
        }
        _, r = analizar("C001", t)
        self.assertEqual(r["nivel_riesgo"], "riesgo_moderado")
        self.assertIn("R23", {x["id"] for x in r["reglas_activadas"]})

    def test_caso_alto(self):
        t = {
            "monto": 3000.0,
            "saldo_disponible": 18500.0,
            "ubicacion": "Quito",
            "hora": 15.0,
            "dispositivo": "equipo",
            "dispositivo_reconocido": True,
            "beneficiario": "Inversiones Delta",
            "transacciones_ultima_hora": 2,
            "intentos_fallidos": 1,
            "credenciales_modificadas": True,
            "sesion_nueva_reciente": True,
            "autenticacion_reforzada": "fallida",
            "multiples_beneficiarios": False,
            "sesiones_geograficamente_incompatibles": False,
            "operaciones_similares": False,
            "beneficiario_registrado_recientemente": True,
            "limite_transferencia_modificado": False,
        }
        _, r = analizar("C002", t)
        self.assertEqual(r["nivel_riesgo"], "riesgo_alto")
        self.assertIn("R29", {x["id"] for x in r["reglas_activadas"]})

    def test_caso_critico(self):
        t = {
            "monto": 2500.0,
            "saldo_disponible": 4850.0,
            "ubicacion": "Guayaquil",
            "hora": 3.25,
            "dispositivo": "equipo",
            "dispositivo_reconocido": False,
            "beneficiario": "Cuenta Externa XYZ",
            "transacciones_ultima_hora": 7,
            "intentos_fallidos": 5,
            "credenciales_modificadas": True,
            "sesion_nueva_reciente": True,
            "autenticacion_reforzada": "fallida",
            "multiples_beneficiarios": True,
            "sesiones_geograficamente_incompatibles": True,
            "operaciones_similares": False,
            "beneficiario_registrado_recientemente": True,
            "limite_transferencia_modificado": True,
        }
        _, r = analizar("C001", t)
        self.assertEqual(r["nivel_riesgo"], "riesgo_critico")
        self.assertTrue(
            {"R33", "R34", "R35", "R42"}
            & {x["id"] for x in r["reglas_activadas"]}
        )

    def test_motor_no_modifica_hechos_entrada(self):
        hechos = {"dispositivo_nuevo", "ubicacion_nueva"}
        copia = set(hechos)
        motor_inferencia(hechos)
        self.assertEqual(hechos, copia)

    def test_selecciona_riesgo_mas_severo(self):
        resultado = motor_inferencia(
            {
                "riesgo_bajo",
                "riesgo_moderado",
                "riesgo_alto",
                "riesgo_critico",
            }
        )
        self.assertEqual(resultado["nivel_riesgo"], "riesgo_critico")

    def test_riesgo_bajo_exige_contexto_seguro(self):
        t = {
            "monto": 90.0,
            "saldo_disponible": 4850.0,
            "ubicacion": "Riobamba",
            "hora": 14.0,
            "dispositivo": "equipo",
            "dispositivo_reconocido": True,
            "beneficiario": "Maria Torres",
            "transacciones_ultima_hora": 1,
            "intentos_fallidos": 0,
            "credenciales_modificadas": True,
            "sesion_nueva_reciente": False,
            "autenticacion_reforzada": "no_aplica",
            "multiples_beneficiarios": False,
            "sesiones_geograficamente_incompatibles": True,
            "operaciones_similares": True,
            "beneficiario_registrado_recientemente": False,
            "limite_transferencia_modificado": False,
        }
        _, r = analizar("C001", t)
        self.assertNotEqual(r["nivel_riesgo"], "riesgo_bajo")


if __name__ == "__main__":
    unittest.main()
