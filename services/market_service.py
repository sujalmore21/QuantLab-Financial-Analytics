"""
=========================================
Module  : market_service.py
Project : QuantLab
Purpose : Market Data Service Layer
=========================================
"""

import streamlit as st

from analytics.loader import load_stock
from analytics.optimizer import (
    load_prices,
    calculate_returns_matrix,
    calculate_covariance_matrix,
    calculate_expected_returns,
)


class MarketService:
    """
    Service layer for market operations.
    """

    def __init__(self):
        self._prices = None
        self._returns = None
        self._covariance = None
        self._expected_returns = None

    def get_stock_data(self, symbol):
        """
        Load single stock data.
        """
        return load_stock(symbol)

    def get_prices(self):
        """
        Get combined price dataframe.
        """
        if self._prices is None:
            self._prices = load_prices()
        return self._prices

    def get_returns(self):
        """
        Get daily returns matrix.
        """
        if self._returns is None:
            prices = self.get_prices()
            self._returns = calculate_returns_matrix(prices)
        return self._returns

    def get_covariance(self):
        """
        Get annual covariance matrix.
        """
        if self._covariance is None:
            self._covariance = calculate_covariance_matrix(self.get_returns())
        return self._covariance

    def get_expected_returns(self):
        """
        Get annual expected returns.
        """
        if self._expected_returns is None:
            self._expected_returns = calculate_expected_returns(self.get_returns())
        return self._expected_returns


# Same fix as PortfolioService: instance-level caching alone doesn't survive
# a Streamlit rerun, so give the whole app ONE shared, cached instance.
@st.cache_resource(show_spinner=False)
def get_market_service() -> "MarketService":
    return MarketService()