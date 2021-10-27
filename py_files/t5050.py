import random


cash = 100000
trades = 0
infinity_loop = 0
var_if = 0
var_else = 0
rpt = 1/100  # 1/100 = 1% Risk per Trade
profitRatio = 1  # 2 = 2:01 Profit Ratio
winRate = 50  # Percentage. Win Ratio, 50 = 50% win rate

while trades < 100:
    dice = random.randint(1, 100)
    if dice <= winRate:
        cash += cash * rpt * profitRatio
        var_if += 1
        # print("if " + str(cash))
    else:
        cash -= cash * rpt
        var_else += 1
        # print("else " + str(cash))
    trades += 1


test = random.randint(0, 1)
print(cash)
print(trades)
print("win : " + str(var_if))
print("lose : " + str(var_else))
