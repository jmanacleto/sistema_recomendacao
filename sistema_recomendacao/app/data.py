import pandas as pd

def carregar_dados():
    df = pd.read_csv("data/netflix_titles.csv")
    df.dropna(subset=['title', 'description'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df