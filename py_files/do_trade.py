import datetime
import backtrader as bt

from Simple_strategy import TestStrategy

cerebro = bt.Cerebro()
cerebro.broker.setcash(10000)

# Create a Data Feed
data = bt.feeds.YahooFinanceCSVData(
    dataname="AAPL.csv",
    # Do not pass values before this date
    fromdate=datetime.datetime(2021, 1, 1),
    # Do not pass values after this date
    todate=datetime.datetime(2021, 10, 10),
    reverse=False)

cerebro.adddata(data)

cerebro.addstrategy(TestStrategy)


print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
txt_print_start = 'Starting Portfolio Value: %.2f' % cerebro.broker.getvalue()

# aaa = cerebro.run()

cerebro.run()

# print("cccccc" + str(ccc))

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
txt_print_final = 'Final Portfolio Value: %.2f' % cerebro.broker.getvalue()

# ##################### pip install matplotlib==3.2.2 #########################3
# cerebro.plot(style="candlestick", barup="green", bardown="red")
