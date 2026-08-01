"""
=========================================
Module  : report_service.py
Project : QuantLab
Purpose : Report Service Layer
=========================================
"""

import streamlit as st

from services.portfolio_service import get_portfolio_service


class ReportService:
    """
    Service responsible for
    preparing report data.
    """

    def __init__(self):
        # Reuse the SAME cached PortfolioService the rest of the app uses,
        # instead of creating a brand new one (which used to trigger its
        # own independent Monte Carlo run every time a report was opened).
        self.portfolio_service = get_portfolio_service()

    def get_summary(self):
        """
        Return complete portfolio summary.

        Returns
        -------
        dict
        """
        return self.portfolio_service.get_portfolio_summary()

    def get_best_portfolio(self):
        """
        Return maximum Sharpe portfolio.
        """
        return self.portfolio_service.get_best_portfolio()

    def get_low_risk_portfolio(self):
        """
        Return minimum risk portfolio.
        """
        return self.portfolio_service.get_low_risk_portfolio()


@st.cache_resource(show_spinner=False)
def get_report_service() -> "ReportService":
    return ReportService()