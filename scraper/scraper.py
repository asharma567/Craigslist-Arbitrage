
from parser import c_list_parser
from utils_scraper import pickle_this, f_df_save
import threetaps
import datetime
import sqlalchemy as sql
import datetime
import requests
import pandas as pd
import cPickle


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
        postings = get_postings(tier_num, metro, pg_num_iterator)
    
    return None

def get_ebay_data():
    api = 'c8cabb30069fe1dd5ea187a03a7294ad'
    url = 'http://api.bidvoy.net/article/analyse/'
    ebay_data = {}

    try:
        for year in xrange(2008, 2015):
            resp = requests.get(url, params={'apikey': api, 'category': 111422, 'keyword': 'Macbook Air 13 ' + str(year)})            
            ebay_data[year] = (float(resp.json()['data']['averagePrice']), 
                                resp.json()['data']['keyword'], 
                                int(resp.json()['data']['analyzedQuantity']))           
    except TypeError:
        print 'error with the API call'
        print resp.json()
        ebay_data = PXS    
    
    ebay_df = pd.DataFrame(ebay_data)
    cPickle.dump(ebay_df, open('ebay_data.pkl', 'w'))
    print 'ebay_data - SAVED'
    
    return ebay_df

