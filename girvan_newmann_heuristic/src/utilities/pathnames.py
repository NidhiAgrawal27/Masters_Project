def pathnames(cur, heuristic, weighted):

    local_dir = '../gn_logs/' 
    server_dir = '/local/scratch/correspondence_network/gn_logs/'
    data_path = '../data/'
    ground_truth_path = data_path + 'ground_truth/btc_ground_truth.csv'

    # below: change local_dir or server_dir in dir_name for accessing local or server dir
    if weighted == 'no': 
        dir_name = local_dir + cur + '_logs/unweighted/' + heuristic + '/'
        figure_dir = local_dir + cur + '_logs/unweighted/figures/'
    else: 
        dir_name = local_dir + cur + '_logs/weighted/' + heuristic + '/'
        figure_dir = local_dir + cur + '_logs/weighted/figures/'
    
    PATHNAMES = {
                    "figure_dir": figure_dir,
                    "generated_files": dir_name + "generated_files/",
                    "logs_home_dir" : local_dir,
                    "data_path" : data_path,
                    "ground_truth_path" : ground_truth_path
                }

    return PATHNAMES

