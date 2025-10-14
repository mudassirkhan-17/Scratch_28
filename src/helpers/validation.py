"""
Basic Input Validation Module
Provides simple validation functions for common input types
"""

def validate_positive_number(value, field_name="value", default=None):
    """Validate that a value is a positive number"""
    try:
        num = float(value)
        if num > 0:
            return num
        else:
            print(f"❌ {field_name} must be positive. Using default: {default}")
            return default
    except (ValueError, TypeError):
        print(f"❌ {field_name} must be a valid number. Using default: {default}")
        return default

def validate_integer(value, field_name="value", default=None):
    """Validate that a value is an integer"""
    try:
        num = int(value)
        return num
    except (ValueError, TypeError):
        print(f"❌ {field_name} must be a valid integer. Using default: {default}")
        return default

def validate_percentage(value, field_name="percentage", default=None):
    """Validate that a value is a valid percentage (0-100)"""
    try:
        num = float(value)
        if 0 <= num <= 100:
            return num
        else:
            print(f"❌ {field_name} must be between 0 and 100. Using default: {default}")
            return default
    except (ValueError, TypeError):
        print(f"❌ {field_name} must be a valid number. Using default: {default}")
        return default

def validate_choice(value, valid_choices, field_name="choice", default=None):
    """Validate that a value is one of the valid choices"""
    if value in valid_choices:
        return value
    else:
        print(f"❌ {field_name} must be one of {valid_choices}. Using default: {default}")
        return default

def validate_ticker(ticker):
    """Validate ticker symbol format"""
    if not ticker or not isinstance(ticker, str):
        print("❌ Ticker must be a non-empty string. Using default: AAPL")
        return "AAPL"
    
    ticker = ticker.upper().strip()
    if len(ticker) < 1 or len(ticker) > 10:
        print("❌ Ticker must be 1-10 characters. Using default: AAPL")
        return "AAPL"
    
    return ticker

def validate_timeframe_period(period):
    """Validate timeframe period format"""
    valid_periods = ["1y", "2y", "5y", "10y", "ytd", "6mo", "3mo", "1mo", "5d", "1d"]
    
    if period in valid_periods:
        return period
    
    # Check if it's a custom period (like "365d")
    if isinstance(period, str) and period.endswith('d'):
        try:
            days = int(period[:-1])
            if 1 <= days <= 3650:  # Max 10 years
                return period
        except ValueError:
            pass
    
    print(f"❌ Invalid period format. Using default: 1y")
    return "1y"

def validate_timeframe_interval(interval):
    """Validate timeframe interval format"""
    valid_intervals = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
    
    if interval in valid_intervals:
        return interval
    
    print(f"❌ Invalid interval format. Using default: 1d")
    return "1d"

def validate_stop_loss_take_profit(sl_value, tp_value, field_name="risk level"):
    """Validate stop loss and take profit values"""
    try:
        sl = float(sl_value)
        tp = float(tp_value)
        
        if sl < 0 or tp < 0:
            print(f"❌ {field_name} must be positive. Using defaults: SL=2%, TP=4%")
            return 2.0, 4.0
        
        if sl > 50 or tp > 100:  # Reasonable limits
            print(f"❌ {field_name} seems too high. Using defaults: SL=2%, TP=4%")
            return 2.0, 4.0
            
        return sl, tp
    except (ValueError, TypeError):
        print(f"❌ {field_name} must be valid numbers. Using defaults: SL=2%, TP=4%")
        return 2.0, 4.0

def validate_timeframe_combination(period, interval):
    """Validate that period and interval combination makes sense"""
    # Define reasonable combinations
    valid_combinations = {
        "1m": ["1d", "5d", "1mo"],
        "2m": ["1d", "5d", "1mo", "3mo"],
        "5m": ["1d", "5d", "1mo", "3mo", "6mo"],
        "15m": ["1d", "5d", "1mo", "3mo", "6mo", "1y"],
        "30m": ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y"],
        "60m": ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"],
        "1h": ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"],
        "1d": ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y"],
        "1wk": ["3mo", "6mo", "1y", "2y", "5y", "10y"],
        "1mo": ["1y", "2y", "5y", "10y"]
    }
    
    if interval in valid_combinations:
        if period not in valid_combinations[interval]:
            print(f"❌ Invalid combination: {period} period with {interval} interval")
            print(f"💡 For {interval} interval, use: {', '.join(valid_combinations[interval])}")
            return False
    
    return True

def validate_capital_allocation(total_capital, per_trade_amount, allocation_percent):
    """Validate capital allocation makes sense"""
    errors = []
    
    # Check per-trade amount vs total capital
    if per_trade_amount > total_capital:
        errors.append(f"Per-trade amount (${per_trade_amount:,.2f}) cannot exceed total capital (${total_capital:,.2f})")
    
    # Check allocation percentage
    if allocation_percent > 100:
        errors.append(f"Allocation percentage ({allocation_percent}%) cannot exceed 100%")
    
    if allocation_percent <= 0:
        errors.append(f"Allocation percentage ({allocation_percent}%) must be positive")
    
    # Check if calculated amount matches
    calculated_amount = total_capital * (allocation_percent / 100)
    if abs(calculated_amount - per_trade_amount) > 1:  # Allow $1 difference for rounding
        errors.append(f"Calculated amount (${calculated_amount:,.2f}) doesn't match per-trade amount (${per_trade_amount:,.2f})")
    
    if errors:
        print("❌ Capital allocation errors:")
        for error in errors:
            print(f"   • {error}")
        return False
    
    return True

def validate_multi_ticker_allocations(allocations):
    """Validate multi-ticker allocation percentages add up correctly"""
    total_allocation = sum(allocations.values())
    
    if abs(total_allocation - 1.0) > 0.01:  # Allow 1% difference for rounding
        print(f"❌ Allocation percentages don't add up to 100%")
        print(f"   Current total: {total_allocation * 100:.1f}%")
        print(f"   Expected: 100.0%")
        return False
    
    for ticker, allocation in allocations.items():
        if allocation <= 0:
            print(f"❌ {ticker} allocation ({allocation * 100:.1f}%) must be positive")
            return False
        if allocation > 1:
            print(f"❌ {ticker} allocation ({allocation * 100:.1f}%) cannot exceed 100%")
            return False
    
    return True

def validate_stop_loss_take_profit_logic(sl_percent, tp_percent):
    """Validate SL/TP logic makes sense"""
    if sl_percent <= 0:
        print("❌ Stop Loss must be positive")
        return False
    
    if tp_percent <= 0:
        print("❌ Take Profit must be positive")
        return False
    
    if sl_percent >= tp_percent:
        print(f"❌ Stop Loss ({sl_percent}%) should be less than Take Profit ({tp_percent}%)")
        print("💡 Otherwise you'll lose money on every trade!")
        return False
    
    if sl_percent > 20:
        print(f"⚠️  Stop Loss ({sl_percent}%) seems high - consider if this is intentional")
    
    if tp_percent > 50:
        print(f"⚠️  Take Profit ({tp_percent}%) seems high - consider if this is realistic")
    
    return True

def validate_indicator_logic(indicator1_name, indicator1_params, indicator2_name, indicator2_params, strategy_type):
    """Validate indicator comparison makes logical sense"""
    # Check for impossible SMA comparisons
    if (indicator1_name == "SMA" and indicator2_name == "SMA" and 
        len(indicator1_params) > 0 and len(indicator2_params) > 0):
        
        period1 = indicator1_params[0]
        period2 = indicator2_params[0]
        
        if strategy_type in ["CROSSED UP", "GREATER THAN"] and period1 >= period2:
            print(f"⚠️  Warning: SMA({period1}) crossing above SMA({period2})")
            print("💡 Shorter period SMA typically moves faster - this might be unusual")
        
        if strategy_type in ["CROSSED DOWN", "LESS THAN"] and period1 <= period2:
            print(f"⚠️  Warning: SMA({period1}) crossing below SMA({period2})")
            print("💡 Longer period SMA typically moves slower - this might be unusual")
    
    # Check for RSI extreme values
    if indicator1_name == "RSI" and len(indicator1_params) > 0:
        period = indicator1_params[0]
        if period < 5 or period > 50:
            print(f"⚠️  Warning: RSI period ({period}) is unusual")
            print("💡 Common RSI periods are 14, 21, or 30")
    
    return True

def validate_candles_ago(candles_ago, data_length=None):
    """Validate candles ago parameter"""
    if candles_ago < 0:
        print("❌ Candles ago cannot be negative")
        return False
    
    if data_length and candles_ago >= data_length:
        print(f"❌ Candles ago ({candles_ago}) cannot exceed data length ({data_length})")
        return False
    
    if candles_ago > 10:
        print(f"⚠️  Warning: Using {candles_ago} candles ago might be too far back")
        print("💡 Consider using more recent data for better signals")
    
    return True
