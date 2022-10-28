import pandas as pd

class PreProcessing:
    
    def __init__(self, df):
        self.df = df
    

    def drop_unnecessary_cols(self, cur, col):

        if 'btc' in cur: col_to_drop = ['block_index', 'timestamp']
        elif 'iota' in cur: col_to_drop = ['message_id', 'milestone_index', 'datetime']
        elif 'cardano' in cur: col_to_drop = ['block_index', 'timestamp']
        elif 'feathercoin' in cur: col_to_drop = ['block_index', 'timestamp']
        elif 'monacoin' in cur: col_to_drop = ['block_index', 'timestamp']
        elif 'iota_split' in cur: col_to_drop = ['message_id', 'milestone_index', 'datetime', 'scraped']


        if col != []:
            col_to_drop.extend(col)

        self.df.drop(col_to_drop, axis=1, inplace=True)

        
    def remove_nan_values(self, addrs_col, amt_col):
        # print('\nTotal Num of transactions before dropping NaN:', self.df.shape[0])
        for col in addrs_col:
            # Since NaN values are stored as string 'nan', select rows without 'nan' values
            self.df = self.df[self.df[col].str.contains("\[nan|nan,|, nan|nan]") == False]
        for col in amt_col:
            self.df = self.df[self.df[col].str.contains("nan") == False]
            
        self.df.dropna(inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        # print('Total Num of transactions after dropping NaN: {}\n'.format(self.df.shape[0]))


    def unique_tx_id(self, file_path):
        # Replace alphanumeric tx id with unique numeric ids
        df_unique_tx_id = pd.DataFrame()
        df_unique_tx_id['transaction_id'] = pd.unique(self.df[['transaction_id']].values.ravel())
        df_unique_tx_id['tx_unique_id'] = df_unique_tx_id.index
        df_unique_tx_id.to_csv(file_path + 'transaction_ids.csv', index=False)

        self.df = self.df.merge(df_unique_tx_id, on='transaction_id', how='left')
        self.df.drop(['transaction_id'], axis=1, inplace=True)
        

    def unique_tx_id_for_split_data(self, df_tx_ids):
            # Replace alphanumeric tx id with unique numeric ids
            df_unique_tx_id = pd.DataFrame()
            df_unique_tx_id['transaction_id'] = pd.unique(self.df[['transaction_id']].values.ravel())

            df_tx_ids = pd.concat([df_tx_ids, df_unique_tx_id])
            df_tx_ids.reset_index(drop=True, inplace=True)
            df_tx_ids['tx_unique_id'] = df_tx_ids.index
            
            df_unique_tx_id = df_unique_tx_id.merge(df_tx_ids, on='transaction_id')

            self.df = self.df.merge(df_unique_tx_id, on='transaction_id', how='left')
            self.df.drop(['transaction_id'], axis=1, inplace=True)

            return df_tx_ids
            



