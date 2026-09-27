import streamlit as st

from experto.explicabilidad import (
    calcular_capas_logicas,
    construir_cadena_principal,
)
from interfaz.utilidades import humanizar_hecho


def mostrar_cadena_inferencia(resultado):
    """Presenta la explicación principal de la inferencia por capas lógicas."""
    cadena = construir_cadena_principal(resultado)

    if not cadena:
        st.info(
            "No fue posible reconstruir una cadena principal de inferencia "
            "para esta evaluación."
        )
        return

    capas = calcular_capas_logicas(cadena)

    st.markdown("### Estructura principal de inferencia")
    st.caption(
        "Las reglas ubicadas en una misma capa pueden activarse de forma "
        "independiente. Las capas posteriores utilizan conclusiones obtenidas "
        "en las anteriores."
    )

    def mostrar_regla(regla):
        with st.container(border=True):
            st.markdown(f"**{regla['id']} · Nivel {regla['nivel']}**")
            st.write("**Condiciones verificadas:**")
            for antecedente in regla["antecedentes"]:
                st.write(f"• {humanizar_hecho(antecedente)}")

            st.write("**Conclusión:**")
            st.markdown(f"### → {humanizar_hecho(regla['conclusion'])}")
            st.caption(regla["descripcion"])

    capas_ordenadas = sorted(capas)
    for posicion, numero_capa in enumerate(capas_ordenadas):
        reglas_capa = capas[numero_capa]
        st.markdown(f"#### Capa lógica {numero_capa}")

        if len(reglas_capa) > 1:
            st.caption("Estas reglas corresponden a ramas paralelas del razonamiento.")

        if len(reglas_capa) == 1:
            mostrar_regla(reglas_capa[0])
        else:
            for inicio in range(0, len(reglas_capa), 2):
                columnas = st.columns(2)
                for indice, regla in enumerate(reglas_capa[inicio : inicio + 2]):
                    with columnas[indice]:
                        mostrar_regla(regla)

        if posicion < len(capas_ordenadas) - 1:
            st.markdown(
                """
                <div style="text-align:center;font-size:30px;padding:8px;">↓</div>
                """,
                unsafe_allow_html=True,
            )

    st.success(
        "Conclusión final: "
        f"{humanizar_hecho(resultado['nivel_riesgo'])}"
    )
