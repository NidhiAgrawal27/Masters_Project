
# btc_sample unweighted
python -m mains.main_girvan_newmann_heuristic --seed 42 --currency btc_sample --heuristic h0 --weighted no
python -m mains.main_girvan_newmann_heuristic --seed 42 --currency btc_sample --heuristic h0_h1 --weighted no
python -m mains.main_plot_metrics --seed 42 --currency btc_sample --weighted no

# btc_sample weighted
python -m mains.main_girvan_newmann_heuristic --seed 42 --currency btc_sample --heuristic h0 --weighted yes
python -m mains.main_girvan_newmann_heuristic --seed 42 --currency btc_sample --heuristic h0_h1 --weighted yes
python -m mains.main_plot_metrics --seed 42 --currency btc_sample --weighted yes

