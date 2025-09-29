import pandas as pd
import numpy as np

def calculate_drawdown(returns):
    """Calculate drawdown from returns series"""
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    return drawdown

def calculate_volatility(returns):
    """Calculate annualized volatility"""
    if len(returns) == 0:
        return 0
    return returns.std() * np.sqrt(252)

def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    """Calculate Sharpe ratio"""
    if len(returns) == 0:
        return 0
    excess_returns = returns - risk_free_rate / 252  # Daily risk-free rate
    if excess_returns.std() == 0:
        return 0
    return np.sqrt(252) * excess_returns.mean() / excess_returns.std()

def calculate_sortino_ratio(returns, risk_free_rate=0.02):
    """Calculate Sortino ratio (uses downside deviation instead of total volatility)"""
    if len(returns) == 0:
        return 0
    
    excess_returns = returns - risk_free_rate / 252  # Daily risk-free rate
    
    # Calculate downside deviation (only negative returns)
    downside_returns = excess_returns[excess_returns < 0]
    if len(downside_returns) == 0:
        return float('inf') if excess_returns.mean() > 0 else 0
    
    downside_deviation = np.sqrt(np.mean(downside_returns**2))
    if downside_deviation == 0:
        return 0
    
    return (excess_returns.mean() / downside_deviation) * np.sqrt(252)

def calculate_calmar_ratio(annual_return, max_drawdown):
    """Calculate Calmar ratio (Annual Return / Max Drawdown)"""
    if max_drawdown == 0:
        return float('inf') if annual_return > 0 else 0
    
    # Convert percentages to decimals for calculation
    annual_return_decimal = annual_return / 100 if abs(annual_return) > 1 else annual_return
    max_drawdown_decimal = abs(max_drawdown / 100) if abs(max_drawdown) > 1 else abs(max_drawdown)
    
    if max_drawdown_decimal == 0:
        return float('inf') if annual_return_decimal > 0 else 0
    
    return annual_return_decimal / max_drawdown_decimal

def calculate_max_drawdown(returns):
    """Calculate maximum drawdown"""
    if len(returns) == 0:
        return 0
    drawdown = calculate_drawdown(returns)
    return drawdown.min()


def calculate_win_rate(trades):
    """Calculate win rate from trades"""
    if not trades:
        return 0
    profitable_trades = sum(1 for trade in trades if trade.get('profit_loss', 0) > 0)
    return profitable_trades / len(trades)

def calculate_profit_factor(trades):
    """Calculate profit factor"""
    if len(trades) == 0:
        return 0
    
    gross_profit = sum(trade.get('profit_loss', 0) for trade in trades if trade.get('profit_loss', 0) > 0)
    gross_loss = abs(sum(trade.get('profit_loss', 0) for trade in trades if trade.get('profit_loss', 0) < 0))
    
    if gross_loss == 0:
        return float('inf') if gross_profit > 0 else 0
    
    return gross_profit / gross_loss

def calculate_annual_return(initial_value, final_value, years):
    """Calculate annualized return"""
    if initial_value == 0 or years == 0:
        return 0
    return (final_value / initial_value) ** (1/years) - 1

def calculate_cumulative_return(initial_value, final_value):
    """Calculate cumulative return"""
    if initial_value == 0:
        return 0
    return (final_value - initial_value) / initial_value

def calculate_advanced_metrics(portfolio, data, trades):
    """Calculate comprehensive trading metrics"""
    if len(data) == 0 or len(trades) == 0:
        return {}
    
    try:
        # Get portfolio values and clean them
        portfolio_values = data['Portfolio_Value'].dropna()
        if len(portfolio_values) < 2:
            return {}
        
        # Remove any infinite or extremely large values that cause overflow
        portfolio_values = portfolio_values.replace([np.inf, -np.inf], np.nan).dropna()
        if len(portfolio_values) < 2:
            return {}
        
        # Calculate returns more safely
        returns = portfolio_values.pct_change().dropna()
        
        # Remove extreme outliers that cause overflow (returns > 1000% or < -100%)
        returns = returns[(returns > -1.0) & (returns < 10.0)]
        if len(returns) == 0:
            returns = pd.Series([0.0])  # Fallback to zero returns
        
        # Basic metrics using actual portfolio values
        initial_value = portfolio_values.iloc[0]
        final_value = portfolio_values.iloc[-1]
        total_return = calculate_cumulative_return(initial_value, final_value)
        
        # Calculate actual years from data length
        years = len(portfolio_values) / 252  # 252 trading days per year
        if years <= 0:
            years = 1.0
        
        # Calculate metrics with safety checks
        annual_return = calculate_annual_return(initial_value, final_value, years)
        volatility = calculate_volatility(returns) if len(returns) > 1 else 0
        sharpe_ratio = calculate_sharpe_ratio(returns) if len(returns) > 1 else 0
        sortino_ratio = calculate_sortino_ratio(returns) if len(returns) > 1 else 0
        
        # Max drawdown calculation (should use portfolio values, not returns)
        max_drawdown = calculate_max_drawdown(returns) if len(returns) > 1 else 0
        
        # Calmar ratio calculation
        calmar_ratio = calculate_calmar_ratio(annual_return * 100, max_drawdown * 100)
        
        # Trade-based metrics
        win_rate = calculate_win_rate(trades)
        profit_factor = calculate_profit_factor(trades)
        
        return {
            'total_return': total_return,
            'cumulative_return': total_return * 100,  # Convert to percentage
            'annual_return': annual_return * 100,  # Convert to percentage
            'volatility': min(volatility * 100, 999.99),  # Cap volatility at reasonable level
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'calmar_ratio': calmar_ratio,
            'max_drawdown': max_drawdown * 100,  # Convert to percentage
            'win_rate': win_rate * 100,  # Convert to percentage
            'profit_factor': profit_factor,
            'total_trades': len(trades),
            'years_traded': years,
            'trading_days': len(portfolio_values)
        }
        
    except Exception as e:
        print(f"⚠️ Error in metrics calculation: {e}")
        return {}
