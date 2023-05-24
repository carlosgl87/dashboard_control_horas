import streamlit as st
import pandas as pd
from azure.cosmos import exceptions, CosmosClient, PartitionKey

## DATABASE
# conectarnos a la instancia
endpoint = "https://registrohoras.documents.azure.com:443/"
key = 'i4Jsp0MGQdqQY4QQvhJKM7SIJ2856GrzPmycWQjJOgEWDS93o8zjLwA1neNtGXkcaRyLc2PbdXGfACDbb06FEg=='
client = CosmosClient(endpoint, key)
DATABASE_NAME = 'controlhoras'
CONTAINER_NAME_PROYECTOS = 'Proyectos'
CONTAINER_NAME_POTENCIALESPROYECTOS = 'PotencialesProyectos'
CONTAINER_NAME_HORAS = 'RegistroHoras'
CONTAINER_EQUIPO = 'Equipo'

database = client.get_database_client(DATABASE_NAME)
container_equipo = database.get_container_client(CONTAINER_EQUIPO)

item_list_equipo = list(container_equipo.read_all_items())
df_equipo = pd.DataFrame(columns=['id','equipo','puesto','tipo_equipo','estado'])
cont = 0
for item in item_list_equipo:
    df_equipo.loc[cont] = [item['id'],item['equipo'],item['puesto'],item['tipo_equipo'],item['estado']]
    cont = cont + 1

output_df_equipo = st.experimental_data_editor(df_equipo,num_rows='dynamic')

submit_button_equipo = st.button("Modificar Equipo")


if submit_button_equipo:
    # st.write(output_df_horas_real)
    # st.write(persona)
    # st.write(campana)
    # st.write(output_df_horas_real['S1'].sum())
    for index, row in output_df_equipo.iterrows():
        dictionario_equipo = {
            'id':row['id'],
            'equipo':row['equipo'],
            'puesto' : row['puesto'],
            'tipo_equipo' : row['tipo_equipo'],
            'estado' : row['estado']
            }
        # st.write(dictionario_horas)
        container_equipo.upsert_item(dictionario_equipo)
    st.success('Se actualizó correctamente el equipo', icon="✅")