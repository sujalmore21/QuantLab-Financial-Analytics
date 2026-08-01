"""
=========================================
Module  : valuation.py
Project : QuantLab
Purpose : Portfolio Valuation Calculations
=========================================
"""


def investment_value(quantity, purchase_price):
    """
    Calculate initial investment value.

    Parameters
    ----------
    quantity : int/float
        Number of shares

    purchase_price : float
        Purchase price per share

    Returns
    -------
    float
    """

    if quantity < 0 or purchase_price < 0:
        raise ValueError(
            "Quantity and price cannot be negative."
        )

    return quantity * purchase_price



def current_value(quantity, current_price):
    """
    Calculate current market value.

    Parameters
    ----------
    quantity : int/float

    current_price : float

    Returns
    -------
    float
    """

    if quantity < 0 or current_price < 0:
        raise ValueError(
            "Quantity and price cannot be negative."
        )

    return quantity * current_price



def profit_loss(quantity, purchase_price, current_price):
    """
    Calculate absolute profit or loss.

    Returns
    -------
    float
    """

    return (
        current_value(
            quantity,
            current_price
        )
        -
        investment_value(
            quantity,
            purchase_price
        )
    )



def profit_loss_percentage(
    quantity,
    purchase_price,
    current_price
):
    """
    Calculate profit/loss percentage.

    Returns
    -------
    float
    """

    invested = investment_value(
        quantity,
        purchase_price
    )

    if invested == 0:
        raise ValueError(
            "Investment value cannot be zero."
        )

    return (
        profit_loss(
            quantity,
            purchase_price,
            current_price
        )
        /
        invested
    )