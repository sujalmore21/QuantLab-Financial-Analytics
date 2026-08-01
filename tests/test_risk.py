from analytics.loader import load_stock
from analytics.returns import (
    calculate_daily_returns
)
from analytics.risk import *

df = load_stock("AAPL")

df = calculate_daily_returns(df)

print("Daily Volatility")
print(volatility(df))

print()

print("Annual Volatility")
print(annual_volatility(df))

print()

print("Sharpe Ratio")
print(sharpe_ratio(df))

print()

print("Maximum Drawdown")
print(max_drawdown(df))