from analytics.optimizer import optimize_portfolio

best_portfolio, safest_portfolio = optimize_portfolio()

print("=" * 60)
print("OPTIMAL PORTFOLIO")
print("=" * 60)

print("Return :", round(best_portfolio["return"], 4))
print("Risk   :", round(best_portfolio["risk"], 4))
print("Sharpe :", round(best_portfolio["sharpe"], 4))

print()

print("=" * 60)
print("LOWEST RISK PORTFOLIO")
print("=" * 60)

print("Return :", round(safest_portfolio["return"], 4))
print("Risk   :", round(safest_portfolio["risk"], 4))
print("Sharpe :", round(safest_portfolio["sharpe"], 4))