import pandas as pd
from utils_pricer import remove_duplicates, remove_key_words, price_filtering
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
import ast
import numpy as np
from grid_search2 import search_best_params
from pricing_panel import find_indices


def grab_data_for_analysis(metro, conn):
    '''
    Raw Scraped FROM SQL -> Filtered DataFrame for analysis
    INPUT    metro: convention used for scraping a particular geo area eg 'USA-NYM' == NYC
             conn: SQL connection to the Database we're scraping from
    OUTPUT   Filtered DataFrame (df)
    '''    
    #Grabbing the data
    SQL_df = pd.read_sql_table('training' + metro + '_df', conn)
    print 'Total scraped - ', len(SQL_df)
    SQL_df = remove_duplicates(SQL_df, 'heading')

    #Removing the NA
    df = SQL_df[SQL_df['year'] != 'NaN']
    df = remove_key_words(df, 'repair')
    
    #Defining an upperbound and lower bound from the sample
    df = price_filtering(df, 1300, 350)

    #unpacking location dictionary and extracting LatLong
    df['loc_dict'] = df['loc_dict'].apply(lambda x: ast.literal_eval(x))
    df['LatLng'] = zip(df['loc_dict'].apply(lambda x: x['lat']), df['loc_dict'].apply(lambda x: x['long']))

    #cleaning up some unicode chars
    df['body']  = df['body'].apply(lambda x:''.join([i if ord(i) < 128 else ' ' for i in x]))
    print 'Filtered down to - ', len(df)

    return df

    
def modeled_indices(X, y, df, model_type= None):
    '''
    We get the largest negatives residuals here
    INPUT  Feature matrix, Labels ie price_filtering, Specify which model
    OUTPUT Sorted residuals from the specified modeled (largest negatives first)
    ''' 
    #Manual override option
    if model_type:

        model = {'L1': Lasso(alpha= 1, tol= .01, warm_start= False, positive= False),
                 'SVR_lin': SVR('linear', C= 6.3095734448019298, gamma= 0.1, degree= 1),
                 'RF': RandomForestRegressor(min_samples_split= 2, n_estimators= 10)}
        y_hat = model[model_type].fit(X, y).predict(X)
        
    else:
        model = search_best_params(X, y, df)
        y_hat = model.fit(X, y).predict(X)
        
    #Used for later for identifying 2stds
    df['predicted_price'] = y_hat
    df['residuals'] =  df['px'] - df['predicted_price']
    
    #Residual as a percentage
    df['price_distance_craig'] =  1 - df['px'] / df['predicted_price']

    return df, find_indices(y_hat, y), model

def find_stds(df, std_multiple=2):
    '''
    return all points 
    '''
    threshold = df['residuals'].mean() - std_multiple * df['residuals'].std()

    return df[threshold > df['residuals']]
    

