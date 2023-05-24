import pandas as pd
import streamlit as st
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import json

## DATABASE
# conectarnos a la instancia
endpoint = "https://registrohoras.documents.azure.com:443/"
key = 'i4Jsp0MGQdqQY4QQvhJKM7SIJ2856GrzPmycWQjJOgEWDS93o8zjLwA1neNtGXkcaRyLc2PbdXGfACDbb06FEg=='
client = CosmosClient(endpoint, key)
DATABASE_NAME = 'controlhoras'
CONTAINER_NAME = 'Proyectos'
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

item_list = list(container.read_all_items())
nombre_proyectos = [item['nombre'] for item in item_list]

proyectos = st.selectbox(
    'Elegir Proyecto',
    nombre_proyectos)
dictionario_seleccionado = next(item for item in item_list if item["nombre"] == proyectos)

st.write('Datos del Proyecto')
st.write(dictionario_seleccionado)

diccionario_horas = json.loads(dictionario_seleccionado['horas_estimadas_equipo'].replace("'",'"').replace('nan',"0").replace('None',"0"))
df_horas = pd.DataFrame.from_dict(diccionario_horas, orient='index')

df_equipo = pd.read_csv('data/equipo.csv',delimiter=';')

output_df_horas_estimadas = st.experimental_data_editor(df_horas, num_rows="dynamic")

submit_button = st.button("Registrar Horas")

if submit_button:
    dictionario_seleccionado['equipo'] = list(output_df_horas_estimadas.index)
    dictionario_seleccionado['horas_estimadas_total'] = str(output_df_horas_estimadas['Total'].map(int).sum())
    dictionario_seleccionado['horas_estimadas_equipo'] = str(output_df_horas_estimadas.to_dict('index'))
    st.write(dictionario_seleccionado)
    container.upsert_item(dictionario_seleccionado)

st.dataframe(df_equipo)