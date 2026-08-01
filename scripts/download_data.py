"""
=========================================
Module : download_data.py
Project: QuantLab
Purpose: Download historical market data
=========================================
"""

import os
import sys

import pandas as pd
import yfinance as yf

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import (
    STOCKS,
    BENCHMARK,
    START_DATE,
    END_DATE,
    RAW_DATA_DIR,
    BENCHMARK_DIR
)


def download_stock(symbol, save_folder):
    """
    Download historical data for one stock.
    """

    try:

        print(f"Downloading {symbol}...")

        df = yf.download(
            symbol,
            start=START_DATE,
            end=END_DATE,
            progress=False,
            auto_adjust=True
        )

        if df.empty:
            print(f"❌ No data for {symbol}")
            return

        # Keep required columns only
        df = df.reset_index()

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df[["Date", "Close", "High", "Low", "Open", "Volume"]]

        filepath = os.path.join(save_folder, f"{symbol}.csv")

        df.to_csv(filepath, index=False)

        print(f"✅ Saved -> {filepath}")

    except Exception as e:

        print(f"❌ {symbol} : {e}")


def main():

    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(BENCHMARK_DIR, exist_ok=True)

    print("=" * 60)
    print("QuantLab Market Downloader")
    print("=" * 60)

    for stock in STOCKS:
        download_stock(stock, RAW_DATA_DIR)

    print("\nDownloading Benchmark...\n")

    download_stock(BENCHMARK, BENCHMARK_DIR)

    print("\n" + "=" * 60)
    print("Market Data Download Completed")
    print("=" * 60)


if __name__ == "__main__":
    main()