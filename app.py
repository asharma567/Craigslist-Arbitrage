from flask import Flask, render_template
import requests
import pandas as pd
import sqlalchemy as sql
from datetime import timedelta
from pricer.utils_pricer import clean_dead_links
from utils_app import display_pipeline_arb, row_to_html

import cPickle

app = Flask(__name__)


@app.route('/')
def dashboard():
    #Lets just focus on the tristate area for now
    metro = 'USA-NYM'
   
    #Specify number of recommendations
    #gets filtered down by removal of dead links
    rec_size = 30

    #gets list with highest profit margins vs eBay
    locs = [row_to_html(row) \
            for index, row in display_pipeline_arb(metro, rec_size).iterrows()]
    html_page = render_template('map_page.html.jinja', markers_list_of_locations = locs)
    
    return html_page

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)





    
