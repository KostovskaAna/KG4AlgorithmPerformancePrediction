#!/bin/bash


algos=("modCMA" "modDE")
dims=("30")
budgets=("2000" "5000" "10000" "50000")
fixed_targets=("10" "1" "0.1")
ks=("50" "100" "150" "200")
losses=("pairwise" "self_adversarial" "nll")
lrs=("0.001" "0.0001")


for algo in ${algos[@]}
do
    for dim in ${dims[@]}
    do
        for budget in ${budgets[@]}
        do
            for fixed_target in ${fixed_targets[@]}
            do
                for k in ${ks[@]}
                do
                    for loss in ${losses[@]}
                    do
                        for lr in ${lrs[@]}
                        do
                        python ../python_scripts/HPO_KG_embeddings.py $dim $budget $fixed_target $algo $k $loss $lr &				
                        done
                    done
                done 
            done
        done
    done
done