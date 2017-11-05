
# coding: utf-8

# In[112]:


import os
import numpy as np
import pandas as pd
import pickle
import quandl
from datetime import datetime

import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff

py.init_notebook_mode(connected = True)

def get_quandl_data(quandl_id):
    cache_path = '{}.pkl'.format(quandl_id).replace('/','-')
    try:
        f = open(cache_path,'rb')
        df = pickle.load(f)
        print('Loaded {} from cache'.format(quandl_id))
    except:
        print('Downloading {} from Quandl'.format(quandl_id))
        df = quandl.get(quandl_id,returns ="pandas")
        df.to_pickle(cache_path)
        print('Cached {} at {}'.format(quandl_id, cache_path))
    return df
def merge_dfs_oncolumn(dataframes,labels,cols):
    series_dict = {}
    for index in range(len(dataframes)):
        series_dict[labels[index]] = dataframes[index][col]
    return pd.DataFrame(series_dict)

exchanges = ['COINBASE','BITSTAMP','ITBIT','KRAKEN']

exchange_data = {}

for exchange in exchanges:
    exchange_code = 'BCHARTS/{}USD'.format(exchange)
    btc_exchange_df = get_quandl_data(exchange_code)
    exchange_data[exchange] = btc_exchange_df
   
columns = ['Open','High','Low', 'Close','Volume (BTC)', 'Volume (Currency)','Weighted Price']
single_var_dataframe = {}
final_frame = pd.DataFrame()

for col in columns:
    single_var_dataframe[col]=merge_dfs_oncolumn(list(exchange_data.values()), list(exchange_data.keys()),col)
    single_var_dataframe[col].replace(0,np.nan,inplace = True)
    single_var_dataframe[col]["Avg {}".format(col)] = single_var_dataframe[col].mean(axis=1)
    for exchange in exchanges:
        del single_var_dataframe[col][exchange]
for i in range(len(columns)):
    if (i==0):
        final_frame = single_var_dataframe[columns[i]]
    else:
        final_frame = final_frame.join(single_var_dataframe[columns[i]])
print(final_frame)   

