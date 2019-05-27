import pandas as pd
import numpy as np


data_2017 = pd.read_csv("datatran2017.csv", sep=";", encoding="latin-1")
data_2018 = pd.read_csv("datatran2018.csv", sep=";", encoding="latin-1")

full_data = pd.concat([data_2017, data_2018])
# full_data.to_csv("full.csv", index=False)

# final = pd.read_csv("final.csv")
# print(final.describe())
# print(final.head())

# print("\nRAW DATA DESCRIPTION:\n")
# print(full_data.describe())
# print(full_data.head())

def clean_data(df):
    # remove colunas que não serão utilizadas
    df.drop(columns=["regional"], inplace=True)
    df.drop(columns=["delegacia"], inplace=True)
    df.drop(columns=["uop"], inplace=True)

    # troca células vazias por NaN
    df.replace("", np.nan, inplace=True)

    df['latitude'] = df['latitude'].apply(lambda x: round(x, 4))
    df['longitude'] = df['longitude'].apply(lambda x: round(x, 4))
    df.drop(df[df['latitude'] >= 6 ].index, inplace=True)
    df.drop(df[df['latitude'] <= -34 ].index, inplace=True)
    df.drop(df[df['longitude'] <= -74 ].index, inplace=True)
    df.drop(df[df['longitude'] >= -35 ].index, inplace=True)

    # remove qualquer linha com NaN
    df.dropna(inplace=True)

    # cria coluna timestamp com data + hora
    df["timestamp"] = pd.to_datetime(df["data_inversa"] + " " + df["horario"])
    df.drop(columns=["data_inversa"], inplace=True)
    df.drop(columns=["horario"], inplace=True)

    # reordena as colunas, colocando timestamp na segunda posição
    cols = df.columns.tolist()
    cols.insert(1, cols[-1])
    cols = cols[:-1]
    df = df[cols]

    # ajusta os tipos
    df["id"] = df["id"].astype(int)
    df["br"] = df["br"].astype(int)
    df["km"].replace(",", ".", regex=True, inplace=True)
    df["km"] = df["km"].astype(float)

    # print("\nCLEANED DATA:\n")
    # print(df.describe())
    # print(df.head())

    df.to_csv("final.csv", index=False)

def lat_lon():
    final = pd.read_csv("final.csv")

    df = final[["id", "latitude", "longitude"]]

    df.to_csv("latlon.csv", index=False)

clean_data(full_data)
lat_lon()