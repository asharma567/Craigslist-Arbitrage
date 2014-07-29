import cPickle
import re
import datetime
import sys
sys.path.append('../')
from utils import db_conn

def re_search(regex, string):
    '''
    Checking for membership first, if so extract the regex
    '''
    if not regex: return None
    m = re.search(regex, string.lower())
    if m is None: return None
    return m.group()

def f_get(dic, key1, key2):
    '''
    Checking a nested dict for membership and extracting data if so 
    easier way dic.get("a", {}).get("B", None) 
    but I like below for syntatical reasons 
    '''
    if key1 in dic and key2 in dic[key1]:
        return dic[key1][key2]
    return None

def pickle_this(name, df):
    '''
    Storing: DataFrame -> DataFrame.pkl 
    Pickle DataFrame as extra backup
    Used extensively during testing
    '''
    query_exec_time = datetime.datetime.now()
    cPickle.dump(df, open(name + '_' + query_exec_time.strftime('%m-%d-%y') + '.pkl', "w"))

# Save a DF to SQL table
def f_df_save(df, table_name, sql_option= 'append'):
    '''
    Storing: DataFrame -> SQL 
    Used extensively for scraping
    '''
    if not table_name:
        table_name = str(df) 

    #Create the SQL table and the schema if it's the initial run
    df.to_sql(table_name, db_conn(), if_exists= sql_option)
