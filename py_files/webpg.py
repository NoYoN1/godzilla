from flask import Flask
from flask import request
import do_trade

# import t5050

app = Flask(__name__)

result = do_trade.cerebro.broker.getvalue()


@app.route("/")
def index():
    celsius = request.args.get("celsius", "")
    if celsius:
        fahrenheit = fahrenheit_from(celsius)
    else:
        fahrenheit = ""
    return (
        """<form action="" method="get">
                Celsius temperature: <input type="text" name="celsius">
                <input type="submit" value="Convert to Fahrenheit">
            </form>"""
        + "Fahrenheit: " + fahrenheit +
        "</p><div id='d'><script>document.write('Hello World from python');</script></div>"
    )


@app.route("/print")
def rst():

    return (
        "trade close: " + str(do_trade.ddd) +
        " Print result:" + str(int(result))
    )


# @app.route("/print1")
# def er():
#     return "cash: " + str(t5050.cash)


def fahrenheit_from(celsius):
    """Convert Celsius to Fahrenheit degrees."""
    try:
        fahrenheit = float(celsius) * 9 / 5 + 32
        fahrenheit = round(fahrenheit, 3)  # Round to three decimal places
        return str(fahrenheit)
    except ValueError:
        return "invalid input"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081, debug=True)
