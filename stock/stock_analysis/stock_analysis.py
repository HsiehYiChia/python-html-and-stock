from yahoo_finance import Share
from datetime import date, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import pandas_talib as ta
import sys
import os


df = pd.DataFrame()
with open("stock_list.txt", encoding = 'utf8') as f:
    content = f.read()
