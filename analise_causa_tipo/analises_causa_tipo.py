#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
pd.set_option('display.max_columns', None)

#%%
csv = pd.read_csv('data/datatran2018.csv', sep=';', encoding='latin-1')
csv.head()

#%%
print('linhas, colunas: ' + str(csv.shape))

#%%
causas = csv[['causa_acidente']].astype('category')
causas.groupby('causa_acidente').size().sort_values(ascending=False)

#%%
tipos = csv[['tipo_acidente']]
tipos.groupby('tipo_acidente').size().sort_values(ascending=False)

#%%
falta_atencao = csv[csv['causa_acidente'] == 'Falta de Atenção à Condução'][['tipo_acidente', 'causa_acidente']]
falta_atencao.groupby('tipo_acidente').size().sort_values(ascending=False)

#%%
corr = falta_atencao.corr(method='pearson')
print(corr)
#cmap = sns.diverging_palette(220, 10, as_cmap=True)
#sns.heatmap(corr, cmap=cmap)

#%%
test = pd.crosstab(index=causas['causa_acidente'], columns=tipos['tipo_acidente']).apply(lambda r: r/r.sum(), axis=1)
print(test)

#%%
plt.figure(figsize=(10,8))
sns.heatmap(test, yticklabels=True)
plt.savefig('teste.png', dpi=500)

#%%
# Existe alguma relação entre as condições meteorológicas e o tipo dos acidentes?
condicao_tipo = pd.crosstab(index=csv['condicao_metereologica'], columns=csv['tipo_acidente'])
condicao_tipo_pct = pd.crosstab(index=csv['condicao_metereologica'], columns=csv['tipo_acidente']).apply(lambda r: r/r.sum(), axis=1)

#%%
plt.figure(figsize=(12,5))
sns.heatmap(condicao_tipo, yticklabels=True)

#%%
plt.figure(figsize=(12,5))
sns.heatmap(condicao_tipo_pct, yticklabels=True)

#%%
# PCA
tipo_causa = csv[['pessoas', 'mortos', 'feridos_leves', 'feridos_graves', 'ilesos', 'ignorados', 'veiculos', 'causa_acidente']]
tipo_causa = tipo_causa.dropna()
causas = tipo_causa.groupby('causa_acidente').size().sort_values(ascending=False)[:3].index.tolist()
tipo_causa = tipo_causa[tipo_causa['causa_acidente'].isin(causas)]
tipo_causa_pca = tipo_causa[['pessoas', 'mortos', 'feridos_leves', 'feridos_graves', 'ilesos', 'ignorados', 'veiculos']]
tipo_causa_pca.head()

#%%
pca = PCA(n_components=2)
result = pca.fit_transform(tipo_causa_pca.values)
tipo_causa_pca['pca-one'] = result[:, 0]
tipo_causa_pca['pca-two'] = result[:, 1]
tipo_causa = pd.concat([tipo_causa, tipo_causa_pca], axis=1)
print(pca.explained_variance_ratio_)

#%%
plt.figure(figsize=(11,6))
sns.scatterplot(x='pca-one', y='pca-two', hue='causa_acidente', data=tipo_causa)
#plt.savefig('pca.png', dpi=500)

#%%
# ANALISE MORTOS
analise_mortos = csv[csv['mortos'] > 0]
analise_mortos.groupby('tipo_acidente').size().sort_values(ascending=False)

#%%
# SITUACAO DOS KMS MAIS LETAIS DA BR
brs = csv.groupby('br').size().sort_values(ascending=False).index.tolist()[:5]
#br_km = csv[csv['br'].isin(brs)]
#br_km['br_km'] = br_km[]
kms = csv[csv['br'].isin(brs)].groupby(['br', 'km']).size().sort_values(ascending=False)
kms


#%%
csv[(csv['br'] == 101.0) & (csv['km'] == '207')]['tipo_pista']

#%%
# Perguntas
#Durante a noite, a principal causa de acidentes é a falta de atenção.
csv[csv['fase_dia'] == 'Plena Noite'].groupby('causa_acidente').size().sort_values(ascending=False) 

#%%
#Os finais de semana são o período com maior número de acidentes por embriaguez ao volante. 
csv[(csv['dia_semana'] == 'sábado') | (csv['dia_semana'] == 'domingo')].groupby('causa_acidente').size().sort_values(ascending=False)


#%%
#Dentre os acidentes que acontecem quando está chovendo, a maior parte são colisões.
csv[(csv['condicao_metereologica'] == 'Chuva') | (csv['condicao_metereologica'] == 'Garoa/Chuvisco') | (csv['condicao_metereologica'] == 'Granizo')].groupby('tipo_acidente').size().sort_values(ascending=False)

#%%
