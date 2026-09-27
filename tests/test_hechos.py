import unittest

from datos.clientes import clientes
from experto.hechos import generar_hechos_iniciales


class TestGeneracionHechos(unittest.TestCase):
    def transaccion_base(self):
        return {
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

    def test_categorias_principales_son_excluyentes(self):
        hechos, _ = generar_hechos_iniciales(clientes["C001"], self.transaccion_base())
        grupos = [
            {"monto_habitual", "monto_elevado", "monto_muy_inusual"},
            {"dispositivo_conocido", "dispositivo_nuevo"},
            {"ubicacion_habitual", "ubicacion_nueva"},
            {"horario_habitual", "horario_inusual"},
            {"beneficiario_conocido", "beneficiario_nuevo"},
            {"frecuencia_normal", "frecuencia_elevada", "frecuencia_muy_alta"},
            {"autenticacion_normal", "algunos_intentos_fallidos", "multiples_intentos_fallidos"},
            {"porcentaje_saldo_normal", "porcentaje_saldo_alto", "porcentaje_saldo_muy_alto"},
        ]
        for grupo in grupos:
            with self.subTest(grupo=grupo):
                self.assertEqual(len(grupo & hechos), 1)

    def test_saldo_actual_de_sesion_se_usa_en_porcentaje(self):
        t = self.transaccion_base()
        t["monto"] = 2500.0
        t["saldo_disponible"] = 3000.0
        hechos, detalles = generar_hechos_iniciales(clientes["C001"], t)
        self.assertIn("porcentaje_saldo_muy_alto", hechos)
        self.assertAlmostEqual(detalles["saldo"]["porcentaje_utilizado"], 83.33, places=2)

    def test_rechaza_monto_no_positivo(self):
        t = self.transaccion_base()
        t["monto"] = 0
        with self.assertRaises(ValueError):
            generar_hechos_iniciales(clientes["C001"], t)

    def test_rechaza_autenticacion_invalida(self):
        t = self.transaccion_base()
        t["autenticacion_reforzada"] = "desconocida"
        with self.assertRaises(ValueError):
            generar_hechos_iniciales(clientes["C001"], t)


if __name__ == "__main__":
    unittest.main()
