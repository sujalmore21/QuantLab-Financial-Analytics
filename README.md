# 📈 QuantLab — Quantitative Investment Analytics Platform

QuantLab is an interactive quantitative analytics and portfolio optimization platform built using Modern Portfolio Theory (MPT) and Monte Carlo simulations. It bridges mathematical finance with clean visualizations, enabling real-time risk/return landscape mapping and automated institutional reporting.

---

## 📸 Platform Previews

### 📊 Dashboard Overview
<p align="center">
  <img src="assets/dashboard.png" alt="QuantLab Dashboard" height="380">
</p>

---

### 🎯 Portfolio Optimizer (Monte Carlo Efficient Frontier)
<p align="center">
  <img src="assets/optimizer.png" alt="QuantLab Optimizer" height="380">
</p>

---

### 📈 Analytics & Reporting

| Performance Analytics | Risk Diagnostics & Heatmap |
| :---: | :---: |
| <img src="assets/performance.png" alt="Performance" height="320"> | <img src="assets/risk.png" alt="Risk Analytics" height="320"> |

| Portfolio Allocation & Weights | Institutional PDF Report |
| :---: | :---: |
| <img src="assets/portfolio.png" alt="Portfolio Weights" height="320"> | <img src="assets/reports.png" alt="Generated Reports" height="320"> |

---

## ✨ Key Features

* **Monte Carlo Optimization Engine:** Simulates 5,000+ candidate portfolio allocations across multi-asset universes in real time.
* **Efficient Frontier Mapping:** Visually identifies Maximum Sharpe Ratio and Minimum Risk portfolios.
* **Risk & Performance Analytics:** Tracks annualized returns, volatility, Sharpe ratio, max drawdown, and cross-asset correlation heatmaps.
* **Automated PDF Export:** Generates downloadable, institutional-grade executive summary reports on demand.

---

## 💡 Key Company-Specific Insights & Takeaways

* **Max Sharpe Growth Driver (Alphabet, NVIDIA, J&J, Tesla):** 
  To achieve maximum risk-adjusted growth (Sharpe 1.32 | Return 39.64%), the algorithm concentrates **~80% of total capital** into just four companies:
  * **Alphabet Inc. ($GOOGL):** 20.92%
  * **NVIDIA ($NVDA):** 20.55%
  * **Johnson & Johnson ($JNJ):** 20.09%
  * **Tesla ($TSLA):** 18.70%

* **Minimum Risk Volatility Penalty (Slashing NVIDIA & Tesla):**
  When optimizing purely for capital preservation and volatility reduction (19.57% Volatility), the algorithm heavily penalizes high-beta stocks:
  * **NVIDIA ($NVDA)** gets ruthlessly slashed from **20.55% → 0.28%**
  * **Tesla ($TSLA)** gets cut from **18.70% → 1.51%**

* **Defensive Safe Havens (Johnson & Johnson, Coca-Cola, Amazon):**
  Capital reallocated away from tech volatility rotates straight into defensive anchors:
  * **Johnson & Johnson ($JNJ)** acts as the primary anchor across both models (~20.09% in Max Sharpe → **22.21%** in Min Risk).
  * **The Coca-Cola Company ($KO)** surges to **20.16%** allocation.
  * **Amazon ($AMZN)** climbs to **13.29%** allocation.

* **Risk Efficiency Trade-off:**
  Moving from *Minimum Risk* to *Max Sharpe* trades an **+8.84% increase in volatility** for a **+20.14% boost in annual return** (~2.28% extra return per 1% extra risk).

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Data & Analytics:** Pandas, NumPy, SciPy
* **Visualization:** Plotly, Streamlit
* **Database:** MySQL
* **Reporting Engine:** ReportLab / PDF Engine

---

## 🚀 Quick Start & Installation

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/sujalmore21/QuantLab-Financial-Analytics.git](https://github.com/sujalmore21/QuantLab-Financial-Analytics.git)
   cd QuantLab-Financial-Analytics
