
# 2021-10-10
# FX,backtest シミュレーションシステム
# Godzilla trade strategy
# team G
# 卒業作品
# TUMUR UILS

from flask import Flask, url_for, redirect, request, render_template, session
import pandas as pd
from pandas.io import json
import py_files.web_data
# import py.coin1 as coin
import backtrader as bt
import py.EdgeStudy as EdgeStudy
import strategy.FxDoji_SRSI_1 as FxDoji_SRSI_1
import strategy.FxMA_Crossover as MA

import strategy.FxDojiSRSI as FxDojiSRSI
# pip install pyrebase4
import pyrebase
app = Flask(__name__)

config = {
    "apiKey": "AIzaSyA5V_y6bCGDO3NxY5sZG1SHVtVFSUiBKKc",
    "authDomain": "flask-d69f2.firebaseapp.com",
    "databaseURL": "https://flask-d69f2-default-rtdb.firebaseio.com",
    "projectId": "flask-d69f2",
    "storageBucket": "flask-d69f2.appspot.com",
    "messagingSenderId": "848651798514",
    "appId": "1:848651798514:web:c010d2af7878cdc2714d6b"

}

# initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

show_result_Data = {0: 0}
show_result_data_paid = {0: 0}

initialCash = 10000
riskPerTrade = 0.01
StopLossATR = 2
TakeProfitATR = 4
dojiValue = 20
RSIvalueUpper = 0.8
RSIvalueLower = 0.2
result = FxDoji_SRSI_1.Simulate(initialCash, riskPerTrade, StopLossATR, TakeProfitATR,
                                dojiValue, RSIvalueUpper, RSIvalueLower)
final_result = result.printFinal()


@app.route('/', methods=["GET", "POST"])
def index():
    show_result_Data = {0: 0}
    jsr = json.dumps(show_result_Data)
    file = open('static/json/show_result_Data.json', 'w')
    file.write(jsr)
    file.close()

    return render_template('index.html')

    # return (render_template('index.html'))


@app.route('/test')
def my_form():
    data = {'username': 'Pang', 'site': 'stackoverflow.com'}
    return (render_template('test.html', data=data))


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
        finalCashMulti = getMultiChartData[1]
        fnLNetMulti = getMultiChartData[2]
        StrikeRateMulti = getMultiChartData[3]
        finalMaxDDMulti = getMultiChartData[4]

        if 1 != dataRequired:
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
        else:
            data = []
            for i in range(1):
                data = {i: chartData, }
            js = json.dumps(data)
            file = open('static/json/chartMulti.json', 'w')
            file.write(js)
            file.close()

        return (render_template('/risk/risk.html',
                                title=title, initialCash=initialCash, tradesRequired=tradesRequired,
                                riskPerTrade=riskPerTrade, profitRatio=profitRatio, winRatio=winRatio,
                                final_result=final_result, chartData=chartData, dataRequired=dataRequired,
                                finalCashMulti=finalCashMulti, finalMaxDDMulti=finalMaxDDMulti, fnLNetMulti=fnLNetMulti,
                                StrikeRateMulti=StrikeRateMulti))
    return render_template('/index.html',)


@app.route('/chart')
def chart_html():

    return (render_template('/risk/chart.html', ))


####################################################################################


@app.route("/login")
def login():

    unsuccessful = "ログイン失敗しました。ユーザーメール、パスワードを確認してください。"
    return render_template("index.html", unsuccessful=unsuccessful)


@app.route("/logout")
def logout():
    person["is_logged_in"] = False

    return redirect(url_for("index"))


@app.route("/signup")
def signup():
    if person["is_logged_in"] == True:
        successful = "登録完了しました。ログイン画面にログインしてください。"
        return render_template("index.html", successful=successful)


@app.route("/welcome")
def welcome():

    show_result_data_paid = {0: 0}
    jsr = json.dumps(show_result_data_paid)
    file = open('static/json/show_result_data_paid.json', 'w')
    file.write(jsr)
    file.close()

    if person["is_logged_in"] == True:

        return render_template("/expert/expert.html", email=person["email"], name=person["name"], final_result=final_result)
    else:
        return redirect(url_for('login'))


##login##
@app.route("/result", methods=["POST", "GET"])
def result():

    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["pass"]

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            return redirect(url_for('welcome'))
        except:
            return redirect(url_for('login'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        try:
            auth.create_user_with_email_and_password(email, password)
            user = auth.sign_in_with_email_and_password(email, password)
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            data = {"name": name, "email": email}
            db.child("users").child(person["uid"]).set(data)
            return redirect(url_for('signup'))
        except:
            return redirect(url_for('index'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('signup'))
        else:
            return redirect(url_for('index'))
####################################################################################


@app.route("/e_strategy", methods=["POST", "GET"])
def paid_strategy():
    clicked = False
    if request.method == "POST":
        person["is_logged_in"] = True
        clicked = True
        # initialCash = request.form["initialCash"]
        initialCash = request.form.get("initialCash", type=int)
        riskPerTrade = request.form.get("riskPerTrade", type=float)

        dojiValue = request.form.get("dojiValue", type=float)
        RSIvalueUpper = request.form.get("RSIvalueUpper", type=float)
        RSIvalueLower = request.form.get("RSIvalueLower", type=float)

        ma20Value = request.form.get("ma20Value", type=float)
        ma50Value = request.form.get("ma50Value", type=float)

        StopLossATR = request.form.get("StopLossATR", type=float)
        TakeProfitATR = request.form.get("TakeProfitATR", type=float)
    else:
        clicked = False
        # temp2.Simulate(initialCash)
    result = FxDoji_SRSI_1.Simulate(initialCash, riskPerTrade, StopLossATR, TakeProfitATR,
                                    dojiValue, RSIvalueUpper, RSIvalueLower)

    final_result = result.printFinal()

    show_result_data_paid = {0: 1}
    jsr = json.dumps(show_result_data_paid)
    file = open('static/json/show_result_data_paid.json', 'w')
    file.write(jsr)
    file.close()
    return render_template("/expert/expert.html",
                           clicked=clicked, initialCash=initialCash, TakeProfitATR=TakeProfitATR,
                           StopLossATR=StopLossATR, riskPerTrade=riskPerTrade, dojiValue=dojiValue,
                           RSIvalueUpper=RSIvalueUpper, RSIvalueLower=RSIvalueLower,
                           final_result=final_result)


@app.route("/strategy1")
def strategy():
    return render_template("strategy/strategy.html")
    # strategy(check, finalResult, setCash, finalValue, finalCash)
    # check, finalResult, setCash, finalValue, finalCash
    # finalResult=finalResult, setCash=setCash, finalValue=finalValue, finalCash=finalCash, check=check


@app.route("/strategy", methods=["POST", "GET"])
def normal_strategy_result():

    # if request.method == "POST":
    if request.method == "POST":
        check = True
        strategy_result = FxDojiSRSI
        firstStrat = strategy_result.firstStrat
        analyzer = firstStrat.analyzers.ta.get_analysis()
        finalResult = strategy_result.printTradeAnalysis(analyzer)
        setCash = strategy_result.setCash
        finalValue = strategy_result.finalValue
        finalCash = strategy_result.finalCash
        # strategy(check, finalResult, setCash, finalValue, finalCash)
        # Since the headers are missing in the csv file, explicitly passing the field names in the program
        csv_file = pd.DataFrame(pd.read_csv("datas/EURUSD_D1.csv", sep=",", names=[
                                "time", "open", "high", "low", "close", "volume"], index_col=False))
        csv_file.to_json("static/json/EURUSD_D1.json", orient="records", date_format="epoch",
                         double_precision=10, force_ascii=True, date_unit="ms", default_handler=None)
        show_result_Data = {0: 1}
        jsr = json.dumps(show_result_Data)
        file = open('static/json/show_result_Data.json', 'w')
        file.write(jsr)
        file.close()
        return render_template("index.html", finalResult=finalResult, setCash=setCash, finalValue=finalValue, finalCash=finalCash, check=check)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5550, debug=True)
