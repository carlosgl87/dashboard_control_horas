import pandas as pd
import streamlit as st
from azure.cosmos import exceptions, CosmosClient, PartitionKey

## DATABASE
# conectarnos a la instancia
endpoint = "https://registrohoras.documents.azure.com:443/"
key = 'i4Jsp0MGQdqQY4QQvhJKM7SIJ2856GrzPmycWQjJOgEWDS93o8zjLwA1neNtGXkcaRyLc2PbdXGfACDbb06FEg=='
client = CosmosClient(endpoint, key)
DATABASE_NAME = 'controlhoras'
CONTAINER_NAME = 'PotencialesProyectos'
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

df_equipo = pd.read_csv('data/equipo.csv',delimiter=';')
st.write("Registrar Nuevo Proyecto")
pot_proy_codigo = st.text_input('Codigo del Potencial Proyecto')
pot_proy_nombre = st.text_input('Nombre del Potencial Proyecto')
pot_proy_equipo = st.multiselect(
    'Equipo Potencial',
    df_equipo['Equipo'].tolist())

pot_proy_estado = st.radio('Estado Potencial Proyecto', ['Idea', 'Estimar'])

submitted = st.button('Registrar Proyecto')

if submitted:
    if pot_proy_codigo == '' or pot_proy_nombre == '' or len(pot_proy_equipo) == 0 or pot_proy_estado == '':
        st.warning('Falta completar los campos', icon="⚠️")
    else:
        dictionario_potencial_proyecto = {
            "id":pot_proy_codigo,
            "nombre":pot_proy_nombre,
            "equipo":pot_proy_equipo,
            "estado": pot_proy_estado,
        }
    container.upsert_item(dictionario_potencial_proyecto)
    st.write(dictionario_potencial_proyecto)
    