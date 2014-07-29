import numpy as np
import pand as pd

'''
All functions were used during EDA
figuring out which features gave the best results
'''

def feature_m(df_all):
    df_X = df_all[['upgraded_HD', 
                   'upgraded_cpu', 
                   'upgraded_memory', 
                   'apple_care',
                   'year',
                   'px', 
                   'cpu_speed',
                   'image_url_ct',
                   'memory',
                   'HD_size']]

    df_X['apple_care'] = binarize_boolean_series(df_X['apple_care'])
    df_X['upgraded_HD'] = binarize_boolean_series(df_X['upgraded_HD'])
    df_X['upgraded_memory'] = binarize_boolean_series(df_X['upgraded_memory'])
    df_X['upgraded_cpu'] = binarize_boolean_series(df_X['upgraded_cpu'])        
    df_X['year'] = df_X['year'].astype(int)
    df_X['px'] = df_X['px'].astype(int)
    df_X['cpu_speed'] = df_X['cpu_speed'].astype(float)
    df_X['HD_size'] = df_X['HD_size'].astype(float)
    df_X['memory'] = df_X['memory'].astype(int)

    pd.scatter_matrix(df_X, figsize=(15,15));
    y = df_X.pop('year').ravel()
    X = np.array(df_X)
    return X, y

def preprocess_from_df2(dfX, dfy):
    dfX['apple_care'] = binarize_boolean_series(dfX['apple_care'])
    dfX['upgraded_HD'] = binarize_boolean_series(dfX['upgraded_HD'])
    dfX['upgraded_memory'] = binarize_boolean_series(dfX['upgraded_memory'])
    dfX['upgraded_cpu'] = binarize_boolean_series(dfX['upgraded_cpu'])        
    dfX['year'] = dfX['year'].astype(int)
    y = dfy.ravel()
    X = np.array(dfX)

    return X, y

def binarize_boolean_series(series):
    series[series == 'true'] = 1
    series[series == 'false'] = 0

    return series