import pandas as pd
import streamlit as st
from azure.cosmos import exceptions, CosmosClient, PartitionKey

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
container_proy = database.get_container_client(CONTAINER_NAME_PROYECTOS)
container_potproy = database.get_container_client(CONTAINER_NAME_POTENCIALESPROYECTOS)
container_horas = database.get_container_client(CONTAINER_NAME_HORAS)
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

######################################################################
## Formulario para creación de nuevo proyecto

st.write("Registrar Nuevo Proyecto")
proy_codigo = st.text_input('Codigo del Proyecto')
proy_nombre = st.text_input('Nombre del Proyecto')
proy_equipo = st.multiselect(
    'Equipo Responsable',
    personas)

proy_horasestimadas = st.number_input('Horas Estimadas Totales', key=int)

df_horas_estimadas = pd.DataFrame(columns = ['Equipo','Total','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13'])

df_horas_estimadas['Equipo'] = proy_equipo
df_horas_estimadoas_input = st.experimental_data_editor(df_horas_estimadas)

submitted = st.button('Registrar Proyecto')

if submitted:
    if proy_codigo == '' or proy_nombre == '' or len(proy_equipo) == 0 or proy_horasestimadas == 0:
        st.warning('Falta completar los campos', icon="⚠️")
    else:
        dictionario_nuevo_proyecto = {
            "id":proy_codigo,
            "nombre":proy_nombre,
            "equipo":proy_equipo,
            "horas_estimadas_total": proy_horasestimadas,
            "horas_estimadas_equipo":str(df_horas_estimadoas_input.set_index('Equipo').to_dict('index'))
        }

        st.write(dictionario_nuevo_proyecto)
        container_proy.upsert_item(dictionario_nuevo_proyecto)
        st.success('Se registró correctamente el nuevo proyecto', icon="✅")

        
