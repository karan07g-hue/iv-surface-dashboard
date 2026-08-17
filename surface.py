from fetcher import fetch_options
from pricing import implied_vol

def compute_surface(ticker_symbol, r = 0.05):
    """
    Fetch options for a ticker, compute IV for each one.
    Returns a DataFrame with columns: strike, expiry, T, options_type, iv, spot

    """
    df = fetch_options(ticker_symbol)

    if df.empty:
        print("No options data found")
        return df
    
    ivs = []
    failed = 0
    
    for i, row in df.iterrows():
        iv = implied_vol(
            market_price = row["market_price"],
            S = row["spot"],
            K = row["strike"],
            T = row["T"],
            r = r,
            option_type = row["option_type"]
        )
        if iv is not None and 0.01 < iv < 3.0:
            ivs.append(iv)
        else:
            ivs.append(None)
            failed += 1
    df["iv"] = ivs
    df = df.dropna(subset=["iv"])

    print(f"Computed IV for {len(df)} options ({failed}) failed)")
    return df

if __name__ == "__main__":
    df = compute_surface("SPY")
    print(f"\nIV range: {df['iv'].min():.2%} - {df['iv'].max():.2%}")
    print(f"Mean IV: {df['iv'].mean():.2%}")
    print(f"\nSample rows:")
    print(df[["strike", "expiry", "option_type", "market_price", "iv"]].head(15))
