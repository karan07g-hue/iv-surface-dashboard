import numpy as np
from scipy.stats import norm

def bs_prices(S,K,T, r, sigma, option_type ="call"):
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
        prices = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        prices = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return prices

# TESTING:
if __name__ == "__main__":
    # Test with known values: S = 200, K = 210, T = 0.25, r = 0.05, sigma = 0.20
    call = bs_prices(200, 210, 0.25, 0.05, 0.20, "call")
    put = bs_prices(200, 210, 0.25, 0.05, 0.20, "put")
    print(f"Call price: ${call:.2f}")
    print(f"Put price: ${put:.2f}") 


    
