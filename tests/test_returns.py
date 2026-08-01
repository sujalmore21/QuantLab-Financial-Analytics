from analytics.loader import load_stock

from analytics.returns import *

df = load_stock("AAPL")

df = calculate_daily_returns(df)

df = calculate_cumulative_returns(df)

print(df.tail())