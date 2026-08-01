"""
=========================================
Module : db.py
Project: QuantLab
Purpose: SQLite Database Connection
=========================================
"""

import sqlite3
from config import DATABASE_PATH


def get_connection():
    """
    Returns SQLite connection.
    """

    conn = sqlite3.connect(DATABASE_PATH)

    conn.row_factory = sqlite3.Row

    return conn