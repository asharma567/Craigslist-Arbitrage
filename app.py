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

app = Flask(__name__)


def grab_data_for_analysis(metro):
	
	#Grabbing the data
	all_metro_df = pd.read_sql_table('training' + metro + '_df', engine)
	print len(all_metro_df)
	all_metro_df = remove_duplicates(all_metro_df,'heading')
	print len(all_metro_df)
	
	#Removing the NA
	df = all_metro_df[all_metro_df['year'] != 'NaN']
	tmpdf = all_metro_df[all_metro_df['year'] == 'NaN']
	df = remove_key_words(df, 'repair')
	df = price_filtering(df, 1300, 350)
	return df
	

def modeled_indices(X, y, model_type= 'RF'):
	
	model = {
				'L1' 		: Lasso(alpha= 1, tol= .01, warm_start= False, positive= False),
				'SVR_lin' 	: SVR('linear', C= 6.3095734448019298, gamma= 0.1, degree= 1),
				'RF' 		: RandomForestRegressor(min_samples_split= 2, n_estimators= 10),
			}
	y_hat = model[model_type].fit(X, y).predict(X)
	
	return find_indices(y_hat, y)


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

