import pandas as pd
import argparse
from utilities import utils
from heuristics import heuristics


CONFIG = {
    "processed_data":"../logs/generated_files/processed_data.csv",
    "addresses_data":"../logs/generated_files/unique_addresses.csv",
    "segregated_iota":"../logs/generated_files/segregated_iota.csv"
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    args = parser.parse_args()

    utils.set_seed(args.seed)

    processed_data=pd.read_csv(CONFIG["processed_data"])
    addresses_data=pd.read_csv(CONFIG["addresses_data"])
    segregated_iota=pd.read_csv(CONFIG["segregated_iota"])

    #only reading necessary data
    processed_data=processed_data[["tx_unique_id","id_input_addresses_x","id_output_addresses_y","input_amounts_x","output_amounts_y"]]

    #converting string to lists
    processed_data["id_input_addresses_x"]=processed_data["id_input_addresses_x"].apply(eval)
    processed_data["id_output_addresses_y"]=processed_data["id_output_addresses_y"].apply(eval)
    processed_data["input_amounts_x"]=processed_data["input_amounts_x"].apply(eval)
    processed_data["output_amounts_y"]=processed_data["output_amounts_y"].apply(eval)

    addresses_data["addrs_in_ip_tx_id"]=addresses_data["addrs_in_ip_tx_id"].apply(eval)
    addresses_data["addrs_in_op_tx_id"]=addresses_data["addrs_in_op_tx_id"].apply(eval)

    #applying the heuristics to the segregated data file
    segregated_iota.apply(lambda x: heuristics.Heuristics(x.id_input_addresses_x, x.id_output_addresses_y,addresses_data,processed_data).implement_heuritsics(segregated_iota), axis=1)
    
    segregated_iota['h0'] = segregated_iota['h0'].astype(int)
    segregated_iota['h1'] = segregated_iota['h1'].astype(int)
    segregated_iota.to_csv(CONFIG["segregated_iota"], index=False)

    # Generate new file for heuristics only
    heuristics_df = pd.DataFrame()
    heuristics_df['id_input_addresses_x'] = segregated_iota['id_input_addresses_x']
    heuristics_df['id_output_addresses_y'] = segregated_iota['id_output_addresses_y']
    heuristics_df['h0'] = segregated_iota['h0']
    heuristics_df['h1'] = segregated_iota['h1']
    heuristics_df.drop_duplicates(inplace=True)
    heuristics_df.to_csv("../logs/generated_files/heuristics.csv", index=False)

    print("Heuristics 0 and 1 completed.\n")
    print('h0 value counts:\n', heuristics_df["h0"].value_counts())
    print('\n\nh1 value counts:\n', heuristics_df["h1"].value_counts(), '\n\n')



if __name__ == "__main__":
    main()