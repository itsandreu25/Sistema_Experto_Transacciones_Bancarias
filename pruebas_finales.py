"""Ejecuta la batería final de pruebas de BankShield Expert."""

import sys
import unittest


def main():
    print("=" * 72)
    print("BANKSHIELD EXPERT · PRUEBAS FINALES")
    print("=" * 72)
    suite = unittest.defaultTestLoader.discover("tests")
    resultado = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    print("=" * 72)
    print(f"Pruebas ejecutadas: {resultado.testsRun}")
    print(f"Fallos: {len(resultado.failures)}")
    print(f"Errores: {len(resultado.errors)}")
    estado = "CORRECTO" if resultado.wasSuccessful() else "REQUIERE REVISIÓN"
    print(f"Estado general: {estado}")
    print("=" * 72)
    return 0 if resultado.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
