import pandas as pd
import streamlit as st
import json
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
CONTAINER_EQUIPO = 'Equipo'

database = client.get_database_client(DATABASE_NAME)
container_proy = database.get_container_client(CONTAINER_NAME_PROYECTOS)
container_equipo = database.get_container_client(CONTAINER_EQUIPO)

item_list_proyectos = list(container_proy.read_all_items())
######################################################################

######################################################################
## Crear DataFrame Proyectos Pared

campanas = ['C4','C5','C6','C7','C8','C9','C10','C11','C12','C13']
df_proyectos_pared = pd.DataFrame(columns=['id','nombre','equipo','horas_estimadas']+campanas)
cont = 0
for item in item_list_proyectos:
    proy_id = item['id']
    proy_nombre = item['nombre']
    print(proy_id,proy_nombre)
    lista_equipo = item['equipo']
    dict_horas = json.loads(item['horas_estimadas_equipo'].replace("'",'"').replace('nan',"0").replace('None',"0"))
    print(lista_equipo)
    for equipo in lista_equipo:
        total_horas = dict_horas[equipo]['Total']
        lista_horas = []
        for camp in campanas:
            lista_horas.append(dict_horas[equipo][camp])
        lista_datos = [proy_id,proy_nombre,equipo,total_horas] + lista_horas
        df_proyectos_pared.loc[cont] = lista_datos
        cont = cont + 1
for camp in campanas:
    df_proyectos_pared[camp] = df_proyectos_pared[camp].map(int)

st.dataframe(df_proyectos_pared)