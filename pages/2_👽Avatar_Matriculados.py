import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
import datetime
from collections import Counter 
import re
from unidecode import unidecode
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

#st.session_state["df_respondentes"]
st.set_page_config(
    layout='wide',
    page_icon='Avatar Matriculados'
)

@st.cache_data
def load_data(file, page):
    #url = 'https://docs.google.com/spreadsheets/d/1jU6I6H2pYhJajJVZqFreYudtIyepPMTbW1MGiUh4edg/edit?gid=1606288776#gid=1606288776'
    #conn = st.connection('gsheets', type=GSheetsConnection)
    #df = conn.read(spreadsheet=url)
    df = pd.read_excel(file, sheet_name=page)
    time.sleep(3)
    return df

#url_matriculados = 'https://docs.google.com/spreadsheets/d/1jU6I6H2pYhJajJVZqFreYudtIyepPMTbW1MGiUh4edg/edit?gid=1606288776#gid=1606288776'

df_matriculados = load_data('Matriculados.xlsx', 'M2')

columns_list = list(df_matriculados.columns.values.tolist())

columns_list[0] = 'Data'
columns_list[1] = 'Email'
columns_list[2] = 'Nome'
columns_list[5] = 'Idade' #grafico
columns_list[6] = 'Regiao'
columns_list[7] = 'Genero' #grafico
columns_list[8] = 'Civil'
columns_list[9] = 'Filhos'
columns_list[10] = 'Escolaridade' #grafico
columns_list[11] = 'Renda' #grafico
columns_list[12] = 'Profissao' #grafico
columns_list[13] = 'Seguidor' #grafico
columns_list[14] = 'Med10KKnowhow'
columns_list[15] = 'ComoConheceu' #grafico
columns_list[16] = 'Trab_mkt_med' #grafico
columns_list[17] = 'Trab_mkt_med_tempo' #grafico
columns_list[18] = 'Clientes_med' #grafico
columns_list[19] = 'Clientes_med_qnt'  #grafico
columns_list[20] = 'ServicosOferecidos'
columns_list[21] = 'Ferramentas'
columns_list[22] = 'Dificuldades_MktMed'  #contador palavras
columns_list[23] = 'Dificuldades_Carreira' #contador palavras
columns_list[24] = 'SatisfacaoMed10k' #contador palavras
columns_list[25] = 'topicos_Med10k' 
columns_list[26] = 'Motivo' #contador palavras
columns_list[27] = 'ObjetivoFaturamento'
columns_list[28] = 'Horas_dedicacao'
columns_list[29] = 'Trab_digital'
columns_list[30] = 'Jornada_trab'
columns_list[31] = 'Agencia'   #grafico
columns_list[32] = 'dia_a_dia'
columns_list[33] = 'conteudos_assistidos' 
columns_list[34] = 'espera_aprender_Med10k' #contador palavras
columns_list[35] = 'Sonho' #contador palavras
columns_list[36] = 'Rede_social'
columns_list[37] = 'Duvida' #contador palavras
columns_list[38] = 'Del1'
columns_list[39] = 'Del2'
columns_list[40] = 'Situacao'
columns_list[41] = 'Acesso_comunidade'
columns_list[42] = 'Acesso_plataforma'
columns_list[43] = 'Consultoria' #filtro
columns_list[44] = 'Ja_fez_consultoria'

df_matriculados.columns = columns_list

df_matriculados = df_matriculados.drop(['Del1'], axis=1)
df_matriculados = df_matriculados.drop(['Del2'], axis=1)

#df_matriculados['Data'] = pd.to_datetime(df_matriculados['Data'].str.title(), infer_datetime_format=True)

df_matriculados['Turma'] = 'NaN'
date_turma2 = datetime.date(2024, 9, 1)

for index, row in df_matriculados.iterrows():
    if row['Data'] >= date_turma2:
        df_matriculados.loc[index,'Turma'] =  str('Turma 2')
    else:
        df_matriculados.loc[index,'Turma'] =  str('Turma 1')


#--------- Logo & Titulo --------
st.image('logo1-1.png', width=220)
#st.image('logo2-2.png', width=150)
st.markdown('## Avatar dos Matriculados 👽')

#---------------SIDEBAR--------------
st.sidebar.markdown('## Filtros')

#---------------FILTROS--------
#select all filter
#por Situacao
situacoes = df_matriculados['Situacao'].value_counts().index.tolist()
situacoes.insert(0, 'Todas') #add 'Select All' option to the top 
selected_situacao = st.sidebar.multiselect('Situação', situacoes, default='ATIVO')

# if select all is chosen, select all artists
if 'Todas' in selected_situacao :
	df_resp_filtered = df_matriculados
else:
#st.write(artist_dropdown)
    df_resp_filtered = df_matriculados[df_matriculados['Situacao'].isin(selected_situacao)]


#por Turma
turmas = df_resp_filtered['Turma'].value_counts().index.tolist()
turmas.insert(0, 'Todas') #add 'Select All' option to the top 
selected_turmas = st.sidebar.multiselect('Turma Med10K', turmas, default='Todas')

# if select all is chosen, select all artists
if 'Todas' in selected_turmas :
	df_resp_filtered2 = df_resp_filtered
else:
#st.write(artist_dropdown)
    df_resp_filtered2 = df_resp_filtered[df_resp_filtered['Turma'].isin(selected_turmas)]


#por renda
rendas = df_resp_filtered2['Renda'].value_counts().index.tolist()
rendas.insert(0, 'Todas') #add 'Select All' option to the top 
selected_renda = st.sidebar.multiselect('Faixa de Renda', rendas, default='Todas')

# if select all is chosen, select all artists
if 'Todas' in selected_renda :
	df_resp_filtered3 = df_resp_filtered2
else:
#st.write(artist_dropdown)
    df_resp_filtered3 = df_resp_filtered2[df_resp_filtered2['Renda'].isin(selected_renda)]

#por profissao
profissoes = df_resp_filtered3['Profissao'].value_counts().index.tolist()
profissoes.insert(0, 'Todas') #add 'Select All' option to the top 
selected_profissoes = st.sidebar.multiselect('Profissão',profissoes, default='Todas')

if 'Todas' in selected_profissoes :
	df_resp_filtered4 = df_resp_filtered3
else:
    df_resp_filtered4 = df_resp_filtered3[df_resp_filtered3['Profissao'].isin(selected_profissoes)]

#por genero 
generos = df_resp_filtered4['Genero'].value_counts().index.tolist()
generos.insert(0, 'Todos') #add 'Select All' option to the top 
selected_genero = st.sidebar.multiselect('Gênero', generos, default='Todos')

# if select all is chosen, select all artists
if 'Todos' in selected_genero :
	df_resp_filtered5 = df_resp_filtered4
else:
#st.write(artist_dropdown)
    df_resp_filtered5 = df_resp_filtered4[df_resp_filtered4['Genero'].isin(selected_genero)]

#por seguidor
seguidores = df_resp_filtered5['Seguidor'].value_counts().index.tolist()
seguidores.insert(0, 'Todas') #add 'Select All' option to the top 
selected_seguidores = st.sidebar.multiselect('Seguidor',seguidores, default='Todas')

if 'Todas' in selected_seguidores :
	df_resp_filtered6 = df_resp_filtered5
else:
    df_resp_filtered6 = df_resp_filtered5[df_resp_filtered5['Seguidor'].isin(selected_seguidores)]


#por consultoria restante
consultorias = df_resp_filtered5['Consultoria'].value_counts().index.tolist()
consultorias.insert(0, 'Todas') #add 'Select All' option to the top 
selected_consultoria = st.sidebar.multiselect('Possui Consultoria?',consultorias, default='Todas')

if 'Todas' in selected_consultoria :
	df_resp_filtered7 = df_resp_filtered6
else:
    df_resp_filtered7 = df_resp_filtered6[df_resp_filtered6['Consultoria'].isin(selected_consultoria)]


#----------Presentation-----
st.sidebar.markdown('Desenvolvido por **Lacaz Data Services**🎲')
st.sidebar.markdown('Dashboard desenvolvido para [Natlhalia Carvalho e Jaque França](https://nathaliamarketingmedico.com/formacao-med10k/?utm_source=Instagram&utm_medium=Bio&utm_id=SVMM+-+LC1)')


#-----------Gráficos-------------------
col1, col2 = st.columns(2)
col1.subheader("Faixa de Renda")
col1.bar_chart(df_resp_filtered7.groupby(['Renda'])['Email'].count(), horizontal=True, color='#01B8AA')
col2.subheader("Escolaridade")
col2.bar_chart(df_resp_filtered7.groupby(['Escolaridade'])['Email'].count(), horizontal=False, color='#01B8AA')


col1, col2, col3 = st.columns([0.44, 0.4, 0.16])
col1.subheader("Profissão")
col1.bar_chart(df_resp_filtered7.Profissao.value_counts()[:10], horizontal=True, color='#01B8AA')
col2.subheader("Seguidor a quanto tempo?")
col2.bar_chart(df_resp_filtered7.groupby(['Seguidor'])['Email'].count(), horizontal=False, color='#01B8AA')
col3.subheader("Como Conheceu o Med10K?")
col3.bar_chart(df_resp_filtered7.ComoConheceu.value_counts()[:10], horizontal=False, color='#01B8AA')


col1, col2, col3, col4 = st.columns([0.34, 0.16, 0.34, 0.16])
col1.subheader("Idade")
col1.bar_chart(df_resp_filtered7.groupby(['Idade'])['Email'].count(), horizontal=False, color='#01B8AA')
col2.subheader("Gênero")
col2.bar_chart(df_resp_filtered7.groupby(['Genero'])['Email'].count(), horizontal=False, color='#01B8AA')
col3.subheader("Estado Civil")
col3.bar_chart(df_resp_filtered7.groupby(['Civil'])['Email'].count(), horizontal=False, color='#01B8AA')
col4.subheader("Tem Filhos?")
col4.bar_chart(df_resp_filtered7.groupby(['Filhos'])['Email'].count(), horizontal=False, color='#01B8AA')


col1, col2, col3, col4 = st.columns([0.2, 0.4, 0.2, 0.2])
col1.subheader("Trabalha com Mrkt Médico?")
col1.bar_chart(df_resp_filtered7.groupby(['Trab_mkt_med'])['Email'].count(), horizontal=False, color='#01B8AA')
col2.subheader("Se sim, quanto tempo?")
col2.bar_chart(df_resp_filtered7.groupby(['Trab_mkt_med_tempo'])['Email'].count(), horizontal=False, color='#01B8AA')
col3.subheader("Possui Clientes Médicos?")
col3.bar_chart(df_resp_filtered7.groupby(['Clientes_med'])['Email'].count(), horizontal=False, color='#01B8AA')
col4.subheader("Pretende ter Agência?")
col4.bar_chart(df_resp_filtered7.groupby(['Agencia'])['Email'].count(), horizontal=False, color='#01B8AA')


# Contagem de valores para o eixo y
#contagem_estado_civil = df_resp_filtered7['Civil'].value_counts().reset_index()

# Renomeando as colunas
#contagem_estado_civil.columns = ['Estado Civil', 'Contagem']

# Ordenando o DataFrame pela contagem de forma descendente
#contagem_estado_civil = contagem_estado_civil.sort_values(by='Contagem', ascending=False)

# Plotando o gráfico
#plt.figure(figsize=(4, 3))
#sns.barplot(x='Estado Civil', y='Contagem', data=contagem_estado_civil)
#plt.title('Estado Civil')

# Exibindo no streamlit
#st.pyplot(plt)


# Contagem de valores para o eixo y
contagem_estado_civil = df_resp_filtered7['Civil'].value_counts().reset_index()

# Renomeando as colunas
contagem_estado_civil.columns = ['Civil', 'Contagem']

# Ordenando o DataFrame pela contagem de forma descendente
contagem_estado_civil = contagem_estado_civil.sort_values(by='Contagem', ascending=False)

# Criando o gráfico com Altair
chart = alt.Chart(contagem_estado_civil).mark_bar().encode(
    x=alt.X('Civil:N', sort='-y'),
    y='Contagem:Q'
).properties(
    title='Estado Civil'
)

# Exibindo o gráfico no Streamlit
st.altair_chart(chart, use_container_width=True)




st.markdown('### 🔟 Palavras Mais Repedidas:')

#funcao contadora de palavras
def words_counter(df, column):
    
    concatenate_column = ''.join(df[column])
    treat_text = unidecode(re.sub(r'[^\w\s]','',concatenate_column).lower())

    by_word_v0 = treat_text.split()

    by_word = []
    for word in by_word_v0:
        if len(word) > 5:
            by_word.append(word)

        else:
            pass 


    word_counter = Counter(by_word)
    most_common_words = word_counter.most_common()
    df_words = pd.DataFrame(most_common_words, columns = ['Palavra','Contagem'])
    return df_words.head(10)


count_sonho = words_counter(df_resp_filtered7, 'Sonho') #ok
count_difmkt = words_counter(df_resp_filtered7, 'Dificuldades_MktMed')
count_difcar = words_counter(df_resp_filtered7, 'Dificuldades_Carreira')
count_satis = words_counter(df_resp_filtered7, 'SatisfacaoMed10k')
count_motivo = words_counter(df_resp_filtered7, 'Motivo') #ok
count_espera = words_counter(df_resp_filtered7, 'espera_aprender_Med10k') #ok
count_duvida = words_counter(df_resp_filtered7, 'Duvida')



col1, col2, col3 = st.columns(3)
col1.subheader('Maior Sonho')
col1.bar_chart(count_sonho, x='Palavra', y='Contagem', x_label = 'Sonho', y_label= '', horizontal=True, color='#01B8AA')
col2.subheader('Motivação')
col2.bar_chart(count_motivo, x='Palavra', y='Contagem', x_label = 'Motivação', y_label= '', horizontal=True, color='#01B8AA')
col3.subheader('Expectativa')
col3.bar_chart(count_espera, x='Palavra', y='Contagem', x_label = 'Expectativa', y_label= '', horizontal=True, color='#01B8AA')

col1, col2, col3 = st.columns(3)
col1.subheader('Dificuldades em Mkt Médico')
col1.bar_chart(count_difmkt, x='Palavra', y='Contagem', x_label = 'Dificuldades Mkt Med', y_label= '', horizontal=True, color='#01B8AA')
col2.subheader('Alguma Dúvida?')
col2.bar_chart(count_duvida, x='Palavra', y='Contagem', x_label = 'Dúvida', y_label= '', horizontal=True, color='#01B8AA')
col3.subheader('Satisfação com o MED10K')
col3.bar_chart(count_satis, x='Palavra', y='Contagem', x_label = 'Expectativa', y_label= '', horizontal=True, color='#01B8AA')


#------------- Origem matriculados----

#url_leads_matriculados = 

#st.markdown('### Origem dos :')

#df_matriculados_utm = load_data(url_leads_matriculados)


#-----Tabela-------
st.write('### 📖 Tabela Detalhada')
df_resp_filtered6







