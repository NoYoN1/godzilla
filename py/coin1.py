from pandas.io import json
import yfinance as yf
temp_all = {}
list = {0: 'JPY=X'}
for i in list:
    data = yf.download(list[i], period='1m')
    val = {"name": list[i], "value": data.values[0]}
    temp_all.update(val)
    js = json.dumps(temp_all)
# print(js)
# print(data)
# file = open('static/json/b.json', 'w')
# file.write(js)
# file.close()
