import streamlit as st
import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
#from sklearn.preprocessing import StandardScaler
#from sklearn.preprocessing import Normalizer
from sklearn.linear_model import LogisticRegression
#from sklearn.linear_model import LinearRegression
import altair as alt

#st.session_state["df_respondentes"]
st.set_page_config(
    layout='wide',
    page_icon='Estatistica dos Matriculados'
)


@st.cache_data
def load_data(file, page):
    #url = 'https://docs.google.com/spreadsheets/d/1jU6I6H2pYhJajJVZqFreYudtIyepPMTbW1MGiUh4edg/edit?gid=1606288776#gid=1606288776'
    #conn = st.connection('gsheets', type=GSheetsConnection)
    #df = conn.read(spreadsheet=url)
    df = pd.read_excel(file, sheet_name=page)
    time.sleep(3)
    return df

#--------- Logo & Titulo --------
st.image('logo1-1.png', width=220)
#st.image('logo2-2.png', width=150)

#---------------SIDEBAR--------------
#st.sidebar.markdown('## Filtros')
#----------Presentation-----
st.sidebar.markdown('Desenvolvido por **Lacaz Data Services**🎲')
st.sidebar.markdown('Dashboard desenvolvido para [Natlhalia Carvalho e Jaque França](https://nathaliamarketingmedico.com/formacao-med10k/?utm_source=Instagram&utm_medium=Bio&utm_id=SVMM+-+LC1)')

#---- Preparacao DataFrame

#url_nao_matriculados = 'https://docs.google.com/spreadsheets/d/15G1fceEst8fr2ORPzUGFtPpfOh9uwMIL1wcf36BAu4Q/edit?gid=1783509356#gid=1783509356'

df_nao_matriculados = load_data('LEADS SVMM - GERAL.xlsx','Pesquisa')
df_nao_matriculados = df_nao_matriculados[df_nao_matriculados["Matricula?"] == "F"]

columns_list_nao_matriculados = list(df_nao_matriculados.columns.values.tolist())

columns_list_nao_matriculados[0] = 'Data'
columns_list_nao_matriculados[1] = 'Email' #
columns_list_nao_matriculados[2] = 'Nome'
columns_list_nao_matriculados[5] = 'Idade' #
columns_list_nao_matriculados[6] = 'Regiao' #
columns_list_nao_matriculados[7] = 'Genero' #
columns_list_nao_matriculados[8] = 'Civil' #
columns_list_nao_matriculados[9] = 'Filhos' #
columns_list_nao_matriculados[10] = 'Escolaridade' #
columns_list_nao_matriculados[11] = 'Renda' #
columns_list_nao_matriculados[12] = 'Profissao' #
columns_list_nao_matriculados[13] = 'Seguidor' #
columns_list_nao_matriculados[14] = 'Motivo'
columns_list_nao_matriculados[15] = 'Impedimento'
columns_list_nao_matriculados[16] = 'Dificuldades'
columns_list_nao_matriculados[17] = 'Problemas'
columns_list_nao_matriculados[19] = 'LiberdadeFinanceira'
columns_list_nao_matriculados[20] = 'Sonho'
columns_list_nao_matriculados[21] = 'Trab_mkt_med'
columns_list_nao_matriculados[22] = 'Clientes_med'
columns_list_nao_matriculados[23] = 'EsperaMed10k'
columns_list_nao_matriculados[24] = 'MediaTicketHj'
columns_list_nao_matriculados[29] = 'email_fixed'

df_nao_matriculados.columns = columns_list_nao_matriculados


df_nao_matriculados['Matricula'] = "Não"


df_nao_matriculados_final = df_nao_matriculados[['Email','Idade','Regiao','Genero','Civil','Filhos','Escolaridade','Renda','Profissao','Seguidor','Matricula']]

#url_matriculados = 'https://docs.google.com/spreadsheets/d/1jU6I6H2pYhJajJVZqFreYudtIyepPMTbW1MGiUh4edg/edit?gid=1606288776#gid=1606288776'

df_matriculados = load_data('Matriculados.xlsx', 'M2')



columns_list_matriculados = list(df_matriculados.columns.values.tolist())

columns_list_matriculados[0] = 'Data'
columns_list_matriculados[1] = 'Email' #
columns_list_matriculados[2] = 'Nome'
columns_list_matriculados[5] = 'Idade' #
columns_list_matriculados[6] = 'Regiao' #
columns_list_matriculados[7] = 'Genero'  #
columns_list_matriculados[8] = 'Civil' #
columns_list_matriculados[9] = 'Filhos' #
columns_list_matriculados[10] = 'Escolaridade' ##
columns_list_matriculados[11] = 'Renda' ##
columns_list_matriculados[12] = 'Profissao' ##
columns_list_matriculados[13] = 'Seguidor' #
columns_list_matriculados[14] = 'Med10KKnowhow'
columns_list_matriculados[15] = 'ComoConheceu' 
columns_list_matriculados[16] = 'Trab_mkt_med' 
columns_list_matriculados[17] = 'Trab_mkt_med_tempo' 
columns_list_matriculados[18] = 'Clientes_med' 
columns_list_matriculados[19] = 'Clientes_med_qnt'  
columns_list_matriculados[20] = 'ServicosOferecidos'
columns_list_matriculados[21] = 'Ferramentas'
columns_list_matriculados[22] = 'Dificuldades_MktMed'  
columns_list_matriculados[23] = 'Dificuldades_Carreira' 
columns_list_matriculados[24] = 'SatisfacaoMed10k' 
columns_list_matriculados[25] = 'topicos_Med10k' 
columns_list_matriculados[26] = 'Motivo' 
columns_list_matriculados[27] = 'ObjetivoFaturamento'
columns_list_matriculados[28] = 'Horas_dedicacao'
columns_list_matriculados[29] = 'Trab_digital'
columns_list_matriculados[30] = 'Jornada_trab'
columns_list_matriculados[31] = 'Agencia'   
columns_list_matriculados[32] = 'dia_a_dia'
columns_list_matriculados[33] = 'conteudos_assistidos' 
columns_list_matriculados[34] = 'espera_aprender_Med10k' 
columns_list_matriculados[35] = 'Sonho' 
columns_list_matriculados[36] = 'Rede_social'
columns_list_matriculados[37] = 'Duvida' 
columns_list_matriculados[38] = 'Del1'
columns_list_matriculados[39] = 'Del2'
columns_list_matriculados[40] = 'Situacao'
columns_list_matriculados[41] = 'Acesso_comunidade'
columns_list_matriculados[42] = 'Acesso_plataforma'
columns_list_matriculados[43] = 'Consultoria' 
columns_list_matriculados[44] = 'Ja_fez_consultoria'

df_matriculados.columns = columns_list_matriculados

df_matriculados['Matricula'] = "Sim"

df_matriculados_final = df_matriculados[['Email','Idade','Regiao','Genero','Civil','Filhos','Escolaridade','Renda','Profissao','Seguidor','Matricula']]

union_all_df = pd.concat([df_nao_matriculados_final, df_matriculados_final], ignore_index=True)

#---------------FILTROS--------

#-----------Gráficos-------------------
#Grafico de colunas com Matricula como %


cross_tab_prop_renda = pd.crosstab(index=union_all_df['Renda'],
                             columns=union_all_df['Matricula'],
                             normalize="index"
                             )


cross_tab_prop_escolaridade = pd.crosstab(index=union_all_df['Escolaridade'],
                             columns=union_all_df['Matricula'],
                             normalize="index"
                             )


cross_tab_prop_profissao = pd.crosstab(index=union_all_df['Profissao'],
                             columns=union_all_df['Matricula'],
                             normalize="index"
                             )


cross_tab_prop_seguidor = pd.crosstab(index=union_all_df['Seguidor'],
                             columns=union_all_df['Matricula'],
                             normalize="index"
                             )


cross_tab_prop_idade = pd.crosstab(index=union_all_df['Idade'],
                             columns=union_all_df['Matricula'],
                             normalize="index"
                             )


cross_tab_prop_regiao = pd.crosstab(index=union_all_df['Regiao'],
                             columns=union_all_df['Matricula'],
                             normalize="index"
                             )

cross_tab_prop_genero = pd.crosstab(index=union_all_df['Genero'],
                             columns=union_all_df['Matricula'],
                             normalize="index"
                             )


cross_tab_prop_civil = pd.crosstab(index=union_all_df['Civil'],
                             columns=union_all_df['Matricula'],
                             normalize="index"
                             )


cross_tab_prop_filhos = pd.crosstab(index=union_all_df['Filhos'],
                             columns=union_all_df['Matricula'],
                             normalize="index"
                             )


col1, col2, col3 = st.columns(3)
col1.subheader("Renda")
col1.bar_chart(cross_tab_prop_renda, stack='normalize', horizontal=False)
col2.subheader("Escolaridade")
col2.bar_chart(cross_tab_prop_escolaridade, stack='normalize', horizontal=False)
col3.subheader("Profissao")
col3.bar_chart(cross_tab_prop_profissao, stack='normalize', horizontal=False)

col1, col2, col3 = st.columns(3)
col1.subheader("Seguidor")
col1.bar_chart(cross_tab_prop_seguidor, stack='normalize', horizontal=False)
col2.subheader("Idade")
col2.bar_chart(cross_tab_prop_idade, stack='normalize', horizontal=False)
col3.subheader("Região")
col3.bar_chart(cross_tab_prop_regiao, stack='normalize', horizontal=False)

col1, col2, col3 = st.columns(3)
col1.subheader("Gênero")
col1.bar_chart(cross_tab_prop_genero, stack='normalize', horizontal=False)
col2.subheader("Civil")
col2.bar_chart(cross_tab_prop_civil, stack='normalize', horizontal=False)
col3.subheader("Filhos")
col3.bar_chart(cross_tab_prop_filhos, stack='normalize', horizontal=False)





#Modelo Machine Learning para o cálculo do Coef Regressao
# trazer função do coef de regressao

#tirar coluna de valores únicos
df_reg = union_all_df.drop(['Email'], axis=1)

#tratamento das colunas categóricas 
dummies_list = ['Idade', 'Regiao','Genero','Civil','Filhos','Escolaridade', 'Renda','Profissao','Seguidor']

df_reg = pd.get_dummies(df_reg, columns = dummies_list)

#alvo para binario
df_reg['Matricula'] = df_reg['Matricula'].replace('Não', 0)
df_reg['Matricula'] = df_reg['Matricula'].replace('Sim', 1)

#separar o alvo
y = df_reg['Matricula']
del df_reg['Matricula']

#separar os dados em conjunto de teste e treino do modelo ML
x_treino, x_teste, y_treino, y_teste = train_test_split(df_reg, y, test_size=0.20)

#normalização dos dados
scaler = preprocessing.Normalizer().fit(x_treino)

x_treino_norm = scaler.transform(x_treino)
x_teste_norm = scaler.transform(x_teste)

#aplicando o algorítimo 
reg = LogisticRegression().fit(x_treino_norm, y_treino)
#reg = LinearRegression().fit(x_treino_norm, y_treino) 
reg.score(x_treino_norm, y_treino)




x_treino_df = pd.DataFrame(x_treino, columns = df_reg.columns.tolist())

importance_df = pd.DataFrame()
importance_df['colunas'] = x_treino_df.columns.tolist()
importance_df['importância'] = reg.coef_.tolist()[0]
importance_df.sort_values('importância',ascending=False).set_index('colunas')

importance_df


# Criando o gráfico com Altair
chart = alt.Chart(importance_df).mark_bar().encode(
    x=alt.X('colunas:N', sort='-y'),
    y='importância:Q'
).properties(
    title='Importância'
)

# Exibindo o gráfico no Streamlit
st.altair_chart(chart, use_container_width=True)

#st.bar_chart(importance_df, x='colunas', y='importância', horizontal=False)

st.write('''
         
#### **Para interpretar os coeficientes de uma regressão logística, podemos seguir as seguintes diretrizes gerais:**

**Coeficientes negativos** indicam uma associação negativa entre a variável explicativa e a probabilidade do alvo ser 1. Ou seja, conforme o valor dessa variável aumenta, a probabilidade do resultado ser 1 diminui.

**Coeficientes positivos** indicam uma associação positiva, ou seja, conforme o valor dessa variável aumenta, a probabilidade do alvo ser 1 também aumenta.

**Coeficientes próximos de zero (tanto negativos quanto positivos)** sugerem que essa variável não tem um grande impacto na previsão do modelo.

#### **Agora vamos analisar alguns casos:**

#### **Principais coeficientes negativos:**
**Profissao_Social Media (-1.993):** Indica uma forte associação negativa entre ser "Social Media" e a probabilidade do alvo ser 1. Ou seja, essa profissão reduz a chance de atingir o alvo 1.
         
**Seguidor_Comecei a te seguir agora (-1.442) e Seguidor_Não sigo (-1.081):** Seguir recentemente ou não seguir está associado a uma menor chance de alcançar o alvo 1.
         
**Renda_Até R$1.000,00 (-0.504):** Pessoas com uma renda mais baixa têm uma chance menor de atingir o alvo 1.

                 
#### **Principais coeficientes positivos:**
**Seguidor_Entre 1 a 3 meses (0.999) e Seguidor_Há menos de um mês (1.896):** Indicam uma forte associação positiva com o alvo, ou seja, pessoas que começaram a seguir há menos de três meses têm uma alta probabilidade de o alvo ser 1.
         
**Profissao_Profissional Liberal (1.924) e Profissao_Empresário(a) (1.939):** Ambas as profissões estão fortemente associadas a um aumento na probabilidade de atingir o alvo 1.
         
**Renda_De R$4.001 à R$5.000 (0.792):** Pessoas com essa faixa de renda têm maior chance de alcançar o alvo 1.

**Variáveis sem impacto (coeficiente zero):**
Há várias profissões com coeficiente zero, sugerindo que elas não influenciam o modelo (exemplo: Profissao_CLT, Profissao_Jornalista). Isso pode indicar que essas categorias não têm impacto relevante na previsão do alvo no seu modelo.

         
**Em resumo, as variáveis relacionadas à profissão, faixa de renda e tempo de seguimento parecem ser as mais impactantes no modelo.**''')