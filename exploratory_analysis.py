
# coding: utf-8

# ## Descrição das fontes de dados
# 
# Os dados utilizados são provenientes da Polícia Rodoviária Federal, e estão  disponíveis
# em https://www.prf.gov.br/portal/dados-abertos/acidentes. Eles consistem em uma série de
# arquivos csv com informações referentes a acidentes ocorridos do ano de 2007 em diante.
#
# Optamos por usar apenas os dados de 2018, mas se for necessário podemos utilizar dados
# de outros anos para fazer um comparativo.

# In[1]:

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# In[2]:

df = pd.read_csv('acidentes2018.csv', sep=';', encoding='latin-1')

# A princípio pensamos que cada linha do csv tivesse informações relativas a um
# acidente, mas após olhar com mais cuidado percebemos que existem várias linhas
# com o mesmo id. Também temos colunas como "idade", "sexo" e "estado_fisico",
# que não fazem sentido quando estamos falando de um acidente.
# 
# Acontece que cada linha representa __uma pessoa envolvida__ em um acidente.
# Então se um acidente envolveu, digamos, 5 pessoas, haverão 5 linhas referentes
# a este acidente no csv. Podemos ver que há uma certa redundância nos dados,
# pois algumas das informações como o horário e o local do acidente são as
# mesmas para todos os envolvidos.

# In[3]:

# Raw data
pd.set_option('display.max_columns', None) # None = mostra todas

print(df.columns)
df.head()

# As features incluem, entre outras informações:
# 
# * __Causa do acidente__: "Defeito Mecânico no Veículo", "Falta de Atenção à Condução", etc
# * __Tipo do acidente__: "Capotamento", "Colisão traseira", etc
# * __Local onde aconteceu__: município, BR e até mesmo a latitude e longitude de onde aconteceu.
# * __Condição meteorológica__: como estava o clima no momento do acidente.
# * __Estado físico dos envolvidos__: "ilesos", "feridos leves", "feridos graves" ou "mortos".
# * __Tipo do veículo__: automóvel, motocicleta, etc
# 
# Optamos por descartar os dados específicos dos envolvidos, e manter apenas as
# informações relativas ao acidente e aos veículos.

# In[4]:

df.dropna(inplace=True)

# Agrupa os dados por acidente
grouped_by_accident = df.groupby('id')

# Se o acidente é o mesmo, essas informações vão ser iguais pra todas as linhas daquele acidente
accident_data = grouped_by_accident[
    'data_inversa', 'dia_semana', 'horario', 'uf', 'br', 'km', 'municipio',
    'causa_acidente', 'tipo_acidente', 'classificacao_acidente', 'fase_dia',
    'sentido_via', 'condicao_metereologica', 'tipo_pista', 'tracado_via',
    'uso_solo', 'latitude', 'longitude', 'regional'
].first()

# Calcula a quantidade de feridos, mortos, etc em cada acidente
accident_data['n_ilesos'] = grouped_by_accident['ilesos'].sum()
accident_data['n_feridos_leves'] = grouped_by_accident['feridos_leves'].sum()
accident_data['n_feridos_graves'] = grouped_by_accident['feridos_graves'].sum()
accident_data['n_mortos'] = grouped_by_accident['mortos'].sum()
accident_data['n_envolvidos'] = accident_data['n_ilesos'] + accident_data['n_feridos_leves'] + accident_data['n_feridos_graves'] + accident_data['n_mortos']

accident_data.head()

# In[5]:

# Agrupa os dados por veículo
grouped_by_vehicle = df.groupby('id_veiculo')

vehicle_data = grouped_by_vehicle[
    'tipo_veiculo', 'ano_fabricacao_veiculo', 'causa_acidente'
].first()

# Calcula a quantidade de feridos, mortos, etc em cada veículo
vehicle_data['n_ilesos'] = grouped_by_vehicle['ilesos'].sum()
vehicle_data['n_feridos_leves'] = grouped_by_vehicle['feridos_leves'].sum()
vehicle_data['n_feridos_graves'] = grouped_by_vehicle['feridos_graves'].sum()
vehicle_data['n_mortos'] = grouped_by_vehicle['mortos'].sum()
vehicle_data['n_envolvidos'] = vehicle_data['n_ilesos'] + vehicle_data['n_feridos_leves'] + vehicle_data['n_feridos_graves'] + vehicle_data['n_mortos']

vehicle_data.head()

# In[6]:

# Algumas estatísticas
accident_data.describe()

# In[7]:

# Número de acidentes por tipo
plt.figure(figsize=(8,4))
sns.countplot(y="tipo_acidente", data=accident_data, order=accident_data['tipo_acidente'].value_counts(ascending=True).index)

# In[8]:

# Número de acidentes por causa
plt.figure(figsize=(8,6))
sns.countplot(y="causa_acidente", data=accident_data, order=accident_data['causa_acidente'].value_counts(ascending=True).index)

# In[9]:

# Número de acidentes por estado
plt.figure(figsize=(8,8))
sns.countplot(y="uf", data=accident_data, order=accident_data['uf'].value_counts(ascending=True).index)

# In[10]:

# Número de acidentes por BR
plt.figure(figsize=(8,25))
sns.countplot(y="br", data=accident_data, order=accident_data['br'].value_counts(ascending=True).index)

# In[11]:

# Número de acidentes por dia da semana
plt.figure(figsize=(8,4))
sns.countplot(x="dia_semana", data=accident_data)

# In[12]:

# Número de acidentes por fase do dia
plt.figure(figsize=(8,4))
sns.countplot(x="fase_dia", data=accident_data, order=['Amanhecer', 'Pleno dia', 'Anoitecer', 'Plena Noite'])

# In[13]:

# Número de acidentes por hora
tmp = pd.DataFrame()
tmp['hora'] = pd.to_datetime(accident_data['horario']).dt.hour

plt.figure(figsize=(8, 4))
sns.countplot(x='hora', data=tmp)

# In[14]:

# Número de acidentes no decorrer do ano (série temporal)

# Já é pra estar ordenado no dataset, mas só pra garantir
accident_data['data_inversa'] = pd.to_datetime(accident_data['data_inversa'])
accident_data.sort_values(by='data_inversa')

plt.figure(figsize=(12, 4))
sns.lineplot(data=accident_data.groupby('data_inversa').size())

# In[15]:

# Número de acidentes por clima
plt.figure(figsize=(12,6))
sns.countplot(x="condicao_metereologica", data=accident_data, order=accident_data['condicao_metereologica'].value_counts(ascending=True).index)

# Não é nenhuma surpresa que automóveis estão envolvidos na maior parte dos acidentes.

# In[16]:

# Acidentes por tipo de veiculo
plt.figure(figsize=(12,8))
sns.countplot(y="tipo_veiculo", data=vehicle_data, order=vehicle_data['tipo_veiculo'].value_counts().index)

# Uma questão que seria interessante explorar é se os carros mais novos são mais seguros, mas não temos dados suficientes para responder isso.

# In[17]:

# Número de mortos x ilesos x feridos graves x feridos leves por ano do veículo
plt.figure(figsize=(12,8))
sns.lineplot(data=vehicle_data.groupby('ano_fabricacao_veiculo')['n_ilesos', 'n_feridos_leves', 'n_feridos_graves', 'n_mortos'].agg('sum'))

# In[18]:

# Latitude e longitude
plt.figure(figsize=(8,8))
sns.scatterplot(x="longitude", y="latitude", data=accident_data)

# In[19]

# Número de acidentes por tipo, para cada tipo de pista
plt.figure(figsize=(8,12))
sns.countplot(y='tipo_acidente', hue='tipo_pista', data=accident_data, order=accident_data['tipo_acidente'].value_counts(ascending=True).index)

