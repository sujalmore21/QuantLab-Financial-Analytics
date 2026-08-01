"""
=========================================
QuantLab Configuration
=========================================
Author  : Sujal More
Project : QuantLab - Institutional Portfolio Intelligence Platform
Purpose : Central configuration for the entire project.
=========================================
"""

from pathlib import Path

# ==========================================================
# Base Directory
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

# ==========================================================
# Portfolio Stocks
# ==========================================================

STOCKS = [
    "AAPL",      # Apple
    "MSFT",      # Microsoft
    "NVDA",      # NVIDIA
    "AMZN",      # Amazon
    "GOOGL",     # Alphabet
    "META",      # Meta
    "TSLA",      # Tesla
    "JPM",       # JPMorgan Chase
    "JNJ",       # Johnson & Johnson
    "KO"         # Coca-Cola
]

# ==========================================================
# Benchmark
# ==========================================================

BENCHMARK = "^GSPC"     # S&P 500

# ==========================================================
# Historical Data Range
# ==========================================================

START_DATE = "2020-01-01"
END_DATE = "2026-01-01"

# ==========================================================
# Portfolio Analytics
# ==========================================================

TRADING_DAYS = 252
RISK_FREE_RATE = 0.02
NUM_SIMULATIONS = 5000
DEFAULT_INVESTMENT = 100000

# ==========================================================
# Data Directories
# ==========================================================

DATA_DIR = BASE_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
BENCHMARK_DIR = DATA_DIR / "benchmark"
EXPORT_DIR = DATA_DIR / "exports"

# ==========================================================
# Database
# ==========================================================

DATABASE_PATH = BASE_DIR / "database" / "portfolio.db"

# ==========================================================
# Dashboard
# ==========================================================

APP_TITLE = "QuantLab"

PAGE_ICON = "📈"

THEME = "dark"

LAYOUT = "wide"

# ==========================================================
# Dashboard Colors
# ----------------------------------------------------------
# NOTE: these must always mirror theme.COLORS in theme.py.
# This file previously had its own blue/slate palette
# (#2563EB etc.) completely separate from theme.py's
# graphite-navy/gold system — any code reading colors from
# config.py instead of theme.py was rendering mismatched
# blue accents against the gold/dark UI. Now single source
# of truth: theme.py owns the palette, config.py just mirrors
# it so both files never drift apart again.
# ==========================================================

PRIMARY_COLOR = "#C9A227"      # gold — was #2563EB (blue, didn't match theme.py)

SECONDARY_COLOR = "#0B0E14"    # graphite-navy bg — was #0F172A (slate, didn't match)

SUCCESS_COLOR = "#4F9D69"      # green — was #16A34A

WARNING_COLOR = "#C9A227"      # gold doubles as the warning/attention accent

DANGER_COLOR = "#B5544B"       # red — was #DC2626

BACKGROUND_COLOR = "#0B0E14"
PANEL_COLOR = "#141A24"
TEXT_COLOR = "#E7E4DC"
MUTED_COLOR = "#8B93A1"

# ==========================================================
# Currency
# ==========================================================

CURRENCY = "USD"

# ==========================================================
# Report Settings
# ==========================================================

REPORT_AUTHOR = "Sujal More"

REPORT_TITLE = "QuantLab Portfolio Report"

REPORT_COMPANY = "QuantLab Analytics"

# ==========================================================
# Export Formats
# ==========================================================

SUPPORTED_EXPORTS = [
    "csv",
    "xlsx",
    "pdf"
]