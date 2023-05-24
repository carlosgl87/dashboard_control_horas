import streamlit as st
st.set_page_config(
    page_title="Home",
    page_icon="👋",
)
st.markdown("## Aplicacion para la gestión de proyectos! 👋")
st.markdown(
    """
    En esta aplicación registrarán los proyectos y potenciales proyectos, 
    así como las horas dedicadas para el desarrollo de los mismos

    #### ¿Qué modulos se tienen?
    - **Registro Horas**: Registrar las horas trabajadas tanto en proyectos como en estimaciones.
    - **Proyectos Pared Estimado**: Todos los proyectos en pared con el equipo dedicado y las horas estimadas
    - **Proyectos Potenciales**: Todos los potenciales proyectos, tanto en idea como para estimar
    - **Control Horas Estimado**: Dashboard con indicadores de la estimación de horas dedicadas del equipo por todo el año
    - **Control Horas Real**: Dashboard sobre el trabajo real del equipo
    - **Registro Proyectos**: Registrar un nuevo proyecto
    - **Registro Proyectos Potenciales**: Registrar un proyecto potencial
    - **Modificar Proyectos**: Modificar equipo del proyecto y estimado de horas
    - **Modificar Potenciales Proyectos**: Modificar equipo del proyecto y estado del proyecto
"""
)