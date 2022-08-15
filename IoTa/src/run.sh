#!/bin/bash

# for seed in {42..46}
for seed in {42..42}
    do

        python -m mains.main_preprocessing --seed $seed
        python -m mains.main_tx_basic_analysis --seed $seed
        python -m mains.iota_gml --seed $seed 
    done

# python -m visualization.visualize
