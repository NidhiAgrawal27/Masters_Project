import pandas as pd
import numpy as np
from typing import Counter
from itertools import count

class Heuristics:

    _ids=count(0)

    def __init__(self,input,output,address_data,raw_data):
        self.input=input
        self.output=output
        self.address_data=address_data
        self.raw_data=raw_data
        self.id = next(self._ids)
        # self.raw_data["id_input_addresses_x"]=self.raw_data["id_input_addresses_x"].apply(eval)
        # self.raw_data["id_output_addresses_y"]=self.raw_data["id_output_addresses_y"].apply(eval)
        # self.raw_data["input_amounts_x"]=self.raw_data["input_amounts_x"].apply(eval)
        # self.raw_data["output_amounts_y"]=self.raw_data["output_amounts_y"].apply(eval)
        
    def heuristic0(self):
        if (len(self.address_data[self.address_data["addresses_id"]==self.output]["addrs_in_ip_tx_id"])==0):
        #if output not in add_map_tx.keys():
            #segregated_iota.loc[((segregated_iota["id_input_addresses_x"]==input) & (segregated_iota["id_output_addresses_y"]==output)) | ((segregated_iota["id_input_addresses_x"]==output) & (segregated_iota["id_output_addresses_y"]==input)),"h0"]=0
            #df.loc[index,"wh0"]=0
            return 0
        else:
            if (len(set(self.address_data[self.address_data["addresses_id"]==self.input]["addrs_in_ip_tx_id"].item()).intersection(self.address_data[self.address_data["addresses_id"]==self.output]["addrs_in_ip_tx_id"].item()))!=0):
            #if (len(add_map_tx[input].intersection(add_map_tx[output]))!=0):
                #segregated_iota.loc[((segregated_iota["id_input_addresses_x"]==input) & (segregated_iota["id_output_addresses_y"]==output)) | ((segregated_iota["id_input_addresses_x"]==output) & (segregated_iota["id_output_addresses_y"]==input)),"h0"]=1
                #df.loc[index,"wh0"]=len(add_map_tx[input].intersection(add_map_tx[output]))
                return 1
            else:
                #segregated_iota.loc[((segregated_iota["id_input_addresses_x"]==input) & (segregated_iota["id_output_addresses_y"]==output)) | ((segregated_iota["id_input_addresses_x"]==output) & (segregated_iota["id_output_addresses_y"]==input)),"h0"]=0
                #df.loc[index,"wh0"]=0
                return 0

    def heuristic1(self):
        transaction_list=set(self.address_data[self.address_data["addresses_id"]==self.input]["addrs_in_ip_tx_id"].item()).intersection(self.address_data[self.address_data["addresses_id"]==self.output]["addrs_in_op_tx_id"].item())
        for transaction in transaction_list:
            #condition 1- (for a single input address), multiple output add---- output amount has to be less than all the input amounts.
            #if (len(tranId_to_inpadd[transaction])==1 and len(tranId_to_outadd[transaction])>1):
            if (len(self.raw_data[self.raw_data["tx_unique_id"]==transaction]["id_output_addresses_y"].item())>1 and len(self.raw_data[self.raw_data["tx_unique_id"]==transaction]["id_input_addresses_x"].item())>1):
                #if output amount is the smallest of all amounts and less than the smallest input amount
                if (self.output==(sorted(self.raw_data[self.raw_data["tx_unique_id"]==transaction]["output_amounts_y"].item())[0]) and self.output<(sorted(self.raw_data[self.raw_data["tx_unique_id"]==transaction]["input_amounts_x"].item())[0])):   #smaller than the least input amount    
                    #condition2- remove the output addresses which have same amounts listed two or more times in the output
                    if (Counter(self.raw_data[self.raw_data["tx_unique_id"]==transaction]["output_amounts_y"].item())[self.output]==1):
                        #segregated_iota.loc[((segregated_iota["id_input_addresses_x"]==self.input) & (segregated_iota["id_output_addresses_y"]==self.output)) | ((segregated_iota["id_input_addresses_x"]==self.output) & (segregated_iota["id_output_addresses_y"]==self.input)),"h1"]=1
                        return 1
                        #break
                    else:
                        return 0
                else:
                    #segregated_iota.loc[((segregated_iota["id_input_addresses_x"]==self.input) & (segregated_iota["id_output_addresses_y"]==self.output)) | ((segregated_iota["id_input_addresses_x"]==self.output) & (segregated_iota["id_output_addresses_y"]==self.input)),"h1"]=0
                    return 0
            else:
                #segregated_iota.loc[((segregated_iota["id_input_addresses_x"]==self.input) & (segregated_iota["id_output_addresses_y"]==self.output)) | ((segregated_iota["id_input_addresses_x"]==self.output) & (segregated_iota["id_output_addresses_y"]==self.input)),"h1"]=0
                return 0

    def implement_heuritsics(self,segregated_iota):
        segregated_iota.loc[self.id,"h0"]=self.heuristic0()
        segregated_iota.loc[self.id,"h1"]=self.heuristic1()
        return       

