from services.market_service import MarketService

market = MarketService()

prices = market.get_prices()

print("=" * 60)
print("PRICE MATRIX")
print("=" * 60)

print(prices.head())

print()

returns = market.get_returns()

print("=" * 60)
print("RETURNS MATRIX")
print("=" * 60)

print(returns.head())

print()

expected = market.get_expected_returns()

print("=" * 60)
print("EXPECTED RETURNS")
print("=" * 60)

print(expected)