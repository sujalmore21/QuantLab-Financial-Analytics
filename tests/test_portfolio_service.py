from services.portfolio_service import PortfolioService

service = PortfolioService()

summary = service.get_portfolio_summary()

print("=" * 60)
print("BEST PORTFOLIO")
print("=" * 60)

best = summary["best_portfolio"]

print("Return :", round(best["return"], 4))
print("Risk   :", round(best["risk"], 4))
print("Sharpe :", round(best["sharpe"], 4))

print()

print("=" * 60)
print("LOW RISK PORTFOLIO")
print("=" * 60)

low = summary["low_risk_portfolio"]

print("Return :", round(low["return"], 4))
print("Risk   :", round(low["risk"], 4))
print("Sharpe :", round(low["sharpe"], 4))