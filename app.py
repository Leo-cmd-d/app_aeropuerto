import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
##################################################################################################################################
#                                                   CARGA DE DATOS
##################################################################################################################################
url = 'https://github.com/juliandariogiraldoocampo/ia_taltech/raw/refs/heads/main/aeropuerto/data_sint_oper_pred_clas.csv'
df = pd.read_csv(url)
##################################################################################################################################
#                                                   ANÁLISIS
##################################################################################################################################
df_tipo_vuelo = df['TIPO_VUELO'].value_counts().reset_index()
estadisticos = df_tipo_vuelo['count'].describe()
maximo=estadisticos['max']
minimo=estadisticos['min']
media = estadisticos['mean']

#TOP 5 AEROPUERTOS CON MAYOR NÚMERO DE OPERACIONES
df_top5_ops_aeropuertos = df['AEROPUERTO_OPERACION'].value_counts().reset_index().head(5)
df_top5_ops_aeropuertos.columns = ['AEROPUERTO_OPERACION','count']

#TOP 10 RUTAS CON MAYOR NÚMERO DE OPERACIONES
df['RUTA'] = df['ORIGEN'] + '↪️' + df['DESTINO']
df_top10_rutas = df['RUTA'].value_counts().reset_index().head(10)
df_top10_rutas.columns = ['RUTA','CANTIDAD']
 
##################################################################################################################################
#                                                   CONFIGURACIÓN DE LA PÁGINA
##################################################################################################################################
# Configuración de la página
st.set_page_config(
    page_title='Operaciones Acumuladas',
    layout='centered',
    initial_sidebar_state='collapsed'
)

#AJUSTE DEL ANCHO MÁXIMO DEL CONTENEDOR PRINCIPAL 1200 PIXELES
st.markdown(
    '''
    <style>
        .block-container{
            max-width: 1200px;
        .st-emotion-cache-rsr9ey {
            color: skyblue;
        }
    </style>
    ''',
    unsafe_allow_html=True
)

# Opciones de Paletas de colores: 'Plotly', 'D3', 'G10', 'T10', 'Alphabet', 'Dark24', 'Light24', 'Set1', 'Set2', 'Set3', 'Pastel1', 'Pastel2', 'Antique', 'Bold', 'Prism'
# https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express
paleta_barras = px.colors.qualitative.Antique


######################################################################################################################################
#                                                   VISUALIZACIÓN
####################################################################################################################################### st.subheader('Máximo')
# st.text(maximo)
# st.subheader('Mínimo')
# st.text(minimo)
# st.subheader('Media')
# st.text(media)

#ESTABLECER IMAGEN EN ENCABEZADO UTILIZANDO UN CONTAINER imagen tomada de: https://www.pexels.com/
st.image('encabezado.png', use_container_width=True)
st.title('Datos Operaciones')
with st.container(border=True):

    col1, col2, col3 =st.columns(3)
    with col1:
        st.metric('Mínimo',f'{minimo:.0f}','100',border=True)
    with col2:
        st.metric('Media',f'{media:.0f}','15%',border=True)
    with col3:
        st.metric('Máximo',f'{maximo:.0f}','-10%',border=True)

    #VER DATAFRAME EN DESPLEGABLE:
with st.expander('Ver Matriz de Datos'):
    st.dataframe(df)

with st.expander('Top 5 Aeropuertos con Mayor Número de operaciones:'):
    st.dataframe(df_top5_ops_aeropuertos)
#ANÁLISIS AEROPUERTOS CON MAYOR NÚMEROS DE OPERACIONES
fig_barras = px.bar(
    df_top5_ops_aeropuertos, 
    x='AEROPUERTO_OPERACION',
    y='count',
    title='Top 5 Aeropuertos con mayor número de operaciones',
    labels={
        'AEROPUERTO_OPERACION' : 'Aeropuerto',
        'count' : 'Número de operaciones'
    },
    color = 'AEROPUERTO_OPERACION',
    color_discrete_sequence=paleta_barras
)
#BORRAR leyenda de paleta colores
fig_barras.update_layout(showlegend=False)
#______________________________________________________________________________________________________________________________
#ANALISIS DE RUTAS
df_top10_rutas = df_top10_rutas.sort_values('CANTIDAD', ascending=True)
fig_rutas = px.bar(
    df_top10_rutas,
    x='CANTIDAD',
    y='RUTA',
    title='TOP 10 RUTAS con mayor número de operaciones',
    color = 'CANTIDAD',
    color_continuous_scale='teal',
)
#BORRAR leyenda de paleta colores
fig_rutas.update_coloraxes(showscale=False)

with st.container(border=True):
    col4, col5=st.columns(2)
    with col4:
        st.plotly_chart(fig_barras,use_container_width=True)
    with col5:
        st.plotly_chart(fig_rutas,use_container_width=True)


tab1, tab2 = st.tabs(['📋Matriz de Datos','📊Gráfica de Barras'])
with tab1:
    st.dataframe(df_top10_rutas)
with tab2:
    fig_rutas = px.bar(
    df_top10_rutas,
    x='CANTIDAD',
    y='RUTA',
    title='🛩️🛩️TOP 10 RUTAS con mayor número de operaciones🛩️🛩️',
    color = 'CANTIDAD',
    color_continuous_scale='cividis',
    )
    fig_rutas.update_coloraxes(showscale=False)
    st.plotly_chart(fig_rutas,use_container_width=True,key='rutas_tab2')
    df_top10_rutas = df_top10_rutas.sort_values('CANTIDAD', ascending=True)