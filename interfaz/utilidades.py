"""Utilidades de presentación compartidas por la interfaz."""


def humanizar_hecho(hecho):
    """Convierte un identificador interno en una etiqueta legible."""
    texto = str(hecho).replace("_", " ")
    reemplazos = {
        "autenticacion": "autenticación",
        "ubicacion": "ubicación",
        "sesion": "sesión",
        "patron": "patrón",
        "atipico": "atípico",
        "atipica": "atípica",
        "anomalo": "anómalo",
        "critico": "crítico",
        "geograficamente": "geográficamente",
        "dispersion": "dispersión",
        "configuracion": "configuración",
        "operacion": "operación",
    }
    for original, corregido in reemplazos.items():
        texto = texto.replace(original, corregido)
    return texto[:1].upper() + texto[1:]


def nombre_modo(modo):
    """Devuelve el nombre visible del modo de análisis."""
    nombres = {"guiado": "Guiado", "automatico": "Automático"}
    return nombres.get(modo, str(modo))
