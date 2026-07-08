"""
market_data.py
A mock market data provider so the system runs standalone without any
external API keys. Swap this out for a real market data feed in production.
"""

import random

random.seed(7)

ASSET_CLASSES = ["Equity", "Bonds", "Gold", "REITs", "Cash/Money Market", "International Equity"]


def get_mock_market_snapshot() -> dict:
    """Returns a simulated snapshot of market conditions."""
    return {
        "equity_trend": random.choice(["BULLISH", "NEUTRAL", "BEARISH"]),
        "interest_rate_environment": random.choice(["RISING", "STABLE", "FALLING"]),
        "inflation_outlook": random.choice(["HIGH", "MODERATE", "LOW"]),
        "volatility_index": round(random.uniform(12, 35), 1),  # like a mock VIX
        "sector_momentum": {
            "Technology": round(random.uniform(-5, 15), 1),
            "Healthcare": round(random.uniform(-3, 10), 1),
            "Financials": round(random.uniform(-4, 12), 1),
            "Energy": round(random.uniform(-8, 20), 1),
            "Consumer Staples": round(random.uniform(-2, 8), 1),
        },
    }


def get_asset_class_returns() -> dict:
    """Simulated historical average annual returns per asset class (%)."""
    return {
        "Equity": 11.5,
        "International Equity": 9.0,
        "Bonds": 6.5,
        "Gold": 7.0,
        "REITs": 8.5,
        "Cash/Money Market": 4.0,
    }
