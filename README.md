# Implied Volatility Surface Dashboard

An interactive Python dashboard that constructs implied volatility surfaces from live options market data. It fetches real-time options chains, inverts the Black-Scholes pricing model using numerical root-finding to extract implied volatility at every available strike and expiry, and renders the result as a rotatable 3D surface and 2D smile cross-sections in a Streamlit web interface.

The project is built around small, modular components: a data fetcher handles the market connection, a pricing engine implements Black-Scholes and the IV solver independently, a surface builder orchestrates the computation across the full options chain, and the dashboard ties everything together with interactive controls and visualisation.

## Why This Exists

Implied volatility is the single most important quantity in options trading. It represents the market's consensus forecast of future price uncertainty, extracted from the prices people are actually willing to pay for options right now. Every options market maker stares at a volatility surface all day. The shape of the surface encodes information that the Black-Scholes model itself cannot capture: fat tails (the smile), crash risk premiums (the skew), and term structure dynamics.

This project implements the full pipeline from raw market data to interactive surface visualisation, demonstrating options pricing theory, numerical methods, and data engineering in a single codebase.

## How It Works

The pipeline has four stages:

1. The fetcher pulls every available option for a given ticker from Yahoo Finance, filters out illiquid contracts (zero bids, no volume), computes time-to-expiry in years, and restricts to strikes within 20% of spot to avoid garbage data at the wings.

2. The pricing engine implements the Black-Scholes closed-form solution for European call and put prices. Since the BS formula cannot be algebraically inverted for volatility, the IV solver wraps it in a root-finding routine via scipy that searches for the volatility input which makes the model price match the observed market price.

3. The surface builder runs the IV solver across every option returned by the fetcher, discards solutions outside a sane range (1% to 200%), and returns a structured DataFrame of (strike, expiry, IV) triples.

4. The Streamlit dashboard provides a ticker input and compute button, renders summary metrics (spot price, number of options analysed, mean IV), a Plotly 3D scatter surface with hover details, and a 2D smile cross-section with a dropdown to select individual expiry dates.

## Repository Layout

    .
    ├── app.py              Streamlit dashboard with Plotly charts
    ├── fetcher.py          Options chain data pipeline from Yahoo Finance
    ├── pricing.py          Black-Scholes formula and IV solver
    ├── surface.py          IV computation across full options chain
    ├── requirements.txt    Python dependencies
    └── README.md

## Key Concepts

Implied Volatility: the volatility parameter that, when plugged into Black-Scholes, reproduces the observed market price of an option. It is not directly observable and must be numerically extracted from prices.

The Volatility Smile: IV is not constant across strikes. Options far from the current price trade at higher IV than at-the-money options. This pattern reflects the market pricing in fatter tails than a lognormal distribution would predict.

The Skew: for equity indices, the smile is asymmetric. Puts carry higher IV than calls. This reflects a crash risk premium that became pronounced after the 1987 crash.

## Setup

    git clone https://github.com/karan07g-hue/iv-surface-dashboard.git
    cd iv-surface-dashboard
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    streamlit run app.py

## Limitations

- Data quality: Yahoo Finance mid-prices are noisy for illiquid options, producing IV outliers at the wings and for short-dated contracts.
- No surface smoothing: raw IV points are plotted as-is. Professional vol surfaces apply SVI parameterisation for a continuous surface.
- Static rate assumption: uses a fixed 5% risk-free rate rather than term-matched Treasury rates.
- Solver coverage: fails on deep ITM options and very short-dated options. These are filtered out.
- European options assumption: Black-Scholes prices European options, but US equity options are American-style.

## Reference

Black, F. and Scholes, M. (1973). The Pricing of Options and Corporate Liabilities. Journal of Political Economy, 81(3), 637-654.

