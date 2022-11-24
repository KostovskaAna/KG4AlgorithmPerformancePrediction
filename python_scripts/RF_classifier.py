import numpy as np
import pandas as pd 
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from xgboost import XGBClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import roc_auc_score
import sys
from imblearn.over_sampling import SMOTE
import joblib

def get_most_frequent_link(X):
    cnt_solved = 0
    cnt_not_solved = 0
    for l in X:
        if l == 1:
            cnt_solved +=1
        elif l == 0:
            cnt_not_solved += 1

    if cnt_solved >= cnt_not_solved:
        return 1
    else:
        return 0

def RF_classifier(algo, dim, budget, fixed_target):
    df_train = pd.read_csv(f'../Results/classification_data/{algo}/ComplEx_dim_{dim}_budget_{budget}_target_{fixed_target:.5f}_train.csv', index_col=0)
    X_train = df_train.iloc[:,:-1]
    y_train = df_train.iloc[:,-1:]
    y_train = [1 if s == 'solved' else 0 for s in np.array(y_train)]

    majority = get_most_frequent_link(y_train)
    
    

    df_test = pd.read_csv(f'../Results/classification_data/{algo}/ComplEx_dim_{dim}_budget_{budget}_target_{fixed_target:.5f}_test.csv', index_col=0)
    X_test = df_test.iloc[:,:-1]
    y_test = df_test.iloc[:,-1:]
    y_test = [1 if s == 'solved' else 0 for s in np.array(y_test)]
  

    clf_dummy = DummyClassifier(strategy='most_frequent')
    clf_dummy.fit(X_train, y_train)
    y_test_preds_dummy = clf_dummy.predict_proba(X_test)[:, 1]
    
    f1_test_dummy = roc_auc_score(y_test, y_test_preds_dummy)

    print("f1-dummy:")
    print(f1_test_dummy)   

    
    clf = RandomForestClassifier(random_state=42, n_estimators=10)
    clf.fit(X_train, y_train)
    y_test_preds =  clf.predict_proba(X_test)[:, 1]

    f1_test = roc_auc_score(y_test, y_test_preds)
                
    print("f1:")
    print(f1_test) 
               
                   
                                    

if __name__ == "__main__":
    algo = "modDE"
    dim = 30
    budget = 2000
    fixed_target = 0.1
    RF_classifier(algo, dim, budget, fixed_target)
    algo = "modDE"
    dim = 30
    budget = 5000
    fixed_target = 0.1
    RF_classifier(algo, dim, budget, fixed_target)
    algo = "modDE"
    dim = 30
    budget = 10000
    fixed_target = 0.1
    RF_classifier(algo, dim, budget, fixed_target)
    algo = "modDE"
    dim = 30
    budget = 50000
    fixed_target = 0.1
    RF_classifier(algo, dim, budget, fixed_target)
