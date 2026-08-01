"""
=========================================
Module  : portfolio_service.py
Project : QuantLab
Purpose : Portfolio Service Layer
=========================================
"""

import streamlit as st

from analytics.optimizer import optimize_portfolio


class PortfolioService:
    """
    Service responsible for
    portfolio optimization operations.
    """

    def __init__(self):
        self._optimized_portfolio = None

    def _load_optimization(self):
        """
        Run optimization only once.
        """
        if self._optimized_portfolio is None:
            best, low_risk = optimize_portfolio()
            self._optimized_portfolio = {
                "best_portfolio": best,
                "low_risk_portfolio": low_risk,
            }

    def get_best_portfolio(self):
        """
        Return maximum Sharpe portfolio.
        """
        self._load_optimization()
        return self._optimized_portfolio["best_portfolio"]

    def get_low_risk_portfolio(self):
        """
        Return minimum volatility portfolio.
        """
        self._load_optimization()
        return self._optimized_portfolio["low_risk_portfolio"]

    def get_portfolio_summary(self):
        """
        Return all optimized portfolios.
        """
        self._load_optimization()
        return self._optimized_portfolio


# ==========================================================
# Single shared, cached instance for the WHOLE app.
#
# IMPORTANT: every page and every other service must obtain a
# PortfolioService through this function — never call
# PortfolioService() directly. Streamlit reruns the entire
# script on every interaction/page navigation, so an instance
# created directly (or an @st.cache_resource wrapper redefined
# separately in each page file) does NOT get shared across
# pages. That was causing the Monte Carlo simulation to run
# independently 3-4 times (once per page, plus once more inside
# ReportService) instead of once for the whole app session.
# ==========================================================
@st.cache_resource(show_spinner="Running portfolio optimization...")
def get_portfolio_service() -> "PortfolioService":
    return PortfolioService()