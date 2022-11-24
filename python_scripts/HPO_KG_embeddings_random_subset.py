import sys
import numpy as np
import pandas as pd 
from ampligraph.latent_features import ComplEx
from ampligraph.discovery import query_topn
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from ampligraph.latent_features import save_model
from statistics import mode
from imblearn.metrics import geometric_mean_score


def get_corruption_entities(X_test):
    array = []
    for triple in X_test:
        s = triple[0]
        p = triple[1]
        o = triple[2]
        p_n = 'not-solved' if p == 'solved' else 'solved'
        array.append([s, p_n, o])
    return array

def get_relation_predictions(model, X_test):
    y_true = []
    y_pred = []
    i = 0
    for test_triplet in X_test:
        i +=1
        if(i%1000==0):
            print(i)
        test_s = test_triplet[0]
        test_p = test_triplet[1]
        test_o = test_triplet[2]
        triples, scores = query_topn(model, top_n=2, 
            head=test_s, 
            relation=None, 
            tail=test_o, 
            ents_to_consider=None, 
            rels_to_consider=['solved', 'not-solved'])
        y_true.append(test_p)
        y_pred.append(triples[0][1])
    return y_true, y_pred, geometric_mean_score(y_true, y_pred, labels=['solved', 'not-solved'], pos_label = 'solved'), accuracy_score(y_true, y_pred), f1_score(y_true, y_pred, labels=['solved', 'not-solved'], pos_label = 'solved')   
    
def get_embeddings(model, dim, budget, fixed_target, algo, removal_mode, rand_n):
    _k = model.k
    con_n = 324 if algo == 'modCMA' else 576
    conf_arr = ['conf_'+str(i) for i in range(0,con_n)]
    problem_instance_arr = ['f'+str(f)+'_i'+str(ist) for f in range(1,25) for ist in range(1,6)]
    embeddings_confs = model.get_embeddings(conf_arr)
    embedings_problems = model.get_embeddings(problem_instance_arr)
        
    df_embeddings_conf = pd.DataFrame(embeddings_confs, columns = ['c_'+str(n) for n in range(0, 2*_k)])
    df_embeddings_conf['conf'] = conf_arr
    df_embeddings_conf= df_embeddings_conf.set_index('conf')
    df_embeddings_conf.to_csv(f'../Results/embeddings_random_subset/{algo}/{removal_mode}/rand_{rand_n}_embeddings_confs_ComplEx_dim_{dim}_budget_{budget}_target_{fixed_target:.5f}.csv')

    df_embeddings_problems = pd.DataFrame(embedings_problems, columns = ['p_'+str(n) for n in range(0, 2*_k)])
    df_embeddings_problems['problem'] = problem_instance_arr
    df_embeddings_problems= df_embeddings_problems.set_index('problem')
    df_embeddings_problems.to_csv(f'../Results/embeddings_random_subset/{algo}/{removal_mode}/rand_{rand_n}_embeddings_problems_ComplEx_dim_{dim}_budget_{budget}_target_{fixed_target:.5f}.csv')                   

def HPO_KG_embedding(dim, budget, fixed_target, algo, removal_mode, rand_n, k, loss, lr):
    X_train = np.load(f'../DATA/KG_random_subset/{algo}/{removal_mode}/rand_{rand_n}_KG_dim_{dim}_budget_{budget}_target_{fixed_target:.5f}_train.npy')
    X_val = np.load(f'../DATA/KG_random_subset/{algo}/{removal_mode}/rand_{rand_n}_KG_dim_{dim}_budget_{budget}_target_{fixed_target:.5f}_val.npy')
    X_test = np.load(f'../DATA/KG_random_subset/{algo}/{removal_mode}/rand_{rand_n}_KG_dim_{dim}_budget_{budget}_target_{fixed_target:.5f}_test.npy')


    text_file = open(f"../Results/HPO_random_subset/{algo}/{removal_mode}/rand_{rand_n}_trace_ComplEx_dim_{dim}_budget_{budget}_target_{fixed_target:.5f}.txt", "a")


    model = ComplEx(batches_count=10, seed=0, epochs=500, k=k, eta=10,
        # Use adam optimizer with learning rate 1e-3
        optimizer='adam', optimizer_params={'lr':lr},
        # Use pairwise loss with margin 0.5
        loss=loss, loss_params={'margin':0.5, 'alpha': 0.5},
        # Use L2 regularizer with regularizer weight 1e-5
        regularizer='LP', regularizer_params={'p':2, 'lambda':1e-5}, 
        # Enable stdout messages (set to false if you don't want to display)
        verbose=True)

    filter = np.concatenate((X_train, X_val, X_test))
    
    # Fit the model on training and validation set
    model.fit(X_train, 
            early_stopping = True,
            early_stopping_params = \
                    {
                        'x_valid': X_val,            # validation set
                        'criteria':'hits10',         # Uses hits10 criteria for early stopping
                        'burn_in': 20,               # early stopping kicks in after 100 epochs
                        'check_interval':20,         # validates every 20th epoch
                        'stop_interval':10,           # stops if 5 successive validation checks are bad.
                        'x_filter': filter,          # Use filter for filtering out positives 
                        'corruption_entities':'all', # corrupt using all entities
                        'corrupt_side':'s+o'         # corrupt subject and object (but not at once)
                    }
    )
    y_test, y_test_preds, gmean, acc, f1 = get_relation_predictions(model, X_test)
    np.save(f"../Results/HPO_random_subset/{algo}/{removal_mode}/rand_{rand_n}_test_preds_ComplEx_dim_{dim}_budget_{budget}_target_{fixed_target:.5f}_k_{k}_loss_{loss}_lr_{lr}.npy", y_test_preds)
    np.save(f"../Results/HPO_random_subset/{algo}/{removal_mode}/rand_{rand_n}_test_true_ComplEx_dim_{dim}_budget_{budget}_target_{fixed_target:.5f}_k_{k}_loss_{loss}_lr_{lr}.npy", y_test)
    text_file.write("gmean = "+str(gmean) +", f1 = "+str(f1)+", acc = "+str(acc)+", k = "+str(k)+", loss = "+str(loss)+", lr = "+str(lr)+"\n")
    text_file.flush()
    print("gmean = "+str(gmean) +", f1 = "+str(f1)+", acc = "+str(acc)+", k = "+str(k)+", loss = "+str(loss)+", lr = "+str(lr)+"\n")

    text_file.close()
    return model 

if __name__ == "__main__":
    dim = int(sys.argv[1]) 
    budget = int(sys.argv[2])
    fixed_target = float(sys.argv[3])
    algo = sys.argv[4]
    removal_mode = sys.argv[5]
    rand_n = int(sys.argv[6])
    k = int(sys.argv[7])
    loss = sys.argv[8]
    lr = float(sys.argv[9])
    model = HPO_KG_embedding(dim, budget, fixed_target, algo, removal_mode, rand_n, k, loss, lr)
    get_embeddings(model, dim, budget, fixed_target, algo, removal_mode, rand_n)