import pandas as pd
import datetime
import re
from utils_scraper import f_get, pickle_this, re_search
from model_dict import features_by_year

f_conv_date                 = lambda x: datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S')
f_make_images_string        = lambda x: str('|'.join([item['full'].decode('utf8') for item in x]))
f_find_year                 = lambda x: re_search(r'\b(200[8-9]|201[0-4])\b', x)
f_find_year_by_words_2013   = lambda x: re_search(r'MD760LL/A', x.lower())
f_find_year_by_words        = lambda x: re_search(r'BNIB|brand new|sealed|latest|unopened|MD760LL/B', x.lower())
f_negotiability_obo         = lambda x: re_search(r'\bobo|best offer', x.lower())
f_negotiability_firm        = lambda x: re_search(r'\bfirm', x.lower())
f_base_or_upgrade           = lambda x,y: bool (re_search(y, x.lower()))
f_find_apple_care           = lambda x: bool(re_search(r'apple warranty|applecare|apple care|warranty', x.lower()))
f_find_cpu                  = lambda x: re_search(r'1\.6|1\.8|1\.86|2\.13|2\.1|2\.0|1\.3|1\.7|1\.4', x)
f_find_memory               = lambda x: re_search(r'\b2 gb\b|\b2gb\b|\b4 gb\b|\b4gb\b|\b8 gb\b|\b8gb\b', x)
f_find_HD                   = lambda x: re_search(r'250|256|516|128|80|64|120', x)
f_take_out_words            = lambda x: re.sub(r'office 200[0-9]|office 201[0-9]|brand new battery|brand new charger|brand new os', '', x.lower())

def c_list_parser(postings, query_execution_time):
    '''
    Parses Craigslist postings: JSON -> DataFrame -> SQL
    '''
    df = pd.DataFrame()
    current_year = datetime.datetime.now().year
    
    for dic in postings:

        str_heading_body = dic['heading'] + " | " + dic['body']
        str_heading_body = f_take_out_words(str_heading_body)            
        
        #Parsing Negotiatiability
        negotiability = 'NaN'
        if f_negotiability_firm(str_heading_body): negotiability = 'firm'
        if f_negotiability_obo(str_heading_body): negotiability = 'obo'

        #Year    
        if f_find_year(str_heading_body):
            year = int(f_find_year(str_heading_body))
        else:
            
            # if we can't find the year in the string, 
            # look for keywords and defualt to the latest year
            if f_find_year_by_words_2013(str_heading_body):
                year = current_year - 1
                print year
            else:                   
                if f_find_year_by_words(str_heading_body): 
                    year = current_year
                else:
                    year = None
                
        #Condition
        condition = f_get(dic, 'annotations','condition')

        #Contact info
        email = f_get(dic, 'annotations', 'source_account')
        phone = f_get(dic, 'annotations', 'phone')

        #Location
        loc_dict            = str(dic['location'])
        
        region = f_get(dic, 'location', 'region')
        city = f_get(dic, 'location', 'city')

        if region:
            loc = region
            loc_metro = region[:7]
        elif city:
            loc = city
            loc_metro = city[:7]
        else:
             loc = None
             loc_metro = f_get(dic, 'location','metro')

        #Craigslist posting information
        heading         = str(dic['heading'])
        body            = dic['body']
        px              = float(dic['price'])
        posting_time    = f_conv_date(dic['timestamp'])
        exp_time        = f_conv_date(dic['expires'])
        image_url       = f_make_images_string(dic['images'])
        image_url_ct    = len(dic['images'])
        url_to_post     = str(dic['external_url'])

        if year:
            upgraded_cpu = f_base_or_upgrade(str_heading_body, features_by_year[year]['processor_speeds']['high'])
            upgraded_memory = f_base_or_upgrade(str_heading_body, features_by_year[year]['memory']['high'])
            upgraded_HD = f_base_or_upgrade(str_heading_body, features_by_year[year]['HD']['high'])       
        else:
            upgraded_cpu = False
            upgraded_memory = False
            upgraded_HD = False

        #additional features 
        apple_care = f_find_apple_care(str_heading_body)
        cpu    = f_find_cpu(str_heading_body)
        memory = f_find_memory(str_heading_body)
        HD     = f_find_HD(str_heading_body)
        
        # if we can't even get one of these features skip
        if not year and not cpu and not memory and not HD: continue
        
        #just for handling the data later
        if not year: year = 'NaN'
        if not cpu: cpu = 'NaN'
        if not memory: memory = 'NaN'
        if not HD: HD = 'NaN'
    
        #All the data extracted from a single post        
        df_row = pd.DataFrame({
                                'heading'        :heading,
                                'body'           :body,
                                'px'             :px,
                                'year'           :year,
                                'condition'      :condition,
                                'phone'          :phone,
                                'posting_time'   :posting_time,
                                'exp_time'       :exp_time,
                                'image_url'      :image_url,
                                'image_url_ct'   :image_url_ct,
                                'url_to_post'    :url_to_post,
                                'negotiability'  :negotiability,
                                'date_of_pull'   :query_execution_time,
                                'email'          :email,
                                'loc'            :loc,
                                'loc_metro'      :loc_metro,
                                'loc_dict'       :loc_dict,
                                'upgraded_cpu'   :upgraded_cpu,
                                'upgraded_memory':upgraded_memory,
                                'upgraded_HD'    :upgraded_HD,
                                'apple_care'     :apple_care,
                                'memory'         :memory,
                                'cpu_speed'      :cpu,
                                'HD_size'        :HD,

                             }, index = [0])
        df = df.append(df_row, ignore_index = True)
        
    return df

