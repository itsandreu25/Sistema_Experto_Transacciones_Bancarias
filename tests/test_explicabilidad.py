import unittest

from datos.clientes import clientes
from experto.explicabilidad import calcular_capas_logicas, construir_cadena_principal
from experto.hechos import generar_hechos_iniciales
from experto.inferencia import motor_inferencia


class TestExplicabilidad(unittest.TestCase):
    def test_cadena_termina_en_riesgo_final(self):
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
        hechos, _ = generar_hechos_iniciales(clientes["C002"], t)
        resultado = motor_inferencia(hechos)
        cadena = construir_cadena_principal(resultado)
        self.assertTrue(cadena)
        self.assertEqual(cadena[-1]["conclusion"], resultado["nivel_riesgo"])

    def test_capas_respetan_dependencias(self):
        cadena = [
            {"id": "A", "antecedentes": ["x"], "conclusion": "y"},
            {"id": "B", "antecedentes": ["z"], "conclusion": "w"},
            {"id": "C", "antecedentes": ["y", "w"], "conclusion": "fin"},
        ]
        capas = calcular_capas_logicas(cadena)
        self.assertEqual({r["id"] for r in capas[1]}, {"A", "B"})
        self.assertEqual([r["id"] for r in capas[2]], ["C"])


if __name__ == "__main__":
    unittest.main()
