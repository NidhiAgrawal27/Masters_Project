import pandas as pd
import argparse
import pathlib
from utilities import utils, preprocessing


CONFIG = {
    "data_path": "../data/first_14_days_UTXO_txs_of_IOTA.csv",
    "figure_dir": "../logs/figures/",
    "generated_files": "../logs/generated_files/"
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    args = parser.parse_args()

    utils.set_seed(args.seed)

    df = pd.read_csv(CONFIG['data_path'])
    preprocess = preprocessing.PreProcessing(df)
    preprocess.drop_unnecessary_cols(col_to_drop = ['message_id', 'milestone_index'])
    preprocess.remove_nan_values(addrs_col = ['input_addresses_x', 'output_addresses_y'], amt_col = ['input_amounts_x', 'output_amounts_y'])
    preprocess.convert_list_to_string(convert_list_cols = ['input_addresses_x', 'input_amounts_x', 'output_addresses_y', 'output_amounts_y'])
    preprocess.convert_to_datetime(datetime_cols=['datetime'])

    # Create 'generated_files' directory if it does not exist.
    pathlib.Path(CONFIG["generated_files"]).mkdir(parents=True, exist_ok=True)

    preprocess.df.to_csv(CONFIG['generated_files'] + "processed_data.csv", index=False)

    # Segregate input and output addresses pair wise
    temp_list = []
    preprocess.df.apply(preprocessing.segregate_ip_op_addrs, axis=1, temp_list = temp_list)
    segregated_df = pd.DataFrame([pd.Series(row) for row in temp_list])
    segregated_df.to_csv(CONFIG['generated_files'] + 'segregated_df.csv', index=False)

    # Generate a new file with unique input and output addresses and assign them ids
    df_unique_addrs = pd.DataFrame()
    df_unique_addrs['addresses'] = pd.unique(segregated_df[['input_addresses_x', 'output_addresses_y']].values.ravel())
    df_unique_addrs['id'] = df_unique_addrs.index
    df_unique_addrs.to_csv(CONFIG['generated_files'] + 'unique_addresses.csv', index=False)


if __name__ == "__main__":
    main()

