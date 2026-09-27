import unittest

from datos.clientes import clientes
from experto.hechos import generar_hechos_iniciales
from experto.inferencia import motor_inferencia
from experto.reglas import reglas


class TestCoberturaReglas(unittest.TestCase):
    def test_las_42_reglas_son_activables_con_casos_validos(self):
        cliente = clientes["C001"]
        base = {
            "dispositivo": "equipo-demo",
            "saldo_disponible": 4850.0,
        }
        casos = [
            {
                "monto": 2500, "ubicacion": "Guayaquil", "hora": 3.0,
                "dispositivo_reconocido": False, "beneficiario": "X",
                "transacciones_ultima_hora": 3, "intentos_fallidos": 4,
                "credenciales_modificadas": True, "sesion_nueva_reciente": True,
                "autenticacion_reforzada": "fallida", "multiples_beneficiarios": True,
                "sesiones_geograficamente_incompatibles": False,
                "operaciones_similares": False,
                "beneficiario_registrado_recientemente": True,
                "limite_transferencia_modificado": True,
            },
            {
                "monto": 600, "ubicacion": "Guayaquil", "hora": 3.0,
                "dispositivo_reconocido": False, "beneficiario": "X",
                "transacciones_ultima_hora": 7, "intentos_fallidos": 1,
                "credenciales_modificadas": True, "sesion_nueva_reciente": False,
                "autenticacion_reforzada": "fallida", "multiples_beneficiarios": True,
                "sesiones_geograficamente_incompatibles": True,
                "operaciones_similares": False,
                "beneficiario_registrado_recientemente": False,
                "limite_transferencia_modificado": True,
            },
            {
                "monto": 4000, "ubicacion": "Guayaquil", "hora": 3.0,
                "dispositivo_reconocido": False, "beneficiario": "X",
                "transacciones_ultima_hora": 7, "intentos_fallidos": 4,
                "credenciales_modificadas": False, "sesion_nueva_reciente": True,
                "autenticacion_reforzada": "no_aplica", "multiples_beneficiarios": False,
                "sesiones_geograficamente_incompatibles": True,
                "operaciones_similares": False,
                "beneficiario_registrado_recientemente": True,
                "limite_transferencia_modificado": False,
            },
            {
                "monto": 90, "ubicacion": "Riobamba", "hora": 14.0,
                "dispositivo_reconocido": True, "beneficiario": "Maria Torres",
                "transacciones_ultima_hora": 1, "intentos_fallidos": 0,
                "credenciales_modificadas": False, "sesion_nueva_reciente": False,
                "autenticacion_reforzada": "correcta", "multiples_beneficiarios": False,
                "sesiones_geograficamente_incompatibles": False,
                "operaciones_similares": True,
                "beneficiario_registrado_recientemente": False,
                "limite_transferencia_modificado": False,
            },
            {
                "monto": 90, "ubicacion": "Riobamba", "hora": 14.0,
                "dispositivo_reconocido": True, "beneficiario": "Maria Torres",
                "transacciones_ultima_hora": 1, "intentos_fallidos": 0,
                "credenciales_modificadas": False, "sesion_nueva_reciente": False,
                "autenticacion_reforzada": "no_aplica", "multiples_beneficiarios": False,
                "sesiones_geograficamente_incompatibles": False,
                "operaciones_similares": True,
                "beneficiario_registrado_recientemente": False,
                "limite_transferencia_modificado": False,
            },
        ]

        activadas = set()
        for caso in casos:
            t = {**base, **caso}
            hechos, _ = generar_hechos_iniciales(cliente, t)
            resultado = motor_inferencia(hechos)
            activadas.update(r["id"] for r in resultado["reglas_activadas"])

        esperadas = {r["id"] for r in reglas}
        self.assertEqual(activadas, esperadas, f"Faltan: {sorted(esperadas-activadas)}")


if __name__ == "__main__":
    unittest.main()
