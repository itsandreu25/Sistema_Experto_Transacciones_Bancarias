import re
import unittest
from collections import Counter
from pathlib import Path

from experto.reglas import RIESGOS_FINALES, reglas


class TestBaseConocimiento(unittest.TestCase):
    def test_hay_42_reglas(self):
        self.assertEqual(len(reglas), 42)

    def test_ids_unicos_y_secuenciales(self):
        ids = [regla["id"] for regla in reglas]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(ids, [f"R{i:02d}" for i in range(1, 43)])

    def test_estructura_reglas(self):
        for regla in reglas:
            with self.subTest(regla=regla["id"]):
                self.assertEqual(
                    set(regla), {"id", "nivel", "si", "entonces", "descripcion"}
                )
                self.assertIn(regla["nivel"], {1, 2, 3, 4})
                self.assertIsInstance(regla["si"], list)
                self.assertGreater(len(regla["si"]), 0)
                self.assertTrue(all(isinstance(x, str) and x for x in regla["si"]))
                self.assertIsInstance(regla["entonces"], str)
                self.assertTrue(regla["entonces"])
                self.assertTrue(regla["descripcion"].strip())

    def test_todos_los_antecedentes_tienen_origen(self):
        texto_hechos = Path("experto/hechos.py").read_text(encoding="utf-8")
        hechos_iniciales = set(
            re.findall(r'hechos\.add\(\s*["\']([^"\']+)', texto_hechos)
        )
        conclusiones = {regla["entonces"] for regla in reglas}
        antecedentes = {hecho for regla in reglas for hecho in regla["si"]}
        faltantes = antecedentes - hechos_iniciales - conclusiones
        self.assertEqual(faltantes, set())

    def test_niveles_de_riesgo(self):
        self.assertEqual(
            RIESGOS_FINALES,
            {
                "riesgo_bajo": 1,
                "riesgo_moderado": 2,
                "riesgo_alto": 3,
                "riesgo_critico": 4,
            },
        )

    def test_distribucion_por_nivel(self):
        niveles = Counter(regla["nivel"] for regla in reglas)
        self.assertEqual(sum(niveles.values()), 42)
        self.assertTrue(all(niveles[n] > 0 for n in (1, 2, 3, 4)))


if __name__ == "__main__":
    unittest.main()
