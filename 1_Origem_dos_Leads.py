import streamlit as st
import pandas as pd
#import time
import altair as alt

#st.session_state["df_respondentes"]
st.set_page_config(
    layout='wide',
    page_icon='Origem dos Leads'
)


@st.cache_data
def load_data():
    #url = 'https://docs.google.com/spreadsheets/d/15G1fceEst8fr2ORPzUGFtPpfOh9uwMIL1wcf36BAu4Q/edit?gid=0#gid=0'
    #conn = st.connection('gsheets', type=GSheetsConnection)
    #df_leads = conn.read(spreadsheet=url)
    df_leads = pd.read_excel('LEADS SVMM - GERAL.xlsx',sheet_name='Inscritos')
    #time.sleep(3)
    return df_leads

df_leads = load_data()
#st.session_state["df_leads"] = df_leads
columns_list = list(df_leads.columns.values.tolist())

#--------- Logo & Titulo --------
st.image('logo1-1.png', width=220)
#st.image('logo2-2.png', width=150)
st.markdown('## ⛲ Origem dos Leads')

#---------------SIDEBAR--------------
st.sidebar.markdown('## Filtros')

#---------------FILTROS--------
#matriculado
matriculados = df_leads['Matriculado?'].value_counts().index.tolist()
matriculados.insert(0, 'Todos') #add 'Select All' option to the top 
selected_matriculado = st.sidebar.multiselect('Lead Matriculado?',matriculados, default='Todos')

if 'Todos' in selected_matriculado :
	df_resp_filtered1 = df_leads
else:
    df_resp_filtered1 = df_leads[df_leads['Matriculado?'].isin(selected_matriculado)]

#renda
rendas = df_resp_filtered1['Renda_Lead'].value_counts().index.tolist()
rendas.insert(0, 'Todas') #add 'Select All' option to the top 
selected_renda = st.sidebar.multiselect('Renda do Lead',rendas, default='Todas')

if 'Todas' in selected_renda :
	df_resp_filtered2 = df_resp_filtered1
else:
    df_resp_filtered2 = df_resp_filtered1[df_resp_filtered1['Renda_Lead'].isin(selected_renda)]

#idade
idades = df_resp_filtered2['Idade_Lead'].value_counts().index.tolist()
idades.insert(0, 'Todas') #add 'Select All' option to the top 
selected_idade = st.sidebar.multiselect('Idade do Lead',idades, default='Todas')

if 'Todas' in selected_idade :
	df_resp_filtered3 = df_resp_filtered2
else:
    df_resp_filtered3 = df_resp_filtered2[df_resp_filtered2['Idade_Lead'].isin(selected_idade)]

#utm_source
utm_sources = df_resp_filtered3['utm_source'].value_counts().index.tolist()
utm_sources.insert(0, 'Todas') #add 'Select All' option to the top 
selected_utm_source = st.sidebar.multiselect('App Fonte do Lead',utm_sources, default='Todas')

if 'Todas' in selected_utm_source :
	df_resp_filtered4 = df_resp_filtered3
else:
    df_resp_filtered4 = df_resp_filtered3[df_resp_filtered3['utm_source'].isin(selected_utm_source)]

#utm_medium
utm_mediuns = df_resp_filtered4['utm_medium'].value_counts().index.tolist()
utm_mediuns.insert(0, 'Todas') #add 'Select All' option to the top 
selected_utm_medium = st.sidebar.multiselect('Fonte Intermediária do Lead',utm_mediuns, default='Todas')

if 'Todas' in selected_utm_medium :
	df_resp_filtered5 = df_resp_filtered4
else:
    df_resp_filtered5 = df_resp_filtered4[df_resp_filtered4['utm_source'].isin(selected_utm_medium)]

#utm_campanha
utm_camps = df_resp_filtered5['utm_campaign'].value_counts().index.tolist()
utm_camps.insert(0, 'Todas') #add 'Select All' option to the top 
selected_utm_camp = st.sidebar.multiselect('Campanha',utm_camps, default='Todas')

if 'Todas' in selected_utm_camp :
	df_resp_filtered6 = df_resp_filtered5
else:
    df_resp_filtered6 = df_resp_filtered5[df_resp_filtered5['utm_campaign'].isin(selected_utm_camp)]

#utm_term
utm_terms = df_resp_filtered6['utm_term'].value_counts().index.tolist()
utm_terms.insert(0, 'Todas') #add 'Select All' option to the top 
selected_utm_terms = st.sidebar.multiselect('Termômetro',utm_terms, default='Todas')

if 'Todas' in selected_utm_terms :
	df_resp_filtered7 = df_resp_filtered6
else:
    df_resp_filtered7 = df_resp_filtered6[df_resp_filtered6['utm_term'].isin(selected_utm_terms)]


#utm_conteudo
utm_cont = df_resp_filtered7['utm_content'].value_counts().index.tolist()
utm_cont.insert(0, 'Todas') #add 'Select All' option to the top 
selected_utm_cont = st.sidebar.multiselect('Conteúdo',utm_cont, default='Todas')

if 'Todas' in selected_utm_cont :
	df_resp_filtered8 = df_resp_filtered7
else:
    df_resp_filtered8 = df_resp_filtered7[df_resp_filtered7['utm_content'].isin(selected_utm_cont)]

#----------Presentation-----
st.sidebar.markdown('Desenvolvido por **Lacaz Data Services**🎲')
st.sidebar.markdown('Dashboard desenvolvido para [Natlhalia Carvalho e Jaque França](https://nathaliamarketingmedico.com/formacao-med10k/?utm_source=Instagram&utm_medium=Bio&utm_id=SVMM+-+LC1)')


#-----------Gráficos-------------------

# Renda
contagem_renda = df_resp_filtered8['Renda_Lead'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_renda.columns = ['Renda Lead', 'Contagem']
contagem_renda = contagem_renda.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_renda = alt.Chart(contagem_renda).mark_bar().encode(
    x=alt.X('Renda Lead:N', sort='-y'),
    y='Contagem:Q'
).properties(
    title='Renda do Lead'
)

# Idade
contagem_idade = df_resp_filtered8['Idade_Lead'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_idade.columns = ['Idade Lead', 'Contagem']
contagem_idade = contagem_idade.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_idade = alt.Chart(contagem_idade).mark_bar().encode(
    x=alt.X('Idade Lead:N', sort='-y'),
    y='Contagem:Q'
).properties(
    title='Idade do Lead'
)

# Genero
contagem_genero = df_resp_filtered8['Genero_Lead'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_genero.columns = ['Genero Lead', 'Contagem']
contagem_genero = contagem_genero.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_genero = alt.Chart(contagem_genero).mark_bar().encode(
    x=alt.X('Genero Lead:N', sort='-y'),
    y='Contagem:Q'
).properties(
    title='Gênero do Lead'
)


#Fonte do Lead
contagem_utm_source = df_resp_filtered8['utm_source'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_utm_source.columns = ['Fonte do Lead', 'Contagem']
contagem_utm_source = contagem_utm_source.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_utm_source = alt.Chart(contagem_utm_source).mark_bar().encode(
    x=alt.X('Fonte do Lead:N', sort='-y'),
    y='Contagem:Q'
).properties(
    title='Fonte do Lead'
)

#Fonte Intermediaria Lead
contagem_utm_medium = df_resp_filtered8['utm_medium'].value_counts().reset_index() #contagem da coluna de interesse y
contagem_utm_medium.columns = ['Fonte do Lead', 'Contagem']
contagem_utm_medium = contagem_utm_medium.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_utm_medium = alt.Chart(contagem_utm_medium).mark_bar().encode(
    x=alt.X('Fonte do Lead:N', sort='-y'),
    y='Contagem:Q'
).properties(
    title='Fonte Intermediária do Lead'
)


#Campanha
contagem_utm_campaign = df_resp_filtered8['utm_campaign'].value_counts()[:10].reset_index() #contagem da coluna de interesse y
contagem_utm_campaign.columns = ['Campanha', 'Contagem']
contagem_utm_campaign = contagem_utm_campaign.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_utm_campaign = alt.Chart(contagem_utm_campaign).mark_bar().encode(
    x=alt.X('Campanha:N', sort='-y'),
    y='Contagem:Q'
).properties(
    title='Campanha'
)

#Termometro
contagem_utm_term = df_resp_filtered8['utm_term'].value_counts()[:10].reset_index() #contagem da coluna de interesse y
contagem_utm_term.columns = ['Termometro', 'Contagem']
contagem_utm_term = contagem_utm_term.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_utm_term = alt.Chart(contagem_utm_term).mark_bar().encode(
    x=alt.X('Termometro:N', sort='-y'),
    y='Contagem:Q'
).properties(
    title='Termometro'
)

#Conteudo
contagem_utm_content = df_resp_filtered8['utm_content'].value_counts()[:10].reset_index() #contagem da coluna de interesse y
contagem_utm_content.columns = ['Conteudo', 'Contagem']
contagem_utm_content = contagem_utm_content.sort_values(by='Contagem', ascending=False) # ordenação
# Criando o gráfico com Altair
chart_utm_content= alt.Chart(contagem_utm_content).mark_bar().encode(
    x=alt.X('Conteudo', sort='-y'),
    y='Contagem'
).properties(
    title='Conteúdo'
)

# Exibindo o gráfico no Streamlit
col1, col2, col3 = st.columns([0.4, 0.4, 0.2])
col1.altair_chart(chart_renda, use_container_width=True)
col2.altair_chart(chart_idade, use_container_width=True)
col3.altair_chart(chart_genero, use_container_width=True)


# Exibindo o gráfico no Streamlit
col1, col2 = st.columns(2)
col1.altair_chart(chart_utm_source, use_container_width=True)
col2.altair_chart(chart_utm_medium, use_container_width=True)


st.altair_chart(chart_utm_campaign, use_container_width=True)
st.altair_chart(chart_utm_term, use_container_width=True)
st.altair_chart(chart_utm_content, use_container_width=True)

#horizontal=True, color='#01B8AA'


#----------Tabela---------
st.write('### 📖 Tabela Detalhada')
st.dataframe(df_resp_filtered3)