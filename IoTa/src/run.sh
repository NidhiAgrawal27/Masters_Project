#!/bin/bash

# for seed in {42..46}
for seed in {42..42}
do

    python -m mains.main_preprocessing --seed $seed
    
done

# python -m visualization.visualize
