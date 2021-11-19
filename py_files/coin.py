#Raw Package
from os import name
from re import X
from threading import setprofile
import numpy as np
import pandas as pd
import time
#Data Source
import yfinance as yf
from yfinance import ticker

list={1:'JPY=X', 2:'TWD=X', 3:'EURUSD=X',4:'USDCAD=X'}

for x in list:
    data = yf.download(list[x],period='1m')
    print(data["Open"].values,data["Low"].values
        ,data["Close"].values,data["Adj Close"].values
        ,data["Volume"].values)