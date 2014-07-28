from parser import c_list_parser
from utils_scraper import pickle_this
import threetaps
import datetime
import sqlalchemy as sql
import datetime


#Query params

macbookair13 = '''"Macbook Air 13" | "Macbook Air 13-inch" \
| "Macbook Air 13inch" | "Macbook Air 13.3-Inch" | \
"Macbook Air 13/11-inch" | "Macbook Air 13.3"'''


fields = "price,heading,annotations,timestamp,expires,body,images,external_url,location,deleted,flagged_status"


manhattan_tier1_macbookair13_params={'location.city': 'USA-NYM-NEY',
                             'tier': '1',
                             'code' :'CRAIG',
                             'status': 'for_sale',
                             'text': macbookair13,
                             'state': 'available',
                             'rpp': 100, 
                             'has_price':'1',
                             'retvals': fields
                             }

client = threetaps.Threetaps('973f359c55ef2ca99b891cd698476d44')

#SQL params
engine  = sql.create_engine('postgresql://Ajay:@localhost/arbitrage')


def get_postings(tier_num, metro,pg_num_iterator = 0):
    tristate_macbookair13_params={'location.metro': metro,
                                 'category_group':'SSSS',
                                 'tier': tier_num,
                                 'page': pg_num_iterator,
                                 'code' :'CRAIG',
                                 'status': 'for_sale',
                                 'text': macbookair13,
                                 'state': 'available',
                                 'rpp': 100, 
                                 'has_price':'1',
                                 'retvals': fields
                                 }
    
    
    sample_page = client.search.search(params = tristate_macbookair13_params)
    print 'number of total matches: ', sample_page['num_matches']
    print '# of postings in sample page:', len(sample_page['postings'])
    print 'next_page: ', sample_page['next_page'], 'next_tier', sample_page['next_tier']

    return sample_page['postings']


def get_training_data(tier_num, metro, just_append_override=False):

    first_run = True
    pg_num_iterator = 0
    
    query_exec_time = datetime.datetime.now()
    postings = get_postings(tier_num, metro, pg_num_iterator)
    while len(postings) > 0:
        
        parse_results = c_list_parser(postings, query_exec_time)
        if just_append_override:
            f_df_save(parse_results,'training' + metro + '_df','append')
            print len(parse_results),'SAVED'
        
        else:
            if first_run:
                f_df_save(parse_results,'training' + metro + '_df','replace')
                first_run = False
                print len(parse_results),'SAVED'
            else:
                f_df_save(parse_results,'training' + metro + '_df','append')
                print len(parse_results),'SAVED'
        
        pg_num_iterator += 1
        postings = get_postings(tier_num, metro,pg_num_iterator)
    
    return None

# Save a DF to SQL table
def f_df_save(df, table_name, sql_option='append'):
    
    if not table_name:
        table_name = str(df) 

    #Create the SQL table and the schema if it's the initial run
    df.to_sql(table_name, engine, if_exists=sql_option)



