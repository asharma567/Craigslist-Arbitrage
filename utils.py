import cPickle
import re
import datetime
from sklearn import cross_validation
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import numpy as np

PXS = {2008: (330.29, u'Macbook Air 13 2008', 57),
 2009: (341.33, u'Macbook Air 13 2009', 24),
 2010: (491.87, u'Macbook Air 13 2010', 58),
 2011: (590.11, u'Macbook Air 13 2011', 138),
 2012: (683.4, u'Macbook Air 13 2012', 121),
 2013: (823.18, u'Macbook Air 13 2013', 140),
 2014: (870.86, u'Macbook Air 13 2014', 7)}


def negotiability_check(df):
    print df['negotiability'].value_counts()
    print 'OBO -', df[df['negotiability'] == 'obo']['px'].mean()
    print 'Firm - ', df[df['negotiability'] == 'firm']['px'].mean()

def re_search(regex, string):
    if not regex: return None
    m = re.search(regex, string.lower())
    if m is None: return None
    return m.group()


def f_get(dic, key1, key2):
#easier but .. dic.get("a", {}).get("B", None)
    if key1 in dic and key2 in dic[key1]:
        return dic[key1][key2]
    return None

# Pickle DataFrame as extra backup
def pickle_this(name, df):
    query_exec_time = datetime.datetime.now()
    cPickle.dump(df, open(name + '_' + query_exec_time.strftime('%m-%d-%y') + '.pkl', "w"))


#removal methods:
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


def preprocess_from_df(dfX,dfy):
    y = dfy.ravel()
    X = np.array(dfX.astype(int))
    X = X.reshape((X.shape[0],1))
    return X,y

def remove_duplicates(input_df,column_name):
    df = input_df[:]
    df = df.drop_duplicates(cols=column_name, take_last=True)
    df.sort_index(inplace=True)
    df = df.reset_index()
    del df['index']
    return df

#if column header and body == 'repair'
def remove_key_words(input_df,keyword):
    filtered_df = input_df[-input_df['heading'].str.lower().str.contains(keyword)]
    filtered_df = input_df[-input_df['body'].str.lower().str.contains(keyword)]
    return filtered_df

def model_score(model, X, y):
        return np.mean(cross_validation.cross_val_score(model, X, y, cv = 20))

def print_links(df, arg_indices, top_n):
    # print 'rank\tindex\tlink'
    links_to_be_shown = []
    ctr = 0

    for i, link in enumerate(df.iloc[arg_indices]['url_to_post']):
        if check_if_removed(link):
            #recursive function maybe
            #top_n - ctr
            continue
        ctr += 1
        # print link
        links_to_be_shown.append(str(link))
        if ctr == top_n: break
    return links_to_be_shown

def make_unicode(s):
    return unicode(s, 'utf-8', errors='ignore')

def price_filtering(input_df, upper_bound, lower_bound):
    
    #abnormally_low_prices
    input_df = input_df[input_df['px'] < upper_bound]
    
    #abnormally_high_prices 
    input_df = input_df[input_df['px'] > lower_bound]
    
    return input_df

def plot_pricevsyear(df, model=None, title=None):
    #Scatter
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

#clustering among top deals
def find_indices(y_hat,y):
    #fix for year
    delta = y - y_hat
    # now how do I impose some threshold say: 2*stds from mean
    indices = np.argsort(delta)
    return indices

def check_if_removed(link):
    checker = lambda x: bool(re.search(r'will be removed in just a few minutes', x))
    r = requests.get(link)
    if r.status_code == 200:
        if checker(r.text): return True
    return False

def get_ebay_data():
    api = 'c8cabb30069fe1dd5ea187a03a7294ad'
    url = 'http://api.bidvoy.net/article/analyse/'
    ebay_data = {}

    try:
        for year in xrange(2008,2015):
            resp = requests.get(url, params={'apikey': api, 'category': 111422, 'keyword': 'Macbook Air 13 ' + str(year)})
            
            ebay_data[year] = (float(resp.json()['data']['averagePrice']), 
                                resp.json()['data']['keyword'], 
                                int(resp.json()['data']['analyzedQuantity']))
               
    except TypeError:
        print 'error with the API call'
        print resp.json()
            
        ebay_data = PXS    
    
    return ebay_data

def testing_samplepage(metro):
    for i in get_postings(0, metro):
        print json.dumps(i, indent= 4, sort_keys= True)

