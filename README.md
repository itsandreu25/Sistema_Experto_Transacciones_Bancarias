# BankShield Expert

Sistema experto académico basado en reglas **SI–ENTONCES** para evaluar el riesgo de posibles anomalías en transferencias bancarias simuladas. El proyecto utiliza Python y Streamlit e implementa encadenamiento hacia adelante, trazabilidad de reglas, dos modos de evaluación y un historial auditable de decisiones.

> **Alcance:** es una simulación educativa. No representa un producto antifraude real ni políticas de una institución financiera.

## Funcionalidades principales

- Banca digital simulada con cuatro perfiles ficticios.
- Detección del dispositivo local, ubicación y hora simulables para la demostración.
- 10 verificaciones de seguridad en **modo guiado**.
- **Modo automático** para simular el comportamiento de una banca real sin interrogar al cliente.
- Base de conocimiento de **42 reglas SI–ENTONCES** organizadas en cuatro niveles.
- Motor de inferencia por **encadenamiento hacia adelante**.
- Resultados: **BAJO, MODERADO, ALTO y CRÍTICO**.
- Acciones simuladas: aprobar, solicitar verificación, retener o bloquear.
- Cadena principal de inferencia por capas lógicas.
- Historial de evaluaciones con hechos y reglas activadas.
- Saldo y movimientos dinámicos durante la sesión.
- Batería final de **25 pruebas automatizadas**.

## Requisitos

- Python 3.11 recomendado.
- Windows, Linux o macOS.

## Instalación

Desde la carpeta del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

En CMD de Windows, la activación es:

```cmd
.venv\Scripts\activate.bat
```

## Ejecutar la aplicación

```powershell
python -m streamlit run app.py
```

Normalmente Streamlit abrirá `http://localhost:8501` en el navegador.

## Ejecutar las pruebas finales

```powershell
python pruebas_finales.py
```

Resultado esperado:

```text
Pruebas ejecutadas: 25
Fallos: 0
Errores: 0
Estado general: CORRECTO
```

También puede ejecutarse directamente la suite estándar:

```powershell
python -m unittest discover -s tests -v
```

## Estructura

```text
BankShield_Expert_FINAL/
├── .streamlit/
│   └── config.toml
├── datos/
│   ├── clientes.py
│   ├── escenarios.py
│   └── movimientos.py
├── experto/
│   ├── hechos.py
│   ├── reglas.py
│   ├── inferencia.py
│   ├── operaciones.py
│   ├── explicabilidad.py
│   └── preguntas.py
├── interfaz/
│   ├── banca.py
│   ├── analisis.py
│   ├── historial.py
│   ├── razonamiento.py
│   ├── utilidades.py
│   └── estilos.py
├── tests/
├── app.py
├── pruebas.py
├── pruebas_finales.py
└── requirements.txt
```

## Modos de evaluación

### Demostración guiada

Un analista revisa y confirma 10 variables antes de iniciar la inferencia. Este modo demuestra de forma explícita la interacción media-alta requerida en la actividad académica.

### Análisis automático

Los mismos datos se incorporan automáticamente y el motor ejecuta la inferencia sin pedir al cliente información técnica que un sistema bancario debería conocer internamente.

## Nota sobre dispositivo, ubicación y hora

En ejecución local, el nombre del equipo se obtiene con el hostname de la máquina que ejecuta Streamlit. En un despliegue web real, el servidor no puede obtener libremente el nombre del computador remoto desde el navegador; un sistema real utilizaría identificadores de dispositivo, sesión y otros mecanismos de seguridad. La ubicación y la hora se simulan en el panel de demostración.
