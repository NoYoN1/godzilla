# 2021-10-10
#
# 卒業作品
#
from re import template
from flask import Flask
from flask import request
from flask import render_template
from flask import Markup
import py_files.web_data
import py.coin1 as coin
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
        # set value EdgeStudy.py
        result = EdgeStudy.Simulate(initialCash, tradesRequired,
                                    riskPerTrade, profitRatio, winRatio)
        result.next(initialCash)
        # result.printFinal()
        final_result = result.printFinal()
        # return result
        chart = result.printTrade(0)[1]
        chart1 = result.printTrade(0)
        riskmanagement.chart = chart
        return (render_template('/risk/risk.html', initialCash=initialCash, tradesRequired=tradesRequired, riskPerTrade=riskPerTrade, profitRatio=profitRatio, winRatio=winRatio, final_result=final_result, chart=chart, chart1=chart1))
    return render_template('/index.html',)


@app.route('/chart')
def chart_html():
    chartData = riskmanagement.chart
    return (render_template('/risk/chart.html', chartData=chartData))


@app.route('/trade')
def trade_html():
    b = coin.js
    print(b)
    return (render_template('trade.html', b=b))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5550, debug=True)
