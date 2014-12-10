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

def mask_for_state(df, state='interictal'):
    return df[['interictal' in i for i in df['paths']]]

def random_sample(df, n='auto'):
    if n == 'auto':
        n = int(sum(df['y']))
    # print(n)
    return df.ix[random.sample(list(df.index), n)]
