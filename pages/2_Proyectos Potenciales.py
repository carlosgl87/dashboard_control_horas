import pandas as pd
import streamlit as st
from azure.cosmos import exceptions, CosmosClient, PartitionKey

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

database = client.get_database_client(DATABASE_NAME)
container_potproy = database.get_container_client(CONTAINER_NAME_POTENCIALESPROYECTOS)
item_list_pot_proy = list(container_potproy.read_all_items())
######################################################################

######################################################################
## Crear dataframe potenciales proyectos
df_potenciales_proyectos = pd.DataFrame(columns=['id','nombre','estado','equipo'])
for i in range(len(item_list_pot_proy)):
    p_id = item_list_pot_proy[i]['id']
    p_nom = item_list_pot_proy[i]['nombre']
    p_est = item_list_pot_proy[i]['estado']
    p_equ = item_list_pot_proy[i]['equipo']
    df_potenciales_proyectos.loc[i] = [p_id,p_nom,p_est,p_equ]

st.dataframe(df_potenciales_proyectos)