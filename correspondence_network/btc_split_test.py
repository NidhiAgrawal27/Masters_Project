import datetime
import numpy as np
import csv
import pandas as pd



btc_2012 = pd.read_csv('/Users/miglekasetaite/Desktop/MP/BTC_TXS_2012.csv')
btc_df = pd.DataFrame(btc_2012)
btc_df['timestamp'] = pd.to_datetime(btc_df['timestamp'], unit = 's')


start_date = datetime.datetime(2012, 1, 1)

end_date = datetime.datetime(2012, 6, 30)
 
# delta time
delta = datetime.timedelta(days=14)
 
# iterate over range of dates
i = 0

while (start_date <= end_date):

    period_end = start_date + delta
    print(start_date, period_end, end="\n")
    btc_df_14 = btc_df[btc_df.timestamp.between(start_date,period_end)]
    file_name_output = f"btc_2012_{i}.csv"
    output_dir = '/Users/miglekasetaite/Desktop/MP/Github/Masters_Project/correspondence_network/data/btc_split/'
    output_path =  output_dir + file_name_output
    btc_df_14.to_csv(output_path, index=False)
    start_date = period_end
    i = i+1
    print(i)
    
