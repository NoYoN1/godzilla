# 2021-10-10
# TUMUR UILS
# 卒業作品
#
from flask import Flask
from flask import request
from flask import render_template
# import web_data
# import do_trade
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


# @app.route('/object', )
# def print_object_data():
#     # return str(web_data.p1.name) + " is " + str(web_data.p1.age) + " years old"

#     # for i in web_data.m:
#     #     return str(i.name)

#     return render_template('object.html', web_data=web_data)


# @app.route('/trade', )
# def print_trade():

#     return render_template('trade.html', do_trade=do_trade)


# @app.route('/test', )
# def print_test():

#     return render_template('test.html', do_trade=do_trade.aaa)

    # return str(do_trade.aaa)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5500, debug=True)
