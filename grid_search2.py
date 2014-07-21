from utils import * 
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso

from sklearn.linear_model import ElasticNet
from sklearn.linear_model import MultiTaskLasso
from sklearn.linear_model import LassoLars 
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.linear_model import MultiTaskLasso
from sklearn.grid_search import GridSearchCV



models = {	"LR" 			        :LinearRegression(),
			"L1"					:Lasso(),
			"Random Forest"			:RandomForestRegressor(),
			"SVR"			        :SVR(),
		 }

L1_parameters  = {'alpha':[10,1,0,.1,.01,.001,.00001],
					'tol':[.01,.001,.00001], 
					'warm_start':[False,True],
					'positive':[False,True]
					}
SVR_parameters = {
				'kernel'                    :['linear','rbf'], 
				'C'                         :np.logspace(-4,2,11),
				'gamma'                     :[.1,1],
				'degree'                    :[1,2,3]
				 }

LR_parameters = {}


RF_parameters = {   
					'n_estimators'			:[1,5,10,50,100,200,300,400],
					'criterion'				:['mse'],
					'min_samples_split'		:[1,2,10],
					'bootstrap'			    :[True, False]
				}

params_dict = {
				   "SVR": SVR_parameters,
					"LR": LR_parameters,
					"L1": L1_parameters,
				   "Random Forest": RF_parameters
			   }

#bag of words, TF-IDF, NMF, LDA, , Kmeans, silhouette score .. iterate through Ks find highest score.
#Decision Tree

def routine(X,y, model,df,pxs):

	
	top_n_recs = 50
	top_indices = find_indices(model.fit(X,y).predict(X),y)
	df 	= df.iloc[top_indices][['heading', 'year', 'px']][:top_n_recs]
	
	max_price = make_pricing_panel(df, pxs)['spread'].max()
	average_spread = make_pricing_panel(df, pxs)['spread'].mean()

	return max_price, average_spread

def search_best_params(X,y,df):
	#loop for model
	# for model_name, model_obj in models.iteritems():
	# 	print '-' * 15 + model_name +'-' * 15
	print '# of examples', len(X)
	# for hyper_param_name in RF_parameters:
	pxs = get_ebay_data()
	bestavg = 0
	print str(params_dict["Random Forest"].keys())
	for number_of_trees in params_dict["Random Forest"]['n_estimators']:
		for crit in params_dict["Random Forest"]['criterion']:
			for min_split in params_dict["Random Forest"]['min_samples_split']:
				for boot in params_dict["Random Forest"]['bootstrap']:
					
					model = RandomForestRegressor(
													n_estimators		=number_of_trees,
												  	criterion			=crit,
												  	min_samples_split	=min_split,
												  	bootstrap			=boot,
												  )
					maxi, avg = routine(X, y, model, df, pxs)
					if avg > bestavg:
						bestavg = avg
						optimal_params = (number_of_trees, crit, min_split, boot, maxi, avg)
	print optimal_params
	
	bestavg = 0
	print str(params_dict["SVR"].keys())
	for k in params_dict["SVR"]['kernel']:
		for c in params_dict["SVR"]['C']:
			for g in params_dict["SVR"]['gamma']:
				for d in params_dict["SVR"]['degree']:
					
					model = SVR(
													kernel		=k,
												  	C			=c,
												  	gamma	    =g,
												  	degree		=d,
												  )
					
					maxi, avg = routine(X, y, model, df, pxs)
					if avg > bestavg:
						bestavg = avg
						optimal_params = (k, c, g, d, maxi, avg)
	print optimal_params

	
	bestavg = 0
	for k in params_dict["L1"]['alpha']:
		for c in params_dict["L1"]['tol']:
			for g in params_dict["L1"]['warm_start']:
				for d in params_dict["L1"]['positive']:
					
					model = Lasso(
													alpha		=k,
												  	tol			=c,
												  	warm_start  =g,
												  	positive	=d,
												  )
					
					maxi, avg = routine(X, y, model, df, pxs)
					if avg > bestavg:
						bestavg = avg
						optimal_params = (k, c, g, d, maxi, avg)
	print params_dict["L1"].keys()
	print optimal_params
			#ask gio about the grid search
			# for  

		# for hyper_parameter_value in params_dict[model_name][hyper_param_name]:
		# 	print hyper_param_name, hyper_parameter_value
		# 	routine(X, y, model_obj(i))

def grid_search_model(model,params): #send in the model eg LinearRegression()
	parameters = params
	clf = GridSearchCV(model,params)
	clf.fit(X,y)
	return clf.best_estimator_


# SVR_parameters = {'kernel':['rbf','linear'],'gamma':arange(0,4),'C':arange(0.1,9)}




	