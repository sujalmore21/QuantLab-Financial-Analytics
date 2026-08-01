from services.report_service import ReportService

service = ReportService()

summary = service.get_summary()

print("=" * 60)
print("REPORT SUMMARY")
print("=" * 60)

best = summary["best_portfolio"]

print("Best Portfolio")

print("Return :", round(best["return"], 4))
print("Risk   :", round(best["risk"], 4))
print("Sharpe :", round(best["sharpe"], 4))

print()

low = summary["low_risk_portfolio"]

print("Lowest Risk Portfolio")

print("Return :", round(low["return"], 4))
print("Risk   :", round(low["risk"], 4))
print("Sharpe :", round(low["sharpe"], 4))