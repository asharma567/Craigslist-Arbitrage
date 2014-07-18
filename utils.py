import cPickle
import re
import datetime

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


def preprocess_from_df(X,y):
    y = df['px'].ravel()
    X = np.array(df['year'].astype(int))
    X = X.reshape((X.shape[0],1))

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

def print_links(df,arg_indices, top_n):
    print 'rank\tindex\tlink'
    for i, link in enumerate(df.iloc[arg_indices]['url_to_post'][:top_n]):
        print i , '\t' ,  link 

def make_unicode(s):
    return unicode(s, 'utf-8', errors='ignore')

def price_filtering(input_df, upper_bound, lower_bound):
    
    #abnormally_low_prices
    input_df = input_df[input_df['px'] < upper_bound]
    
    #abnormally_high_prices 
    input_df = input_df[input_df['px'] > lower_bound]
    
    return input_df

def plot_pricevsyear(df,model=None):
    #Scatter
    fig, ax = plt.subplots()
    ax.scatter(df['year'], df['px'], alpha=0.5, color='orchid')
    fig.suptitle('Year vs Price')

    #could turn into def, df.columns
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.set_xlabel(r'$Year$',    fontsize=16)
    ax.set_ylabel(r'$Price$',   fontsize=16)
    fig.tight_layout(pad=2)
    
    if model:
        X = np.arange(2007, 2015)
        years = np.arange(2007, 2015).reshape(len(X),1)
        prediction = np.array(model.predict(years))
        plt.plot(years, prediction,'b--',alpha=0.5)
    
    plt.show()