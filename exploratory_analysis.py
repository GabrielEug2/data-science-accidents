
# coding: utf-8

# Elabore um documento descrevendo sua análise exploratória usando elementos visuais adequados. O documento deve conter:
# 
# * Descrição das fontes de dados
# * Descrição das principais variáveis (features)
# * Análises inciais de distribuição e/ou correlação com gráficos adequados
# * Conclusões/ideias/hipóteses iniciais
# 
# Vamos colocando essas células de markdown no decorrer do código, aí já gera o PDF pelo próprio notebook)

# In[144]:


import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt


# In[145]:


df = pd.read_csv('acidentes2018.csv', sep=';', encoding='latin-1')


# In[146]:


# Raw data
pd.set_option('display.max_columns', None) # None = mostra todas

print(df.columns)
df.describe()


# In[147]:


# Descartando informações específicas dos envolvidos, porque a principio não vamos usar

grouped_by_accident = df.groupby('id')

# Se o acidente é o mesmo, essas informações vão ser iguais pra todas as linhas daquele acidente
accident_data = grouped_by_accident[
    'data_inversa', 'dia_semana', 'horario', 'uf', 'br', 'km', 'municipio',
    'causa_acidente', 'tipo_acidente', 'classificacao_acidente', 'fase_dia',
    'sentido_via', 'condicao_metereologica', 'tipo_pista', 'tracado_via',
    'uso_solo', 'ilesos', 'feridos_leves', 'feridos_graves', 'mortos',
    'latitude', 'longitude', 'regional', 'delegacia', 'uop'
].first()

# Calcula a quantidade de feridos, mortos, etc no acidente
accident_data['n_ilesos'] = grouped_by_accident['ilesos'].sum()
accident_data['n_feridos_leves'] = grouped_by_accident['feridos_leves'].sum()
accident_data['n_feridos_graves'] = grouped_by_accident['feridos_graves'].sum()
accident_data['n_mortos'] = grouped_by_accident['mortos'].sum()

accident_data['n_envolvidos'] = accident_data['n_ilesos'] + accident_data['n_feridos_leves'] + accident_data['n_feridos_graves'] + accident_data['n_mortos']

accident_data.head()


# In[148]:


accident_data.describe()


# In[160]:


# Número de acidentes por tipo de acidente
plt.figure(figsize=(8,4))
sb.countplot(y="tipo_acidente", data=accident_data, order=accident_data['tipo_acidente'].value_counts(ascending=True).index)


# In[150]:


# Número de acidentes por causa
plt.figure(figsize=(8,6))
sb.countplot(y="causa_acidente", data=accident_data, order=accident_data['causa_acidente'].value_counts(ascending=True).index)


# In[151]:


# Número de acidentes por dia da semana
plt.figure(figsize=(8,4))
sb.countplot(x="dia_semana", data=accident_data)


# In[152]:


# Número de acidentes por fase do dia
plt.figure(figsize=(8,4))
sb.countplot(x="fase_dia", data=accident_data, order=['Amanhecer', 'Pleno dia', 'Anoitecer', 'Plena Noite'])


# In[153]:


# Número de acidentes por hora
tmp = pd.DataFrame()
tmp['hora'] = pd.to_datetime(accident_data['horario']).dt.hour

plt.figure(figsize=(8, 4))
sb.countplot(x='hora', data=tmp)


# In[154]:


# Número de acidentes no decorrer do ano (série temporal)

# Já é pra estar ordenado no dataset, mas só pra garantir
accident_data['data_inversa'] = pd.to_datetime(accident_data['data_inversa'])
accident_data.sort_values(by='data_inversa')

plt.figure(figsize=(12, 4))
time_series = sb.lineplot(data=accident_data.groupby('data_inversa').size())


# In[155]:


# Acidentes por estado
plt.figure(figsize=(8,8))
sb.countplot(y="uf", data=accident_data, order=accident_data['uf'].value_counts(ascending=True).index)


# In[156]:


# Acidentes por BR
plt.figure(figsize=(8,25))
sb.countplot(y="br", data=accident_data, order=accident_data['br'].value_counts(ascending=True).index)


# In[157]:


# Acidentes por clima
plt.figure(figsize=(12,6))
sb.countplot(x="condicao_metereologica", data=accident_data, order=accident_data['condicao_metereologica'].value_counts(ascending=True).index)


# In[158]:


# As informações dos veículos não dá pra fazer como a gente tava fazendo até agora
# porque alguns acidentes envolvem mais de um veículo. Se pegar só o primeiro,
# nós estamos descartando vários deles.
# Temos que repensar essas estatísticas

# Acidentes por tipo de veiculo
#pd.value_counts(accident_data['tipo_veiculo']).plot('bar')

# mortos por ano do veículo (carros mais novos são mais seguros, será?)

# absoluto
#sns.lineplot(data=accident_data.groupby('ano_fabricacao_veiculo').agg('sum')['n_mortos'])

# média
#sns.lineplot(data=accident_data.groupby('ano_fabricacao_veiculo').agg('mean')['n_mortos'])

