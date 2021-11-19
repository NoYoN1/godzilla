# 2021-10-10
#
# 卒業作品
#
from re import template
from flask import Flask
from flask import request
from flask import render_template
from flask import Markup
# import web_data
import static.javaScript
import py.EdgeStudy as EdgeStudy
app = Flask(__name__)


@app.route('/',)
def index():

    return (render_template('index.html'))

# @app.route('/')
# def my_form():
#     return (render_template('index.html', web_data=web_data))


# @app.route('/', methods=['POST'])
# def my_form_post():
#     text1 = request.form['text1']
#     text2 = request.form['text2']
#     if text1 == text2:
#         return "<h1>文字列は同じです !</h1>"
#     elif text1 == "" or text2 == "":
#         return "<h1>Insert the text</h1>"
#     else:
#         return "<h1>文字列は違います !</h1>"


# @app.route('/object', )
# def print_object_data():
#     # return str(web_data.p1.name) + " is " + str(web_data.p1.age) + " years old"

#     # for i in web_data.m:
#     #     return str(i.name)

#     return render_template('object.html', web_data=web_data)


# @app.route('/risk',)
# def print_trade():

#     return (render_template('/risk/risk.html'))


@app.route('/#risk-management', methods=["GET", "POST"])
def riskmanagement():
    if request.method == "POST":
        # getting input with name = initialCash in HTML form
        initialCash = request.form.get("initialCash", type=float)
        # getting input with name = tradesRequired in HTML form
        tradesRequired = request.form.get("tradesRequired", type=float)
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
    return (render_template('/risk/risk.html', initialCash=initialCash, tradesRequired=tradesRequired, riskPerTrade=riskPerTrade, profitRatio=profitRatio, winRatio=winRatio, final_result=final_result))


# labels = [
#     'JAN', 'FEB', 'MAR', 'APR',
#     'MAY', 'JUN', 'JUL', 'AUG',
#     'SEP', 'OCT', 'NOV', 'DEC'
# ]

# values = [
#     967.67, 1190.89, 1079.75, 1349.19,
#     2328.91, 2504.28, 2873.83, 4764.87,
#     4349.29, 6458.30, 9907, 16297
# ]

# colors = [
#     "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
#     "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
#     "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


# @ app.route('/bar')
# def bar():
#     bar_labels = labels
#     bar_values = values
#     return render_template('bar_chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=bar_labels, values=bar_values)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5550, debug=True)
