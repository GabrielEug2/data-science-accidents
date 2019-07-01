import json
import pandas as pd
import numpy as np


data_2017 = pd.read_csv("datatran2017.csv", sep=";", encoding="latin-1")
data_2018 = pd.read_csv("datatran2018.csv", sep=";", encoding="latin-1")
full_data = pd.concat([data_2017, data_2018])

CLEAN_DATA_FILENAME = "final.csv"
VISUALIZATIONS_DATA_FILENAME = "visualizations_data.csv"
DANGER_INDICATOR_ACCIDENTS_FILENAME = "only_brs_with_most_accidents.csv"


def clean_data(df):
    # remove colunas que não serão utilizadas
    df.drop(columns=["regional", "delegacia", "uop"], inplace=True)

    # troca células vazias por NaN
    df.replace("", np.nan, inplace=True)

    # remove qualquer linha com NaN
    df.dropna(inplace=True)

    df['latitude'] = df['latitude'].apply(lambda x: round(x, 4))
    df['longitude'] = df['longitude'].apply(lambda x: round(x, 4))

    df.drop(df[ df['latitude'] >= 6 ].index, inplace=True)
    df.drop(df[ df['latitude'] <= -34 ].index, inplace=True)
    df.drop(df[ df['longitude'] <= -74 ].index, inplace=True)
    df.drop(df[ df['longitude'] >= -35 ].index, inplace=True)

    # cria coluna timestamp com data + hora
    # df["timestamp"] = pd.to_datetime(df["data_inversa"] + " " + df["horario"])
    # df.drop(columns=["data_inversa"], inplace=True)
    # df.drop(columns=["horario"], inplace=True)

    # reordena as colunas, colocando timestamp na segunda posição
    # cols = df.columns.tolist()
    # cols.insert(1, cols[-1])
    # cols = cols[:-1]
    # df = df[cols]

    # ajusta os tipos
    df["id"] = df["id"].astype(int)
    df["br"] = df["br"].astype(int)
    df["km"].replace(",", ".", regex=True, inplace=True)
    df["km"] = df["km"].astype(float)

    # print("\nCLEANED DATA:\n")
    # print(df.describe())
    # print(df.head())

    df.to_csv(CLEAN_DATA_FILENAME, index=False)


def preprocess_data_for_visualizations():
    df = pd.read_csv(CLEAN_DATA_FILENAME)

    df = df[["data_inversa", "id", "latitude", "longitude", "fase_dia", "condicao_metereologica", "mortos", "uf"]]

    df.loc[df['mortos'] > 0, 'mortos'] = 1
    df.loc[df['mortos'] <= 0, 'mortos'] = 0
    # df['mortos'] = np.where(df['mortos'] == True, 1, 0)

    df.to_csv(VISUALIZATIONS_DATA_FILENAME, index=False)


def preprocess_data_for_danger_indicator():
    df = pd.read_csv(CLEAN_DATA_FILENAME)

    df = df[['id', 'br', 'km', 'latitude', 'longitude', 'horario', 'condicao_metereologica', 'mortos']]

    # Deixa só as brs com mais dados
    # print(df.groupby('br').size().sort_values(ascending=False))
    brs_with_most_accidents = df.groupby('br').size().sort_values(ascending=False).head(10).index
    df = df[df['br'].isin(brs_with_most_accidents)]

    # print(df.groupby('condicao_metereologica').size().sort_values(ascending=False))
    df = df[df['condicao_metereologica'] != 'Ignorado']

    # Número de mortos também não interessa, só se teve ou não
    df.loc[df['mortos'] > 0, 'mortos'] = 1
    df.loc[df['mortos'] <= 0, 'mortos'] = 0
    # df['mortos'] = np.where(df['mortos'] == True, 1, 0)

    df.to_csv(DANGER_INDICATOR_ACCIDENTS_FILENAME, index=False)


def create_state_json(data):
    df = pd.DataFrame(columns=['uf', 'total', 'rank', 'top_city', 'city_total', 'top_br', 'br_total', 'top_cause'])

    total = pd.DataFrame({'total' : data.groupby(['uf']).size()}).reset_index()
    total['rank'] = total['total'].rank(ascending=0, method='max').astype(int)
    
    df[['uf', 'total']] = total[['uf', 'total']]
    df[['uf', 'rank']] = total[['uf', 'rank']]
    df[['uf', 'top_city', 'city_total']] = pd.DataFrame({'total': data[['uf', 'municipio']].groupby(['uf', 'municipio']).size().sort_values().groupby(level=0).tail(1)}).sort_values(by=['uf']).reset_index()[['uf', 'municipio', 'total']]
    df[['uf', 'top_br', 'br_total']] = pd.DataFrame({'total': data[['uf', 'br']].groupby(['uf', 'br']).size().sort_values().groupby(level=0).tail(1)}).sort_values(by=['uf']).reset_index()[['uf', 'br', 'total']]
    # df[['uf', 'top_type']] = pd.DataFrame({'total': data[['uf', 'tipo_acidente']].groupby(['uf', 'tipo_acidente']).size().sort_values().groupby(level=0).tail(1)}).sort_values(by=['uf']).reset_index()[['uf', 'tipo_acidente']]
    df[['uf', 'top_cause']] = pd.DataFrame({'total': data[['uf', 'causa_acidente']].groupby(['uf', 'causa_acidente']).size().sort_values().groupby(level=0).tail(1)}).sort_values(by=['uf']).reset_index()[['uf', 'causa_acidente']]

    df.set_index('uf', inplace=True)

    with open('states.json', 'w', encoding='utf-8') as outfile:
        json.dump(json.loads(df.to_json(orient='index')), outfile, ensure_ascii=False)


def sortkey(x):
    values = x.split('/')
    return [int(values[0]), int(values[1])]

def create_race_data(data):
    data["timestamp"] = pd.to_datetime(data["data_inversa"] + " " + data["horario"])
    data['month_year'] = data['timestamp'].apply(lambda x: str(x.month) + "/" + str(x.year))
    state_period = pd.DataFrame({'total': data[['uf', 'month_year']].groupby(['uf', 'month_year']).size()}).reset_index()[['uf', 'month_year', 'total']]
    
    states = sorted(set(state_period['uf']))
    # months = sorted(set(state_period['month_year']), sortkey)
    months = sorted(set(state_period['month_year']), key = lambda x: pd.to_datetime(x, infer_datetime_format=True))
    print(months)
    
    rows = []
    for state in states:
        row = []
        row.append(state)
        if state in ['SC', 'PR', 'RS']:
            row.append('Sul')
        elif state in ['SP', 'RJ', 'MG', 'ES']:
            row.append('Sudeste')
        elif state in ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO']:
            row.append('Norte')
        elif state in ['GO', 'MT', 'MS', 'DF']:
            row.append('Centro-Oeste')
        elif state in ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE']:
            row.append('Nordeste')
        count = 0
        for month in months:
            temp = state_period[(state_period['uf'] == state) & (state_period['month_year'] == month)]
            count += int(temp['total'])
            row.append(count)
        rows.append(row)

    months = list(map(lambda x: str(x).zfill(7), months))
    
    df = pd.DataFrame(rows)
    df.columns = ['uf', 'region'] + months
    print(df)
    df.to_csv('race.csv', index=False)


# clean_data(data_2018)
# preprocess_data_for_visualizations()
# preprocess_data_for_danger_indicator()
# create_state_json(data_2018)
create_race_data(full_data)
