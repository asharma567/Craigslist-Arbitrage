import numpy as np
import pandas as pd
import cPickle
from pricing_panel import find_indices, make_pricing_panel
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.grid_search import GridSearchCV

import sys
sys.path.append('../')
from utils import db_conn


models = {"LR": LinearRegression(),
          "L1": Lasso(),
          "Random Forest": RandomForestRegressor(),
          "SVR": SVR()}

L1_parameters = {'alpha': [10, 1, 0, .1, .01, .001, .00001], 
                 'tol': [.01, .001, .00001],  
                 'warm_start': [False, True], 
                 'positive': [False, True]}

SVR_parameters = {'kernel': ['linear', 'rbf'],  
                  'C': np.logspace(-4, 2, 11), 
                  'gamma': [.1, 1], 
                  'degree': [1, 2, 3]}

RF_parameters = {'n_estimators': [1, 5, 10, 50, 100, 200, 300], 
                 'criterion': ['mse'],
                 'min_samples_split': [1, 2, 10], 
                 'bootstrap': [True, False]}

params_dict = {"SVR": SVR_parameters,
               "LR": None,
               "L1": L1_parameters,
               "Random Forest": RF_parameters}


def routine(X, y, model, df, pxs):
    '''
    INPUT  Feature Matrix, labels, Original DataFrame, eBay prices
    OUTPUT Recommendation Table (Ranked respectively)
    '''
    # this should be in some proportion to the sample size
    top_n_recs = int(len(df) * .15)
    top_indices = find_indices(model.fit(X,y).predict(X),y)
    df  = df.iloc[top_indices][['heading', 'year', 'px']][:top_n_recs]
    max_price = make_pricing_panel(df, pxs)['spread'].max()
    average_spread = make_pricing_panel(df, pxs)['spread'].mean()

    return max_price, average_spread

def search_best_params(X, y, df):
    '''
    Grid Search for the model that yields the optimal recommendations table. 
    Validating versus eBay pricing. Optimizes for the highest spread: eBay - Craigslist = Profit
    INPUT  Feature Matrix, labels, Original DataFrame, eBay prices
    OUTPUT Optimal tuned model, prints all model with thier best parameters
    '''
    print '# of examples', len(X)
    
    #Grab eBay's data to validate against
    pxs = cPickle.load(open('scraper/ebay_data.pkl', 'r'))
    optimal_model = {}
    
    #First tune each model to it's optimal parameters
    #================================================

    #Random Forest Regressor

    bestavg = 0
    for number_of_trees in params_dict['Random Forest']['n_estimators']:
        for crit in params_dict['Random Forest']['criterion']:
            for min_split in params_dict['Random Forest']['min_samples_split']:
                for boot in params_dict['Random Forest']['bootstrap']:
                    
                    model = RandomForestRegressor(n_estimators=number_of_trees,
                                                  criterion=crit,
                                                  min_samples_split=min_split,
                                                  bootstrap=boot)

                    maxi, avg = routine(X, y, model, df, pxs)
                    if avg > bestavg:
                        best_model = model
                        bestavg = avg
                        optimal_params = (number_of_trees, crit, min_split, boot, maxi, bestavg, best_model)
                        optimal_model['Random Forest'] = optimal_params

    print 'n_estimators=%d, criterion=%s, min_samples_split=%d, bootstrap=%s' % \
    (optimal_params[0], optimal_params[1], optimal_params[2], optimal_params[3])
    
    print 'Max - %d, Avg Spread - %d' % \
    (optimal_params[4], optimal_params[5])
    
    #Support Vector Machine Regression 

    bestavg = 0
    for k in params_dict['SVR']['kernel']:
        for c in params_dict['SVR']['C']:
            for g in params_dict['SVR']['gamma']:
                for d in params_dict['SVR']['degree']:
                    
                    model = SVR(kernel=k,
                                C=c,
                                gamma=g,
                                degree=d)

                    maxi, avg = routine(X, y, model, df, pxs)
                    #write this as a function
                    if avg > bestavg:
                        best_model = model
                        bestavg = avg
                        optimal_params = (k, c, g, d, maxi, avg, best_model)
                        optimal_model['SVR'] = optimal_params
    
    print 'kernel=%s, C=%d, gamma=%d, degree=%d' % \
    (optimal_params[0], optimal_params[1], optimal_params[2], optimal_params[3])
    
    print 'Max - %d, Avg Spread - %d' % \
    (optimal_params[4], optimal_params[5])

    #Lasso Regression   
    
    bestavg = 0
    for a in params_dict['L1']['alpha']:
        for t in params_dict['L1']['tol']:
            for w in params_dict['L1']['warm_start']:
                for p in params_dict['L1']['positive']:
                    
                    model = Lasso(alpha=a,
                                  tol=t,
                                  warm_start=w,
                                  positive=p)
                    
                    maxi, avg = routine(X, y, model, df, pxs)
                    if avg > bestavg:
                        best_model = model
                        bestavg = avg
                        optimal_params = (a, t, w, p, maxi, avg, best_model)
                        optimal_model['L1'] = optimal_params
                        
    # print 'alpha=%d, tol=%d, warm_start=%s, positive=%s' % \
    print (optimal_params[0], optimal_params[1], optimal_params[2], optimal_params[3])
    
    print 'Max - %d, Avg Spread - %d' % \
    (optimal_params[4], optimal_params[5])
    
    #find the model the yielded highest average profit
    best_spread = 0
    for model_name, params in optimal_model.iteritems():
        #NOTE - no option for tie
        if params[5] > best_spread:
            best_spread = params[5]
            best_model = model_name
    print 'Best Model: ', best_model

    #An instance of the best model (pretuned) is returned
    return optimal_model[best_model][6]


def grid_search_model(model, params):
#to send in the model eg LinearRegression() 
    parameters = params
    clf = GridSearchCV(model,params)
    clf.fit(X,y)
    return clf.best_estimator_







