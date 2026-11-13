
"""Historical market data for the Active Equity Portfolio Lab."""

from pathlib import Path

import pandas as pd
import yfinance as yf


TICKERS = ["MSFT", "GOOGL", "NEE"]
START_DATE = "2021-01-01"


def get_adjusted_prices(tickers, start_date=START_DATE):
    """Retrieve historical adjusted closing prices."""

    price_series = []

    for ticker in tickers:
        print(f"Downloading {ticker}...")

        history = yf.Ticker(ticker).history(
            start=start_date,
            interval="1d",
            auto_adjust=True,
            actions=False,
            raise_errors=True,
        )

        if history.empty or "Close" not in history:
            raise ValueError(f"No price data for {ticker}")

        close = history["Close"].copy()
        close.name = ticker

        close.index = (
            pd.to_datetime(close.index)
            .tz_localize(None)
            .normalize()
        )

        price_series.append(close)

    prices = pd.concat(price_series, axis=1)
    prices = prices.sort_index().dropna()

    if len(prices) < 2:
        raise ValueError("Not enough overlapping price data")

    return prices


def calculate_daily_returns(prices):
    """Calculate daily percentage returns."""
    return prices.pct_change(fill_method=None).dropna()


def main():
    prices = get_adjusted_prices(TICKERS)
    returns = calculate_daily_returns(prices)

    output = Path("data/processed")
    output.mkdir(parents=True, exist_ok=True)

    prices.to_csv(output / "adjusted_prices.csv")
    returns.to_csv(output / "daily_returns.csv")

    print("\nLatest adjusted prices:")
    print(prices.tail())

    print("\nLatest daily returns:")
    print(returns.tail())

    print("\nData saved successfully.")


if __name__ == "__main__":
    main()
