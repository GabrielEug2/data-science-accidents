
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns


# In[2]:


df = pd.read_csv('acidentes2018.csv', sep=';', encoding='latin-1')


# In[3]:


print(df.columns)
df.describe()


# In[4]:


# Descartando informações específicas dos envolvidos, porque a principio não vamos usar

grouped_by_accident = df.groupby('id')

# Se o acidente é o mesmo, essas informações vão ser iguais pra todas as linhas daquele acidente
accident_data = grouped_by_accident[
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


# In[5]:


accident_data.describe()


# In[6]:

# sns.pairplot(accident_data)

# In[7]:

# Número de acidentes por dia da semana
pd.value_counts(accident_data['dia_semana']).plot('bar')

# In[8]:

# Número de acidentes por tipo de acidente
pd.value_counts(accident_data['tipo_acidente']).plot('bar')

# In[9]:

# Número de acidentes por fase do dia
pd.value_counts(accident_data['fase_dia']).plot('bar')

# In[10]:

# Número de acidentes por causa
pd.value_counts(accident_data['causa_acidente']).plot('bar')

# In[11]:

# Série temporal
sns.lineplot(hue="event", data=accident_data.groupby('data_inversa').size())

# In[12]:

# Acidentes por estado
pd.value_counts(accident_data['uf']).plot('bar')

# In[13]:

# Acidentes por BR
pd.value_counts(accident_data['br']).plot('bar')

# In[13]:

# Acidentes por clima
pd.value_counts(accident_data['condicao_metereologica']).plot('bar')

# In[14]:

# Acidentes por tipo de veiculo
pd.value_counts(accident_data['tipo_veiculo']).plot('bar')

# In[15]:
# mortos por ano do veículo (carros mais novos são mais seguros, será?)

# absoluto
sns.lineplot(hue="event", data=accident_data.groupby('ano_fabricacao_veiculo').agg('sum')['n_mortos'])

# média
sns.lineplot(hue="event", data=accident_data.groupby('ano_fabricacao_veiculo').agg('mean')['n_mortos'])
