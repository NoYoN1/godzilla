# 2021-10-10
# TUMUR UILS
# 卒業作品
#
from flask import Flask
from flask import request
from flask import render_template
from flask import Markup
import web_data
# import do_trade
import py.EdgeStudy as EdgeStudy
app = Flask(__name__)


@app.route('/')
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


@app.route('/object', )
def print_object_data():
    # return str(web_data.p1.name) + " is " + str(web_data.p1.age) + " years old"

    # for i in web_data.m:
    #     return str(i.name)

    return render_template('object.html', web_data=web_data)


@app.route('/trade',)
def print_trade():

    return (render_template('trade.html', EdgeStudy=EdgeStudy))


# @app.route('/test', )
# def print_test():

#     return render_template('test.html', do_trade=do_trade.aaa)

    # return str(do_trade.aaa)

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


@app.route('/bar')
def bar():
    bar_labels = labels
    bar_values = values
    return render_template('bar_chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=bar_labels, values=bar_values)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5500, debug=True)
