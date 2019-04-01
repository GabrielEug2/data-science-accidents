
# coding: utf-8

# Elabore um documento descrevendo sua análise exploratória usando elementos visuais adequados. O documento deve conter:
# 
# * Descrição das fontes de dados
# * Descrição das principais variáveis (features)
# * Análises inciais de distribuição e/ou correlação com gráficos adequados
# * Conclusões/ideias/hipóteses iniciais
# 
# Vamos escrevendo essas coisas em comentários no decorrer do código.
# No .py aparece só como comentários, mas quando a gente for passar pro Jupyter dá pra colocar em células de markdown, e gerar o PDF pra entregar
# 
# ==============================================

# # Relatório - Análise Exploratória
# 
# Gabriel Eugenio Brito, Renan de Souza Antunes, Aurélio Vinicius Cabral Funes

# ## Descrição das fontes de dados
# 
# Os dados utilizados são provenientes da Polícia Rodoviária Federal, e estão disponíveis em https://www.prf.gov.br/portal/dados-abertos/acidentes. Eles consistem em uma série de arquivos csv com informações referentes a acidentes ocorridos do ano de 2007 em diante. Optamos por usar apenas os dados de 2018, mas se for  necessário podemos utilizar dados de outros anos para fazer um comparativo.

# In[1]:


import pandas as pd
# usa sns pro seaborn, é o padrão
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


df = pd.read_csv('acidentes2018.csv', sep=';', encoding='latin-1')


# A princípio pensamos que cada linha do csv tivesse informações relativas a um acidente, mas após olhar com mais cuidado percebemos que existem várias linhas com o mesmo id. Na verdade cada linha representa um envolvido em um acidente.

# In[3]:


# Raw data
pd.set_option('display.max_columns', None) # None = mostra todas

print(df.columns)
df.head()


# In[4]:


# Descarta informações específicas dos envolvidos, porque a principio não vamos usar

grouped_by_accident = df.groupby('id')

grouped_by_vehicle = df.groupby('id_veiculo')

# Se o acidente é o mesmo, essas informações vão ser iguais pra todas as linhas daquele acidente
accident_data = grouped_by_accident[
    'data_inversa', 'dia_semana', 'horario', 'uf', 'br', 'km', 'municipio',
    'causa_acidente', 'tipo_acidente', 'classificacao_acidente', 'fase_dia',
    'sentido_via', 'condicao_metereologica', 'tipo_pista', 'tracado_via',
    'uso_solo', 'ilesos', 'feridos_leves', 'feridos_graves', 'mortos',
    'latitude', 'longitude', 'regional', 'delegacia', 'uop'
].first()

# Se o acidente é o mesmo, essas informações vão ser iguais pra todas as linhas daquele acidente
accident_data_by_vehicle = grouped_by_vehicle[
    'data_inversa', 'dia_semana', 'horario', 'uf', 'br', 'km', 'municipio', 'causa_acidente',
    'tipo_acidente', 'classificacao_acidente', 'fase_dia', 'sentido_via',
    'condicao_metereologica', 'tipo_pista', 'tracado_via', 'uso_solo', 'tipo_veiculo',
    'ano_fabricacao_veiculo', 'latitude', 'longitude', 'regional', 'delegacia', 'uop'
].first()

# Calcula a quantidade de feridos, mortos, etc no acidente
accident_data['n_ilesos'] = grouped_by_accident['ilesos'].sum()
accident_data['n_feridos_leves'] = grouped_by_accident['feridos_leves'].sum()
accident_data['n_feridos_graves'] = grouped_by_accident['feridos_graves'].sum()
accident_data['n_mortos'] = grouped_by_accident['mortos'].sum()
accident_data['n_envolvidos'] = accident_data['n_ilesos'] + accident_data['n_feridos_leves'] + accident_data['n_feridos_graves'] + accident_data['n_mortos']

accident_data.head()

accident_data_by_vehicle['n_ilesos'] = grouped_by_vehicle['ilesos'].sum()
accident_data_by_vehicle['n_feridos_leves'] = grouped_by_vehicle['feridos_leves'].sum()
accident_data_by_vehicle['n_feridos_graves'] = grouped_by_vehicle['feridos_graves'].sum()
accident_data_by_vehicle['n_mortos'] = grouped_by_vehicle['mortos'].sum()
accident_data_by_vehicle['n_envolvidos'] = accident_data_by_vehicle['n_ilesos'] + accident_data_by_vehicle['n_feridos_leves'] + accident_data_by_vehicle['n_feridos_graves'] + accident_data_by_vehicle['n_mortos']


# In[5]:


# Algumas estatísticas
accident_data.describe()


# In[6]:


# Número de acidentes por tipo de acidente
plt.figure(figsize=(8,4))
sns.countplot(y="tipo_acidente", data=accident_data, order=accident_data['tipo_acidente'].value_counts(ascending=True).index)


# In[7]:


# Número de acidentes por causa
plt.figure(figsize=(8,6))
sns.countplot(y="causa_acidente", data=accident_data, order=accident_data['causa_acidente'].value_counts(ascending=True).index)


# In[8]:


# Número de acidentes por dia da semana
plt.figure(figsize=(8,4))
sns.countplot(x="dia_semana", data=accident_data)


# In[9]:


# Número de acidentes por fase do dia
plt.figure(figsize=(8,4))
sns.countplot(x="fase_dia", data=accident_data, order=['Amanhecer', 'Pleno dia', 'Anoitecer', 'Plena Noite'])


# In[10]:


# Número de acidentes por hora
tmp = pd.DataFrame()
tmp['hora'] = pd.to_datetime(accident_data['horario']).dt.hour

plt.figure(figsize=(8, 4))
sns.countplot(x='hora', data=tmp)


# In[11]:


# Número de acidentes no decorrer do ano (série temporal)

# Já é pra estar ordenado no dataset, mas só pra garantir
accident_data['data_inversa'] = pd.to_datetime(accident_data['data_inversa'])
accident_data.sort_values(by='data_inversa')

plt.figure(figsize=(12, 4))
time_series = sns.lineplot(data=accident_data.groupby('data_inversa').size())


# In[12]:


# Acidentes por estado
plt.figure(figsize=(8,8))
sns.countplot(y="uf", data=accident_data, order=accident_data['uf'].value_counts(ascending=True).index)


# In[13]:


# Acidentes por BR
plt.figure(figsize=(8,25))
sns.countplot(y="br", data=accident_data, order=accident_data['br'].value_counts(ascending=True).index)


# In[14]:


# Acidentes por clima
plt.figure(figsize=(12,6))
sns.countplot(x="condicao_metereologica", data=accident_data, order=accident_data['condicao_metereologica'].value_counts(ascending=True).index)


# In[15]:


# As informações dos veículos não dá pra fazer como a gente tava fazendo até agora
# porque alguns acidentes envolvem mais de um veículo. Se pegar só o primeiro,
# nós estamos descartando vários deles.
# Temos que repensar essas estatísticas

# id_veiculo é justamente pra isso

# Acidentes por tipo de veiculo
plt.figure(figsize=(12,8))
sns.countplot(y="tipo_veiculo", data=accident_data_by_vehicle, order=accident_data_by_vehicle['tipo_veiculo'].value_counts().index)


# In[16]:

# (carros mais novos são mais seguros, será?) tem muito pouco dado pra responder isso...

# mortos x ilesos x feridos graves x feridos leves por ano do veículo
plt.figure(figsize=(12,8))
sns.lineplot(data=accident_data_by_vehicle[['ano_fabricacao_veiculo', 'n_mortos', 'n_ilesos', 'n_feridos_graves', 'n_feridos_leves']].groupby('ano_fabricacao_veiculo').agg('sum'))
