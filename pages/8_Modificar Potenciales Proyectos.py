import pandas as pd
import streamlit as st
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import json

######################################################################
# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
st.markdown(hide_table_row_index, unsafe_allow_html=True)

######################################################################
## DATABASE
endpoint = "https://registrohoras.documents.azure.com:443/"
key = 'i4Jsp0MGQdqQY4QQvhJKM7SIJ2856GrzPmycWQjJOgEWDS93o8zjLwA1neNtGXkcaRyLc2PbdXGfACDbb06FEg=='
client = CosmosClient(endpoint, key)
DATABASE_NAME = 'controlhoras'
CONTAINER_NAME_PROYECTOS = 'Proyectos'
CONTAINER_NAME_POTENCIALESPROYECTOS = 'PotencialesProyectos'
CONTAINER_NAME_HORAS = 'RegistroHoras'
CONTAINER_EQUIPO = 'Equipo'

database = client.get_database_client(DATABASE_NAME)
#container_proy = database.get_container_client(CONTAINER_NAME_PROYECTOS)
container_potproy = database.get_container_client(CONTAINER_NAME_POTENCIALESPROYECTOS)
#container_horas = database.get_container_client(CONTAINER_NAME_HORAS)
container_equipo = database.get_container_client(CONTAINER_EQUIPO)
######################################################################

######################################################################
## Cargar los datos del equipo y crear la lista de campañas
item_list_equipo = list(container_equipo.read_all_items())
df_equipo = pd.DataFrame(columns=['id','equipo','puesto','tipo_equipo','estado'])
cont = 0
for item in item_list_equipo:
    df_equipo.loc[cont] = [item['id'],item['equipo'],item['puesto'],item['tipo_equipo'],item['estado']]
    cont = cont + 1

personas = list(df_equipo['equipo'].unique())
campanas = ['C4','C5','C6','C7','C8','C9','C10','C11','C12','C13']
######################################################################

item_list_pot_proy = list(container_potproy.read_all_items())
nombre_proyectos = [item['nombre'] for item in item_list_pot_proy]

proyectos = st.selectbox(
    'Elegir Proyecto',
    nombre_proyectos)

diccionario_seleccionado = next(item for item in item_list_pot_proy if item["nombre"] == proyectos)
st.write('Datos del Proyecto')
st.write(diccionario_seleccionado)

pot_proy_estado = st.radio('Estado Potencial Proyecto', ['Idea', 'Estimar','Proyecto','Cancelado'])

pot_proy_equipo = st.multiselect(
    'Equipo Potencial',
    personas,diccionario_seleccionado['equipo'])

submit_button_actualizar_potenciales = st.button("Actualizar datos")

if submit_button_actualizar_potenciales:
    diccionario_seleccionado['equipo'] = pot_proy_equipo
    diccionario_seleccionado['estado'] = pot_proy_estado
    container_potproy.upsert_item(diccionario_seleccionado)
    st.success('Se actualizó correctamente el proyecto potencial', icon="✅")
