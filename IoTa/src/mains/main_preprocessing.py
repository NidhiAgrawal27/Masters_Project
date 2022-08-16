import pandas as pd
import argparse
import pathlib
from utilities import utils, preprocessing


CONFIG = {
    "data_path": "../data/first_14_days_UTXO_txs_of_IOTA.csv",
    # "data_path": "../data/sample_data.csv",
    "figure_dir": "../logs/figures/",
    "generated_files": "../logs/generated_files/"
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    args = parser.parse_args()

    utils.set_seed(args.seed)

    # Cleaning and preprocessing the data
    df = pd.read_csv(CONFIG['data_path'])
    preprocess = preprocessing.PreProcessing(df)
    preprocess.drop_unnecessary_cols(col_to_drop = ['message_id', 'milestone_index'])
    preprocess.remove_nan_values(addrs_col = ['input_addresses_x', 'output_addresses_y'], amt_col = ['input_amounts_x', 'output_amounts_y'])
    preprocess.convert_string_to_list(convert_list_cols = ['input_addresses_x', 'input_amounts_x', 'output_addresses_y', 'output_amounts_y'])
    preprocess.convert_to_datetime(datetime_cols=['datetime'])

    preprocess.df['num_input_addresses'] = pd.Series(len(_list) for _list in preprocess.df['input_addresses_x'])
    preprocess.df['num_output_addresses'] = pd.Series(len(_list) for _list in preprocess.df['output_addresses_y'])
    preprocess.df['sum_input_amounts'] = pd.Series(preprocessing.sum_amounts(_list) for _list in preprocess.df['input_amounts_x'])
    preprocess.df['sum_output_amounts'] = pd.Series(preprocessing.sum_amounts(_list) for _list in preprocess.df['output_amounts_y'])
    preprocess.df['sum_input_amounts'] = preprocess.df['sum_input_amounts'].astype(float)
    preprocess.df['sum_output_amounts'] = preprocess.df['sum_output_amounts'].astype(float)

    # Create 'generated_files' directory if it does not exist.
    pathlib.Path(CONFIG["generated_files"]).mkdir(parents=True, exist_ok=True)

    # preprocess.df.to_csv(CONFIG['generated_files'] + "processed_data.csv", index=False)

    # Generate a new file with unique transaction ids and assign them unique numbers
    df_unique_tx_id = pd.DataFrame()
    df_unique_tx_id['transaction_id'] = pd.unique(preprocess.df[['transaction_id']].values.ravel())
    df_unique_tx_id['tx_unique_id'] = df_unique_tx_id.index
    df_unique_tx_id.to_csv(CONFIG['generated_files'] + 'transaction_id.csv', index=False)

    # Segregate input and output addresses pair wise
    temp_list = []
    preprocess.df.apply(preprocessing.segregate_ip_op_addrs, axis=1, temp_list = temp_list)
    segregated_df = pd.DataFrame([pd.Series(row) for row in temp_list])

    # Generate a new df with unique input and output addresses and assign them ids
    df_unique_addrs = pd.DataFrame()
    df_unique_addrs['addresses'] = pd.unique(segregated_df[['input_addresses_x', 'output_addresses_y']].values.ravel())
    df_unique_addrs['addresses_id'] = df_unique_addrs.index

    # Adding id corresponding to input addresses in segregated df
    df_unique_addrs.rename(columns={'addresses': 'input_addresses_x'}, inplace=True)
    segregated_df = pd.merge(segregated_df, df_unique_addrs, on='input_addresses_x', how='left')
    segregated_df.rename(columns={'addresses_id': 'id_input_addresses_x'}, inplace=True)
    segregated_df.dropna(inplace=True)

    # Adding id corresponding to output addresses in segregated df
    df_unique_addrs.rename(columns={'input_addresses_x': 'output_addresses_y'}, inplace=True)
    segregated_df = pd.merge(segregated_df, df_unique_addrs, on='output_addresses_y', how='left')
    segregated_df.rename(columns={'addresses_id': 'id_output_addresses_y'}, inplace=True)
    segregated_df.dropna(inplace=True)

    # Adding id corresponding to transaction_id in segregated df
    segregated_df = pd.merge(segregated_df, df_unique_tx_id, on='transaction_id', how='left')
    segregated_df.rename(columns={'id': 'tx_unique_id'}, inplace=True)
    segregated_df.dropna(inplace=True)

    # Rearrange transaction_unique_id column in segregated_df
    column_to_move = segregated_df.pop("tx_unique_id")
    segregated_df.insert(0, "tx_unique_id", column_to_move)
    segregated_df.drop(['transaction_id'], axis=1, inplace=True)

    # Rearrange id_input_addresses_x column in segregated_df
    column_to_move = segregated_df.pop("id_input_addresses_x")
    segregated_df.insert(1, "id_input_addresses_x", column_to_move)
    segregated_df.drop(['input_addresses_x'], axis=1, inplace=True)

    # Rearrange id_output_addresses_y column in segregated_df
    column_to_move = segregated_df.pop("id_output_addresses_y")
    segregated_df.insert(2, "id_output_addresses_y", column_to_move)
    segregated_df.drop(['output_addresses_y'], axis=1, inplace=True)

    # Generate a new file with unique input and output addresses, their ids and 
    # corresponding transactions where these addresses are input addresses and outputs addresses
    df_unique_addrs.rename(columns={'output_addresses_y': 'addresses'}, inplace=True)
    df_unique_addrs['addrs_in_ip_tx_id'] = df_unique_addrs['addresses_id'].apply(preprocessing.get_tx_id, df = segregated_df, col_name = 'id_input_addresses_x')
    df_unique_addrs['addrs_in_op_tx_id'] = df_unique_addrs['addresses_id'].apply(preprocessing.get_tx_id, df = segregated_df, col_name = 'id_output_addresses_y')
    
    df_unique_addrs.to_csv(CONFIG['generated_files'] + 'unique_addresses.csv', index=False)
    print('\n\nUNIQUE ADDRESSES DF:')
    print(df_unique_addrs.info())

    preprocess.df['id_input_addresses_x'] = pd.Series(preprocessing.get_id(_list, df_unique_addrs, 'addresses', 'addresses_id') for _list in preprocess.df['input_addresses_x'])
    preprocess.df['id_output_addresses_y'] = pd.Series(preprocessing.get_id(_list, df_unique_addrs, 'addresses', 'addresses_id') for _list in preprocess.df['output_addresses_y'])
    preprocess.df['tx_unique_id'] = df_unique_tx_id[df_unique_tx_id['transaction_id']==preprocess.df['transaction_id']]['tx_unique_id']
    
    print('\nPROCESSED DF:')
    print(preprocess.df.info())
    preprocess.df.to_csv(CONFIG['generated_files'] + "processed_data.csv", index=False)

    # Remove rows where ip and op addresses are exactly same
    index_names = segregated_df[(segregated_df['id_input_addresses_x'] == segregated_df['id_output_addresses_y'])].index
    segregated_df.drop(index_names, inplace = True)
    segregated_df.drop_duplicates(inplace=True)

    # Get count of same tuple (ip adrs, op adrs) in segregated df
    segregated_df['count_repeat_pair'] = segregated_df.groupby(['id_input_addresses_x', 'id_output_addresses_y'])['id_input_addresses_x'].transform('count')

    segregated_df.reset_index(drop=True)
    segregated_df.to_csv(CONFIG['generated_files'] + 'segregated_iota.csv', index=False)
    print('\n\nSEGREGATED IP & OP ADDRESSES DF:')
    print(segregated_df.info())


if __name__ == "__main__":
    main()

