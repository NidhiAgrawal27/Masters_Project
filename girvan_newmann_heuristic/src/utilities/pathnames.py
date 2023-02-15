def pathnames(cur, heuristic, wt):

    local_dir = '../gn_logs/' 
    server_dir = '/local/scratch/correspondence_network/gn_logs/'
    ground_truth_path = '../data/ground_truth/btc_ground_truth.csv'

    # below: change local_dir or server_dir in dir_name for accessing local or server dir
    
    dir_name = local_dir + cur + '_logs/'+ wt +'/' + heuristic + '/'
    generated_files = local_dir + cur + '_logs/'+ wt +'/generated_files/'
    figure_dir = local_dir + cur + '_logs/'+ wt +'/figures/'
    
    # for data_path, pass server_data_path when running on server
    PATHNAMES = {
                    "figure_dir": figure_dir,
                    "generated_files": generated_files,
                    "logs_home_dir" : local_dir,
                    "ground_truth_path" : ground_truth_path
                }

    return PATHNAMES

