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

    df = df[["data_inversa", "id", "latitude", "longitude", "fase_dia", "condicao_metereologica", "mortos"]]

    df.loc[df['mortos'] > 0, 'mortos'] = True
    df.loc[df['mortos'] <= 0, 'mortos'] = False
    df['mortos'] = np.where(df['mortos'] == True, 1, 0)

    df.to_csv(VISUALIZATIONS_DATA_FILENAME, index=False)


def preprocess_data_for_danger_indicator():
    df = pd.read_csv(CLEAN_DATA_FILENAME)

    df = df[['id', 'br', 'km', 'latitude', 'longitude', 'horario', 'condicao_metereologica', 'mortos']]

    # Deixa só as BRs com mais dados
    # print(df.groupby('br').size().sort_values(ascending=False))
    brs_with_most_accidents = df.groupby('br').size().sort_values(ascending=False).head(10).index
    df = df[df['br'].isin(brs_with_most_accidents)]

    # print(df.groupby('condicao_metereologica').size().sort_values(ascending=False))
    df = df[df['condicao_metereologica'] != 'Ignorado']

    # Número de mortos também não interessa, só se teve ou não
    df.loc[df['mortos'] > 0, 'mortos'] = True
    df.loc[df['mortos'] <= 0, 'mortos'] = False
    df['mortos'] = np.where(df['mortos'] == True, 1, 0)

    df.to_csv(DANGER_INDICATOR_ACCIDENTS_FILENAME, index=False)


clean_data(data_2018)
preprocess_data_for_visualizations()
preprocess_data_for_danger_indicator()