from flask import Flask, request, render_template
import requests
import pandas as pd
import seaborn as sns
from utils import *
import sqlalchemy as sql
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from scraper import get_training_data
from celery import Celery
from datetime import timedelta
from pricing import grab_data_for_analysis
from pricing import modeled_indices

app = Flask(__name__)



def display_panel(df, indices, top_n = 10):
	columns = ['heading', 'year', 'px','url_to_post']
	new_df 		= df.iloc[indices][columns][:top_n]

	return make_pricing_panel(new_df).sort('spread')[::-1]


#http://0.0.0.0:6950/dashboard
@app.route('/dashboard')
def dashboard():
	metro = 'USA-NYM'
	df = grab_data_for_analysis(metro)
	X, y = preprocess_from_df(df['year'],df['px'])
	show_this_df = display_panel(df, modeled_indices(X, y, 'RF'), 10)
	pd.set_option('display.height', 1000)
	pd.set_option('display.max_rows', 500)
	pd.set_option('display.max_columns', 500)
	pd.set_option('display.width', 1000)
	html_page = render_template('some.html.jinja', 
			df= show_this_df[['heading', 'year', 'px']].to_html(),
			links= show_this_df)

	#will have to come back to this bit later.
	return html_page



# @app.route('/dashboard?city = NYC')
# def dashboard():
#     return render_template('some.html.jinja', predictions=grab_data())


if __name__ == '__main__':
	# Setup database connection
	engine = sql.create_engine('postgresql://Ajay:@localhost/arbitrage')
	if engine.connect(): 
		print 'Connected to SQL DB'

	# Load model
	# model = load_model()
	print "Loaded predictive model"

	# R
	flask_app_port = 5213

	app.run(host='0.0.0.0', port=flask_app_port, debug=True)

'''
{% for index, row in df.iterrows() %}
<tr>
<td>{{ row['year'] }}</td>
<td>{{ row['px'] }}</td>
</tr></br>
{% endfor %}
'''

