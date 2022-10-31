
# # iota
# python -m mains.main_correspondence_ntwrk --seed 42 --currency iota --heuristic h0 --vis no --data_is_split no --load_graph no
# python -m mains.main_correspondence_ntwrk --seed 42 --currency iota --heuristic h0+h1 --vis no --data_is_split no --load_graph no

# # iota_split
# python -m mains.main_correspondence_ntwrk --seed 42 --currency iota_split --heuristic h0 --vis no --data_is_split no_modin_split --load_graph no --chunksize 1000
# python -m mains.main_correspondence_ntwrk --seed 42 --currency iota_split --heuristic h0+h1 --vis no --data_is_split no_modin_split --load_graph no --chunksize 1000

# btc_sample
python -m mains.main_correspondence_ntwrk --seed 42 --currency btc_sample --heuristic h0 --vis no --data_is_split no --load_graph no
# python -m mains.main_correspondence_ntwrk --seed 42 --currency btc_sample --heuristic h0+h1 --vis no --data_is_split no --load_graph no

# # btc_2012
# python -m mains.main_correspondence_ntwrk --seed 42 --currency btc_2012 --heuristic h0 --vis no --data_is_split no --load_graph no
# python -m mains.main_correspondence_ntwrk --seed 42 --currency btc_2012 --heuristic h0+h1 --vis no --data_is_split no --load_graph no

# # cardano
# python -m mains.main_split_correspondence_ntwrk --seed 42 --currency cardano --heuristic h0 --vis no --data_is_split yes --load_graph no --chunksize 1000000
# python -m mains.main_split_correspondence_ntwrk --seed 42 --currency cardano --heuristic h0+h1 --vis no --data_is_split yes --load_graph no --chunksize 1000000

# # monacoin
# python -m mains.main_correspondence_ntwrk --seed 42 --currency monacoin --heuristic h0 --vis no --data_is_split no --load_graph no
# python -m mains.main_correspondence_ntwrk --seed 42 --currency monacoin --heuristic h0+h1 --vis no --data_is_split no --load_graph no

# # feathercoin
# python -m mains.main_correspondence_ntwrk --seed 42 --currency feathercoin --heuristic h0 --vis no --data_is_split no --load_graph no
# python -m mains.main_correspondence_ntwrk --seed 42 --currency feathercoin --heuristic h0+h1 --vis no --data_is_split no --load_graph no

