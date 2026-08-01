from analytics.loader import load_stock

df = load_stock("AAPL")

print(df.head())

print()

print(df.info())