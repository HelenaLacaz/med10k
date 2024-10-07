import streamlit as st
import pandas as pd
#import time
import datetime
from collections import Counter 
import re
from unidecode import unidecode
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
    #time.sleep(3)
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
date_turma2 = pd.Timestamp(datetime.date(2024, 9, 1))

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
# Renda
contagem_renda = df_resp_filtered7['Renda'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_renda.columns = ['Faixa de Renda', 'Contagem']
contagem_renda = contagem_renda.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_renda = alt.Chart(contagem_renda).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Faixa de Renda:N', sort='-y', axis=alt.Axis(labelAngle=-90, labelLimit=120), title=None),  # Rotaciona os rótulos e define limite de tamanho),
    y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)) 
).properties(
    title='Faixa de Renda'
).interactive()

# Idade
contagem_idade = df_resp_filtered7['Idade'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_idade.columns = ['Idade', 'Contagem']
contagem_idade = contagem_idade.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_idade = alt.Chart(contagem_idade).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Idade:N', sort='-y', title=None),
    y=alt.Y('Contagem:Q', axis=alt.Axis(title=None))
).properties(
    title='Faixa de Idade'
).interactive()


# Escolaridade
contagem_escol = df_resp_filtered7['Escolaridade'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_escol.columns = ['Escolaridade', 'Contagem']
contagem_escol = contagem_escol.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_escol = alt.Chart(contagem_escol).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Escolaridade:N', sort='-y', axis=alt.Axis(labelAngle=-90, labelLimit=120), title=None),  # Rotaciona os rótulos e define limite de tamanho),
    y=alt.Y('Contagem:Q', axis=alt.Axis(title=None))
).properties(
    title='Escolaridade',
    height=450 
).interactive()


#Profissao
contagem_profissao = df_resp_filtered7['Profissao'].value_counts()[:10].reset_index() #contagem da coluna de interesse y
contagem_profissao.columns = ['Profissao', 'Contagem']
contagem_profissao = contagem_profissao.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_profissao= alt.Chart(contagem_profissao).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Contagem', title=None),
    y=alt.Y('Profissao', sort='-x', axis=alt.Axis(labelLimit=150, title=None))
).properties(
    title='Profissão Top10',
    height=450 
).interactive()


# Seguidor
contagem_seguidor = df_resp_filtered7['Seguidor'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_seguidor.columns = ['Seguidor', 'Contagem']
contagem_seguidor = contagem_seguidor.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_seguidor = alt.Chart(contagem_seguidor).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Seguidor:N', sort='-y', axis=alt.Axis(labelAngle=-90, labelLimit=120), title=None),  # Rotaciona os rótulos e define limite de tamanho),
    y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)) 
).properties(
    title='Seguidor a quanto tempo?',
    height=450 
).interactive()


# Como conheceu med10k
contagem_10k = df_resp_filtered7['ComoConheceu'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_10k.columns = ['ComoConheceu', 'Contagem']
contagem_10k = contagem_10k.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_10k = alt.Chart(contagem_10k).mark_arc(innerRadius=50).encode(
    theta=alt.Theta('Contagem:Q'),
    color = alt.Color('ComoConheceu:N', legend=alt.Legend(orient='bottom', direction='horizontal'), title=None)
).properties(
    title='Como conheceu o Med10k?'
).interactive()


# Genero
contagem_genero = df_resp_filtered7['Genero'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_genero.columns = ['Genero', 'Contagem']
contagem_genero = contagem_genero.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_genero = alt.Chart(contagem_genero).mark_arc(innerRadius=50).encode(
    theta=alt.Theta('Contagem:Q'),
    color = alt.Color('Genero:N', legend=alt.Legend(orient='bottom', direction='horizontal'), title=None)
).properties(
    title='Gênero'
).interactive()


# Filhos
contagem_filhos = df_resp_filtered7['Filhos'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_filhos.columns = ['Filhos', 'Contagem']
contagem_filhos = contagem_filhos.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_filhos = alt.Chart(contagem_filhos).mark_arc(innerRadius=50).encode(
    theta=alt.Theta('Contagem:Q'),
    color = alt.Color('Filhos:N', legend=alt.Legend(orient='bottom', direction='horizontal'), title=None)
).properties(
    title='Tem Filhos?'
).interactive()

#Civil
contagem_civil = df_resp_filtered7['Civil'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_civil.columns = ['Civil', 'Contagem']
contagem_civil = contagem_civil.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_civil = alt.Chart(contagem_civil).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Civil:N', sort='-y', axis=alt.Axis(labelAngle=-90, labelLimit=120), title=None),  # Rotaciona os rótulos e define limite de tamanho),
    y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)) 
).properties(
    title='Estado Civil',
    height=450 
).interactive()




#Trab_mkt_med
contagem_trab_mkt_med = df_resp_filtered7['Trab_mkt_med'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_trab_mkt_med.columns = ['Trab_mkt_med', 'Contagem']
contagem_trab_mkt_med = contagem_trab_mkt_med.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_trab_mkt_med = alt.Chart(contagem_trab_mkt_med).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Trab_mkt_med:N', sort='-y', axis=alt.Axis(labelAngle=-90, labelLimit=120), title=None),  # Rotaciona os rótulos e define limite de tamanho),
    y=alt.Y('Contagem:Q', axis=alt.Axis(title=None))
).properties(
    title='Trabalha com Mrkt Médico?',
    height=450 
).interactive()


#Trab_mkt_med
contagem_tempo = df_resp_filtered7['Trab_mkt_med_tempo'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_tempo.columns = ['Trab_mkt_med_tempo', 'Contagem']
contagem_tempo = contagem_tempo.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_tempo = alt.Chart(contagem_tempo).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Trab_mkt_med_tempo:N', sort='-y', axis=alt.Axis(labelAngle=-90, labelLimit=120), title=None),  # Rotaciona os rótulos e define limite de tamanho),
    y=alt.Y('Contagem:Q', axis=alt.Axis(title=None))
).properties(
    title='Se sim, quanto tempo?',
    height=450 
).interactive()


#Tclientes Med
contagem_clientes_med = df_resp_filtered7['Clientes_med'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_clientes_med.columns = ['Clientes_med', 'Contagem']
contagem_clientes_med = contagem_clientes_med.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_clientes_med = alt.Chart(contagem_clientes_med).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Clientes_med:N', sort='-y', axis=alt.Axis(labelAngle=-90, labelLimit=120), title=None),  # Rotaciona os rótulos e define limite de tamanho),
    y=alt.Y('Contagem:Q', axis=alt.Axis(title=None)) 
).properties(
    title='Possui Clientes Médicos?',
    height=450 
).interactive()


#Agencia
contagem_agencia = df_resp_filtered7['Agencia'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_agencia.columns = ['Agencia', 'Contagem']
contagem_agencia = contagem_agencia.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_agencia = alt.Chart(contagem_agencia).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Agencia:N', sort='-y', axis=alt.Axis(labelAngle=-90, labelLimit=120), title=None),  # Rotaciona os rótulos e define limite de tamanho),
    y=alt.Y('Contagem:Q', axis=alt.Axis(title=None))
).properties(
    title='Pretende ter Agência?',
    height=450 
).interactive()


col1, col2 = st.columns(2)
col1.altair_chart(chart_renda, use_container_width=True)
col2.altair_chart(chart_idade, use_container_width=True)

col1, col2 = st.columns(2)
col1.altair_chart(chart_profissao, use_container_width=True)
col2.altair_chart(chart_escol, use_container_width=True)

col1, col2 = st.columns([0.7, 0.3])
col1.altair_chart(chart_seguidor, use_container_width=True)
col2.altair_chart(chart_10k, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.altair_chart(chart_genero, use_container_width=True)
col2.altair_chart(chart_civil, use_container_width=True)
col3.altair_chart(chart_filhos, use_container_width=True)


col1, col2, col3,col4 = st.columns([0.2, 0.4, 0.2, 0.2])
col1.altair_chart(chart_trab_mkt_med, use_container_width=True)
col2.altair_chart(chart_tempo, use_container_width=True)
col3.altair_chart(chart_clientes_med, use_container_width=True)
col4.altair_chart(chart_agencia, use_container_width=True)


st.markdown('### 🔟 Palavras Mais Repedidas:')

#funcao contadora de palavras
def words_counter(df, column):
    
    concatenate_column = ''.join(df[column])
    treat_text = unidecode(re.sub(r'[^\w\s]','',concatenate_column).lower())

    by_word_v0 = treat_text.split()

    by_word = []
    for word in by_word_v0:
        if len(word) > 5 and word != 'nathalia' and word != 'medica' and word != 'minhas':
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



#count_sonho
contagem_sonho = count_sonho.sort_values(by='Contagem', ascending=False) # ordenação
chart_sonho= alt.Chart(contagem_sonho).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Contagem', title=None),
    y=alt.Y('Palavra', sort='-x', axis=alt.Axis(labelLimit=150, title=None))
).properties(
    title='Maior Sonho',
    height=450 
).interactive()


#Motivação
contagem_motivo = count_motivo.sort_values(by='Contagem', ascending=False) # ordenação
chart_motivo= alt.Chart(contagem_motivo).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Contagem', title=None),
    y=alt.Y('Palavra', sort='-x', axis=alt.Axis(labelLimit=150, title=None))
).properties(
    title='Motivação',
    height=450 
).interactive()



#Expectativa
contagem_expec = count_espera.sort_values(by='Contagem', ascending=False) # ordenação
chart_expec= alt.Chart(contagem_expec).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Contagem', title=None),
    y=alt.Y('Palavra', sort='-x', axis=alt.Axis(labelLimit=150, title=None))
).properties(
    title='Expectativa',
    height=450 
).interactive()


#Dificuldades_MktMed
contagem_dif = count_difmkt.sort_values(by='Contagem', ascending=False) # ordenação
chart_dif= alt.Chart(contagem_dif).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Contagem', title=None),
    y=alt.Y('Palavra', sort='-x', axis=alt.Axis(labelLimit=150, title=None))
).properties(
    title='Dificuldades em Mkt Médico',
    height=450 
).interactive()



#Duvida
contagem_duv = count_duvida.sort_values(by='Contagem', ascending=False) # ordenação
chart_duv= alt.Chart(contagem_duv).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Contagem', title=None),
    y=alt.Y('Palavra', sort='-x', axis=alt.Axis(labelLimit=150, title=None))
).properties(
    title='Alguma Dúvida?',
    height=450 
).interactive()



#Dificuldades_MktMed
contagem_satis = count_satis.sort_values(by='Contagem', ascending=False) # ordenação
chart_satis= alt.Chart(contagem_satis).mark_bar(color= '#01B8AA').encode(
    x=alt.X('Contagem', title=None),
    y=alt.Y('Palavra', sort='-x', axis=alt.Axis(labelLimit=150, title=None))
).properties(
    title='Satisfação com o MED10K',
    height=450 
).interactive()



col1, col2, col3 = st.columns(3)
col1.altair_chart(chart_sonho, use_container_width=True)
col2.altair_chart(chart_motivo, use_container_width=True)
col3.altair_chart(chart_expec, use_container_width=True)


col1, col2, col3 = st.columns(3)
col1.altair_chart(chart_dif, use_container_width=True)
col2.altair_chart(chart_duv, use_container_width=True)
col3.altair_chart(chart_satis, use_container_width=True)



#-----Tabela-------
st.write('### 📖 Tabela Detalhada')
df_resp_filtered6







