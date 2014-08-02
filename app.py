from flask import Flask, render_template
import requests
import pandas as pd
import sqlalchemy as sql
from datetime import timedelta
from pricer.utils_pricer import clean_dead_links
from utils_app import display_pipeline_arb, row_to_html

import cPickle

app = Flask(__name__)

#have something that runs the routine and pickles the df perhaps mains? 
#or attach to the periodic scraper also clean the deadlinks

#Have the dashboard just unpickle and map the 

@app.route('/')
def dashboard():
    '''
    This app should just display the stored 
    recs that have been pickled earlier the day

    It takes time to scrape, grid search, recommend, clean deadlinks, 
    better do as a scheduled task vs doing it on the fly
    '''

    #Lets just focus on the tristate area for now
    metro = 'USA-NYM'

    df = cPickle.load(open('recs.pkl','rb')) 
   
    #gets list with highest profit margins vs eBay
    locs = [row_to_html(row) \
            for index, row in df.iterrows()]
    html_page = render_template('map_page.html.jinja', markers_list_of_locations = locs)
    
    return html_page

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)





    
