import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

st.set_page_config(
    layout='wide',
    page_icon='Avatar Inscritos'
)


@st.cache_data
def load_data():
    url = 'https://docs.google.com/spreadsheets/d/15G1fceEst8fr2ORPzUGFtPpfOh9uwMIL1wcf36BAu4Q/edit?gid=1783509356#gid=1783509356'
    conn = st.connection('gsheets', type=GSheetsConnection)
    df_respondentes = conn.read(spreadsheet=url)
    time.sleep(3)
    return df_respondentes

df_respondentes = load_data()
#st.session_state["df_respondentes"] = df_respondentes

columns_list = list(df_respondentes.columns.values.tolist())

columns_list[0] = 'Data'
columns_list[1] = 'Email'
columns_list[2] = 'Nome'
columns_list[5] = 'Idade'
columns_list[6] = 'Regiao'
columns_list[7] = 'Genero'
columns_list[8] = 'Civil'
columns_list[9] = 'Filhos'
columns_list[10] = 'Escolaridade'
columns_list[11] = 'Renda'
columns_list[12] = 'Profissao'
columns_list[13] = 'Seguidor'
columns_list[14] = 'Motivo'
columns_list[15] = 'Impedimento'
columns_list[16] = 'Dificuldades'
columns_list[17] = 'Problemas'
columns_list[19] = 'LiberdadeFinanceira'
columns_list[20] = 'Sonho'
columns_list[21] = 'Trab_mkt_med'
columns_list[22] = 'Clientes_med'
columns_list[23] = 'EsperaMed10k'
columns_list[24] = 'MediaTicketHj'
columns_list[29] = 'email_fixed'

df_respondentes.columns = columns_list

#---------------SIDEBAR--------------
#st.image('logo1-1.png')
st.image('logo2-2.png', width=150)
st.markdown('# Avatar dos Inscritos')
st.sidebar.markdown('## Filtros')

#-------------FILTROS-----------------
#select all filter
#por renda
rendas = df_respondentes['Renda'].value_counts().index.tolist()
rendas.insert(0, 'Todas') #add 'Select All' option to the top 
selected_renda = st.sidebar.multiselect('Faixa de Renda', rendas, default='Todas')

# if select all is chosen, select all artists
if 'Todas' in selected_renda :
	df_resp_filtered = df_respondentes
else:
#st.write(artist_dropdown)
    df_resp_filtered = df_respondentes[df_respondentes['Renda'].isin(selected_renda)]

#por profissao
profissoes = df_resp_filtered['Profissao'].value_counts().index.tolist()
profissoes.insert(0, 'Todas') #add 'Select All' option to the top 
selected_profissoes = st.sidebar.multiselect('Profissão',profissoes, default='Todas')

if 'Todas' in selected_profissoes :
	df_resp_filtered2 = df_resp_filtered
else:
    df_resp_filtered2 = df_resp_filtered[df_resp_filtered['Profissao'].isin(selected_profissoes)]

#por genero 
generos = df_resp_filtered2['Genero'].value_counts().index.tolist()
generos.insert(0, 'Todos') #add 'Select All' option to the top 
selected_genero = st.sidebar.multiselect('Gênero', generos, default='Todos')

# if select all is chosen, select all artists
if 'Todos' in selected_genero :
	df_resp_filtered3 = df_resp_filtered2
else:
#st.write(artist_dropdown)
    df_resp_filtered3 = df_resp_filtered2[df_resp_filtered2['Genero'].isin(selected_genero)]

#por utm_medium - orgiem do lead
origens_lead = df_resp_filtered3['utm_medium'].value_counts().index.tolist()
origens_lead.insert(0, 'Todas') #add 'Select All' option to the top 
selected_utm_medium = st.sidebar.multiselect('Origem do Lead',origens_lead, default='Todas')

if 'Todas' in selected_utm_medium :
	df_resp_filtered4 = df_resp_filtered3
else:
    df_resp_filtered4 = df_resp_filtered3[df_resp_filtered3['utm_medium'].isin(selected_utm_medium)]

#----------Presentation-----
st.sidebar.markdown('Desenvolvido por **Lacaz Data Services**🎲')
st.sidebar.markdown('Dashboard desenvolvido para [Natlhalia Carvalho e Jaque França](https://nathaliamarketingmedico.com/formacao-med10k/?utm_source=Instagram&utm_medium=Bio&utm_id=SVMM+-+LC1)')

#-----------Gráficos-------------------
col1, col2 = st.columns(2)

col1.subheader("Faixa de Renda")
col1.bar_chart(df_resp_filtered4.groupby(['Renda'])['Email'].count(), horizontal=True, color='#01B8AA')
col2.subheader("Escolaridade")
col2.bar_chart(df_resp_filtered4.groupby(['Escolaridade'])['Email'].count(), horizontal=False, color='#01B8AA')

#st.write(df_respondentes.Profissao.value_counts()[:10])

col1, col2 = st.columns(2)

col1.subheader("Profissão")
col1.bar_chart(df_resp_filtered4.Profissao.value_counts()[:10], horizontal=True, color='#01B8AA')
col2.subheader("Idade")
col2.bar_chart(df_resp_filtered4.groupby(['Idade'])['Email'].count(), horizontal=False, color='#01B8AA')

col1, col2 = st.columns([0.3, 0.7])

col1.subheader("Gênero")
col1.bar_chart(df_resp_filtered4.groupby(['Genero'])['Email'].count(), horizontal=False, color='#01B8AA')
col2.subheader("Origem do Lead")
col2.bar_chart(df_resp_filtered4.groupby(['utm_medium'])['Email'].count(), horizontal=False, color='#01B8AA')

#-----Tabela-------
st.write('### 📖 Tabela Detalhada')
df_resp_filtered4


