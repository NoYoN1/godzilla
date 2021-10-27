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
import sys

# sys.stdout = open("C:/Users/edwar/PycharmProjects/Hakushi/template/readme.txt", "w")

'''
Catch the Waves.
This strategy uses moving averages to as supports and ride trends.

Entry
1. Identify if there is a trend. If no, don't trade
    I. 3 Moving averages lining up Fast>Med>Slow
2. Wait for 1st swing to confirm.
    I.   Price touches support
    II.  Price bounces from support. What is a bounce? Where should it go to consider as a bounce?
    III. If I and II happened, it it considered as a bounce.
3. Wait for the Swing to fall to support.
4. Enter when it touches support and (confirmation bar).

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


def bullish_engulfing(open0, close0, open1, high1, low1, close1):
    if close0 > open0 and close1 < open1:  # Current Body is Green and Previous is Red
        # Current Body is at least 1.1x bigger than Previous Body
        if (close0 - open0) / (open1 - close1) > 1.1:
            if (high1 - open1) + (close1 - low1) < (
                    open1 - close1) / 2:  # Previous Wick is at least 2x shorter than Previous Body
                return True
            else:
                return False


def bearish_engulfing(open0, close0, open1, high1, low1, close1):
    if close0 < open0 and close1 > open1:  # Current Body is Red and Previous is Green
        # Current Body is at least 1.1x bigger than Previous Body
        if (open0 - close0) / (close1 - open1) > 1.1:
            if (high1 - close1) + (open1 - low1) < (
                    close1 - open1) / 2:  # Previous Wick is at least 2x shorter than Previous Body
                return True
            else:
                return False


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


def bullmasupp(ma, open0, low0, close0, low1):

    if low1 >= ma:  # Price has to go from up to down
        if low0 <= ma and open0 < close0:  # Green Low touches MA, and closes above ma
            return True
        elif low0 <= ma < open0 and open0 > close0:  # Red Low touches MA, and opens above ma
            return True


def bullbounceentry(ma, open0, low0, close0, open1, close1, low1):

    if open0 < close0 and open1 > close1:  # P0 Green , P1 Red
        if low0 <= ma or low1 <= ma:  # Low0/Low1 touches ma and
            if close0 >= ma:
                return True

    # Bullish Engulfing Entry
    # elif open0<close0 and open1>close1:                #P0 is GREEN and P1 is RED
        # if low1 <= ma or low0 <= ma:
            # if close0-open0 > open1-close1:             #P0 Body is bigger than P1 Body
                # if close0 > open1:                      #P0's Close is higher than P1's Open
                # return True


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
    # RPT in CASH. -490,000 from cash to bcs of the margin simulation
    rptic = (cash - 490000) * rpt
    # GAP From Entry Position to Stoploss
    slgap = (entryprice - stoploss) / entryprice
    entryic = rptic / slgap  # Entry in Cash = $100 / SLGap
    qty = math.floor(entryic / entryprice)
    return qty  # Returns number of Shares/Contracts to buy/sell


def shortsizing(cash, entryprice, stoploss):
    rpt = 0.01  # 0.01 = 1% risk per trade
    # RPT in CASH. -490,000 from cash to bcs of the margin simulation
    rptic = (cash - 490000) * rpt
    slgap = (stoploss - entryprice) / entryprice  # GAP From High
    entryic = rptic / slgap  # Entry in Cash = $100 / SLGap
    qty = math.floor(entryic / entryprice)
    return qty  # Returns number of Shares/Contracts to buy/sell


class DonchianChannels(bt.Indicator):
    alias = ('DCH', 'DonchianChannel',)
    lines = ('dcm', 'dch', 'dcl',)  # dc middle, dc high, dc low
    params = dict(
        period=20,
        lookback=-1,  # (-1) = doesnt count current bar
    )
    plotinfo = dict(subplot=False)  # plot along with data
    plotlines = dict(
        dch=dict(color="black"),  # use same color as prev line (dcm)
        # dcl=dict(_samecolor=False),  # use same color as prev line (dch)
    )

    def __init__(self):
        hi, lo = self.data.high, self.data.low
        if self.p.lookback:  # move backwards as needed
            hi, lo = hi(self.p.lookback), lo(self.p.lookback)

        self.l.dch = bt.ind.Highest(hi, period=self.p.period)
        # self.l.dcl = bt.ind.Lowest(lo, period=5)


class FxWaves(bt.Strategy):
    # list of parameters which are configurable for the strategy
    stoploss = 0
    takeprofit = 0
    tradeinicash = 10000
    islong = False
    skip = False
    skipperiods = 0
    supporttest = 0

    params = dict(
        pfaster=20,
        pfast=50,
        pslow=200,
    )

    def __init__(self):

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.dataopen = self.datas[0].open
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        self.dataclose = self.datas[0].close
        self.dataopen1 = self.datas[0].open(-1)
        self.datahigh1 = self.datas[0].high(-1)
        self.datalow1 = self.datas[0].low(-1)
        self.dataclose1 = self.datas[0].close(-1)
        self.dataopen2 = self.datas[0].open(-2)
        self.datahigh2 = self.datas[0].high(-2)
        self.datalow2 = self.datas[0].low(-2)
        self.dataclose2 = self.datas[0].close(-2)
        self.dataopen3 = self.datas[0].open(-3)
        self.datahigh3 = self.datas[0].high(-3)
        self.datalow3 = self.datas[0].low(-3)
        self.dataclose3 = self.datas[0].close(-3)
        self.dataopen4 = self.datas[0].open(-4)
        self.datahigh4 = self.datas[0].high(-4)
        self.datalow4 = self.datas[0].low(-4)
        self.dataclose4 = self.datas[0].close(-4)
        self.dataopen5 = self.datas[0].open(-5)
        self.datahigh5 = self.datas[0].high(-5)
        self.datalow5 = self.datas[0].low(-5)
        self.dataclose5 = self.datas[0].close(-5)

        # MA Function
        self.sma0 = bt.ind.EMA(period=self.p.pfaster)  # faster moving average
        self.sma1 = bt.ind.EMA(period=self.p.pfast)    # mid moving average
        self.sma2 = bt.ind.EMA(period=self.p.pslow)    # slow moving average

        self.dc = DonchianChannels()

    # LOGGING FUNCTION
    def log(self, txt, dt=None):
        """ Logging function for this strategy"""
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        if self.skip:
            self.skip = False
            return

        # ATR FUNCTION
        range_total = 0
        for i in range(-13, 1):
            x = self.datahigh[i] - self.datalow[i]
            y = self.datahigh[i] - self.dataclose1[i]
            z = self.datalow[i] - self.dataclose1[i]
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

        # Instants
        if 1 == 1:
            open0 = self.dataopen[0]
            high0 = self.datahigh[0]
            low0 = self.datalow[0]
            close0 = self.dataclose[0]
            open1 = self.dataopen1[0]
            high1 = self.datahigh1[0]
            low1 = self.datalow1[0]
            close1 = self.dataclose1[0]
            open2 = self.dataopen2[0]
            high2 = self.datahigh2[0]
            low2 = self.datalow2[0]
            close2 = self.dataclose2[0]

        close = self.dataclose[0]
        cash = cerebro.broker.getcash()
        atr = self.atr

        # FALSE SIGNAL
        # This function is to cancel an existing MA Support.
        # If the HEAD of a candle goes below SMA0, support is canceled.
        if self.supporttest == 1 or self.supporttest == 2:
            if open0 < close0:  # GREEN HEAD = CLOSE
                head = close0
            else:  # RED HEAD   = OPEN
                head = open0
            if head < self.sma0:  # If Head goes below MA -> Support is fake/canceled
                self.supporttest = 0
                self.log("Support Cancelled")

        # The Touch
        if bullmasupp(self.sma0, open0, low0, close0, low1):
            self.supporttest = 1
            self.log("Support")

        # self.log('C: %.5f' % (self.dataclose[0]))
        # ORDER CHECK (If order is in place, can't place another until filled)
        if self.order:
            return
        # LONG ENTRY
        if not self.position:
            if self.sma0 > self.sma1 > self.sma2:
                if self.supporttest == 2:
                    if bullbounceentry(self.sma0, open0, low0, close0, open1, close1, low1):
                        self.tradeinicash = (cash - 490000)
                        self.stoploss = self.dataclose[0] - (self.atr * 1.2)
                        self.takeprofit = self.dataclose[0] + (self.atr * 1.2)
                        qty = longsizing(cerebro.broker.get_cash(
                        ), self.dataclose[0], self.stoploss)  # Long Entry Sizing

                        self.order = self.buy_bracket(size=qty, price=self.dataclose[0],
                                                      limitprice=self.takeprofit,
                                                      stopprice=self.stoploss)
                        self.log('[   LONG ENTRY    ] P: %.5f, Qty: %.1f, B: %.2f, ATR: %.5f, TP: %.5f, SL: %.5f' %
                                 (close, qty, cash-490000, atr, self.takeprofit, self.stoploss))

            # SHORT ENTRY
        elif 1 == 2 and self.sma0 < self.sma1 < self.sma2:
            self.tradeinicash = (cash - 490000)
            self.stoploss = self.dataclose[0] + (self.atr * 1.2)
            self.takeprofit = self.dataclose[0] - (self.atr * 1.2)
            qty = shortsizing(cerebro.broker.get_cash(
            ), self.dataclose[0], self.stoploss)  # Short Entry Sizing

            self.order = self.sell_bracket(size=1, price=self.dataclose[0],
                                           limitprice=self.takeprofit,
                                           stopprice=self.stoploss)
            self.log('[   SHORT ENTRY   ] P: %.5f, Qty: %.1f, B: %.2f, ATR: %.5f, TP: %.5f, SL: %.5f' %
                     (close, qty, cash, atr, self.takeprofit, self.stoploss))

        # The Swing High
        if high0 >= self.dc.dch and self.supporttest == 1:
            self.supporttest = 2
            self.log("Bounced!")

    # EXECUTED ORDER NOTIFICATIONS
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        # Check if an order has been completed. Broker could reject if not enough cash
        price = (order.executed.price)
        qty = (order.executed.size)
        balance = (cerebro.broker.getcash())
        cost = (order.executed.value)
        comm = (order.executed.comm)
        atr = (self.atr)

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    "[   BUY EXECUTED  ] P: %.5f, Qty: %.1f, B: %.2f, Cost: %.5f, Comm %.5f, ATR: %.5f" %
                    (price, qty, balance-490000, cost, comm, atr))

            elif order.issell():
                self.log(
                    "[  SELL EXECUTED  ] P: %.5f, Qty:-%.1f, B: %.2f, Cost: %.5f, Comm %.5f" %
                    (price, (qty * -1), (balance-490000), cost, comm))

            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        self.order = None

    # CLOSED OPERATION LOG
    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        cp = ((cerebro.broker.getcash() - 490000) / 10000) * \
            100  # Cumulative profit. 100% is the Initial Amount
        # Gain/Loss in Percentage from the amount before the trade
        profitpercent = (
            ((cerebro.broker.getcash() - 490000) / self.tradeinicash) - 1) * 100

        self.log("[    OPERATION PROFIT   ] GROSS: %.2f, NET: %.2f, B: %.2f" %
                 (trade.pnl, trade.pnlcomm, cerebro.broker.getcash()))
        self.log("[     In Percentage     ] G/L: %.2f Percent, Cumulative: %.2f Percent" %
                 (profitpercent, cp))

        self.skip = True
        print()


def printTradeAnalysis(analyzer):
    '''
    Function to print the Technical Analysis results in a nice format.
    '''
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
    dataname="datas/Forex/EURUSD_H4.csv",
    nullvalue=0.0,
    dtformat=('%Y-%m-%d %H:%M'),
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
cerebro.adddata(data)  # Add the data feed
cerebro.broker.set_cash(500000)
cerebro.broker.setcommission(commission=0.000)
cerebro.addstrategy(FxWaves)  # Add the trading strategy
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")

print("Starting Portfolio Value :%.5f" % (cerebro.broker.getvalue() - 490000))
strategies = cerebro.run()  # run it all
firstStrat = strategies[0]
print("Final Portfolio Value:%.5f" % (cerebro.broker.getvalue() - 490000))
print("Final Portfolio Cash :%.5f" % (cerebro.broker.getcash() - 490000))

printTradeAnalysis(firstStrat.analyzers.ta.get_analysis())
printSQN(firstStrat.analyzers.sqn.get_analysis())
cerebro.plot(style="candlestick", barup='green', bardown='black')
