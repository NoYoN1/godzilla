# 2021-10-10
#
# 卒業作品
#
from re import S, template
from flask import Flask, url_for, redirect,  request, render_template
from pandas.io import json
from flask import Markup
import py_files.web_data
# import py.coin1 as coin
import py.EdgeStudy as EdgeStudy
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


@app.route('/',)
def index():

    return (render_template('index.html'))


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

        return (render_template('/risk/risk.html', title=title, initialCash=initialCash, tradesRequired=tradesRequired, riskPerTrade=riskPerTrade, profitRatio=profitRatio, winRatio=winRatio, final_result=final_result, chartData=chartData, dataRequired=dataRequired, finalCashMulti=finalCashMulti, finalMaxDDMulti=finalMaxDDMulti, fnLNetMulti=fnLNetMulti, StrikeRateMulti=StrikeRateMulti))
    return render_template('/index.html',)


@app.route('/chart')
def chart_html():

    return (render_template('/risk/chart.html', ))


@app.route('/st1')
def st1_html():

    return (render_template('/strategy/strategy1.html', ))


@app.route('/trade')
def trade_html():
    print(b)
    return (render_template('trade.html',))


@app.route("/r")
def reg():

    return (render_template('/user/register.html'))

##########################################


@app.route("/login")
def login():
    successful = "OK"
    unsuccessful = "ログイン失敗しました。ユーザーメール、パスワードを確認してください。"
    return render_template("index.html", us=unsuccessful)


@app.route("/signup")
def signup():
    return render_template("index.html")


@app.route("/welcome")
def welcome():
    if person["is_logged_in"] == True:
        return render_template("/expert/expert.html", email=person["email"], name=person["name"])
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
    success = "OK"
    unsuccess = "NO"
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
            return redirect(url_for('welcome'))
        except:
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5550, debug=True)
