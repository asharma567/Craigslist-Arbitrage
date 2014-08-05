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
