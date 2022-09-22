#!/bin/bash

# for seed in {42..46}
for seed in {42..42}
    do

        python -m mains.main_correspondence_ntwrk --seed $seed --currency iota --heuristic h0 --vis yes
        python -m mains.main_correspondence_ntwrk --seed $seed --currency iota --heuristic h0+h1 --vis yes
        python -m mains.main_network_analysis --seed $seed --currency iota --heuristic h0
        python -m mains.main_network_analysis --seed $seed --currency iota --heuristic h0+h1


        python -m mains.main_correspondence_ntwrk --seed $seed --currency btc --heuristic h0 --vis yes
        python -m mains.main_correspondence_ntwrk --seed $seed --currency btc --heuristic h0+h1 --vis yes
        python -m mains.main_network_analysis --seed $seed --currency btc --heuristic h0
        python -m mains.main_network_analysis --seed $seed --currency btc --heuristic h0+h1

        
    done

