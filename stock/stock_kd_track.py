from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data
import numpy as np
import pandas as pd
from pandas import DataFrame
import talib as ta

def Get_kd(data):
    indicators={}
    # calculate KD
    indicators['k'],indicators['d']=ta.STOCH(np.array(data['High']),np.array(data['Low']),np.array(data['Close']),fastk_period=9,slowk_period=3,slowk_matype=0,slowd_period=3,slowd_matype=0)
    indicators=pd.DataFrame(indicators)
    return indicators


# Dow Jones
param = {
	'q': "0050.TW", # Stock symbol (ex: "AAPL")
	'i': "86400", # Interval size in seconds ("86400" = 1 day intervals)
	#'x': "TWSE", # Stock exchange symbol on which stock is traded (ex: "NASD")
	'p': "1Y" # Period (Ex: "1Y" = 1 year)
}

# get price data (return pandas dataframe)
price_df = get_price_data(param)
kd = Get_kd(price_df)
print (kd)







