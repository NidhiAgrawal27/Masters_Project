#!/bin/bash

# for seed in {42..46}
for seed in {42..42}
    do

        python -m mains.main_correspondence_ntwrk --seed $seed --currency sample
        
        python -m mains.main_correspondence_ntwrk --seed $seed --currency iota

    done

# python -m visualization.visualize
