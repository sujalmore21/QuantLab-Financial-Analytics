from analytics.loader import load_stock

from analytics.performance import *

df = load_stock("AAPL")

print("Total Return")

print(total_return(df))

print()

print("Annual Return")

print(annual_return(df))