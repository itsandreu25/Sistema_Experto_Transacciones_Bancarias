# ==========================================================
# VERIFICACIONES DEL SISTEMA EXPERTO
# BankShield Expert
# ==========================================================
#
# Estas variables no son preguntas dirigidas al cliente.
#
# En el modo de demostración, un analista confirma
# 10 datos provenientes de diferentes fuentes internas.
# ==========================================================


VERIFICACIONES = [

    {
        "id": "V01",

        "campo":
            "transacciones_ultima_hora",

        "tipo":
            "numero",

        "titulo":
            "Actividad transaccional reciente",

        "descripcion":
            "Número de transacciones registradas durante "
            "la última hora.",

        "fuente":
            "Historial transaccional",

        "unidad":
            "operaciones"
    },

    {
        "id": "V02",

        "campo":
            "intentos_fallidos",

        "tipo":
            "numero",

        "titulo":
            "Intentos de autenticación",

        "descripcion":
            "Intentos fallidos registrados antes de "
            "la operación actual.",

        "fuente":
            "Registro de autenticación",

        "unidad":
            "intentos"
    },

    {
        "id": "V03",

        "campo":
            "credenciales_modificadas",

        "tipo":
            "si_no",

        "titulo":
            "Cambios de credenciales",

        "descripcion":
            "Existencia de cambios recientes en contraseña, "
            "PIN u otros mecanismos de acceso.",

        "fuente":
            "Registro de seguridad de la cuenta"
    },

    {
        "id": "V04",

        "campo":
            "sesion_nueva_reciente",

        "tipo":
            "si_no",

        "titulo":
            "Nueva sesión o dispositivo",

        "descripcion":
            "Registro reciente de una nueva sesión "
            "o dispositivo asociado a la cuenta.",

        "fuente":
            "Registro de sesiones y dispositivos"
    },

    {
        "id": "V05",

        "campo":
            "autenticacion_reforzada",

        "tipo":
            "opciones",

        "titulo":
            "Autenticación adicional",

        "descripcion":
            "Resultado del mecanismo adicional de "
            "autenticación aplicado a la sesión.",

        "fuente":
            "Servicio de autenticación",

        "opciones": [
            "correcta",
            "fallida",
            "no_aplica"
        ],

        "etiquetas": {

            "correcta":
                "Autenticación correcta",

            "fallida":
                "Autenticación fallida",

            "no_aplica":
                "No se solicitó"
        }
    },

    {
        "id": "V06",

        "campo":
            "multiples_beneficiarios",

        "tipo":
            "si_no",

        "titulo":
            "Diversidad de beneficiarios",

        "descripcion":
            "Existencia de múltiples transferencias recientes "
            "hacia beneficiarios diferentes.",

        "fuente":
            "Historial transaccional"
    },

    {
        "id": "V07",

        "campo":
            "sesiones_geograficamente_incompatibles",

        "tipo":
            "si_no",

        "titulo":
            "Consistencia geográfica",

        "descripcion":
            "Existencia de sesiones desde ubicaciones "
            "geográficamente incompatibles en un periodo corto.",

        "fuente":
            "Registro de sesiones"
    },

    {
        "id": "V08",

        "campo":
            "operaciones_similares",

        "tipo":
            "si_no",

        "titulo":
            "Comportamiento histórico",

        "descripcion":
            "Existencia de operaciones anteriores con "
            "características semejantes a la actual.",

        "fuente":
            "Perfil histórico del cliente"
    },

    {
        "id": "V09",

        "campo":
            "beneficiario_registrado_recientemente",

        "tipo":
            "si_no",

        "titulo":
            "Registro del beneficiario",

        "descripcion":
            "El beneficiario fue agregado recientemente "
            "a la cuenta.",

        "fuente":
            "Gestión de beneficiarios"
    },

    {
        "id": "V10",

        "campo":
            "limite_transferencia_modificado",

        "tipo":
            "si_no",

        "titulo":
            "Cambios en límites de transferencia",

        "descripcion":
            "El límite permitido de transferencias fue "
            "modificado recientemente.",

        "fuente":
            "Configuración de seguridad de la cuenta"
    }
]


def obtener_verificacion(indice):

    if 0 <= indice < len(VERIFICACIONES):
        return VERIFICACIONES[indice]

    return None


def cantidad_verificaciones():

    return len(VERIFICACIONES)

# Alias de compatibilidad con versiones anteriores del proyecto.
PREGUNTAS = VERIFICACIONES
obtener_pregunta = obtener_verificacion
cantidad_preguntas = cantidad_verificaciones
