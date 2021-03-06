import pandas as pd
import random

def build_df(data):
    X, y, paths = data
    df = pd.DataFrame(X)
    df['y'] = y
    df['paths'] = paths
    return df

def mask_for_mat(df, path):
    return df[df['paths'] == path]

def mask_for_state(df, state='preictal'):
    return df[[state in i for i in df['paths']]]

def mask_for_random_sample(df, n='auto'):
    if n == 'auto':
        n = int(sum(df['y']))
    # print(n)
    return df.ix[random.sample(list(df.index), n)]

def wrap_df_to_data(df):
    X = df.iloc[:, :-2].values
    y = df['y']
    y = y.as_matrix()
    paths = list(df['paths'])
    return X, y, paths

def train_strategy(data):
    df = build_df(data)
    df_1 = mask_for_random_sample(df)
    df_2 = mask_for_state(df)
    df = pd.concat([df_1, df_2])
    return wrap_df_to_data(df)