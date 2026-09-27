# ==========================================================
# BASE DE CONOCIMIENTO
# Sistema experto para detección de posibles fraudes
# ==========================================================
#
# Cada regla contiene:
#
# id          -> identificador único de la regla
# nivel       -> etapa del proceso de razonamiento
# si          -> hechos necesarios para activar la regla
# entonces    -> nuevo hecho que genera
# descripcion -> explicación en lenguaje natural
#
# IMPORTANTE:
# Los niveles no significan que el motor de inferencia solo
# pueda recorrer las reglas una vez. El motor continuará
# evaluándolas hasta que ya no pueda generar nuevos hechos.
# ==========================================================


reglas = [

    # ======================================================
    # NIVEL 1
    # DETECCIÓN DE ANOMALÍAS BÁSICAS
    # ======================================================

    {
        "id": "R01",
        "nivel": 1,
        "si": [
            "dispositivo_nuevo",
            "ubicacion_nueva"
        ],
        "entonces": "acceso_atipico",
        "descripcion":
            "El acceso se considera atípico porque se utiliza "
            "un dispositivo nuevo desde una ubicación no habitual."
    },

    {
        "id": "R02",
        "nivel": 1,
        "si": [
            "horario_inusual",
            "ubicacion_nueva"
        ],
        "entonces": "contexto_operacional_inusual",
        "descripcion":
            "La operación ocurre fuera del horario habitual y "
            "desde una ubicación no reconocida."
    },

    {
        "id": "R03",
        "nivel": 1,
        "si": [
            "beneficiario_nuevo",
            "monto_elevado"
        ],
        "entonces": "transferencia_inusual",
        "descripcion":
            "Se realiza una transferencia elevada hacia un "
            "beneficiario que no pertenece al historial habitual."
    },

    {
        "id": "R04",
        "nivel": 1,
        "si": [
            "beneficiario_nuevo",
            "monto_muy_inusual"
        ],
        "entonces": "transferencia_inusual",
        "descripcion":
            "Se realiza una transferencia muy superior al promedio "
            "hacia un beneficiario nuevo."
    },

    {
        "id": "R05",
        "nivel": 1,
        "si": [
            "porcentaje_saldo_alto",
            "beneficiario_nuevo"
        ],
        "entonces": "transferencia_alto_impacto",
        "descripcion":
            "La operación utiliza una parte considerable del saldo "
            "y tiene como destino un beneficiario nuevo."
    },

    {
        "id": "R06",
        "nivel": 1,
        "si": [
            "porcentaje_saldo_muy_alto",
            "beneficiario_nuevo"
        ],
        "entonces": "transferencia_alto_impacto",
        "descripcion":
            "La operación utiliza una proporción muy alta del saldo "
            "disponible y se dirige a un beneficiario nuevo."
    },

    {
        "id": "R07",
        "nivel": 1,
        "si": [
            "frecuencia_elevada",
            "multiples_beneficiarios"
        ],
        "entonces": "patron_transaccional_anomalo",
        "descripcion":
            "Se detecta una frecuencia superior a la habitual junto "
            "con transferencias hacia varios beneficiarios."
    },

    {
        "id": "R08",
        "nivel": 1,
        "si": [
            "frecuencia_muy_alta",
            "multiples_beneficiarios"
        ],
        "entonces": "patron_transaccional_anomalo",
        "descripcion":
            "Existe una cantidad muy elevada de operaciones hacia "
            "distintos beneficiarios."
    },

    {
        "id": "R09",
        "nivel": 1,
        "si": [
            "multiples_intentos_fallidos",
            "dispositivo_nuevo"
        ],
        "entonces": "autenticacion_sospechosa",
        "descripcion":
            "Se registran varios intentos fallidos desde un "
            "dispositivo que no pertenece al historial del cliente."
    },

    {
        "id": "R10",
        "nivel": 1,
        "si": [
            "algunos_intentos_fallidos",
            "dispositivo_nuevo"
        ],
        "entonces": "autenticacion_atipica",
        "descripcion":
            "Existen intentos fallidos de autenticación desde "
            "un dispositivo nuevo."
    },

    {
        "id": "R11",
        "nivel": 1,
        "si": [
            "credenciales_modificadas",
            "sesion_nueva_reciente"
        ],
        "entonces": "credenciales_en_riesgo",
        "descripcion":
            "Se modificaron recientemente las credenciales y además "
            "se inició una nueva sesión."
    },

    {
        "id": "R12",
        "nivel": 1,
        "si": [
            "sesiones_geograficamente_incompatibles",
            "dispositivo_nuevo"
        ],
        "entonces": "acceso_geograficamente_inconsistente",
        "descripcion":
            "La cuenta presenta sesiones desde ubicaciones "
            "geográficamente incompatibles y un dispositivo nuevo."
    },


    # ======================================================
    # NIVEL 2
    # CONSTRUCCIÓN DE PATRONES
    # ======================================================

    {
        "id": "R13",
        "nivel": 2,
        "si": [
            "acceso_atipico",
            "autenticacion_sospechosa"
        ],
        "entonces": "posible_acceso_no_autorizado",
        "descripcion":
            "Un acceso atípico combinado con fallos reiterados "
            "de autenticación puede indicar acceso no autorizado."
    },

    {
        "id": "R14",
        "nivel": 2,
        "si": [
            "acceso_geograficamente_inconsistente",
            "autenticacion_sospechosa"
        ],
        "entonces": "posible_acceso_no_autorizado",
        "descripcion":
            "La inconsistencia geográfica junto con una autenticación "
            "sospechosa refuerza la hipótesis de acceso no autorizado."
    },

    {
        "id": "R15",
        "nivel": 2,
        "si": [
            "credenciales_en_riesgo",
            "autenticacion_reforzada_fallida"
        ],
        "entonces": "posible_toma_de_cuenta",
        "descripcion":
            "Los cambios recientes de credenciales y el fallo de "
            "autenticación adicional pueden indicar compromiso "
            "de la cuenta."
    },

    {
        "id": "R16",
        "nivel": 2,
        "si": [
            "acceso_atipico",
            "credenciales_en_riesgo"
        ],
        "entonces": "posible_toma_de_cuenta",
        "descripcion":
            "Un acceso atípico posterior a modificaciones de "
            "credenciales puede corresponder a una posible toma "
            "de control de la cuenta."
    },

    {
        "id": "R17",
        "nivel": 2,
        "si": [
            "transferencia_inusual",
            "transferencia_alto_impacto"
        ],
        "entonces": "operacion_financiera_sensible",
        "descripcion":
            "La transferencia es inusual y además compromete una "
            "proporción importante del saldo disponible."
    },

    {
        "id": "R18",
        "nivel": 2,
        "si": [
            "patron_transaccional_anomalo",
            "transferencia_inusual"
        ],
        "entonces": "posible_dispersion_fondos",
        "descripcion":
            "Una secuencia de operaciones anómalas hacia diferentes "
            "beneficiarios puede representar dispersión de fondos."
    },

    {
        "id": "R19",
        "nivel": 2,
        "si": [
            "patron_no_habitual",
            "monto_muy_inusual"
        ],
        "entonces": "desviacion_fuerte_patron",
        "descripcion":
            "La operación se aleja fuertemente del comportamiento "
            "histórico por su monto y por no tener antecedentes "
            "similares."
    },

    {
        "id": "R20",
        "nivel": 2,
        "si": [
            "desviacion_fuerte_patron",
            "transferencia_inusual"
        ],
        "entonces": "operacion_altamente_atipica",
        "descripcion":
            "La desviación respecto al comportamiento histórico "
            "coincide con una transferencia hacia un destinatario "
            "inusual."
    },

    {
        "id": "R21",
        "nivel": 2,
        "si": [
            "contexto_operacional_inusual",
            "acceso_atipico"
        ],
        "entonces": "sesion_altamente_atipica",
        "descripcion":
            "La sesión combina ubicación, horario y dispositivo "
            "diferentes al comportamiento habitual."
    },

    {
        "id": "R22",
        "nivel": 2,
        "si": [
            "autenticacion_atipica",
            "autenticacion_reforzada_fallida"
        ],
        "entonces": "autenticacion_comprometida",
        "descripcion":
            "Los intentos fallidos desde un dispositivo nuevo y el "
            "fallo de autenticación adicional indican un proceso "
            "de autenticación comprometido."
    },


    # ======================================================
    # NIVEL 3
    # EVALUACIÓN DEL NIVEL DE RIESGO
    # ======================================================

    {
        "id": "R23",
        "nivel": 3,
        "si": [
            "acceso_atipico",
            "monto_elevado"
        ],
        "entonces": "riesgo_moderado",
        "descripcion":
            "Existe un acceso atípico asociado con una operación "
            "de monto superior al comportamiento habitual."
    },

    {
        "id": "R24",
        "nivel": 3,
        "si": [
            "transferencia_inusual",
            "patron_no_habitual"
        ],
        "entonces": "riesgo_moderado",
        "descripcion":
            "La transferencia no corresponde con el patrón histórico "
            "del cliente."
    },

    {
        "id": "R25",
        "nivel": 3,
        "si": [
            "frecuencia_elevada",
            "beneficiario_nuevo"
        ],
        "entonces": "riesgo_moderado",
        "descripcion":
            "La frecuencia de operaciones es elevada y aparece "
            "un beneficiario nuevo."
    },

    {
        "id": "R26",
        "nivel": 3,
        "si": [
            "credenciales_modificadas",
            "dispositivo_nuevo"
        ],
        "entonces": "riesgo_moderado",
        "descripcion":
            "Se detecta un dispositivo nuevo después de cambios "
            "recientes en las credenciales."
    },

    {
        "id": "R27",
        "nivel": 3,
        "si": [
            "autenticacion_reforzada_fallida",
            "sesion_nueva_reciente"
        ],
        "entonces": "riesgo_moderado",
        "descripcion":
            "Una nueva sesión presenta un fallo en el mecanismo "
            "adicional de autenticación."
    },

    {
        "id": "R28",
        "nivel": 3,
        "si": [
            "posible_acceso_no_autorizado",
            "operacion_financiera_sensible"
        ],
        "entonces": "riesgo_alto",
        "descripcion":
            "Coinciden indicadores de acceso no autorizado con una "
            "operación financiera de alto impacto."
    },

    {
        "id": "R29",
        "nivel": 3,
        "si": [
            "posible_toma_de_cuenta",
            "transferencia_inusual"
        ],
        "entonces": "riesgo_alto",
        "descripcion":
            "Una posible toma de control de la cuenta coincide con "
            "una transferencia fuera del comportamiento habitual."
    },

    {
        "id": "R30",
        "nivel": 3,
        "si": [
            "posible_dispersion_fondos",
            "monto_muy_inusual"
        ],
        "entonces": "riesgo_alto",
        "descripcion":
            "Se detecta posible dispersión de fondos junto con "
            "un monto muy superior al promedio."
    },

    {
        "id": "R31",
        "nivel": 3,
        "si": [
            "operacion_altamente_atipica",
            "autenticacion_sospechosa"
        ],
        "entonces": "riesgo_alto",
        "descripcion":
            "Una operación altamente atípica ocurre junto con "
            "señales sospechosas de autenticación."
    },

    {
        "id": "R32",
        "nivel": 3,
        "si": [
            "autenticacion_comprometida",
            "transferencia_inusual"
        ],
        "entonces": "riesgo_alto",
        "descripcion":
            "Una autenticación comprometida coincide con una "
            "transferencia fuera del patrón habitual."
    },


    # ======================================================
    # NIVEL 4
    # SITUACIONES DE RIESGO CRÍTICO Y OPERACIONES NORMALES
    # ======================================================

    {
        "id": "R33",
        "nivel": 4,
        "si": [
            "posible_toma_de_cuenta",
            "posible_dispersion_fondos"
        ],
        "entonces": "riesgo_critico",
        "descripcion":
            "Existen simultáneamente señales de posible toma de "
            "cuenta y dispersión de fondos."
    },

    {
        "id": "R34",
        "nivel": 4,
        "si": [
            "posible_acceso_no_autorizado",
            "operacion_altamente_atipica"
        ],
        "entonces": "riesgo_critico",
        "descripcion":
            "Un posible acceso no autorizado coincide con una "
            "operación que se aleja fuertemente del comportamiento "
            "histórico."
    },

    {
        "id": "R35",
        "nivel": 4,
        "si": [
            "posible_acceso_no_autorizado",
            "transferencia_alto_impacto",
            "autenticacion_reforzada_fallida"
        ],
        "entonces": "riesgo_critico",
        "descripcion":
            "Coinciden acceso posiblemente no autorizado, una "
            "transferencia de alto impacto y fallo en la "
            "autenticación adicional."
    },

    {
        "id": "R36",
        "nivel": 4,
        "si": [
            "monto_habitual",
            "dispositivo_conocido",
            "ubicacion_habitual",
            "beneficiario_conocido",
            "frecuencia_normal",
            "autenticacion_normal",
            "patron_conocido",
            "credenciales_sin_cambios",
            "sin_sesion_nueva_reciente",
            "beneficiarios_sin_variacion",
            "sin_incompatibilidad_geografica",
            "beneficiario_no_registrado_recientemente",
            "limite_transferencia_sin_cambios",
            "autenticacion_reforzada_correcta"
        ],
        "entonces": "riesgo_bajo",
        "descripcion":
            "La operación coincide ampliamente con el comportamiento "
            "histórico y los mecanismos de autenticación fueron "
            "satisfactorios."
    },

    {
        "id": "R37",
        "nivel": 4,
        "si": [
            "monto_habitual",
            "dispositivo_conocido",
            "ubicacion_habitual",
            "beneficiario_conocido",
            "frecuencia_normal",
            "autenticacion_normal",
            "patron_conocido",
            "credenciales_sin_cambios",
            "sin_sesion_nueva_reciente",
            "beneficiarios_sin_variacion",
            "sin_incompatibilidad_geografica",
            "beneficiario_no_registrado_recientemente",
            "limite_transferencia_sin_cambios",
            "autenticacion_reforzada_no_aplica"
        ],
        "entonces": "riesgo_bajo",
        "descripcion":
            "La operación coincide con el comportamiento habitual "
            "del cliente y no se requería autenticación adicional."
    },

    # ======================================================
    # REGLAS ADICIONALES
    # CAMBIOS PREVIOS A LA TRANSACCIÓN
    # ======================================================

    {
        "id": "R38",
        "nivel": 1,
        "si": [
            "beneficiario_registrado_recientemente",
            "beneficiario_nuevo"
        ],
        "entonces": "beneficiario_sensible",
        "descripcion":
            "El beneficiario es nuevo y además fue registrado "
            "recientemente antes de la transferencia."
    },

    {
        "id": "R39",
        "nivel": 1,
        "si": [
            "limite_transferencia_modificado",
            "monto_muy_inusual"
        ],
        "entonces": "configuracion_financiera_sensible",
        "descripcion":
            "Se modificó recientemente el límite de transferencias "
            "y posteriormente se intenta realizar una operación "
            "muy superior al comportamiento habitual."
    },

    {
        "id": "R40",
        "nivel": 2,
        "si": [
            "beneficiario_sensible",
            "configuracion_financiera_sensible"
        ],
        "entonces": "patron_preparatorio_sospechoso",
        "descripcion":
            "La combinación de un beneficiario recién registrado "
            "y cambios recientes en los límites puede constituir "
            "un patrón preparatorio inusual."
    },

    {
        "id": "R41",
        "nivel": 3,
        "si": [
            "patron_preparatorio_sospechoso",
            "autenticacion_sospechosa"
        ],
        "entonces": "riesgo_alto",
        "descripcion":
            "El patrón preparatorio inusual coincide con señales "
            "sospechosas durante la autenticación."
    },

    {
        "id": "R42",
        "nivel": 4,
        "si": [
            "patron_preparatorio_sospechoso",
            "posible_toma_de_cuenta"
        ],
        "entonces": "riesgo_critico",
        "descripcion":
            "Un patrón preparatorio sospechoso coincide con "
            "indicadores de posible toma de control de la cuenta."
    }
]


# ==========================================================
# HECHOS QUE REPRESENTAN RESULTADOS FINALES DE RIESGO
# ==========================================================

RIESGOS_FINALES = {
    "riesgo_bajo": 1,
    "riesgo_moderado": 2,
    "riesgo_alto": 3,
    "riesgo_critico": 4
}