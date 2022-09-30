
# iota
python -m mains.main_correspondence_ntwrk --seed 42 --currency iota --heuristic h0 --vis yes
python -m mains.main_correspondence_ntwrk --seed 42 --currency iota --heuristic h0+h1 --vis yes
python -m mains.main_network_analysis --seed 42 --currency iota --heuristic h0
python -m mains.main_network_analysis --seed 42 --currency iota --heuristic h0+h1

# # btc_sample
# python -m mains.main_correspondence_ntwrk --seed 42 --currency btc_sample --heuristic h0 --vis yes
# python -m mains.main_correspondence_ntwrk --seed 42 --currency btc_sample --heuristic h0+h1 --vis yes
# python -m mains.main_network_analysis --seed 42 --currency btc_sample --heuristic h0
# python -m mains.main_network_analysis --seed 42 --currency btc_sample --heuristic h0+h1

# # btc_3GB_chunk
# python -m mains.main_split_correspondence_ntwrk --seed 42 --currency btc_3GB_chunk --heuristic h0 --vis no --chunksize 1000000
# python -m mains.main_split_correspondence_ntwrk --seed 42 --currency btc_3GB_chunk --heuristic h0+h1 --vis no --chunksize 1000000
# python -m mains.main_network_analysis --seed 42 --currency btc_3GB_chunk --heuristic h0
# python -m mains.main_network_analysis --seed 42 --currency btc_3GB_chunk --heuristic h0+h1

# # btc
# python -m mains.main_split_correspondence_ntwrk --seed 42 --currency btc --heuristic h0 --vis no --chunksize 1000000
# python -m mains.main_split_correspondence_ntwrk --seed 42 --currency btc --heuristic h0+h1 --vis no --chunksize 1000000
# python -m mains.main_network_analysis --seed 42 --currency btc --heuristic h0
# python -m mains.main_network_analysis --seed 42 --currency btc --heuristic h0+h1

# # cardano
# python -m mains.main_split_correspondence_ntwrk --seed 42 --currency cardano --heuristic h0 --vis no  --chunksize 1000000
# python -m mains.main_split_correspondence_ntwrk --seed 42 --currency cardano --heuristic h0+h1 --vis no  --chunksize 1000000
# python -m mains.main_network_analysis --seed 42 --currency cardano --heuristic h0
# python -m mains.main_network_analysis --seed 42 --currency cardano --heuristic h0+h1

# # monacoin
# python -m mains.main_correspondence_ntwrk --seed 42 --currency monacoin --heuristic h0 --vis no
# python -m mains.main_correspondence_ntwrk --seed 42 --currency monacoin --heuristic h0+h1 --vis no
# python -m mains.main_network_analysis --seed 42 --currency monacoin --heuristic h0
# python -m mains.main_network_analysis --seed 42 --currency monacoin --heuristic h0+h1

# # feathercoin
# python -m mains.main_correspondence_ntwrk --seed 42 --currency feathercoin --heuristic h0 --vis no
# python -m mains.main_correspondence_ntwrk --seed 42 --currency feathercoin --heuristic h0+h1 --vis no
# python -m mains.main_network_analysis --seed 42 --currency feathercoin --heuristic h0
# python -m mains.main_network_analysis --seed 42 --currency feathercoin --heuristic h0+h1


