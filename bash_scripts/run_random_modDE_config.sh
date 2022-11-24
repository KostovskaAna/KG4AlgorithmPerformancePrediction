#!/bin/bash


algos=("modDE")
rands=("1" "2" "3" "4" "5")
budgets=("2000" "5000" "10000" "50000")
modes=("config")
ks=("50" "100" "150" "200")
losses=("pairwise" "self_adversarial" "nll")
lrs=("0.001" "0.0001")


for algo in ${algos[@]}
do
    for rand in ${rands[@]}
    do
        for budget in ${budgets[@]}
        do
            for mode in ${modes[@]}
            do
                for k in ${ks[@]}
                do
                    for loss in ${losses[@]}
                    do
                        for lr in ${lrs[@]}
                        do
                        python ../python_scripts/HPO_KG_embeddings_random_subset.py 5 $budget 0.1 $algo $mode $rand $k $loss $lr &				
                        done
                    done
                done 
            done
        done
    done
done