"""
=========================================
Module : schema.py
Project: QuantLab
Purpose: Create Database Tables
=========================================
"""

from database.db import get_connection


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    # ===================================
    # Users
    # ===================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        full_name TEXT NOT NULL,

        email TEXT UNIQUE,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ===================================
    # Portfolios
    # ===================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolios(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        portfolio_name TEXT,

        benchmark TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)

    )
    """)

    # ===================================
    # Transactions
    # ===================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        portfolio_id INTEGER,

        ticker TEXT,

        trade_date DATE,

        transaction_type TEXT,

        quantity REAL,

        price REAL,

        FOREIGN KEY(portfolio_id)
        REFERENCES portfolios(id)

    )
    """)

    conn.commit()

    conn.close()

    print("=" * 50)
    print("Database Created Successfully")
    print("=" * 50)


if __name__ == "__main__":
    create_tables()