import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt

#Extend DCF to include Monte Carlo Simulation for Expected Returns

def calculate_dcf(cash_flows, discount_rate, num_simulations=1000):
    """
    Calculate the DCF-based expected return for an asset using Monte Carlo simulations.
    """
    n = len(cash_flows)
    # Simulate cash flow uncertainty (using a normal distribution for simplicity)
    simulated_cash_flows = np.random.normal(cash_flows, 0.05 * np.array(cash_flows), (num_simulations, n))

    discounted_values = [np.sum([simulated_cash_flows[i][t] / (1 + discount_rate) ** (t + 1)
                                 for t in range(n)]) for i in range(num_simulations)]

    # Take the mean of the simulated discounted values as the expected return
    return np.mean(discounted_values)

# Include Value at Risk (VaR) and Conditional VaR (CVaR)
def calculate_var_cvar(returns, confidence_level=0.95):
    """
    Calculate Value at Risk (VaR) and Conditional Value at Risk (CVaR).
    """
    sorted_returns = np.sort(returns)
    index = int((1 - confidence_level) * len(sorted_returns))
    var = sorted_returns[index]
    cvar = np.mean(sorted_returns[:index])
    return var, cvar

#Calculate Sharpe Ratio
def calculate_sharpe_ratio(portfolio_return, portfolio_stddev, risk_free_rate=0.01):
    """
    Calculate the Sharpe Ratio for a portfolio.
    """
    return (portfolio_return - risk_free_rate) / portfolio_stddev

#Fama-French Three Factor Model for Expected Returns
def fama_french_three_factor_model(market_returns, smb, hml, risk_free_rate=0.01):
    """
    Calculate expected returns using the Fama-French Three-Factor Model.
    """
    market_premium = market_returns - risk_free_rate
    return risk_free_rate + 0.5 * market_premium + 0.3 * smb + 0.2 * hml  # Example factor weights

#Rebalancing Strategy
def rebalance_portfolio(weights, target_weights, tolerance=0.05):
    """
    Rebalance portfolio to target weights within a tolerance level.
    """
    deviation = np.abs(weights - target_weights)
    if np.any(deviation > tolerance):
        return target_weights
    else:
        return weights

#Efficient Frontier and Optimization (from previous code)
def portfolio_performance(weights, mean_returns, cov_matrix):
    portfolio_return = np.dot(weights, mean_returns)
    portfolio_stddev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return portfolio_return, portfolio_stddev

def minimize_risk(weights, mean_returns, cov_matrix):
    return portfolio_performance(weights, mean_returns, cov_matrix)[1]

def efficient_frontier(mean_returns, cov_matrix, target_return):
    n_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)
    constraints = ({'type': 'eq', 'fun': lambda x: portfolio_performance(x, mean_returns, cov_matrix)[0] - target_return},
                   {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for asset in range(n_assets))
    result = minimize(minimize_risk, n_assets * [1. / n_assets], args=args, bounds=bounds, constraints=constraints)
    return result.x

#Fetch Real Market Data (using yfinance)
import yfinance as yf

def fetch_market_data(ticker, start_date, end_date):
    """
    Fetch historical market data from Yahoo Finance.
    """
    data = yf.download(ticker, start=start_date, end=end_date)
    return data['Adj Close']

# Example data for stocks (use real tickers in practice)
tickers = ['AAPL', 'MSFT', 'GOOGL']
start_date = '2020-01-01'
end_date = '2023-01-01'
# Calculate daily returns from the price data
price_df = pd.DataFrame(price_data)
returns = price_df.pct_change().dropna()

#Calculate mean returns and covariance matrix from historical returns
mean_returns = returns.mean()  # Average returns for each asset
cov_matrix = returns.cov()     # Covariance matrix of returns

#Run the efficient frontier function with the calculated values
optimal_weights = efficient_frontier(mean_returns, cov_matrix, target_return=0.02)
print("Optimal Portfolio Weights:", optimal_weights)
# Fetch historical data
price_data = {ticker: fetch_market_data(ticker, start_date, end_date) for ticker in tickers}

#Active Management with Transaction Costs
def adjust_portfolio_with_costs(weights, market_signal, transaction_cost=0.005):
    """
    Adjust portfolio weights dynamically based on market signals, accounting for transaction costs.
    """
    new_weights = weights * (1 + market_signal)
    return new_weights * (1 - transaction_cost)

# Visualize Efficient Frontier (as before)
def plot_efficient_frontier(mean_returns, cov_matrix):
    target_returns = np.linspace(min(mean_returns), max(mean_returns), 100)
    risks = [minimize_risk(efficient_frontier(mean_returns, cov_matrix, ret), mean_returns, cov_matrix) for ret in target_returns]
    plt.plot(risks, target_returns, label='Efficient Frontier')
    plt.xlabel('Risk (Standard Deviation)')
    plt.ylabel('Return')
    plt.title('Efficient Frontier')
    plt.show()

# Example of running the extended model
optimal_weights = efficient_frontier(mean_returns, cov_matrix, target_return=0.02)
print("Optimal Portfolio Weights:", optimal_weights)

# Simulate market signals and transaction costs
adjusted_weights = adjust_portfolio_with_costs(optimal_weights, market_signal=0.01)
print("Adjusted Weights (after market signal):", adjusted_weights)

# Run VaR and CVaR on simulated returns
portfolio_returns = np.dot(returns, optimal_weights)
var, cvar = calculate_var_cvar(portfolio_returns)
print(f"Value at Risk (VaR): {var:.4f}, Conditional Value at Risk (CVaR): {cvar:.4f}")
