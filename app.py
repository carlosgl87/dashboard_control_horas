import pandas as pd
import streamlit as st 

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

df = pd.read_excel('Horas_Equipo.xlsx',sheet_name='Proyectos')
df_potencial = pd.read_excel('Horas_Equipo.xlsx',sheet_name='Potenciales')

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


personas = list(df[df['Tipo_Equipo'].isin(tipo_equipo)]['Equipo'].unique())
campanas = ['C4','C5','C6','C7','C8','C9','C10','C11','C12','C13']

df_resumen = pd.DataFrame(columns=['Persona','#Proyectos']+campanas)
df_resumen_porcentaje = pd.DataFrame(columns=['Persona','#Proyectos']+campanas)
i = 0
for per in personas:
    lista_horas_camp = []
    lista_horas_camp_porc = []
    for camp in campanas:
        lista_campana_temp = [item for item in list(df.columns) if camp in item]
        horas = df[df['Equipo']==per][camp].sum()
        horas = horas*(1+incluir_incremento)
        lista_horas_camp.append(int(horas))
        lista_horas_camp_porc.append(int((horas/(40*4))*100))
        lista_proyectos = df[(df['Equipo']==per)&(df['Tipo_Proyecto']=='Pared')]['Proyecto'].tolist()
    #print([per]+lista_horas_camp)
    df_resumen.loc[i] = [per,len(lista_proyectos)]+lista_horas_camp
    df_resumen_porcentaje.loc[i] = [per,len(lista_proyectos)]+lista_horas_camp_porc
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



df_persona = df[df['Equipo']==option][['Equipo','Proyecto','Horas']+campanas].fillna(0).reset_index(drop=True)
for var in ['Horas'] + campanas:
    df_persona[var] = df_persona[var].map(int)

st.markdown('## Proyectos Actuales (Pared)')
st.table(df_persona)

st.markdown('## Proyectos Potenciales')
st.table(df_potencial[df_potencial['Equipo']==option][['Proyecto']])