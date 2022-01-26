from multiprocessing import Value
from pandas.io import json
import yfinance as yf
temp_all = {}
temp_final = {}
list = {0: 'JPY=X', 1: 'EURUSD=X', 2: 'GBPUSD=X', 3: 'AUDUSD=X', 4: 'NZDUSD=X', 5: 'EURJPY=X',
        6: 'GBPJPY=X', 7: 'EURGBP=X', 8: 'EURCAD=X', 9: 'EURSEK=X', 10: 'EURCHF=X', 11: 'EURHUF=X',
        12: 'EURJPY=X', 13: 'CNY=X', 14: 'HKD=X', 15: 'SGD=X', 16: 'INR=X', 17: 'MXN=X',
        18: 'PHP=X', 19: 'IDR=X', 20: 'MYR=X', 21: 'ZAR=X', 22: 'RUB=X', 23: 'TWDJPY=X',
        24: 'TWDUSD=X'
        }
for i in list:
    data = yf.download(list[i], period='1m')
    val = {
        i: {"name": list[i],
            "value": data.values[0]
            }
    }
    temp_all.update(val)
    js = json.dumps(val)
    file = open('static/json/a.json', 'a')
    file.write(js)
    file.close()

temp_final = {"text": temp_all}
js = json.dumps(temp_final)
file = open('static/json/b.json', 'w')
file.write(js)
file.close()
