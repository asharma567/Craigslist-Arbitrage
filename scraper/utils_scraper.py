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
