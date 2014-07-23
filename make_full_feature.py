
def feature_m(df_all):

    df_all['apple_care'] = binarize_boolean_series(df_all['apple_care'])
    df_all['upgraded_HD'] = binarize_boolean_series(df_all['upgraded_HD'])
    df_all['upgraded_memory'] = binarize_boolean_series(df_all['upgraded_memory'])
    df_all['upgraded_cpu'] = binarize_boolean_series(df_all['upgraded_cpu'])        
    df_all['year'] = df_all['year'].astype(int)
    df_all['px'] = df_all['px'].astype(int)
    df_all['cpu_speed'] = df_all['cpu_speed'].astype(float)
    df_all['HD_size'] = df_all['HD_size'].astype(float)
    # df_all['memory'][df_all['memory'] == None] = 0
    # df_all['memory'] = df_all['memory'].apply(lambda x: re_search(r'\d',x))
    # df_all['memory'] = df_all['memory'].astype(int) fails on none
    # df_all['memory'][df_all['memory'] == None]
    pd.scatter_matrix(df_all[['upgraded_HD', 'upgraded_cpu', 'upgraded_memory', 'apple_care','year','px', 'cpu_speed','image_url_ct','memory','HD_size']],figsize=(15,15));
    return X,y




    


df[['upgraded_HD', 'upgraded_cpu', 'upgraded_memory', 'apple_care','year','px', 'cpu_speed','image_url_ct','HD_size']].fillna(value=0)
X, y = preprocess_from_df2(df[['upgraded_HD', 'upgraded_cpu', 'upgraded_memory', 'apple_care','year','px', 'cpu_speed','image_url_ct','HD_size']],df['px'])

return X, y

def preprocess_from_df2(dfX,dfy):
    y = dfy.ravel()
    
    dfX['apple_care'] = binarize_boolean_series(dfX['apple_care'])
    dfX['upgraded_HD'] = binarize_boolean_series(dfX['upgraded_HD'])
    dfX['upgraded_memory'] = binarize_boolean_series(dfX['upgraded_memory'])
    dfX['upgraded_cpu'] = binarize_boolean_series(dfX['upgraded_cpu'])        
    dfX['year'] = dfX['year'].astype(int)
    X = np.array(dfX)
#     X = X.reshape((X.shape[0],1))
    return X,y

def binarize_boolean_series(series):
    #Process of going form DF to SQL changes the format
    #we need to revert
    series[series == 'true'] = 1
    series[series == 'false'] = 0
    return series