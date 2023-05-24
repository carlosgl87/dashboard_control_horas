import pandas as pd
import streamlit as st 
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import json

######################################################################

def color_survived(val):
    color = '#fa8072' if val==0 else '#f2a400' if val <= 30 else '#fff68f' if val<=80 else '#21cc89'
    return f'background-color: {color}'

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
st.markdown(hide_table_row_index, unsafe_allow_html=True)

######################################################################

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
#df_equipo = pd.read_csv('data/equipo.csv',delimiter=';')
personas = list(df_equipo['equipo'].unique())
campanas = ['C4','C5','C6','C7','C8','C9','C10','C11','C12','C13']

######################################################################

## Crear los Dataframes


## dataframe de estimados de proyectos 
df_estimado_proyectos = pd.DataFrame(columns=['id','nombre','equipo','total_horas']+campanas)
item_list_proyectos = list(container_proy.read_all_items())
cont = 0
for item in item_list_proyectos:
    proy_id = item['id']
    proy_nombre = item['nombre']
    lista_equipo = item['equipo']
    dict_horas = json.loads(item['horas_estimadas_equipo'].replace("'",'"').replace('nan',"0").replace('None',"0"))
    for equipo in lista_equipo:
        total_horas = dict_horas[equipo]['Total']
        lista_horas = []
        for camp in campanas:
            lista_horas.append(dict_horas[equipo][camp])
        lista_datos = [proy_id,proy_nombre,equipo,total_horas] + lista_horas
        df_estimado_proyectos.loc[cont] = lista_datos
        cont = cont + 1

df_estimado_proyectos['total_horas'] = df_estimado_proyectos['total_horas'].map(int)
for camp in campanas:
    df_estimado_proyectos[camp] = df_estimado_proyectos[camp].map(int)
#print(df_estimado_proyectos)

## dataframe de potenciales proyectos
item_list = list(container_potproy.read_all_items())
df_proyectos_potenciales = pd.DataFrame(columns=['id','nombre','estado','equipo'])
cont = 0
for item in item_list:
    id_pot_proy = item['id']
    nombre_pot_proy = item['nombre']
    estado_pot_proy = item['estado']
    equipo_pot_proy = item['equipo']
    for equipo in equipo_pot_proy:
        df_proyectos_potenciales.loc[cont] = [id_pot_proy,nombre_pot_proy,estado_pot_proy,equipo]
        cont = cont + 1

#print(df_proyectos_potenciales)

st.markdown('# GENERAL')

col1, col2 = st.columns(2)

with col1:
   tiempo_extra = st.radio(
    'Incluir tiempo contingencia (20% extra)',
    ('Si', 'No'))

with col2:
   consultores = st.radio(
    'Incluir consultores',
    ('Si', 'No'),index=1)


if tiempo_extra == 'Si':
    incluir_incremento = 0.2
else:
    incluir_incremento = 0

if consultores == 'Si':
    tipo_equipo = ['Staff','Consultor']
else:
    tipo_equipo = ['Staff']

campanas = ['C4','C5','C6','C7','C8','C9','C10','C11','C12','C13']

df_resumen = pd.DataFrame(columns=['Persona','Tipo Proyecto','#Proyectos']+campanas)
df_resumen_porcentaje = pd.DataFrame(columns=['Persona','Tipo Proyecto','#Proyectos']+campanas)
i = 0
for per in personas:
    lista_horas_camp = []
    lista_horas_camp_porc = []
    for camp in campanas:
        lista_campana_temp = [item for item in list(df_estimado_proyectos.columns) if camp in item]
        horas = df_estimado_proyectos[df_estimado_proyectos['equipo']==per][camp].sum()
        horas = horas*(1+incluir_incremento)
        lista_horas_camp.append(int(horas))
        lista_horas_camp_porc.append(int((horas/(40*4))*100))
    lista_proyectos = df_estimado_proyectos[(df_estimado_proyectos['equipo']==per)]['nombre'].tolist()
    lista_ids = df_estimado_proyectos[(df_estimado_proyectos['equipo']==per)]['id'].tolist()
    lista_tipo_proyecto = []
    for ids in lista_ids:
        if 'Run' in ids:
            lista_tipo_proyecto.append('Run')
        else:
            lista_tipo_proyecto.append('Pared')
    lista_tipo_proyecto = list(set(lista_tipo_proyecto))
    #print(lista_tipo_proyecto,len(lista_tipo_proyecto))
    if len(lista_tipo_proyecto) > 1:
        tipo_proyecto = 'Pared/Run'
    else:
        tipo_proyecto = lista_tipo_proyecto[0]
    df_resumen.loc[i] = [per,tipo_proyecto,len(lista_proyectos)]+lista_horas_camp
    df_resumen_porcentaje.loc[i] = [per,tipo_proyecto,len(lista_proyectos)]+lista_horas_camp_porc
    i = i + 1



st.markdown('## Resumen general a nivel de horas')

st.table(df_resumen)

st.markdown('## Resumen general a nivel de porcentaje')
st.markdown("<span style='color:#fa8072'>Sin horas asignadas (0)</span> <br> <span style='color:#f2a400'>Bajas horas asignadas (<30%)</span><br><span style='color:#fff68f'>Medias horas asignadas (<80%)</span><br><span style='color:#21cc89'>Altas horas asignadas (>80%)</span>",
             unsafe_allow_html=True)

st.table(df_resumen_porcentaje.style.applymap(color_survived, subset=campanas))

st.markdown('# DETALLE POR PERSONA')

option = st.selectbox(
    'Elegir Persona',
    personas)



df_persona = df_estimado_proyectos[df_estimado_proyectos['equipo']==option][['equipo','nombre','total_horas']+campanas].fillna(0).reset_index(drop=True)
for var in ['total_horas'] + campanas:
    df_persona[var] = df_persona[var].map(int)

st.markdown('## Proyectos Actuales (Pared)')
st.table(df_persona)

st.markdown('## Proyectos Potenciales')
st.table(df_proyectos_potenciales[(df_proyectos_potenciales['equipo']==option)&(df_proyectos_potenciales['estado'].isin(['Idea','Estimar']))][['nombre','estado']])