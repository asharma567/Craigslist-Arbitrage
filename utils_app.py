from pricer.pricing import grab_data_for_analysis, modeled_indices, find_stds
from pricer.pricing_panel import make_pricing_panel
from pricer.utils_pricer import preprocess_from_df, clean_dead_links
from scraper.scraper import get_training_data
from utils import engine
import cPickle

def row_to_html(df_row):
    '''
    Row of DataFrame -> Google Api Infowindow post
    '''
    headingopen = '<h1 id="firstHeading" class="firstHeading">'
    headingclose = '</h1>'

    bodyopen = '<div id="bodyContent"><p>'
    bodyclose = '</p></div>'

    linkopen = '<a href='
    linkmid = '>'
    linkclose = '</a>'

    footopen = '<p>'
    footend = '</p>'

    # All properties of an Infowindow Google Maps Api
    heading = headingopen + linkopen + str(df_row['url_to_post']) + \
                linkmid + str(df_row['heading']) + linkclose + headingclose 
    
    body = bodyopen + str(df_row['body']) + bodyclose 
    
    footer = footopen + str(df_row['px']) + ' posted - ' + str(df_row['ebay_price']) + \
             ' eBay  = ' + str(df_row['spread']) +' profit'+ footend
    
    Latitude = float(df_row['LatLng'][0]), 
    Longitude = float(df_row['LatLng'][1])
    infowindow = heading + body + footer
    return [infowindow, Latitude[0], Longitude]

def display_pipeline_arb(metro, top_n=20):
    '''
    Grabbing DataFrame -> cleansed and filtered
    '''
    df = grab_data_for_analysis(metro, engine)
    X, y = preprocess_from_df(df['year'], df['px'])
    df_modeled, indices, model = modeled_indices(X, y, df)

    df_2_stds = find_stds(df_modeled, 1)

    print 50 * '='
    print len(df_2_stds)
    # print df_modeled['residuals'],df_modeled['px'] 
    print 50 * '='
    # show_this_df = display_panel(df_2_stds, None, 10)
    # return show_this_df
    show_this_df = display_panel(df, indices, top_n)
    arb_only_show_this_df = show_this_df[show_this_df['spread'] > 0]
    
    # return clean_dead_links(arb_only_show_this_df)
    return arb_only_show_this_df
    

def display_panel(df, indices=None, top_n=10):
    '''
    returns the optimal records within the raw DataFrame
    Filters recommendation window size to be shown 
    Only grabs necessary columns
    '''
    PXS = cPickle.load(open('scraper/ebay_data.pkl', 'r'))
    columns = ['heading', 'year', 'px','url_to_post','LatLng','body']
    
    if indices != None:
        new_df = df.iloc[indices][columns][:top_n]
    else:
        new_df = df[columns][:top_n]
    # new_df = df.iloc[indices][columns][:top_n]
    
    return make_pricing_panel(new_df, PXS).sort('spread')[::-1]
