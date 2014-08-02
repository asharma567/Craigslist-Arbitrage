import sqlalchemy as sql


def db_conn(conn_string = 'postgresql://Ajay:@localhost/arbitrage'):
    '''
    Houses the connection info to the SQL db
    '''
    # Setup database connection
    engine = sql.create_engine(conn_string)
    if engine.connect(): 
        print 'Connected to SQL DB'
        return engine 

engine = db_conn()

def return_active_links(df, arg_indices, top_n):
    
    links_to_be_shown = []
    ctr = 0
    dead_link_ctr = 0

    for i, link in enumerate(df.iloc[arg_indices]['url_to_post']):
        
        if check_if_removed(link): 
            print 'removed 1' 
            dead_link_ctr += 1
            continue
        ctr += 1
        
        links_to_be_shown.append(str(link))
        if ctr == top_n: break
    print dead_link_ctr

    return links_to_be_shown

def make_unicode(s):
    return unicode(s, 'utf-8', errors='ignore')

def testing_samplepage(metro):
    for i in get_postings(0, metro):
        print json.dumps(i, indent= 4, sort_keys= True)

