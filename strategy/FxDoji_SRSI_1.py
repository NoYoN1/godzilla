"""
Tes Strategy #2
1:1.5 Risk Reward

LONG Entry:
Bullish Engulfing
Limit order on Current Close

LONG Exit:
SL: Low - ATR*1.5
TP: Current Close + (Current Close - SL)

SHORT Entry:
Bearish Engulfing
Limit Order on Current Close

SHORT Exit:
SL: High + ATR*1.5
TP: Current Close - (SL-Current Close)

------------------------------------------
H1
(2007/01/11 - 2010/12/21)(1141 Days)

AUDJPY
AUDUSD
CADJPY
CHFJPY
EURGBP
EURJPY
EURUSD
GBPJPY
NZDUSD
USDCAD
USDCHF
USDJPY
XAUUSD



"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
import datetime
import math
from colorama import Fore
import matplotlib.pyplot as plt
import mpld3
import backtrader.plot as plt


'''
README
This strategy utilizes Stoch RSI and DOJI patterns to trade reversals.


'''


def printTradeAnalysis(analyzer):
    """
    Function to print the Technical Analysis results in a nice format.
    """
    # Get the results we are interested in
    total_open = analyzer.total.open
    total_closed = analyzer.total.closed
    total_won = analyzer.won.total
    total_lost = analyzer.lost.total
    win_streak = analyzer.streak.won.longest
    lose_streak = analyzer.streak.lost.longest
    pnl_net = round(analyzer.pnl.net.total, 2)
    strike_rate = round((total_won / total_closed) * 100, 2)
    # Designate the rows
    h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
    h2 = ['Strike Rate', 'Win Streak', 'Losing Streak', 'PnL Net']
    r1 = [total_open, total_closed, total_won, total_lost]
    r2 = [strike_rate, win_streak, lose_streak, pnl_net]
    # Check which set of headers is the longest.
    if len(h1) > len(h2):
        header_length = len(h1)
    else:
        header_length = len(h2)
    # Print the rows
   # print_list = [h1, r1, h2, r2]
    row_format = "{:<15}" * (header_length + 1)
   # print("Trade Analysis Results:")
    for row in print_list:
        print(row_format.format('', *row))
    return (r1, r2)


def printSQN(analyzer):
    sqn = round(analyzer.sqn, 2)
   # print('SQN: {}'.format(sqn))


def longSizing(cash, entryprice, stoploss, RPT):
    rpt = RPT  # 0.01 = 1% risk per trade
    rptic = cash * rpt  # RPT in CASH.
    # GAP From Entry Position to Stoploss
    slgap = (entryprice - stoploss) / entryprice
    entryic = rptic / slgap  # Entry ni Cash = $100 / SLGap
    qty = math.floor(entryic / entryprice)
    return qty  # Returns number of Shares/Contracts to buy/sell


def shortSizing(cash, entryprice, stoploss, RPT):
    rpt = RPT  # 0.01 = 1% risk per trade
    rptic = cash * rpt  # RPT in CASH.
    slgap = (stoploss - entryprice) / entryprice  # GAP From High
    entryic = rptic / slgap  # Entry in Cash = $100 / SLGap
    qty = math.floor(entryic / entryprice)
    return qty  # Returns number of Shares/Contracts to buy/sell


def longStopLoss(atr, close0, SLATR):
    return close0 - (atr * SLATR)


def longTakeProfit(atr, close0, TPATR):
    return close0 + (atr * TPATR)


def shortStopLoss(atr, close0, SLATR):
    return close0 + (atr * SLATR)


def shortTakeProfit(atr, close0, TPATR):
    return close0 - (atr * TPATR)


def doji(open0, high0, low0, close0, dojiValue):
    if close0 > open0:  # GREEN BAR
        if close0 - open0 <= (
                (high0 - close0) + (open0 - low0)) / dojiValue:  # Body < (Top Wick + Bot Wick) / 20
            return True
    elif close0 < open0:  # RED BAR
        if open0 - close0 <= (
                (high0 - open0) + (close0 - low0)) / dojiValue:  # Body < (Top Wick + Bot Wick) / 20
            return True


class Simulate:
    def __init__(self, cash, RPT, SLATR, TPATR, dojiValue, rsiValueUpper, rsiValueLower):

        self.cerebro = bt.Cerebro()  # create a "Cerebro" engine instance
        self.cerebro.addvalues(cash, RPT, SLATR, TPATR,
                               dojiValue,  # v1
                               rsiValueUpper,  # v2
                               rsiValueLower,  # v3
                               0,  # v4
                               0)  # v5

        data = bt.feeds.GenericCSVData(
            dataname="datas/EURJPY_D1.csv",
            nullvalue=0.0,
            dtformat='%Y-%m-%d %H:%M',
            timeframe=bt.TimeFrame.Minutes,
            compression=240,
            fromdate=datetime.datetime(2007, 1, 1, 00, 00, 00),
            todate=datetime.datetime(2010, 12, 29, 23, 59, 00),
            open=1,
            high=2,
            low=3,
            close=4,
            openinterest=-1
        )
        self.cerebro.adddata(data)
        self.cerebro.broker.set_cash(cash)
        setCash = self.cerebro.broker.set_cash(cash)

        self.cerebro.broker.setcommission(
            commission=0.000, margin=0, leverage=200.0)
        self.cerebro.addstrategy(FxMain)
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
        self.cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")

        #print("Starting Portfolio Value :%.5f" %
             # (self.cerebro.broker.getvalue()))
        strategies = self.cerebro.run()  # run it all
        self.firstStrat = strategies[0]
        finalValue = self.cerebro.broker.getvalue()
        finalCash = self.cerebro.broker.getcash()
        #print("Final Portfolio Value:%.5f" % (self.cerebro.broker.getvalue()))
        #print("Final Portfolio Cash :%.5f" % (self.cerebro.broker.getcash()))

        #printTradeAnalysis(self.firstStrat.analyzers.ta.get_analysis())
        #printSQN(self.firstStrat.analyzers.sqn.get_analysis())
        # self.cerebro.plot(style="candlestick", barup='tan',
        #                   bardown='darkslategrey')

    def printFinal(self):

        #print("Final Portfolio Value:%.5f" % (self.cerebro.broker.getvalue()))
        #print("Final Portfolio Cash :%.5f" % (self.cerebro.broker.getcash()))

        #printTradeAnalysis(self.firstStrat.analyzers.ta.get_analysis())
        #printSQN(self.firstStrat.analyzers.sqn.get_analysis())

        getValue = self.cerebro.broker.getvalue()
        getCash = self.cerebro.broker.getcash()
        getTotalOpen = self.firstStrat.analyzers.ta.get_analysis().total.open
        getTotalClosed = self.firstStrat.analyzers.ta.get_analysis().total.closed
        getTotalWon = self.firstStrat.analyzers.ta.get_analysis().won.total

        getTotalLost = self.firstStrat.analyzers.ta.get_analysis().lost.total
        getWinStreak = self.firstStrat.analyzers.ta.get_analysis().streak.won.longest
        getLoseStreak = self.firstStrat.analyzers.ta.get_analysis().streak.lost.longest
        getPNLNET = round(
            self.firstStrat.analyzers.ta.get_analysis().pnl.net.total, 2)
        getStrikeRate = round((getTotalWon / getTotalClosed) * 100, 2)

        return (getValue, getCash, getTotalOpen, getTotalClosed, getTotalWon,
                getTotalLost, getWinStreak, getLoseStreak, getPNLNET, getStrikeRate,
                getPNLNET)


class FxMain(bt.Strategy):
    class StochRSI(bt.Indicator):
        lines = ('stochrsi',)
        params = dict(
            period=14,  # to apply to RSI
            pperiod=None,  # if passed apply to HighestN/LowestN, else "period"
        )

        def __init__(self):
            rsi = bt.ind.RSI(self.data, period=self.p.period)

            pperiod = self.p.pperiod or self.p.period
            maxrsi = bt.ind.Highest(rsi, period=pperiod)
            minrsi = bt.ind.Lowest(rsi, period=pperiod)

            self.l.stochrsi = (rsi - minrsi) / (maxrsi - minrsi)
    params = dict(
        pfaster=20,
        pfast=50,
        pslow=200,
    )

    def atrFunction(self):
        # ATR FUNCTION
        range_total = 0
        for i in range(-13, 1):
            x = self.high0[i] - self.low0[i]
            y = self.high0[i] - self.close1[i]
            z = self.low0[i] - self.close1[i]
            if x > y:
                temp_truerange = x
            else:
                temp_truerange = y

            if temp_truerange > z:
                true_range = temp_truerange
            else:
                true_range = z

            range_total += true_range
        self.atr = range_total / 14

    def __init__(self):
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.stopLoss = None
        self.takeProfit = None
        self.open0 = self.datas[0].open
        self.high0 = self.datas[0].high
        self.low0 = self.datas[0].low
        self.close0 = self.datas[0].close
        self.open1 = self.datas[0].open(-1)
        self.high1 = self.datas[0].high(-1)
        self.low1 = self.datas[0].low(-1)
        self.close1 = self.datas[0].close(-1)
        self.open2 = self.datas[0].open(-2)
        self.high2 = self.datas[0].high(-2)
        self.low2 = self.datas[0].low(-2)
        self.close2 = self.datas[0].close(-2)
        self.open3 = self.datas[0].open(-3)
        self.high3 = self.datas[0].high(-3)
        self.low3 = self.datas[0].low(-3)
        self.close3 = self.datas[0].close(-3)
        self.open4 = self.datas[0].open(-4)
        self.high4 = self.datas[0].high(-4)
        self.low4 = self.datas[0].low(-4)
        self.close4 = self.datas[0].close(-4)
        self.open5 = self.datas[0].open(-5)
        self.high5 = self.datas[0].high(-5)
        self.low5 = self.datas[0].low(-5)
        self.close5 = self.datas[0].close(-5)

        self.atr = None
        self.tradeIniCash = None

        # Data position and counts
        self.dataCount = 0
        self.dataCountBuy = []
        self.dataCountSell = []

        self.srsi = self.StochRSI()

    # LOGGING FUNCTION
   # def log(self, txt, dt=None):
   #     """ Logging function for this strategy"""
   #     dt = dt or self.datas[0].datetime.datetime(0)
   #     print('%s, %s' % (dt.isoformat(), txt))

    # MAIN FUNCTION HERE
    def next(self):
        self.atrFunction()
        # Instants
        if 0 == 0:
            open0 = self.open0[0]
            high0 = self.high0[0]
            low0 = self.low0[0]
            close0 = self.close0[0]
            open1 = self.open1[0]
            high1 = self.high1[0]
            low1 = self.low1[0]
            close1 = self.close1[0]
            open2 = self.open2[0]
            high2 = self.high2[0]
            low2 = self.low2[0]
            close2 = self.close2[0]
            open3 = self.open3[0]
            high3 = self.high3[0]
            low3 = self.low3[0]
            close3 = self.close3[0]
            open4 = self.open4[0]
            high4 = self.high4[0]
            low4 = self.low4[0]
            close4 = self.close4[0]

            atr = self.atr
            cash = self.cerebro.broker.getcash()
            RPT = self.cerebro.getRPT()
            SLATR = self.cerebro.getSLATR()
            TPATR = self.cerebro.getTPATR()
            v1 = self.cerebro.getv1()      # dojiValue
            v2 = self.cerebro.getv2()      # rsiValueUpper
            v3 = self.cerebro.getv3()      # rsiValueLower
            v4 = self.cerebro.getv4()      #
            v5 = self.cerebro.getv5()      #

        # Log Close
        #self.log('C: %.5f' % close0)
        self.dataCount += 1
        # ORDER CHECK (If order is in place, can't place another until filled)
        if self.order:
            return

        if not self.position:
            # LONG ENTRY
            if self.srsi.stochrsi <= v3:
                if doji(open0, high0, low0, close0, v1):
                    self.tradeIniCash = cash  # Cash before the trade

                    self.stopLoss = longStopLoss(self.atr, close0, SLATR)
                    self.takeProfit = longTakeProfit(self.atr, close0, TPATR)

                    # Long Entry Sizing
                    qty = longSizing(cash, close0, self.stopLoss, RPT)

                    self.order = self.buy_bracket(size=qty, price=close0,
                                                  limitprice=self.takeProfit,
                                                  stopprice=self.stopLoss)
                    self.log('[   LONG ENTRY    ] B: %.2f, P: %.5f x%.f (TP: %.5f, SL: %.5f) ATR: %.5f' %
                             (cash, close0, qty, self.takeProfit, self.stopLoss, atr))

            # SHORT ENTRY
            if self.srsi.stochrsi >= v2:
                if doji(open0, high0, low0, close0, v1):
                    self.tradeIniCash = cash  # Cash before the trade

                    self.stopLoss = shortStopLoss(self.atr, close0, SLATR)
                    self.takeProfit = shortTakeProfit(self.atr, close0, TPATR)
                    # Short Entry Sizing
                    qty = shortSizing(cash, close0, self.stopLoss, RPT)

                    self.order = self.sell_bracket(size=qty, price=close0,
                                                   limitprice=self.takeProfit,
                                                   stopprice=self.stopLoss)
                    self.log('[   SHORT ENTRY   ] B: %.2f, P: %.5f x%.1f(TP: %.5f, SL: %.5f) ATR: %.5f' %
                             (cash, close0, qty, self.takeProfit, self.stopLoss, atr))

    # EXECUTED ORDER NOTIFICATIONS

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        price = order.executed.price
        qty = order.executed.size
        balance = self.cerebro.broker.getcash()
        cost = order.executed.value
        comm = order.executed.comm
        atr = self.atr

        # Check if an order has been completed. Broker could reject if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    "[   BUY EXECUTED  ] B: %.2f, P: %.5f x%.f = %.5f, Comm %.5f" %
                    (balance, price, qty, cost, comm))
                self.dataCountBuy.append(self.dataCount)

            elif order.issell():
                self.log(
                    "[  SELL EXECUTED  ] B: %.2f, P: %.5f x%.f = %.5f, Comm %.5f" %
                    (balance, price, (qty * -1), cost, comm))
                self.dataCountSell.append(self.dataCount)

            self.bar_executed = len(self)
        elif order.status in [order.Canceled]:
            self.log("Order Canceled")
        elif order.status in [order.Margin]:
            self.log("Order Margin")
        elif order.status in [order.Rejected]:
            self.log("Order Rejected")

        self.order = None

    # CLOSED OPERATION LOG
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        # Gain/Loss in Percentage from the amount before the trade
        profitpercent = (trade.pnlcomm/self.tradeIniCash) * 100
        cp = ((self.cerebro.broker.getcash() / self.cerebro.getInitCash())
              * 100) - 100  # Cumulative profit. 0% is the Initial Amount

       # if profitpercent < 0:
       #     print(Fore.RED, end="")
       # elif profitpercent > 0:
       #     print(Fore.GREEN, end="")

       # self.log("[    OPERATION PROFIT   ] B: %.2f, GROSS: %.2f, NET: %.2f" %
       #          (self.cerebro.broker.getcash(), trade.pnl, trade.pnlcomm))
       # self.log("[                       ] G/L: %.2f Percent, Cumulative: %.2f Percent" %
       #          (profitpercent, cp))

        #self.skip = True
       # print(Fore.RESET)


# Simulate(10000, 0.01, 2, 4,
#           20, 0.8, 0.2)
# Simulate(cash, RPT, SLATR, TPATR,
#         v1, v2, v3, v4, v5)
