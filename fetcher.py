import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_options(ticker_symbol):
    """
    Fetch all options for a ticker, return a clean DataFrame with:
    strike, expiry, days_to_expire, T(years), option_type, market_price, spot
    """

    ticker = yf.Ticker(ticker_symbol)
    spot = ticker.history(period = "1d")["Close"].iloc[-1]
    expiry_dates = ticker.options

    all_options = []

    for expiry in expiry_dates:
        chain  = ticker.option_chain(expiry)

        for option_type, data in [("call", chain.calls), ("put", chain.puts)]:
            for _, row in data.iterrows():
                # Use mid price(average of bid and ask) for accuracy
                mid_price = (row["bid"] + row["ask"])/2

                # Skip if no real market(zero bid or zero volume)
                if row["bid"] <= 0 or row["ask"] <= 0:
                    continue
                if row["volume"] is None or row["volume"] <= 0:
                    continue

                # Compute time to expiry in years
                expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
                days = (expiry_date - datetime.now()).days
                if days <= 0:
                    continue
                T = days/ 365.0

                # Filter: only keep options within 20% of spot price
                if row["strike"] < spot * 0.80 or row["strike"] > spot * 1.20:
                    continue

                all_options.append({
                    "strike": row["strike"],
                    "expiry": expiry,
                    "days_to_expiry": days,
                    "T": T,
                    "option_type": option_type,
                    "market_price" : mid_price,
                    "spot" : spot

                })
    df = pd.DataFrame(all_options)
    return df
if __name__ == "__main__":
    df = fetch_options("SPY")
    print(f"Spot price: ${df['spot'].iloc[0]:.2f}")
    print(f"Total options fetched: {len(df)}")
    print(f"Expiry dates: {df['expiry'].nunique()}")
    print(f"Strike range: ${df['strike'].min():.0f} - ${df['strike'].max():.0f}")
    print(df.head(10))
        
