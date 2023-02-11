#extracts the entities from the ent_df dataframe, takes less time than to compare with groundtruth, 
# takes input lists of addresses, returns dictionary in the form-> address: entity

def extract_entities(df, addresses): 
    result = {}
    for index, row in df.iterrows():
        for address in addresses:
            if address in row['addresses']:
                result[address] = row['entity'][row['addresses'].index(address)]
    return result
