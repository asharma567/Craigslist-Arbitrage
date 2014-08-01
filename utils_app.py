from pricer.pricing import grab_data_for_analysis, modeled_indices, find_stds
from pricer.pricing_panel import make_pricing_panel
from pricer.utils_pricer import preprocess_from_df, clean_dead_links
from scraper.scraper import get_training_data
from utils import engine
import cPickle
import datetime

def row_to_html(df_row):
    '''
    Row of DataFrame -> Google Api Infowindow post
    Populates the following stats: 
                                   <Title>
                                   <Pic> 
                                   <body>
                                      780.0 price
                                    - 870.86 eBay
                                    = 90.86 profit

                                    percentage below mean
                                    10% eBay
                                    9% Craigs

                                    Age: 1 days, 11 hours, and 49 mins
    '''

    headingopen = '<h1 id="firstHeading" class="firstHeading">'
    headingclose = '</h1>'

    bodyopen = '<div id="bodyContent"><p>'
    bodyclose = '</p></div>'

    linkopen = '<a href='
    linkmid = '>'
    linkclose = '</a>'

    footopen = '<p ALIGN="RIGHT"><strong>'
    footend = '</strong></p>'

    spacing = '<br><br>'
    newline = '<br>'
    popen = '<p ALIGN="RIGHT">'
    pclose = '</p>'

    distance_from_mean_craigs = "{:.0%}".format(df_row['price_distance_craig'])  
    distance_from_mean_ebay = "{:.0%}".format(1 - df_row['px'] / df_row['ebay_price'])

    # All properties of an Infowindow Google Maps Api
    heading = headingopen + linkopen + str(df_row['url_to_post']) + \
                linkmid + str(df_row['heading']) + linkclose + headingclose                 
    
    body = bodyopen + str(df_row['body']) + bodyclose 
    
    footer = footopen + 3 * '&nbsp' + str(df_row['px']) + ' price'+ newline + \
                        ' - ' + str(df_row['ebay_price']) + ' eBay' + newline + \
                        '=  ' + str(df_row['spread'])  + ' profit' + footend
    
    distance = popen + 'percentage below mean' + newline + \
                     str(distance_from_mean_ebay) + ' eBay'+ newline + \
                     str(distance_from_mean_craigs) + ' Craigs' + pclose
    
    duration = popen + 'Age: ' + posting_duration_calc(str(df_row['posting_time'])) + pclose
    craig_posting_img = str(df_row['image_url'].split('|')[0])

    
    if craig_posting_img != '':
        imgopen = '<IMG BORDER="1" ALIGN="Left" SRC="'
        imgclose = '" width="150" height="125">'
        img = imgopen + craig_posting_img + imgclose
    else:
        img = ''

    Latitude = float(df_row['LatLng'][0]), 
    Longitude = float(df_row['LatLng'][1])

    infowindow = heading + img + body + footer + distance + duration
    
    return [infowindow, Latitude[0], Longitude]

def strfdelta(tdelta, fmt):
    '''
    Used only in row_to_html to calc duration of posting
    '''
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

def posting_duration_calc(timestring):
    '''
    Calcs the duration of posting
    Used only in row_to_html to calc duration of posting
    '''   
    new = datetime.datetime.strptime(timestring, '%Y-%m-%d %H:%M:%S')
    cur = datetime.datetime.now()
    time_delta_obj = cur - new
    dur = strfdelta(time_delta_obj, "{days} days, {hours} hours, and {minutes} mins")
    return dur

def display_pipeline_arb(metro, top_n=20):
    '''
    Grabbing DataFrame -> cleansed and filtered
    '''
    df = grab_data_for_analysis(metro, engine)
    X, y = preprocess_from_df(df['year'], df['px'])
    df_modeled, indices, model = modeled_indices(X, y, df)

    show_this_df = display_panel(df, indices, top_n)
    arb_only_show_this_df = show_this_df[show_this_df['spread'] > 0]
    
    return clean_dead_links(arb_only_show_this_df)
    

    

def display_panel(df, indices=None, top_n=10):
    '''
    Returns the optimal records within the raw DataFrame
    Filters recommendation window size to be shown 
    Only grabs necessary columns
    '''
    PXS = cPickle.load(open('scraper/ebay_data.pkl', 'r'))
    
    #For efficiency sake here are the cols we're going to include in the app
    columns = [
                'heading', 
                'year', 
                'px',
                'url_to_post',
                'LatLng',
                'body', 
                'image_url',
                'posting_time',
                'email',
                'price_distance_craig',
                ]
    
    if indices != None:
        new_df = df.iloc[indices][columns][:top_n]
    else:
        new_df = df[columns][:top_n]
    
    return make_pricing_panel(new_df, PXS).sort('spread')[::-1]
