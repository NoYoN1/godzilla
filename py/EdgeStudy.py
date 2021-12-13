import random
from colorama import Fore
import matplotlib.pyplot as plt

"""
Trading Strategy Edge Simulator

1. Simulates trades based on RPT and Edge.

"""


class Simulate:
    def __init__(self, initialCash, tradesRequired,
                 riskPerTrade, profitRatio, winRatio):

        # self.printTradeTrue = True
        # Initial_cash = 10000  # Initial Cash
        # self.cash = Initial_cash
        # self.tradesRequired = 100
        # self.rpt = 1 / 100  # 1/100 = 1% Risk per Trade
        # self.profitRatio = 1  # 2 = 2:1 Profit Ratio
        # self.winRate = 50  # Percentage. Win Ratio, 50 = 50% win rate

        self.printTradeTrue = True
        Initial_cash = initialCash  # Initial Cash
        self.cash = Initial_cash
        self.tradesRequired = tradesRequired
        self.rpt = riskPerTrade / 100  # 1/100 = 1% Risk per Trade
        self.profitRatio = profitRatio  # 2 = 2:1 Profit Ratio
        self.winRate = winRatio  # Percentage. Win Ratio, 50 = 50% win rate

        self.money = []
        self.tradeIndex = []
        self.portfolio = 0
        self.trades = 0
        self.printTimes = 0

        self.pnlNet = 0
        self.tradeIsWin = False
        self.win = 0
        self.loss = 0
        self.strikeRate = 0
        self.winStreak = 0
        self.currentWinStreak = 0
        self.lossStreak = 0
        self.currentLossStreak = 0
        self.positionChange = 0
        self.grossProfit = 0
        self.grossLoss = 0

        self.ATLow = self.cash
        self.ATHigh = self.cash
        self.ATLowPos = 0
        self.ATHighPos = 0
        self.portfolioPeak = 0
        self.portfolioLow = 999
        self.positionPeak = 0
        self.positionLow = 0
        self.drawdown = 0
        self.maxDrawdown = 0
        self.maxDDPeakPos = 0
        self.maxDDLowPos = 0

    def printTrade(self, i):
        if self.positionChange > 0:
            print(Fore.GREEN + 'Trade %.0f = $%.2f || $%.2f' %
                  (self.trades, self.money[i], self.positionChange))
        else:
            print(Fore.RED + 'Trade %.0f = $%.2f || $%.2f ' %
                  (self.trades, self.money[i], self.positionChange,))
        return(self.trades, self.money)

    def printSetup(self, Initial_cash):
        print(Fore.CYAN)
        print('Initial Cash     : $%.f' % Initial_cash)
        print('Number of Trades : %.f' % self.tradesRequired)
        print('Risk Per Trade   : %.f' % (self.rpt*100) + '%')
        print('Profit Ratio     : %.f' % self.profitRatio + ':1')
        print('Win Rate         : %.f' % self.winRate + '%')

    def printFinal(self,):
        # print(Fore.RESET)
        # print('Final Cash  : $%.2f' % self.cash)
        # print('Gross Profit: $%.f' % self.grossProfit)
        # print('Gross Loss  : $%.f' % self.grossLoss)
        # print('PnL Net     : %.2f' % self.pnlNet + '%')
        # print('Strike Rate : %.1f' % self.strikeRate)
        # print('Win         : %.f ||   Loss         : %.f' %
        #       (self.win, self.loss))
        # print('Win Streak  : %.f   ||   Loss Streak  : %.f' %
        #       (self.winStreak, self.lossStreak))
        # print('Max Drawdown: %.3f' % self.maxDrawdown + '%')
        # print('Max Drawdown Peak: %.f || Max Drawdown Low: %.f' %
        #       (self.maxDDPeakPos, self.maxDDLowPos))
        # print('Max All Time High: $%.f || Max All time Low: $%.2f' %
        #       (self.ATHigh, self.ATLow))
        # print('Max ATLOWPOS: %.f' % self.ATLowPos)
        return self.cash, self.grossProfit, self.grossLoss, self.pnlNet, self.strikeRate, self.win, self.loss, self.winStreak, self.lossStreak, self.maxDrawdown, self.maxDDPeakPos, self.maxDDLowPos, self.ATHigh, self.ATLow, self.ATLowPos

    def trade(self, i):
        dice = random.randint(1, 100)
        self.positionChange = 0

        if dice <= self.winRate:
            self.tradeIsWin = True
        elif dice >= self.winRate:
            self.tradeIsWin = False

        if self.tradeIsWin:
            self.positionChange += self.cash * self.rpt * self.profitRatio
        elif not self.tradeIsWin:
            self.positionChange -= self.cash * self.rpt

        self.cash += self.positionChange

        self.trades += 1
        self.money.append(self.cash)
        self.tradeIndex.append(i)
        self.basicAnalyzer(i)

        # if self.printTradeTrue:
        #     self.printTrade(i)

    # def next(self, Initial_cash):
    #     # print(f"Starting Cash: ${Initial_cash}")
    #     # print()
    #     while self.trades < self.tradesRequired:
    #         self.trade(self.trades)

        # self.printSetup(Initial_cash)
        # self.printFinal()
        # plt.plot(self.tradeIndex, self.money,)
        # plt.ylabel('Money')
        # plt.show()

    def multiple(self, initialCash, tradesRequired,
                 riskPerTrade, profitRatio, winRatio):

        portfolioIndex = []
        multi = []
        cashR = []
        pnlR = []
        strikeR = []
        maxR = []
        # self.printSetup(initialCash)
        print(Fore.RESET)
        for i in range(0, 10):
            self.__init__(initialCash, tradesRequired,
                          riskPerTrade, profitRatio, winRatio)
            self.printTradeTrue = False
            while self.trades < self.tradesRequired:
                self.trade(self.trades)
            portfolioIndex.append(self.money)
            # print('Final Cash #%.f  : $%.2f || PnL Net: %.2f || Strike Rate: %.1f || MAX DD: %.2f' %
            #       (i + 1, self.cash, self.pnlNet, self.strikeRate, self.maxDrawdown))
            plt.plot(self.tradeIndex, portfolioIndex[i], )
            multi.append(portfolioIndex[i])
            cashR.append(self.cash)
            pnlR.append(self.pnlNet)
            strikeR.append(self.strikeRate)
            maxR.append(self.maxDrawdown)
        # plt.ylabel('Money')
        # plt.show()
        return (multi, cashR, pnlR, strikeR, maxR)

    def basicAnalyzer(self, i):
        # Gross Profit / Loss
        if self.positionChange > 0:
            self.grossProfit += self.positionChange
        if self.positionChange < 0:
            self.grossLoss += self.positionChange

        # Win/Lose Streaks
        if self.tradeIsWin:
            self.currentWinStreak += 1

            if self.currentLossStreak > self.lossStreak:
                self.lossStreak = self.currentLossStreak
            self.currentLossStreak = 0
        elif not self.tradeIsWin:
            self.currentLossStreak += 1

            if self.currentWinStreak > self.winStreak:
                self.winStreak = self.currentWinStreak
            self.currentWinStreak = 0

        # Cumulative
        self.pnlNet = (self.cash-100000)/100000 * 100

        # Strike Rate
        if self.tradeIsWin:
            self.win += 1
        else:
            self.loss += 1
        self.strikeRate = (self.win/(self.win+self.loss)) * 100

        # All Time High and Low
        if self.money[i] > self.ATHigh:
            self.ATHigh = self.money[i]
        if self.money[i] < self.ATLow:
            self.ATLow = self.money[i]
            self.ATLowPos = i+1
        # Drawdowns
        if self.money[i] > self.portfolioPeak:
            self.portfolioPeak = self.money[i]
            self.positionPeak = i
            self.portfolioLow = 100000000000000000000
            self.positionLow = 0
        if self.money[i] <= self.portfolioLow:
            self.portfolioLow = self.money[i]
            self.positionLow = i

        self.drawdown = (
            (self.portfolioPeak - self.portfolioLow)/self.portfolioPeak)*100
        if self.drawdown > self.maxDrawdown:
            self.maxDrawdown = self.drawdown
            self.maxDDPeakPos = self.positionPeak+1
            self.maxDDLowPos = self.positionLow+1


# s1 = Simulate(initialCash, tradesRequired, riskPerTrade, profitRatio, winRatio)
# # s1.printFinal()
# Initial_cash = s1.cash
# select = True
# if select == True:
#     s1.multiple(Initial_cash)
# else:
#     s1.next(Initial_cash)
# aaa = s1.cash
# bbb = Initial_cash

# print(aaa)
# print(bbb)

# s1.multiple(Initial_cash)
