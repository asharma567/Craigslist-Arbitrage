from flask import Flask, render_template
import requests
import pandas as pd
import sqlalchemy as sql
from scraper.scraper import get_training_data
from datetime import timedelta
from pricer.pricing import grab_data_for_analysis, modeled_indices
from pricer.pricing_panel import make_pricing_panel
from pricer.utils_pricer import preprocess_from_df, clean_dead_links
from utils import db_conn
import cPickle

app = Flask(__name__)

#EDIT put this in the row function


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


def display_panel(df, indices, top_n= 10):
    columns = ['heading', 'year', 'px','url_to_post','LatLng','body']
    new_df      = df.iloc[indices][columns][:top_n]

    return make_pricing_panel(new_df, PXS).sort('spread')[::-1]

@app.route('/')
def dashboard():
    metro = 'USA-NYM'
    df = grab_data_for_analysis(metro, engine)
    X, y = preprocess_from_df(df['year'], df['px'])
    # show_this_df = clean_dead_links(display_panel(df, modeled_indices(X, y, 'RF'), 20))
    
    show_this_df = display_panel(df, modeled_indices(X, y, df), 20)
    arb_only_show_this_df = show_this_df[show_this_df['spread'] > 0]

    
    #gets list with highest profit margins vs eBay
    #EDIT
    locs = [row_to_html(row) for index, row in clean_dead_links(arb_only_show_this_df).iterrows()]
    
    html_page = render_template('map_page.html.jinja2', 
                                    df=arb_only_show_this_df.to_html(),
                                    l=locs,
                                    links=arb_only_show_this_df)

    return html_page

if __name__ == '__main__':
    engine = db_conn()
    PXS = cPickle.load(open('scraper/ebay_data.pkl', 'r'))
    app.run(host='0.0.0.0', port=80, debug=True)





    
