import pandas as pd
import numpy as np
from typing import Counter
from itertools import count

class Clustering:

    _ids=count(0)

    def __init__(self,h0,h1,df):
        self.h0=h0
        self.h1=h1
        self.df=df
        self.id = next(self._ids)

    def h0_and_h1(self):
        if (self.h0 == self.h1 == 1):
            return 1
        else: 
            return 0

    def h0_or_h1(self):
        if (self.h0 == 1):
            return 1
        
        elif (self.h1 == 1):
            return 1
        
        else:
            return 0
           
    def implement_clustering(self,segregated_iota):
        segregated_iota.loc[self.id,"h0 & h1"]=self.h0_and_h1()
        segregated_iota.loc[self.id,"h0 or h1"]=self.h0_or_h1()
        return  