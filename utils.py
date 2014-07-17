import cPickle

# Pickle DataFrame as extra backup
def pickle_this(name, df):
    cPickle.dump(df, open(name + '_' + query_exec_time.strftime('%m-%d-%y') + '.pkl', "w"))

# Save a DF to SQL table
def f_df_save(df, table_name, sql_option='append'):
    #get the original table name if possible
    if not table_name:
        table_name = str(df) 
    #Save them somewhere: User should be given option here
    pickle_this(table_name, df)

    #Create the SQL table and the schema if it's the initial run. Yes, I know - amazing.
    df.to_sql(table_name, engine, if_exists=sql_option)