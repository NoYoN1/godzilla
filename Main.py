# 2021-10-10
#
# 卒業作品
#
from re import S, template
from flask import Flask
from pandas.io import json
from flask import request
from flask import render_template
from flask import Markup
import py_files.web_data
# import py.coin1 as coin
import py.EdgeStudy as EdgeStudy
app = Flask(__name__)


@app.route('/',)
def index():

    return (render_template('index.html'))


@app.route('/test')
def my_form():

    return (render_template('test.html'))


# @app.route('/object', )
# def print_object_data():
#     # return str(web_data.p1.name) + " is " + str(web_data.p1.age) + " years old"

#     # for i in web_data.m:
#     #     return str(i.name)

#     return render_template('object.html', web_data=web_data)


@app.route('/risk-management', methods=["GET", "POST"])
def riskmanagement():
    if request.method == "POST":
        title = "GODZILLA TRADE STRATEGY"
        # getting input with name = initialCash in HTML form
        initialCash = request.form.get("initialCash", type=float)
        # getting input with name = tradesRequired in HTML form
        tradesRequired = request.form.get("tradesRequired", type=int)
        # getting input with name = riskPerTrade in HTML form
        riskPerTrade = request.form.get("riskPerTrade", type=float)
        # getting input with name = profitRatio in HTML form
        profitRatio = request.form.get("profitRatio", type=float)
        # getting input with name = winRatio in HTML form
        winRatio = request.form.get("winRatio", type=float)
        # getting input with name = dataRequired in HTML form
        dataRequired = request.form.get("dataRequired", type=int)

        # set value EdgeStudy.py
        result = EdgeStudy.Simulate(initialCash, tradesRequired,
                                    riskPerTrade, profitRatio, winRatio)
        getMultiChartData = result.multiple(initialCash, tradesRequired,
                                            riskPerTrade, profitRatio, winRatio)

        final_result = result.printFinal()
        # get single data
        chartData = result.printTrade(0)[1]
        # get multi data result

        # mm = [*range(1, 6, 1)]
        # for m in range(1, 5):
        #     mm = getMultiChartData

        # get multi data
        dataMulti = {}
        for k in range(dataRequired):
            for v in getMultiChartData[0]:
                dataMulti[k] = v
                getMultiChartData[0].remove(v)
                break
        jsMulti = json.dumps(dataMulti)
        file = open('static/json/chartMulti.json', 'w')
        file.write(jsMulti)
        file.close()

        # data = []
        # for i in range(1):
        #     data = {i: chartData, }
        # js = json.dumps(data)
        # file = open('static/json/chart.json', 'w')
        # file.write(js)
        # file.close()

        return (render_template('/risk/risk.html', title=title, initialCash=initialCash, tradesRequired=tradesRequired, riskPerTrade=riskPerTrade, profitRatio=profitRatio, winRatio=winRatio, final_result=final_result, chartData=chartData))
    return render_template('/index.html',)


@ app.route('/chart')
def chart_html():

    return (render_template('/risk/chart.html', ))


@ app.route('/trade')
def trade_html():
    print(b)
    return (render_template('trade.html',))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5550, debug=True)
