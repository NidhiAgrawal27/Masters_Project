import pandas as pd

class PreProcessing:
    
    def __init__(self, df):
        self.df = df
    
    def drop_unnecessary_cols(self, col_to_drop):
        self.df.drop(col_to_drop, axis=1, inplace=True)
        
    def remove_nan_values(self, addrs_col, amt_col):
        print('\nTotal Num of transactions before dropping NaN:', self.df.shape[0])
        for col in addrs_col:
            # Since NaN values are stored as string 'nan', select rows without 'nan' values
            self.df = self.df[self.df[col].str.contains("\[nan|nan,|, nan|nan]") == False]
        for col in amt_col:
            self.df = self.df[self.df[col].str.contains("nan") == False]
            
        self.df.dropna(inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        print('Total Num of transactions after dropping NaN: {}\n'.format(self.df.shape[0]))

    def convert_string_to_list(self, convert_list_cols):
        for col in convert_list_cols:
            self.df[col] = self.df[col].apply(eval)

    def convert_to_datetime(self, datetime_cols):
        for col in datetime_cols:
            self.df[col] = pd.to_datetime(self.df[col]) # converting object to datetime type


# function to segregate input and output addresses pair wise
def segregate_ip_op_addrs(arg, temp_list):
    if arg.index[1] == 'input_addresses_x' and arg.index[3] == 'output_addresses_y':
        for i in range(len(arg[1])): # arg[1] is input_addresses_x in df
            for j in range(len(arg[3])): # arg[3] is output_addresses_y in df
                new_row = {
                            arg.index[0]: arg[0],
                            arg.index[1]: arg[1][i],
                            arg.index[2]: arg[2][i],
                            arg.index[3]: arg[3][j],
                            arg.index[4]: arg[4][j]
                        }
                if len(arg) > 5:
                    for row_length in range(5, len(arg)):
                        new_row[arg.index[row_length]] = arg[row_length]

                temp_list.append(new_row)
    else:
        print('ERROR: Incorrect column position for input_addresses_x and output_addresses_y.')
    return temp_list


def sum_amounts(_list):
    amount  = 0
    for amt in _list:
        amount += amt
    return round(amount,1)


def get_tx_id(addrs_id, df, col_name):
    return list(set(df[df[col_name]==addrs_id]['tx_unique_id']))


def get_id(_list, df, col_name, id_col_name):
    id_list = []
    for l in _list:      
        id_list.append(df[df[col_name]==l][id_col_name].values[0])
    return id_list

