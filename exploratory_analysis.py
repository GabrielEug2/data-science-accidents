
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sb


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
    'data_inversa', 'uf', 'br', 'km', 'municipio', 'causa_acidente',
    'tipo_acidente', 'classificacao_acidente', 'fase_dia', 'sentido_via',
    'condicao_metereologica', 'tipo_pista', 'tracado_via', 'uso_solo',
    'latitude', 'longitude', 'regional', 'delegacia', 'uop'
].first()

# Calcula a quantidade de feridos, mortos, etc no acidente
accident_data['n_ilesos'] = grouped_by_accident['ilesos'].sum()
accident_data['n_feridos_leves'] = grouped_by_accident['feridos_leves'].sum()
accident_data['n_feridos_graves'] = grouped_by_accident['feridos_graves'].sum()
accident_data['n_mortos'] = grouped_by_accident['mortos'].sum()

accident_data['n_envolvidos'] = accident_data['n_ilesos'] + accident_data['n_feridos_leves'] +                                 accident_data['n_feridos_graves'] + accident_data['n_mortos']

accident_data.head()


# In[5]:


accident_data.describe()


# In[6]:


# Algumas coisas para plotar

# Número de acidentes por dia da semana
# Número de acidentes por tipo de acidente
# Número de acidentes por fase do dia
# Número de acidentes por causa

sb.pairplot(accident_data)

