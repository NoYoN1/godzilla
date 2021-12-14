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

'''
README
This strategy utilizes Stoch RSI and DOJI patterns to trade reversals.

if StochRSI <= 0.2 and DOJI = True:
    LONG
if StochRSI >= 0.8 and DOJI = True:
    LONG

1:1 Take Profit:Stop Loss
1.2x ATR 
matplotlib
'''


def doji(open0, high0, low0, close0):
    if close0 > open0:  # Close higher than Open, Resulting in a GREEN BAR
        # Body < (Top Wick + Bot Wick) / 20
        if close0 - open0 <= ((high0 - close0) + (open0 - low0)) / 20:
            return True
    elif close0 < open0:  # Close lower than Open, Resulting in a RED BAR
        # Body < (Top Wick + Bot Wick) / 20
        if open0 - close0 <= ((high0 - open0) + (close0 - low0)) / 20:
            return True


def bullpin(open0, high0, low0, close0):
    # Body should be at least 70% above
    standard = (low0 + ((high0 - low0) * 0.7))

    # bullpin's BODY is at least 5x smaller than TOTAL WICK
    if greencandle(open0, high0, low0, close0, 0.2):
        if open0 > standard:  # Open is higher than middle of the candle's range
            return True
    # bullpin's BODY is at least 5x smaller than TOTAL WICK
    elif redcandle(open0, high0, low0, close0, 0.2):
        if close0 > standard:  # CLOSE is higher than middle of the candle's range
            return True


def bearpin(open0, high0, low0, close0):
    # Body should be at least 30% below
    standard = (low0 + ((high0 - low0) * 0.3))

    # bearpin's BODY is at least 5x smaller than TOTAL WICK
    if greencandle(open0, high0, low0, close0, 0.2):
        if close0 < standard:  # CLOSE is LOWER than middle of the candle's range
            return True
    # bearpin's BODY is at least 5x smaller than TOTAL WICK
    elif redcandle(open0, high0, low0, close0, 0.2):
        if open0 < standard:  # OPEN is LOWER than middle of the candle's range
            return True


def greencandle(openn, high, low, close, bodywickratio):
    body = close - openn
    wick = (high - close) + (openn - low)

    if openn < close:  # Open is LOWER than Close indicating GREEN CANDLE

        # Body/Wick is at least BIGGER than to the issued ratio.
        if bodywickratio > 1:
            if wick != 0:
                # e.g. Thick bars : 1.5 >= 1.4  .Body should be at least 40% bigger.
                if body / wick >= bodywickratio:
                    return True
                else:
                    return False
        # Body/Wick is at least SMALLER than to the issued ratio.
        elif bodywickratio < 1:
            if wick != 0:
                # e.g. DOJI       : 0.05 <= 0.1 .Body should be at least 10x smaller.
                if body / wick <= bodywickratio:
                    return True
                else:
                    return False


def redcandle(openn, high, low, close, bodywickratio):
    body = openn - close
    wick = (high - openn) + (close - low)

    if openn > close:  # Open is HIGHER than Close indicating RED CANDLE

        # Body/Wick is at least BIGGER than to the issued ratio.
        if bodywickratio > 1:
            if wick != 0:  # e.g. Thick bars : 1.5 >= 1.4
                # print(body/wick)
                if body / wick >= bodywickratio:  # Body should be at least 40% bigger
                    return True
                else:
                    return False

        # Body/Wick is at least SMALLER than to the issued ratio.
        elif bodywickratio < 1:
            if wick != 0:  # e.g. DOJI       : 0.05 <= 0.1 .
                # Body should be at least 10x smaller.
                if body / wick <= bodywickratio:
                    return True
                else:
                    return False


def longsizing(cash, entryprice, stoploss):
    rpt = 0.01  # 0.01 = 1% risk per trade
    rptic = cash * rpt  # RPT in CASH.
    # GAP From Entry Position to Stoploss
    slgap = (entryprice - stoploss) / entryprice
    entryic = rptic / slgap  # Entry in Cash = $100 / SLGap
    qty = math.floor(entryic / entryprice)
    return qty  # Returns number of Shares/Contracts to buy/sell


def shortsizing(cash, entryprice, stoploss):
    rpt = 0.01  # 0.01 = 1% risk per trade
    rptic = cash * rpt  # RPT in CASH.
    slgap = (stoploss - entryprice) / entryprice  # GAP From High
    entryic = rptic / slgap  # Entry in Cash = $100 / SLGap
    qty = math.floor(entryic / entryprice)
    return qty  # Returns number of Shares/Contracts to buy/sell


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


class FxMain(bt.Strategy):
    # list of parameters which are configurable for the strategy
    stoploss = 0
    takeprofit = 0
    islong = False
    skip = False
    skipperiods = 0

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

        self.atr = 0

        #self.rsi = bt.indicators.RSI_SMA(self.data.close, period=14)
        self.srsi = StochRSI()

    # LOGGING FUNCTION
    def log(self, txt, dt=None):
        """ Logging function for this strategy"""
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt.isoformat(), txt))

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

            cash = cerebro.broker.getcash()
            atr = self.atr

        # Log Close
        #self.log('C: %.5f' % close0)
        # ORDER CHECK (If order is in place, can't place another until filled)
        if self.order:
            return

        if not self.position:
            # LONG ENTRY
            if self.srsi.stochrsi <= 0.2:
                if doji(open0, high0, low0, close0):
                    self.tradeIniCash = cash  # Cash before the trade

                    self.stoploss = close0 - (self.atr * 3)
                    self.takeprofit = close0 + (self.atr * 4)
                    qty = longsizing(cerebro.broker.get_cash(),
                                     close0, self.stoploss)  # Long Entry Sizing

                    self.order = self.buy_bracket(size=qty, price=close0,
                                                  limitprice=self.takeprofit,
                                                  stopprice=self.stoploss)
                    self.log('[   LONG ENTRY    ] B: %.2f, P: %.5f x%.f (TP: %.5f, SL: %.5f) ATR: %.5f' %
                             (cash, close0, qty, self.takeprofit, self.stoploss, atr))
            # SHORT ENTRY
            if self.srsi.stochrsi >= 0.8:
                if doji(open0, high0, low0, close0):
                    self.tradeIniCash = cash  # Cash before the trade

                    self.stoploss = close0 + (self.atr * 3)
                    self.takeprofit = close0 - (self.atr * 4)
                    qty = shortsizing(cerebro.broker.get_cash(
                    ), close0, self.stoploss)  # Short Entry Sizing

                    self.order = self.sell_bracket(size=qty, price=close0,
                                                   limitprice=self.takeprofit,
                                                   stopprice=self.stoploss)
                    self.log('[   SHORT ENTRY   ] B: %.2f, P: %.5f x%.1f(TP: %.5f, SL: %.5f) ATR: %.5f' %
                             (cash, close0, qty, self.takeprofit, self.stoploss, atr))

    # EXECUTED ORDER NOTIFICATIONS

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        price = order.executed.price
        qty = order.executed.size
        balance = cerebro.broker.getcash()
        cost = order.executed.value
        comm = order.executed.comm
        atr = self.atr

        # Check if an order has been completed. Broker could reject if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    "[   BUY EXECUTED  ] B: %.2f, P: %.5f x%.f = %.5f, Comm %.5f" %
                    (balance, price, qty, cost, comm))

            elif order.issell():
                self.log(
                    "[  SELL EXECUTED  ] B: %.2f, P: %.5f x%.f = %.5f, Comm %.5f" %
                    (balance, price, (qty * -1), cost, comm))

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
        # Cumulative profit. 100% is the Initial Amount
        cp = ((cerebro.broker.getcash() / 10000) * 100) - 100

        if profitpercent < 0:
            print(Fore.RED, end="")
        elif profitpercent > 0:
            print(Fore.GREEN, end="")

        self.log("[    OPERATION PROFIT   ] B: %.2f, GROSS: %.2f, NET: %.2f" %
                 (cerebro.broker.getcash(), trade.pnl, trade.pnlcomm))
        self.log("[                       ] G/L: %.2f Percent, Cumulative: %.2f Percent" %
                 (profitpercent, cp))

        #self.skip = True
        print(Fore.RESET)


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
    print_list = [h1, r1, h2, r2]
    row_format = "{:<15}" * (header_length + 1)
    print("Trade Analysis Results:")
    for row in print_list:
        print(row_format.format('', *row))


def printSQN(analyzer):
    sqn = round(analyzer.sqn, 2)
    print('SQN: {}'.format(sqn))


cerebro = bt.Cerebro()  # create a "Cerebro" engine instance
data = bt.feeds.GenericCSVData(
    dataname="datas/EURUSD_H4.csv",
    nullvalue=0.0,
    dtformat='%Y-%m-%d %H:%M',
    timeframe=bt.TimeFrame.Minutes,
    compression=240,
    fromdate=datetime.datetime(2007, 1, 1, 00, 00, 00),
    todate=datetime.datetime(2020, 12, 29, 23, 59, 00),
    open=1,
    high=2,
    low=3,
    close=4,
    openinterest=-1
)
cerebro.adddata(data)
cerebro.broker.set_cash(10000)
cerebro.broker.setcommission(commission=0.000, margin=0, leverage=200.0)
cerebro.addstrategy(FxMain)
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")

print("Starting Portfolio Value :%.5f" % (cerebro.broker.getvalue()))
strategies = cerebro.run()  # run it all
firstStrat = strategies[0]
print("Final Portfolio Value:%.5f" % (cerebro.broker.getvalue()))
print("Final Portfolio Cash :%.5f" % (cerebro.broker.getcash()))

printTradeAnalysis(firstStrat.analyzers.ta.get_analysis())
printSQN(firstStrat.analyzers.sqn.get_analysis())
cerebro.plot(style="candlestick", barup='green', bardown='red')
