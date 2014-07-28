from flask import Flask, render_template
import requests
import pandas as pd
import sqlalchemy as sql
from scraper.scraper import get_training_data
from datetime import timedelta
from pricer.pricing import grab_data_for_analysis, modeled_indices, make_pricing_panel
from pricer.utils_pricer import preprocess_from_df, clean_dead_links

app = Flask(__name__)

#Ask gio where to put this
headingopen = '<h1 id="firstHeading" class="firstHeading">'
headingclose = '</h1>'

bodyopen = '<div id="bodyContent"><p>'
bodyclose = '</p></div>'

linkopen = '<a href='
linkmid = '>'
linkclose = '</a>'

footopen = '<p>'
footend = '</p>'


def display_panel(df, indices, top_n = 10):
    columns = ['heading', 'year', 'px','url_to_post','LatLng','body']
    new_df      = df.iloc[indices][columns][:top_n]

    return make_pricing_panel(new_df).sort('spread')[::-1]



@app.route('/dashboard')
def dashboard():
    metro = 'USA-NYM'
    df = grab_data_for_analysis(metro, engine)
    X, y = preprocess_from_df(df['year'],df['px'])
    #NOTE - Arb
    # show_this_df = clean_dead_links(display_panel(df, modeled_indices(X, y, 'RF'), 20))
    
    show_this_df = display_panel(df, modeled_indices(X, y, 'RF'), 20)
    
    #gets list with highest profit margins vs eBay
    locs = [[headingopen + linkopen + str(row['url_to_post']) + linkmid +  \
                str(row['heading']) + linkclose + headingclose + \
                bodyopen + str(row['body']) + bodyclose + \
                footopen + str(row['px']) + ' posted - ' + str(row['ebay_price']) + ' eBay  = ' + str(row['spread']) +' profit'+ footend, \
                float(row['LatLng'][0]), float(row['LatLng'][1])] \
                for index, row in show_this_df.iterrows()]
    
    
    html_page = render_template('map_page.html.jinja', 
            df= show_this_df.to_html(),
            l= locs,
            links= show_this_df)

    return html_page

# @app.route('/dashboard?city = NYC')
# def dashboard():
#     return render_template('some.html.jinja', predictions=grab_data())

if __name__ == '__main__':
    # Setup database connection
    engine = sql.create_engine('postgresql://Ajay:@localhost/arbitrage')
    if engine.connect(): 
        print 'Connected to SQL DB'

    flask_app_port = 5233

    app.run(host='0.0.0.0', port=flask_app_port, debug=True)


'''
Random jinja notes
{% for index, row in df.iterrows() %}
<tr>
<td>{{ row['year'] }}</td>
<td>{{ row['px'] }}</td>
</tr></br>
{% endfor %}
'''
# <html>
# <body>

# {% block content %}
# <h1>Hi!</h1>
# {{df | safe}}
# {% endblock %}

# {% for index, row in links.iterrows() %}
# <tr>
# {{ row['year'] }}
# {{ row['ebay_price'] }}
# {{ row['px'] }}
# {{ row['spread'] }}
# <a href={{ row['url_to_post'] }}> {{ row['heading'] }} </a>

# </tr></br>
# {% endfor %}

# </body>
# </html>



    
