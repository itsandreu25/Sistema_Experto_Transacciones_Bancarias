# ==========================================================
# ESCENARIOS DE SEGURIDAD
# BankShield Expert
# ==========================================================
#
# Estos datos simulan información que normalmente provendría
# de registros internos de una institución financiera:
#
# - historial transaccional
# - registros de autenticación
# - sesiones
# - configuración de seguridad
#
# El cliente NO introduce estos valores.
# ==========================================================


ESCENARIOS_SEGURIDAD = {

    "habitual": {

        "nombre":
            "Actividad habitual",

        "descripcion":
            "No existen eventos relevantes de seguridad "
            "antes de la operación.",

        "datos": {

            "transacciones_ultima_hora": 1,

            "intentos_fallidos": 0,

            "credenciales_modificadas": False,

            "sesion_nueva_reciente": False,

            "autenticacion_reforzada": "correcta",

            "multiples_beneficiarios": False,

            "sesiones_geograficamente_incompatibles": False,

            "operaciones_similares": True,

            "beneficiario_registrado_recientemente": False,

            "limite_transferencia_modificado": False
        }
    },


    "atipica": {

        "nombre":
            "Actividad parcialmente atípica",

        "descripcion":
            "Se observan algunos cambios respecto al "
            "comportamiento normal de la cuenta.",

        "datos": {

            "transacciones_ultima_hora": 3,

            "intentos_fallidos": 1,

            "credenciales_modificadas": False,

            "sesion_nueva_reciente": True,

            "autenticacion_reforzada": "correcta",

            "multiples_beneficiarios": False,

            "sesiones_geograficamente_incompatibles": False,

            "operaciones_similares": False,

            "beneficiario_registrado_recientemente": False,

            "limite_transferencia_modificado": False
        }
    },


    "compromiso": {

        "nombre":
            "Señales de posible compromiso",

        "descripcion":
            "Los registros presentan varios eventos "
            "de autenticación y acceso inusuales.",

        "datos": {

            "transacciones_ultima_hora": 4,

            "intentos_fallidos": 3,

            "credenciales_modificadas": True,

            "sesion_nueva_reciente": True,

            "autenticacion_reforzada": "fallida",

            "multiples_beneficiarios": False,

            "sesiones_geograficamente_incompatibles": True,

            "operaciones_similares": False,

            "beneficiario_registrado_recientemente": False,

            "limite_transferencia_modificado": False
        }
    },


    "anomalias_multiples": {

        "nombre":
            "Múltiples anomalías de seguridad",

        "descripcion":
            "Se simula un contexto con numerosos indicadores "
            "de comportamiento inusual.",

        "datos": {

            "transacciones_ultima_hora": 7,

            "intentos_fallidos": 5,

            "credenciales_modificadas": True,

            "sesion_nueva_reciente": True,

            "autenticacion_reforzada": "fallida",

            "multiples_beneficiarios": True,

            "sesiones_geograficamente_incompatibles": True,

            "operaciones_similares": False,

            "beneficiario_registrado_recientemente": True,

            "limite_transferencia_modificado": True
        }
    }
}