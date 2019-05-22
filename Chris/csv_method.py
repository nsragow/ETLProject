import pandas as pd
def csv_to_pd(path_to_csv):
    df_2 = pd.read_csv(path_to_csv)
    df_2.drop(['Unnamed: 0'], axis=1, inplace=True)
    return df_2
