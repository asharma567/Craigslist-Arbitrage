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

 
def remove_duplicates(input_df,column_name):
    df = input_df[:]
    df = df.drop_duplicates(cols=column_name, take_last=True)
    df.sort_index(inplace=True)
    df = df.reset_index()
    return df

def preprocess_from_df(X,y):
    y = df['px'].ravel()
    X = np.array(df['year'].astype(int))
    X = X.reshape((X.shape[0],1))