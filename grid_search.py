from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
'''
Grid Search_Model:
INPUT: Feature Matrix (X) , label (y)
OUTPUT: Best model with ideal parameters
'''

# **Classification**
# 'accuracy'                 :func:`sklearn.metrics.accuracy_score`
# 'average_precision'        :func:`sklearn.metrics.average_precision_score`
# 'f1'                       :func:`sklearn.metrics.f1_score`
# 'precision'                :func:`sklearn.metrics.precision_score`
# 'recall'                   :func:`sklearn.metrics.recall_score`
# 'roc_auc'                  :func:`sklearn.metrics.roc_auc_score`


def grid_search_model(X,y):

    models = {	"LR" 			        :LogisticRegression(penalty='l2'),
                #"Naive Bayes"			:MultinomialNB(),
                "Random Forest"			:RandomForestClassifier(n_estimators=400,bootstrap=False),
                #"SVC"			        :SVC()
            }

    SVC_parameters = {'kernel'                  :('linear','rbf','poly'), 
                    'C'                         :np.logspace(-4,2,11)
                     }

    LR_parameters = {#'penalty'					:('l1','l2'), 
                    'C'       					:[0.01, 0.1, 1.0],
                    'dual'    					: (True,False),
                    'class_weight'				:('auto',None)	 #True if log_penalty == 'l2' else False
                    }

    NB_parameters = {'alpha'					:[5.0, 2.0, 1.5, 1.0, 0.5, 0.1]},
    RF_parameters = {   #'n_estimators'			:[400, 500],#200,300,400,500,10],
                        'criterion'				:('entropy','gini'),
                        'min_samples_split'		:[1,2],
                        #'bootstrap'			:(True, False)
                    }
    
    params_dict = {"LR": LR_parameters,
                   #"Naive Bayes": NB_parameters,
                   "Random Forest": RF_parameters
                   }
    
    scoring = ['average_precision','f1', 'precision', 'recall','roc_auc']

    for model_name, model_obj in models.iteritems():
        print '-' * 10 + model_name +'-' * 10
        run_model(model_obj, X, y, params_dict[model_name],'roc_auc')

def run_model(Model, X,y, parameters, scoring):
    clf = GridSearchCV(Model, parameters, scoring = scoring, cv = 5)
    h = clf.fit(X,y)
    print scoring
    print h.grid_scores_
    print h.best_params_




