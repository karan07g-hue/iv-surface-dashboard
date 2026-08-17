import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

def bs_price(S,K,T, r, sigma, option_type ="call"):
    """
    Black-Scholes option pricing formula
    S: spot price
    K: strike price
    T: time to expiry(years)
    r: risk-free rate
    sigma: volatility
    option_type: "call" or "put"
    """

    d1 = (np.log(S/K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return price

def implied_vol(market_price, S, K, T, r, option_type="call"):
    """
    Solve for thr volaltility that makes Black-Scholes match the market price
    Returns IV as a decimal(e.g., 0.20 = 20%).
    Returns None if solver fails(bad data, no solution).
    """
    def objective(sigma):
        return bs_price(S,K,T,r, sigma, option_type) - market_price

    try:
        iv = brentq(objective, 0.001, 5.0, xtol = 1e-6)
        return iv
    except ValueError:
        return None
    


# TESTING:
if __name__ == "__main__":
    # Test Black-Scholes pricing
    call = bs_price(200, 210, 0.25, 0.05, 0.20, "call")
    put = bs_price(200, 210, 0.25, 0.05, 0.20, "put")
    print(f"Call price: ${call:.2f}")
    print(f"Put price: ${put:.2f}") 

    # Test IV solver: feed in the price we just computed, should recover sgima = 0.20
    recovered_iv = implied_vol( call,200, 210, 0.25, 0.05, "call")
    print(f"Recovered IV: {recovered_iv:.4f}")
    print(f"Expected IV: 0.2000")


    
