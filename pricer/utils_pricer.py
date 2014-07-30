from sklearn import cross_validation
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import numpy as np
import re

def clean_dead_links(df):
    '''
    Filters DataFrame of of dead links (posts taken down)
    INPUT   DataFrame with field url_to_post ie hyperlinks to posts
    OUTPUT  DataFrame with cleansed of dead links
    '''
    orig_size = len(df)
    df['checker'] = df['url_to_post'].apply(check_if_removed)
    clean_df = df[df['checker'] == False]
    del clean_df['checker']
    print 'removed - ', orig_size - len(clean_df)
    
    return clean_df

def check_if_removed(link):
    checker = lambda x: bool(re.search(r'will be removed in just a few minutes', x))
    r = requests.get(link)
    if r.status_code == 200:
        if checker(r.text): return True
    
    return False

def plot_pricevsyear(df, model=None, title=None):
    '''
    Calculate the residuals versus the model and sorts by largest negatives first
    INPUT  numpy array predicted (modeled) points and observed points
    OUTPUT numpy array of sorted indices
    '''
    fig, ax = plt.subplots()
    ax.scatter(df['year'], df['px'], alpha=0.5, color='orchid')
    fig.suptitle(title)

    #could turn into def, df.columns
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.set_xlabel(r'$Year$', fontsize=16)
    ax.set_ylabel(r'$Price$', fontsize=16)
    fig.tight_layout(pad=2)
    
    if model:
        X = np.arange(2007, 2015)
        years = np.arange(2007, 2015).reshape(len(X),1)
        prediction = np.array(model.predict(years))
        plt.plot(years, prediction,'b--',alpha=0.5)
    
    plt.show() 

def negotiability_check(df):
    '''
    Calculate the residuals versus the model and sorts by largest negatives first
    INPUT  numpy array predicted (modeled) points and observed points
    OUTPUT numpy array of sorted indices
    '''
    print df['negotiability'].value_counts()
    print 'OBO -', df[df['negotiability'] == 'obo']['px'].mean()
    print 'Firm - ', df[df['negotiability'] == 'firm']['px'].mean()

def preprocess_from_df(dfX, dfy):
    y = dfy.ravel()
    X = np.array(dfX.astype(int))
    X = X.reshape((X.shape[0] ,1))
    
    return X, y

def remove_duplicates(input_df, column_name):
    '''
    INPUT  DataFrame with column_name
    OUTPUT DataFrame with duplicates checking only the series column_name
    '''
    df = input_df[:]
    df = df.drop_duplicates(cols= column_name, take_last= True)
    df.sort_index(inplace= True)
    df = df.reset_index()
    del df['index']
    
    return df

def remove_all_same_features(input_df):
    df = input_df[:]
    df['all_features'] = df['cpu_speed']+\
                            df['HD_size']+\
                            df['memory']+\
                            df['year']+\
                            str(df['px'])+\
                            df['apple_care']+\
                            df['upgraded_HD']+\
                            df['upgraded_cpu']+\
                            df['upgraded_memory']
    
    return remove_duplicates(df,'all_features')

def remove_key_words(input_df,keyword):
    filtered_df = input_df[-input_df['heading'].str.lower().str.contains(keyword)]
    filtered_df = input_df[-input_df['body'].str.lower().str.contains(keyword)]
    
    return filtered_df

def price_filtering(input_df, upper_bound, lower_bound):
    
    #abnormally_low_prices
    input_df = input_df[input_df['px'] < upper_bound]
    
    #abnormally_high_prices 
    input_df = input_df[input_df['px'] > lower_bound]
    
    return input_df

def model_score(model, X, y): return np.mean(cross_validation.cross_val_score(model, X, y, cv = 20))
