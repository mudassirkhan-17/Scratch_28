from indicators import *
from comparisons import *
from display import *
from metrics import *
from comparision_types import ComparisonType
import yfinance as yf
# Multi-condition detector will be imported when needed



"""Get user inputs for trading strategy"""

"""
1) ticker
2) period, interval
3) entry comparison 1, which is the first comparison between indicators, constants, or price
4) get candles ago for entry comparison 1'
5) entry strategy get_strategy_selection()
6) entry comparision 2 and then exit start



"""

def get_strategy_inputs():

    print("\n" + "="*60)
    print("TRADING STRATEGY SELECTION")
    print("="*60)
    
    # Ticker
    ticker = input("Enter ticker symbol [default: AAPL]: ").upper().strip()
    if not ticker: ticker = "AAPL" # If empty input, default to AAPL

    period, interval = get_time_interval_inputs() # Time interval selection
    
    # Capital Management
    total_capital = get_total_capital()
    per_trade_config = get_per_trade_allocation(total_capital)
    
    print("\n--- ENTRY STRATEGY ---")
    
    """Capture comparision between indicators, constants, or price"""

    print("Entry Comparison 1:") # Entry Comparison 1
    entry_comp1_type = get_comparison_type()
    if entry_comp1_type is None:
        entry_comp1_type = ComparisonType.INDICATOR # If empty input, default to indicators
    
    if entry_comp1_type == ComparisonType.INDICATOR: # tracking which option is selected
        entry_comp1_name = get_indicator_selection() # get indicator selection
        if entry_comp1_name is None:
            entry_comp1_name = "SMA" # If empty input, default to SMA
        entry_comp1_params = get_indicator_params(entry_comp1_name)
    elif entry_comp1_type == ComparisonType.CONSTANT: # get constant value
        entry_comp1_name = "CONSTANT"
        entry_comp1_params = (get_constant_value(),)
    else:  # PRICE # get price column
        entry_comp1_name = "PRICE"
        entry_comp1_params = (get_price_column(),)
    
    
    entry_comp1_candles_ago = get_candles_ago("Entry Comparison 1") # Get candles ago for entry comparison 1
    
    # Entry Strategy
    entry_strategy = get_strategy_selection()
    if entry_strategy is None:
        return None
    
    # Entry Comparison 2
    print("\nEntry Comparison 2:")
    entry_comp2_type = get_comparison_type()
    if entry_comp2_type is None:
        return None
    
    if entry_comp2_type == ComparisonType.INDICATOR:
        entry_comp2_name = get_indicator_selection()
        if entry_comp2_name is None:
            return None
        entry_comp2_params = get_indicator_params(entry_comp2_name)
    elif entry_comp2_type == ComparisonType.CONSTANT:
        entry_comp2_name = "CONSTANT"
        entry_comp2_params = (get_constant_value(),)
    else:  # PRICE
        entry_comp2_name = "PRICE"
        entry_comp2_params = (get_price_column(),)
    
    # Get candles ago for entry comparison 2
    entry_comp2_candles_ago = get_candles_ago("Entry Comparison 2")
    
    # Exit Strategy
    print("\n--- EXIT STRATEGY ---")
    
    # Exit Comparison 1
    print("Exit Comparison 1:")
    exit_comp1_type = get_comparison_type()
    if exit_comp1_type is None:
        return None
    
    if exit_comp1_type == ComparisonType.INDICATOR:
        exit_comp1_name = get_indicator_selection()
        if exit_comp1_name is None:
            return None
        exit_comp1_params = get_indicator_params(exit_comp1_name)
    elif exit_comp1_type == ComparisonType.CONSTANT:
        exit_comp1_name = "CONSTANT"
        exit_comp1_params = (get_constant_value(),)
    else:  # PRICE
        exit_comp1_name = "PRICE"
        exit_comp1_params = (get_price_column(),)
    
    # Get candles ago for exit comparison 1
    exit_comp1_candles_ago = get_candles_ago("Exit Comparison 1")
    
    # Exit Strategy
    exit_strategy = get_strategy_selection()
    if exit_strategy is None:
        return None
    
    # Exit Comparison 2
    print("\nExit Comparison 2:")
    exit_comp2_type = get_comparison_type()
    if exit_comp2_type is None:
        return None
    
    if exit_comp2_type == ComparisonType.INDICATOR:
        exit_comp2_name = get_indicator_selection()
        if exit_comp2_name is None:
            return None
        exit_comp2_params = get_indicator_params(exit_comp2_name)
    elif exit_comp2_type == ComparisonType.CONSTANT:
        exit_comp2_name = "CONSTANT"
        exit_comp2_params = (get_constant_value(),)
    else:  # PRICE
        exit_comp2_name = "PRICE"
        exit_comp2_params = (get_price_column(),)
    
    # Get candles ago for exit comparison 2
    exit_comp2_candles_ago = get_candles_ago("Exit Comparison 2")
    
    return (ticker, period, interval, total_capital, per_trade_config, entry_comp1_type, entry_comp1_name, entry_comp1_params,
            entry_comp2_type, entry_comp2_name, entry_comp2_params,
            exit_comp1_type, exit_comp1_name, exit_comp1_params,
            exit_comp2_type, exit_comp2_name, exit_comp2_params,
            entry_strategy, exit_strategy, entry_comp1_candles_ago, entry_comp2_candles_ago,
            exit_comp1_candles_ago, exit_comp2_candles_ago)

def get_strategy_direction():
    """Get strategy direction selection"""
    print("\n--- STRATEGY DIRECTION ---")
    print("1. Long Only (Buy on crossover, sell on crossdown)")
    print("2. Short Only (Sell on crossdown, buy on crossover)")
    print("3. Long/Short Reversal (Flip positions automatically)")
    
    while True:
        try:
            choice = input("Enter choice (1-3) [default: 1]: ").strip()
            
            # If empty input, default to 1
            if not choice:
                choice = "1"
            
            direction_map = {
                "1": "Long Only",
                "2": "Short Only", 
                "3": "Long/Short Reversal"
            }
            
            if choice in direction_map:
                return direction_map[choice]
            else:
                print("❌ Invalid choice! Please enter 1, 2, or 3.")
                continue
                
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled!")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

def get_strategy_selection():
    """Get strategy selection"""
    print("\nSelect Strategy:")
    strategies = ["CROSSED UP", "CROSSED DOWN", "GREATER THAN", "LESS THAN", "EQUAL", 
                  "GREATER OR EQUAL", "LESS OR EQUAL", "WITHIN RANGE", "INCREASED", "DECREASED", "CROSSED"]
    for i, strategy in enumerate(strategies, 1):
        print(f"{i}. {strategy}")
    choice = input(f"Enter choice (1-{len(strategies)}) [default: 1]: ").strip()
    
    # If empty input, default to 1
    if not choice:
        choice = "1"
    
    try:
        return strategies[int(choice)-1]
    except (ValueError, IndexError):
        print("❌ Invalid choice!")
        return None

def show_trading_examples():
    """Show examples of trading strategies"""
    print("\n" + "="*60)
    print("TRADING STRATEGY EXAMPLES")
    print("="*60)
    print("✅ PRACTICAL STRATEGIES:")
    print("1. SMA(10) crosses SMA(20) - Classic trend following")
    print("2. EMA(12) crosses EMA(26) - MACD-style crossover")
    print("3. RSI(14) > 70 - Overbought signal")
    print("4. RSI(14) < 30 - Oversold signal")
    print("5. Close > SMA(20) - Price above trend")
    print("6. High > 100 - Price breakout")
    print("7. Low < 50 - Price breakdown")
    print("8. Open crosses Close - Gap analysis")
    print("\n🚀 CANDLES AGO STRATEGIES (NEW!):")
    print("9. RSI(14) 0 cdl. ago > RSI(14) 1 cdl. ago - RSI momentum building")
    print("10. Close 0 cdl. ago > Close 1 cdl. ago - Price momentum")
    print("11. MACD 0 cdl. ago > MACD 1 cdl. ago - MACD momentum")
    print("12. Volume 0 cdl. ago > Volume 1 cdl. ago - Volume increasing")
    print("13. Price 0 cdl. ago crosses Price 1 cdl. ago - Price reversal")
    print("14. RSI 0 cdl. ago vs Price 0 cdl. ago divergence - Divergence analysis")
    print("="*60)

def get_comparison_type():
    """Get comparison type selection"""
    print("\nSelect Comparison Type:")
    print("1. Indicators (Active)")
    print("2. Constant Value (Active)")
    print("3. Price (Active)")
    choice = input("Enter choice (1-3) [default: 1]: ").strip()
    
    # If empty input, default to 1
    if not choice:
        choice = "1"
    
    if choice == "1":
        return ComparisonType.INDICATOR
    elif choice == "2":
        return ComparisonType.CONSTANT
    elif choice == "3":
        return ComparisonType.PRICE
    else:
        print("❌ Choosing Default: Indicators")
        return ComparisonType.INDICATOR

def get_indicator_selection():
    """Get indicator selection"""
    print("\nSelect Indicator:")
    indicators = indicator_registry.list_indicators()
    for i, indicator in enumerate(indicators, 1):
        print(f"{i}. {indicator}")
    choice = input(f"Enter choice (1-{len(indicators)}) [default: 1]: ").strip()
    
    # If empty input, default to 1
    if not choice:
        choice = "1"
    
    try:
        return indicators[int(choice)-1]
    except (ValueError, IndexError):
        print("❌ Choosing Default: SMA")
        return "SMA"
        return None

def get_indicator_params(indicator_name):
    """Get parameters for indicator"""
    if indicator_name in ["RSI", "RSI2"]:
        length = int(input(f"{indicator_name} Length (default 14): ") or "14")
        upper = int(input(f"{indicator_name} Upper Level (default 70): ") or "70")
        lower = int(input(f"{indicator_name} Lower Level (default 30): ") or "30")
        return (length, upper, lower)
    elif indicator_name in ["SSMA"]:
        period = int(input(f"{indicator_name} Period (default 14): ") or "14")
        upper = float(input(f"{indicator_name} Upper Threshold (default 1.0): ") or "1.0")
        lower = float(input(f"{indicator_name} Lower Threshold (default -1.0): ") or "-1.0")
        return (period, upper, lower)
    elif indicator_name in ["EMA2"]:
        period = int(input(f"{indicator_name} Period (default 20): ") or "20")
        upper = float(input(f"{indicator_name} Upper Threshold (default 0.03): ") or "0.03")
        lower = float(input(f"{indicator_name} Lower Threshold (default -0.03): ") or "-0.03")
        return (period, upper, lower)
    elif indicator_name in ["MOMENTUM"]:
        period = int(input(f"{indicator_name} Period (default 10): ") or "10")
        upper = float(input(f"{indicator_name} Upper Threshold (default 1.0): ") or "1.0")
        lower = float(input(f"{indicator_name} Lower Threshold (default -1.0): ") or "-1.0")
        return (period, upper, lower)
    elif indicator_name in ["MARKET_MOMENTUM"]:
        period = int(input(f"{indicator_name} Period (default 14): ") or "14")
        upper = float(input(f"{indicator_name} Upper Threshold (default 0.05): ") or "0.05")
        lower = float(input(f"{indicator_name} Lower Threshold (default -0.05): ") or "-0.05")
        return (period, upper, lower)
    elif indicator_name in ["OBV"]:
        baseline = float(input(f"{indicator_name} Baseline (default 0): ") or "0")
        upper = float(input(f"{indicator_name} Upper Threshold (default 100000): ") or "100000")
        lower = float(input(f"{indicator_name} Lower Threshold (default -100000): ") or "-100000")
        return (baseline, upper, lower)
    elif indicator_name in ["TYPICAL_PRICE", "VWAP"]:
        threshold = float(input(f"{indicator_name} Threshold (default 0.01): ") or "0.01")
        return (threshold,)
    elif indicator_name == "ALL_MA":
        short = int(input(f"{indicator_name} Short Period (default 5): ") or "5")
        medium = int(input(f"{indicator_name} Medium Period (default 20): ") or "20")
        long = int(input(f"{indicator_name} Long Period (default 50): ") or "50")
        threshold = float(input(f"{indicator_name} Threshold Percent (default 0.02): ") or "0.02")
        return (short, medium, long, threshold)
    elif indicator_name == "DEMA":
        period = int(input(f"{indicator_name} Period (default 20): ") or "20")
        distance = float(input(f"{indicator_name} Distance Threshold (default 0.01): ") or "0.01")
        return (period, distance)
    elif indicator_name == "HULL_MA":
        period = int(input(f"{indicator_name} Period (default 14): ") or "14")
        price_threshold = float(input(f"{indicator_name} Price Threshold (default 0.01): ") or "0.01")
        return (period, price_threshold)
    elif indicator_name == "KAMA":
        period = int(input(f"{indicator_name} Period (default 10): ") or "10")
        fast = int(input(f"{indicator_name} Fast Period (default 2): ") or "2")
        slow = int(input(f"{indicator_name} Slow Period (default 30): ") or "30")
        distance = float(input(f"{indicator_name} Distance Threshold (default 0.01): ") or "0.01")
        return (period, fast, slow, distance)
    elif indicator_name == "JMA":
        period = int(input(f"{indicator_name} Period (default 20): ") or "20")
        phase = float(input(f"{indicator_name} Phase (default 0.0): ") or "0.0")
        power = float(input(f"{indicator_name} Power (default 1.0): ") or "1.0")
        distance = float(input(f"{indicator_name} Distance Threshold (default 0.01): ") or "0.01")
        return (period, phase, power, distance)
    elif indicator_name == "FRAMA":
        period = int(input(f"{indicator_name} Period (default 10): ") or "10")
        upper_div = float(input(f"{indicator_name} Upper Divergence (default 0.03): ") or "0.03")
        lower_div = float(input(f"{indicator_name} Lower Divergence (default -0.03): ") or "-0.03")
        return (period, upper_div, lower_div)
    elif indicator_name == "SEMA":
        period = int(input(f"{indicator_name} Period (default 14): ") or "14")
        baseline = float(input(f"{indicator_name} Baseline (default 0): ") or "0")
        upper = float(input(f"{indicator_name} Upper Threshold (default 1.0): ") or "1.0")
        lower = float(input(f"{indicator_name} Lower Threshold (default -1.0): ") or "-1.0")
        return (period, baseline, upper, lower)
    elif indicator_name == "TRIANGULAR_MA":
        period = int(input(f"{indicator_name} Period (default 20): ") or "20")
        threshold = float(input(f"{indicator_name} Threshold Percentage (default 0.01): ") or "0.01")
        return (period, threshold)
    elif indicator_name == "T3_MA":
        period = int(input(f"{indicator_name} Period (default 10): ") or "10")
        v = float(input(f"{indicator_name} V Factor (default 0.7): ") or "0.7")
        price_col = input(f"{indicator_name} Price Column (default Close): ") or "Close"
        pos = float(input(f"{indicator_name} Positive Threshold (default 0.02): ") or "0.02")
        neg = float(input(f"{indicator_name} Negative Threshold (default -0.02): ") or "-0.02")
        return (period, v, price_col, pos, neg)
    elif indicator_name in ["ZLEMA", "ZLSMA", "WMA", "VWMA"]:
        period = int(input(f"{indicator_name} Period (default 14): ") or "14")
        deviation = float(input(f"{indicator_name} Deviation Threshold (default 0.01): ") or "0.01")
        return (period, deviation)
    elif indicator_name == "MCGINLEY_DYNAMIC":
        period = int(input(f"{indicator_name} Period (default 14): ") or "14")
        threshold = float(input(f"{indicator_name} Threshold (default 0.01): ") or "0.01")
        return (period, threshold)
    elif indicator_name in ["EVMA"]:
        period = int(input(f"{indicator_name} Period (default 14): ") or "14")
        upper = float(input(f"{indicator_name} Upper Threshold (default 0.01): ") or "0.01")
        lower = float(input(f"{indicator_name} Lower Threshold (default -0.01): ") or "-0.01")
        return (period, upper, lower)
    elif indicator_name == "SINE_WMA":
        period = int(input(f"{indicator_name} Period (default 14): ") or "14")
        baseline = float(input(f"{indicator_name} Baseline (default 0): ") or "0")
        upper = float(input(f"{indicator_name} Upper Threshold (default 1.0): ") or "1.0")
        lower = float(input(f"{indicator_name} Lower Threshold (default -1.0): ") or "-1.0")
        return (period, baseline, upper, lower)
    elif indicator_name == "PASCAL_WMA":
        period = int(input(f"{indicator_name} Period (default 10): ") or "10")
        lower = float(input(f"{indicator_name} Lower Threshold (default -1): ") or "-1")
        upper = float(input(f"{indicator_name} Upper Threshold (default 1): ") or "1")
        return (period, lower, upper)
    elif indicator_name == "SYMMETRIC_WMA":
        period = int(input(f"{indicator_name} Period (default 5): ") or "5")
        price_col = input(f"{indicator_name} Price Column (default Close): ") or "Close"
        pos = float(input(f"{indicator_name} Positive Threshold (default 0.02): ") or "0.02")
        neg = float(input(f"{indicator_name} Negative Threshold (default -0.02): ") or "-0.02")
        return (period, price_col, pos, neg)
    elif indicator_name == "FIBONACCI_WMA":
        period = int(input(f"{indicator_name} Period (default 10): ") or "10")
        upper = float(input(f"{indicator_name} Upper Threshold (default 0.03): ") or "0.03")
        lower = float(input(f"{indicator_name} Lower Threshold (default -0.03): ") or "-0.03")
        return (period, upper, lower)
    elif indicator_name == "HOLT_WINTER_MA":
        alpha = float(input(f"{indicator_name} Alpha (default 0.2): ") or "0.2")
        beta = float(input(f"{indicator_name} Beta (default 0.1): ") or "0.1")
        deviation = float(input(f"{indicator_name} Deviation Threshold (default 2.0): ") or "2.0")
        return (alpha, beta, deviation)
    elif indicator_name == "HULL_EMA":
        period = int(input(f"{indicator_name} Period (default 14): ") or "14")
        deviation = float(input(f"{indicator_name} Deviation Threshold (default 2.0): ") or "2.0")
        return (period, deviation)
    elif indicator_name == "ALMA":
        period = int(input(f"{indicator_name} Period (default 14): ") or "14")
        offset = float(input(f"{indicator_name} Offset (default 0.85): ") or "0.85")
        sigma = float(input(f"{indicator_name} Sigma (default 6): ") or "6")
        baseline = float(input(f"{indicator_name} Baseline (default 0): ") or "0")
        lower = float(input(f"{indicator_name} Lower Threshold (default -0.5): ") or "-0.5")
        upper = float(input(f"{indicator_name} Upper Threshold (default 0.5): ") or "0.5")
        return (period, offset, sigma, baseline, lower, upper)
    # Volume Indicators
    elif indicator_name in ["AOBV", "FVE", "NVI", "PVI", "PVR", "PVT", "PV", "VAMA", "VFI", "VPT", "VP", "VZO", "WOBV"]:
        period = int(input(f"{indicator_name} Period (default 14): ") or "14")
        upper = float(input(f"{indicator_name} Upper Threshold (default 0.05): ") or "0.05")
        lower = float(input(f"{indicator_name} Lower Threshold (default -0.05): ") or "-0.05")
        return (period, upper, lower)
    elif indicator_name in ["EV_MACD", "VW_MACD"]:
        fast = int(input(f"{indicator_name} Fast Period (default 12): ") or "12")
        slow = int(input(f"{indicator_name} Slow Period (default 26): ") or "26")
        signal = int(input(f"{indicator_name} Signal Period (default 9): ") or "9")
        upper = float(input(f"{indicator_name} Upper Threshold (default 0.05): ") or "0.05")
        lower = float(input(f"{indicator_name} Lower Threshold (default -0.05): ") or "-0.05")
        return (fast, slow, signal, upper, lower)
    elif indicator_name == "KVO":
        fast = int(input(f"{indicator_name} Fast Period (default 34): ") or "34")
        slow = int(input(f"{indicator_name} Slow Period (default 55): ") or "55")
        upper = float(input(f"{indicator_name} Upper Threshold (default 0.05): ") or "0.05")
        lower = float(input(f"{indicator_name} Lower Threshold (default -0.05): ") or "-0.05")
        return (fast, slow, upper, lower)
    elif indicator_name == "PVO":
        fast = int(input(f"{indicator_name} Fast Period (default 12): ") or "12")
        slow = int(input(f"{indicator_name} Slow Period (default 26): ") or "26")
        upper = float(input(f"{indicator_name} Upper Threshold (default 0.05): ") or "0.05")
        lower = float(input(f"{indicator_name} Lower Threshold (default -0.05): ") or "-0.05")
        return (fast, slow, upper, lower)
    # Price Indicators
    elif indicator_name in ["APZ", "AP", "DP", "DPO", "IP", "MP", "MPP", "PD", "WCP"]:
        period = int(input(f"{indicator_name} Period (default 14): ") or "14")
        upper = float(input(f"{indicator_name} Upper Threshold (default 0.05): ") or "0.05")
        lower = float(input(f"{indicator_name} Lower Threshold (default -0.05): ") or "-0.05")
        return (period, upper, lower)
    elif indicator_name in ["APO", "PPO"]:
        fast = int(input(f"{indicator_name} Fast Period (default 12): ") or "12")
        slow = int(input(f"{indicator_name} Slow Period (default 26): ") or "26")
        upper = float(input(f"{indicator_name} Upper Threshold (default 0.05): ") or "0.05")
        lower = float(input(f"{indicator_name} Lower Threshold (default -0.05): ") or "-0.05")
        return (fast, slow, upper, lower)
    # Trend Indicators
    elif indicator_name == "ADX":
        period = int(input(f"{indicator_name} Period (default 14): ") or "14")
        threshold = float(input(f"{indicator_name} ADX Threshold (default 25): ") or "25")
        return (period, threshold)
    elif indicator_name in ["CMO", "PDI", "MDI", "PDM", "MDM", "MBB"]:
        period = int(input(f"{indicator_name} Period (default 14): ") or "14")
        upper = float(input(f"{indicator_name} Upper Threshold (default 50): ") or "50")
        lower = float(input(f"{indicator_name} Lower Threshold (default -50): ") or "-50")
        return (period, upper, lower)
    elif indicator_name == "DM":
        period = int(input(f"{indicator_name} Period (default 14): ") or "14")
        baseline = float(input(f"{indicator_name} Baseline (default 0): ") or "0")
        upper = float(input(f"{indicator_name} Upper Threshold (default 5): ") or "5")
        lower = float(input(f"{indicator_name} Lower Threshold (default -5): ") or "-5")
        return (period, baseline, upper, lower)
    elif indicator_name == "TS":
        short = int(input(f"{indicator_name} Short Period (default 10): ") or "10")
        long = int(input(f"{indicator_name} Long Period (default 50): ") or "50")
        threshold = float(input(f"{indicator_name} Threshold (default 0): ") or "0")
        return (short, long, threshold)
    elif indicator_name == "STC":
        fast = int(input(f"{indicator_name} Fast Period (default 23): ") or "23")
        slow = int(input(f"{indicator_name} Slow Period (default 50): ") or "50")
        cycle = int(input(f"{indicator_name} Cycle Period (default 10): ") or "10")
        baseline = float(input(f"{indicator_name} Baseline (default 50): ") or "50")
        upper = float(input(f"{indicator_name} Upper Threshold (default 75): ") or "75")
        lower = float(input(f"{indicator_name} Lower Threshold (default 25): ") or "25")
        return (fast, slow, cycle, baseline, upper, lower)
    elif indicator_name == "WTO":
        period1 = int(input(f"{indicator_name} Period 1 (default 10): ") or "10")
        period2 = int(input(f"{indicator_name} Period 2 (default 21): ") or "21")
        signal = int(input(f"{indicator_name} Signal Period (default 4): ") or "4")
        upper = float(input(f"{indicator_name} Upper Threshold (default 60): ") or "60")
        lower = float(input(f"{indicator_name} Lower Threshold (default -60): ") or "-60")
        return (period1, period2, signal, upper, lower)
    # Fixed broken indicators
    elif indicator_name == "VPT":
        ma_period = int(input(f"{indicator_name} MA Period (default 14): ") or "14")
        threshold = float(input(f"{indicator_name} Threshold Percentage (default 0.01): ") or "0.01")
        return (ma_period, threshold)
    elif indicator_name == "VP":
        period = int(input(f"{indicator_name} Period (default 14): ") or "14")
        bin_size = int(input(f"{indicator_name} Bin Size (default 1): ") or "1")
        value_area = float(input(f"{indicator_name} Value Area Percentage (default 0.7): ") or "0.7")
        return (period, bin_size, value_area)
    elif indicator_name == "VW_MACD":
        fast = int(input(f"{indicator_name} Fast Period (default 12): ") or "12")
        slow = int(input(f"{indicator_name} Slow Period (default 26): ") or "26")
        signal = int(input(f"{indicator_name} Signal Period (default 9): ") or "9")
        threshold = float(input(f"{indicator_name} Threshold (default 0): ") or "0")
        return (fast, slow, signal, threshold)
    elif indicator_name == "WOBV":
        ma_period = int(input(f"{indicator_name} MA Period (default 20): ") or "20")
        return (ma_period,)
    elif indicator_name == "APZ":
        period = int(input(f"{indicator_name} Period (default 20): ") or "20")
        multiplier = float(input(f"{indicator_name} Multiplier (default 0.5): ") or "0.5")
        baseline = float(input(f"{indicator_name} Baseline (default 0): ") or "0")
        return (period, multiplier, baseline)
    elif indicator_name == "MPP":
        period = int(input(f"{indicator_name} Period (default 20): ") or "20")
        threshold = float(input(f"{indicator_name} Threshold (default 0.01): ") or "0.01")
        return (period, threshold)
    else:
        period = int(input(f"{indicator_name} Period (default 20): ") or "20")
        return (period,)

def get_constant_value():
    """Get constant value"""
    return float(input("Enter constant value: "))

def get_price_column():
    """Get price column selection"""
    print("\nSelect Price Column:")
    print("1. Close")
    print("2. Open") 
    print("3. High")
    print("4. Low")
    print("5. Custom")
    
    choice = input("Enter choice (1-5) [default: 1]: ").strip()
    
    # If empty input, default to 1
    if not choice:
        choice = "1"
    
    if choice == "1":
        return "Close"
    elif choice == "2":
        return "Open"
    elif choice == "3":
        return "High"
    elif choice == "4":
        return "Low"
    elif choice == "5":
        custom = input("Enter custom price column name: ").strip()
        return custom
    else:
        print("❌ Invalid choice! Using Close")
        return "Close"

def get_candles_ago(comparison_name):
    """Get number of candles ago for comparison"""
    print(f"\n{comparison_name} - Candles Ago:")
    print("0. Current candle (0 candles ago)")
    print("1. Previous candle (1 candle ago)")
    print("2. Two candles ago")
    print("3. Three candles ago")
    print("4. Four candles ago")
    print("5. Five candles ago")
    print("6. Custom")
    
    choice = input("Enter choice (0-6) [default: 0]: ").strip()
    
    # If empty input, default to 0
    if not choice:
        return 0
    
    if choice == "0":
        return 0
    elif choice == "1":
        return 1
    elif choice == "2":
        return 2
    elif choice == "3":
        return 3
    elif choice == "4":
        return 4
    elif choice == "5":
        return 5
    elif choice == "6":
        try:
            custom = int(input("Enter number of candles ago (0-20): ").strip())
            if 0 <= custom <= 20:
                return custom
            else:
                print("❌ Invalid range! Using 0")
                return 0
        except ValueError:
            print("❌ Invalid input! Using 0")
            return 0
    else:
        print("❌ Invalid choice! Using 0")
        return 0

def get_time_interval_inputs():
    """Get time period and interval from user"""
    print("\n--- TIME INTERVAL SELECTION ---")
    
    # Time period selection
    print("Select Time Period:")
    print("1. 1 year")
    print("2. 2 years") 
    print("3. 5 years")
    print("4. 10 years")
    print("5. Custom period")
    
    period_choice = input("Enter choice (1-5) [default: 1]: ").strip()
    
    # If empty input, default to 1
    if not period_choice:
        period_choice = "1"
    
    if period_choice == "1":
        period = "1y"
    elif period_choice == "2":
        period = "2y"
    elif period_choice == "3":
        period = "5y"
    elif period_choice == "4":
        period = "10y"
    elif period_choice == "5":
        period = input("Enter custom period (e.g., '3y', '6mo', '2y'): ").strip()
    else:
        print("❌ Invalid choice! Using default 5 years")
        period = "5y"
    
    # Interval selection
    print("\nSelect Data Interval:")
    print("1. 1 minute")
    print("2. 5 minutes")
    print("3. 15 minutes")
    print("4. 30 minutes")
    print("5. 1 hour")
    print("6. 4 hours")
    print("7. 1 day")
    print("8. 1 week")
    print("9. 1 month")
    print("10. Custom interval")
    
    interval_choice = input("Enter choice (1-10) [default: 1]: ").strip()
    
    # If empty input, default to 1
    if not interval_choice:
        interval_choice = "1"
    
    if interval_choice == "1":
        interval = "1d"
    elif interval_choice == "2":
        interval = "5m"
    elif interval_choice == "3":
        interval = "15m"
    elif interval_choice == "4":
        interval = "30m"
    elif interval_choice == "5":
        interval = "1h"
    elif interval_choice == "6":
        interval = "4h"
    elif interval_choice == "7":
        interval = "1d"
    elif interval_choice == "8":
        interval = "1wk"
    elif interval_choice == "9":
        interval = "1mo"
    elif interval_choice == "10":
        interval = input("Enter custom interval (e.g., '2h', '6h', '3d'): ").strip()
    else:
        print("❌ Invalid choice! Using default 4 hours")
        interval = "4h"
    
    return period, interval

def download_and_prepare_data(ticker, period="5y", interval="4h"):
    """Download and prepare stock data with configurable period and interval"""
    print(f"Downloading {period} of {interval} data for {ticker}...")
    
    try:
        data = yf.Ticker(ticker).history(period=period, interval=interval)
        
        if data.empty:
            print(f"❌ No data available for {ticker} with {period} period and {interval} interval")
            print("💡 Try shorter periods for intraday data (e.g., 1y for 1h, 60d for 15m)")
            return None
        
        # Reset index and format date
        data_reset = data.reset_index()
        
        # Handle different date formats
        if 'Date' in data_reset.columns:
            data_reset['Date'] = data_reset['Date'].dt.date
        elif 'Datetime' in data_reset.columns:
            data_reset['Date'] = data_reset['Datetime'].dt.date
        else:
            # If no date column, use index
            data_reset['Date'] = data_reset.index.date
        
        print(f"✅ Downloaded {len(data_reset)} {interval} intervals of data ({period})")
        return data_reset
        
    except Exception as e:
        print(f"❌ Error downloading data: {str(e)}")
        print("💡 Try different period/interval combinations:")
        print("   - Daily data: up to 10 years")
        print("   - 4-hour data: up to 2 years") 
        print("   - 1-hour data: up to 2 years")
        print("   - 15-minute data: up to 60 days")
        return None

def get_number_of_conditions(condition_type):
    """Get number of conditions from user"""
    print(f"\n--- {condition_type.upper()} CONDITIONS ---")
    while True:
        try:
            user_input = input(f"Enter number of {condition_type} conditions (1-20) [default: 1]: ").strip()
            if not user_input:  # Empty input, use default
                return 1
            num = int(user_input)
            if 1 <= num <= 20:
                return num
            else:
                print("❌ Please enter a number between 1 and 20!")
        except ValueError:
            print("❌ Please enter a valid number!")

def get_multi_condition_inputs(condition_type, num_conditions):
    """Get multiple condition inputs from user"""
    conditions = []
    
    for i in range(num_conditions):
        print(f"\n--- {condition_type.upper()} CONDITION {i+1} ---")
        
        # Comparison 1
        print(f"Condition {i+1} - Comparison 1:")
        comp1_type = get_comparison_type()
        if comp1_type is None:
            return None
        
        if comp1_type == ComparisonType.INDICATOR:
            comp1_name = get_indicator_selection()
            if comp1_name is None:
                return None
            comp1_params = get_indicator_params(comp1_name)
        elif comp1_type == ComparisonType.CONSTANT:
            comp1_name = "CONSTANT"
            comp1_params = (get_constant_value(),)
        else:  # PRICE
            comp1_name = "PRICE"
            comp1_params = (get_price_column(),)
        
        # Get candles ago for comparison 1
        comp1_candles_ago = get_candles_ago(f"Condition {i+1} - Comparison 1")
        
        # Strategy
        strategy = get_strategy_selection()
        if strategy is None:
            return None
        
        # Comparison 2
        print(f"Condition {i+1} - Comparison 2:")
        comp2_type = get_comparison_type()
        if comp2_type is None:
            return None
        
        if comp2_type == ComparisonType.INDICATOR:
            comp2_name = get_indicator_selection()
            if comp2_name is None:
                return None
            comp2_params = get_indicator_params(comp2_name)
        elif comp2_type == ComparisonType.CONSTANT:
            comp2_name = "CONSTANT"
            comp2_params = (get_constant_value(),)
        else:  # PRICE
            comp2_name = "PRICE"
            comp2_params = (get_price_column(),)
        
        # Get candles ago for comparison 2
        comp2_candles_ago = get_candles_ago(f"Condition {i+1} - Comparison 2")
        
        conditions.append({
            'comp1_type': comp1_type, 'comp1_name': comp1_name, 'comp1_params': comp1_params,
            'comp2_type': comp2_type, 'comp2_name': comp2_name, 'comp2_params': comp2_params,
            'strategy': strategy, 'comp1_candles_ago': comp1_candles_ago, 'comp2_candles_ago': comp2_candles_ago
        })
    
    return conditions

# OLD FUNCTION - COMMENTED OUT (replaced by new multi-condition implementation)
# def detect_multi_strategy_signals(data, entry_conditions, exit_conditions, 
#                                  entry_logic='AND', exit_logic='AND'):
#     """Detect entry and exit signals using multiple conditions with AND/OR logic"""
#     # This function has been replaced by the new MultiConditionDetector approach
#     pass

def get_number_of_tickers():
    """Get number of tickers from user"""
    print("\n--- MULTI-TICKER PORTFOLIO ---")
    while True:
        try:
            user_input = input("Enter number of tickers (1-10) [default: 1]: ").strip()
            if not user_input:  # Empty input, use default
                return 1
            num = int(user_input)
            if 1 <= num <= 10:
                return num
            else:
                print("❌ Please enter a number between 1 and 10!")
        except ValueError:
            print("❌ Please enter a valid number!")

def get_ticker_names(num_tickers):
    """Get ticker names from user"""
    tickers = []
    for i in range(num_tickers):
        while True:
            ticker = input(f"Enter ticker {i+1} [default: AAPL]: ").upper().strip()
            if ticker:
                tickers.append(ticker)
                break
            else:
                # If empty input, use AAPL as default
                tickers.append("AAPL")
                break
    return tickers

def get_total_capital():
    """Get total portfolio capital from user"""
    while True:
        try:
            capital = float(input("Enter total portfolio capital ($) [default: 10000]: ").strip())
            if capital > 0:
                return capital
            else:
                return 10000
        except ValueError:
            return 10000

def get_allocation_percentages(tickers):
    """Get allocation percentages for each ticker"""
    print(f"\n--- ALLOCATION PERCENTAGES ---")
    print("Enter percentage allocation for each ticker (must total 100%):")
    
    allocations = {}
    total_percentage = 0
    
    for i, ticker in enumerate(tickers):
        while True:
            try:
                user_input = input(f"{ticker} allocation (%) [default: 100]: ").strip()
                if not user_input:  # Default to 100%
                    percentage = 100.0
                else:
                    percentage = float(user_input)
                
                if 0 <= percentage <= 100:
                    allocations[ticker] = percentage
                    total_percentage += percentage
                    break
                else:
                    print("❌ Please enter a percentage between 0 and 100!")
            except ValueError:
                print("❌ Please enter a valid number!")
    
    # Check if total is 100%
    if abs(total_percentage - 100.0) > 0.01:
        print("❌ Total allocation must equal 100%! Please re-enter allocations:")
        return get_allocation_percentages(tickers)
    
    return allocations

def get_trade_size_percentages(tickers):
    """Get trade size percentages for each ticker"""
    print(f"\n--- TRADE SIZE PERCENTAGES ---")
    print("Enter percentage of allocated capital to use per trade for each ticker:")
    print("💡 Example: 10% means each trade uses 10% of that ticker's allocated capital")
    
    trade_sizes = {}
    
    for ticker in tickers:
        while True:
            try:
                percentage = float(input(f"{ticker} trade size (%) [default: 10]: ").strip() or "10")
                if 0 < percentage <= 100:
                    trade_sizes[ticker] = percentage
                    break
                else:
                    return 10
            except ValueError:
                print("❌ Please enter a valid number!")
    
    return trade_sizes

def get_multi_ticker_multi_strategy_inputs():
    """Get user inputs for multi-ticker multi-strategy trading"""
    print("\n" + "="*60)
    print("MULTI-TICKER MULTI-STRATEGY PORTFOLIO")
    print("="*60)
    print("💡 TIP: Each ticker can have its own unique strategy!")
    print("Example: AAPL with SMA crossover, MSFT with EMA crossover, TSLA with RSI strategy")
    print("="*60)
    
    # Number of tickers
    num_tickers = get_number_of_tickers()
    
    # Ticker names
    tickers = get_ticker_names(num_tickers)
    
    # Total capital
    total_capital = get_total_capital()
    
    # Allocation percentages
    allocations = get_allocation_percentages(tickers)
    
    # Trade size percentages
    trade_sizes = get_trade_size_percentages(tickers)
    
    # Time interval selection
    period, interval = get_time_interval_inputs()
    
    # Individual strategies for each ticker
    ticker_strategies = {}
    
    for ticker in tickers:
        print(f"\n--- STRATEGY FOR {ticker} ---")
        print("Choose strategy type:")
        print("1. Single Condition Strategy")
        print("2. Multi-Condition Strategy")
        strategy_choice = input("Enter choice (1-2) [default: 1]: ").strip()
        
        if strategy_choice == "1":
            # Single condition strategy
            print(f"\n--- {ticker} ENTRY STRATEGY ---")
            entry_comp1_type = get_comparison_type()
            if entry_comp1_type is None:
                return None
            
            if entry_comp1_type == ComparisonType.INDICATOR:
                entry_comp1_name = get_indicator_selection()
                if entry_comp1_name is None:
                    return None
                entry_comp1_params = get_indicator_params(entry_comp1_name)
            elif entry_comp1_type == ComparisonType.CONSTANT:
                entry_comp1_name = "CONSTANT"
                entry_comp1_params = (get_constant_value(),)
            else:  # PRICE
                entry_comp1_name = "PRICE"
                entry_comp1_params = (get_price_column(),)
            
            entry_comp1_candles_ago = get_candles_ago("Entry Comparison 1")
            entry_strategy = get_strategy_selection()
            if entry_strategy is None:
                return None
            
            print(f"\n{ticker} Entry Comparison 2:")
            entry_comp2_type = get_comparison_type()
            if entry_comp2_type is None:
                return None
            
            if entry_comp2_type == ComparisonType.INDICATOR:
                entry_comp2_name = get_indicator_selection()
                if entry_comp2_name is None:
                    return None
                entry_comp2_params = get_indicator_params(entry_comp2_name)
            elif entry_comp2_type == ComparisonType.CONSTANT:
                entry_comp2_name = "CONSTANT"
                entry_comp2_params = (get_constant_value(),)
            else:  # PRICE
                entry_comp2_name = "PRICE"
                entry_comp2_params = (get_price_column(),)
            
            entry_comp2_candles_ago = get_candles_ago("Entry Comparison 2")
            
            print(f"\n--- {ticker} EXIT STRATEGY ---")
            exit_comp1_type = get_comparison_type()
            if exit_comp1_type is None:
                return None
            
            if exit_comp1_type == ComparisonType.INDICATOR:
                exit_comp1_name = get_indicator_selection()
                if exit_comp1_name is None:
                    return None
                exit_comp1_params = get_indicator_params(exit_comp1_name)
            elif exit_comp1_type == ComparisonType.CONSTANT:
                exit_comp1_name = "CONSTANT"
                exit_comp1_params = (get_constant_value(),)
            else:  # PRICE
                exit_comp1_name = "PRICE"
                exit_comp1_params = (get_price_column(),)
            
            exit_comp1_candles_ago = get_candles_ago("Exit Comparison 1")
            exit_strategy = get_strategy_selection()
            if exit_strategy is None:
                return None
            
            print(f"\n{ticker} Exit Comparison 2:")
            exit_comp2_type = get_comparison_type()
            if exit_comp2_type is None:
                return None
            
            if exit_comp2_type == ComparisonType.INDICATOR:
                exit_comp2_name = get_indicator_selection()
                if exit_comp2_name is None:
                    return None
                exit_comp2_params = get_indicator_params(exit_comp2_name)
            elif exit_comp2_type == ComparisonType.CONSTANT:
                exit_comp2_name = "CONSTANT"
                exit_comp2_params = (get_constant_value(),)
            else:  # PRICE
                exit_comp2_name = "PRICE"
                exit_comp2_params = (get_price_column(),)
            
            exit_comp2_candles_ago = get_candles_ago("Exit Comparison 2")
            
            ticker_strategies[ticker] = {
                'type': 'single',
                'entry_comp1_type': entry_comp1_type,
                'entry_comp1_name': entry_comp1_name,
                'entry_comp1_params': entry_comp1_params,
                'entry_comp1_candles_ago': entry_comp1_candles_ago,
                'entry_comp2_type': entry_comp2_type,
                'entry_comp2_name': entry_comp2_name,
                'entry_comp2_params': entry_comp2_params,
                'entry_comp2_candles_ago': entry_comp2_candles_ago,
                'exit_comp1_type': exit_comp1_type,
                'exit_comp1_name': exit_comp1_name,
                'exit_comp1_params': exit_comp1_params,
                'exit_comp1_candles_ago': exit_comp1_candles_ago,
                'exit_comp2_type': exit_comp2_type,
                'exit_comp2_name': exit_comp2_name,
                'exit_comp2_params': exit_comp2_params,
                'exit_comp2_candles_ago': exit_comp2_candles_ago,
                'entry_strategy': entry_strategy,
                'exit_strategy': exit_strategy
            }
        
        else:
            # Multi-condition strategy
            print(f"\n--- {ticker} ENTRY LOGIC ---")
            print("1. AND - All conditions must be true")
            print("2. OR - Any condition can be true")
            entry_choice = input("Enter choice (1-2) [default: 1]: ").strip()
            entry_logic = 'AND' if entry_choice == '1' else 'OR'
            
            num_entry_conditions = get_number_of_conditions("entry")
            entry_conditions = get_multi_condition_inputs("entry", num_entry_conditions)
            if entry_conditions is None:
                return None
            
            print(f"\n--- {ticker} EXIT LOGIC ---")
            print("1. AND - All conditions must be true")
            print("2. OR - Any condition can be true")
            exit_choice = input("Enter choice (1-2) [default: 1]: ").strip()
            exit_logic = 'AND' if exit_choice == '1' else 'OR'
            
            num_exit_conditions = get_number_of_conditions("exit")
            exit_conditions = get_multi_condition_inputs("exit", num_exit_conditions)
            if exit_conditions is None:
                return None
            
            ticker_strategies[ticker] = {
                'type': 'multi',
                'entry_conditions': entry_conditions,
                'exit_conditions': exit_conditions,
                'entry_logic': entry_logic,
                'exit_logic': exit_logic
            }
    
    return {
        'type': 'multi_strategy',
        'tickers': tickers,
        'total_capital': total_capital,
        'allocations': allocations,
        'trade_sizes': trade_sizes,
        'period': period,
        'interval': interval,
        'ticker_strategies': ticker_strategies
    }

def get_multi_ticker_inputs():
    """Get user inputs for multi-ticker trading strategy"""
    print("\n" + "="*60)
    print("MULTI-TICKER PORTFOLIO STRATEGY")
    print("="*60)
    print("💡 TIP: Diversify your portfolio across multiple stocks!")
    print("Example: 40% AAPL, 60% MSFT with same strategy")
    print("="*60)
    
    # Number of tickers
    num_tickers = get_number_of_tickers()
    
    # Ticker names
    tickers = get_ticker_names(num_tickers)
    
    # Total capital
    total_capital = get_total_capital()
    
    # Allocation percentages
    allocations = get_allocation_percentages(tickers)
    
    # Trade size percentages
    trade_sizes = get_trade_size_percentages(tickers)
    
    # Time interval selection
    period, interval = get_time_interval_inputs()
    
    # Strategy selection (same for all tickers)
    print("\n--- STRATEGY SELECTION (Same for all tickers) ---")
    print("Choose strategy type:")
    print("1. Single Condition Strategy")
    print("2. Multi-Condition Strategy")
    strategy_choice = input("Enter choice (1-2) [default: 1]: ").strip()
    
    # If empty input, default to 1
    if not strategy_choice:
        strategy_choice = "1"
    
    if strategy_choice == "1":
        # Single condition strategy
        print("\n--- ENTRY STRATEGY ---")
        entry_comp1_type = get_comparison_type()
        if entry_comp1_type is None:
            return None
        
        if entry_comp1_type == ComparisonType.INDICATOR:
            entry_comp1_name = get_indicator_selection()
            if entry_comp1_name is None:
                return None
            entry_comp1_params = get_indicator_params(entry_comp1_name)
        elif entry_comp1_type == ComparisonType.CONSTANT:
            entry_comp1_name = "CONSTANT"
            entry_comp1_params = (get_constant_value(),)
        else:  # PRICE
            entry_comp1_name = "PRICE"
            entry_comp1_params = (get_price_column(),)
        
        entry_comp1_candles_ago = get_candles_ago("Entry Comparison 1")
        entry_strategy = get_strategy_selection()
        if entry_strategy is None:
            return None
        
        print("\nEntry Comparison 2:")
        entry_comp2_type = get_comparison_type()
        if entry_comp2_type is None:
            return None
        
        if entry_comp2_type == ComparisonType.INDICATOR:
            entry_comp2_name = get_indicator_selection()
            if entry_comp2_name is None:
                return None
            entry_comp2_params = get_indicator_params(entry_comp2_name)
        elif entry_comp2_type == ComparisonType.CONSTANT:
            entry_comp2_name = "CONSTANT"
            entry_comp2_params = (get_constant_value(),)
        else:  # PRICE
            entry_comp2_name = "PRICE"
            entry_comp2_params = (get_price_column(),)
        
        entry_comp2_candles_ago = get_candles_ago("Entry Comparison 2")
        
        print("\n--- EXIT STRATEGY ---")
        exit_comp1_type = get_comparison_type()
        if exit_comp1_type is None:
            return None
        
        if exit_comp1_type == ComparisonType.INDICATOR:
            exit_comp1_name = get_indicator_selection()
            if exit_comp1_name is None:
                return None
            exit_comp1_params = get_indicator_params(exit_comp1_name)
        elif exit_comp1_type == ComparisonType.CONSTANT:
            exit_comp1_name = "CONSTANT"
            exit_comp1_params = (get_constant_value(),)
        else:  # PRICE
            exit_comp1_name = "PRICE"
            exit_comp1_params = (get_price_column(),)
        
        exit_comp1_candles_ago = get_candles_ago("Exit Comparison 1")
        exit_strategy = get_strategy_selection()
        if exit_strategy is None:
            return None
        
        print("\nExit Comparison 2:")
        exit_comp2_type = get_comparison_type()
        if exit_comp2_type is None:
            return None
        
        if exit_comp2_type == ComparisonType.INDICATOR:
            exit_comp2_name = get_indicator_selection()
            if exit_comp2_name is None:
                return None
            exit_comp2_params = get_indicator_params(exit_comp2_name)
        elif exit_comp2_type == ComparisonType.CONSTANT:
            exit_comp2_name = "CONSTANT"
            exit_comp2_params = (get_constant_value(),)
        else:  # PRICE
            exit_comp2_name = "PRICE"
            exit_comp2_params = (get_price_column(),)
        
        exit_comp2_candles_ago = get_candles_ago("Exit Comparison 2")
        
        return {
            'type': 'single',
            'tickers': tickers,
            'total_capital': total_capital,
            'allocations': allocations,
            'trade_sizes': trade_sizes,
            'period': period,
            'interval': interval,
            'entry_comp1_type': entry_comp1_type,
            'entry_comp1_name': entry_comp1_name,
            'entry_comp1_params': entry_comp1_params,
            'entry_comp1_candles_ago': entry_comp1_candles_ago,
            'entry_comp2_type': entry_comp2_type,
            'entry_comp2_name': entry_comp2_name,
            'entry_comp2_params': entry_comp2_params,
            'entry_comp2_candles_ago': entry_comp2_candles_ago,
            'exit_comp1_type': exit_comp1_type,
            'exit_comp1_name': exit_comp1_name,
            'exit_comp1_params': exit_comp1_params,
            'exit_comp1_candles_ago': exit_comp1_candles_ago,
            'exit_comp2_type': exit_comp2_type,
            'exit_comp2_name': exit_comp2_name,
            'exit_comp2_params': exit_comp2_params,
            'exit_comp2_candles_ago': exit_comp2_candles_ago,
            'entry_strategy': entry_strategy,
            'exit_strategy': exit_strategy
        }
    
    else:
        # Multi-condition strategy
        print("\n--- ENTRY LOGIC ---")
        print("1. AND - All conditions must be true")
        print("2. OR - Any condition can be true")
        entry_choice = input("Enter choice (1-2) [default: 1]: ").strip()
        
        # If empty input, default to 1
        if not entry_choice:
            entry_choice = "1"
        entry_logic = 'AND' if entry_choice == '1' else 'OR'
        
        num_entry_conditions = get_number_of_conditions("entry")
        entry_conditions = get_multi_condition_inputs("entry", num_entry_conditions)
        if entry_conditions is None:
            return None
        
        print("\n--- EXIT LOGIC ---")
        print("1. AND - All conditions must be true")
        print("2. OR - Any condition can be true")
        exit_choice = input("Enter choice (1-2) [default: 1]: ").strip()
        
        # If empty input, default to 1
        if not exit_choice:
            exit_choice = "1"
        exit_logic = 'AND' if exit_choice == '1' else 'OR'
        
        num_exit_conditions = get_number_of_conditions("exit")
        exit_conditions = get_multi_condition_inputs("exit", num_exit_conditions)
        if exit_conditions is None:
            return None
        
        return {
            'type': 'multi',
            'tickers': tickers,
            'total_capital': total_capital,
            'allocations': allocations,
            'trade_sizes': trade_sizes,
            'period': period,
            'interval': interval,
            'entry_conditions': entry_conditions,
            'exit_conditions': exit_conditions,
            'entry_logic': entry_logic,
            'exit_logic': exit_logic
        }

def get_multi_strategy_inputs():
    """Get user inputs for multi-condition trading strategy"""
    print("\n" + "="*60)
    print("MULTI-CONDITION TRADING STRATEGY SELECTION")
    print("="*60)
    print("💡 TIP: Use multiple conditions to reduce false signals!")
    print("Example: Buy when SMA(10) > SMA(20) AND RSI > 30 AND Volume > Average")
    print("="*60)
    
    # Ticker
    ticker = input("Enter ticker symbol [default: AAPL]: ").upper().strip()
    
    # If empty input, default to AAPL
    if not ticker:
        ticker = "AAPL"
    
    # Time interval selection
    period, interval = get_time_interval_inputs()
    
    # Entry logic selection
    print("\n--- ENTRY LOGIC ---")
    print("1. AND - All conditions must be true")
    print("2. OR - Any condition can be true")
    entry_choice = input("Enter choice (1-2) [default: 1]: ").strip()
    
    # If empty input, default to 1
    if not entry_choice:
        entry_choice = "1"
    entry_logic = 'AND' if entry_choice == '1' else 'OR'
    
    # Entry conditions
    num_entry_conditions = get_number_of_conditions("entry")
    entry_conditions = get_multi_condition_inputs("entry", num_entry_conditions)
    if entry_conditions is None:
        return None
    
    # Exit logic selection
    print("\n--- EXIT LOGIC ---")
    print("1. AND - All conditions must be true")
    print("2. OR - Any condition can be true")
    exit_choice = input("Enter choice (1-2) [default: 1]: ").strip()
    
    # If empty input, default to 1
    if not exit_choice:
        exit_choice = "1"
    exit_logic = 'AND' if exit_choice == '1' else 'OR'
    
    # Exit conditions
    num_exit_conditions = get_number_of_conditions("exit")
    exit_conditions = get_multi_condition_inputs("exit", num_exit_conditions)
    if exit_conditions is None:
        return None
    
    return ticker, period, interval, entry_conditions, exit_conditions, entry_logic, exit_logic

def get_sl_tp_configuration():
    """Get Stop Loss and Take Profit configuration from user"""
    print("\n" + "="*50)
    print("📊 STOP LOSS & TAKE PROFIT CONFIGURATION")
    print("="*50)
    
    # Ask if user wants SL/TP
    while True:
        enable_sl_tp = input("Enable Stop Loss & Take Profit? (y/n) [default: y]: ").strip().lower()
        if not enable_sl_tp:  # Default to 'y' if empty
            enable_sl_tp = 'y'
        if enable_sl_tp in ['y', 'yes']:
            enable_sl_tp = True
            break
        elif enable_sl_tp in ['n', 'no']:
            enable_sl_tp = False
            break
        else:
            print("❌ Please enter 'y' or 'n'")
    
    if not enable_sl_tp:
        return {
            'enabled': False,
            'sl_type': None,
            'tp_type': None,
            'sl_value': 0,
            'tp_value': 0,
            'trailing_sl_enabled': False,
            'trailing_sl_type': None,
            'trailing_sl_value': 0
        }
    
    print("\n📋 Choose SL/TP Method:")
    print("1. Percentage-based (e.g., 5% loss, 10% profit)")
    print("2. Dollar-based (e.g., $100 loss, $200 profit)")
    
    while True:
        try:
            method_input = input("Select method (1 or 2) [default: 1]: ").strip()
            method = int(method_input or "1")
            if method in [1, 2]:
                break
            else:
                print("❌ Please enter 1 or 2")
        except ValueError:
            print("❌ Please enter a valid number")
    
    if method == 1:
        # Percentage-based
        print("\n📊 PERCENTAGE-BASED SL/TP:")
        
        while True:
            try:
                sl_input = input("Stop Loss percentage (e.g., 5 for 5%) [default: 5]: ").strip()
                sl_percent = float(sl_input or "5")
                if 0 < sl_percent <= 100:
                    break
                else:
                    print("❌ Please enter a percentage between 0 and 100")
            except ValueError:
                print("❌ Please enter a valid number")
        
        while True:
            try:
                tp_input = input("Take Profit percentage (e.g., 10 for 10%) [default: 10]: ").strip()
                tp_percent = float(tp_input or "10")
                if 0 < tp_percent <= 1000:
                    break
                else:
                    print("❌ Please enter a percentage between 0 and 1000")
            except ValueError:
                print("❌ Please enter a valid number")
        
        # Ask about trailing stop loss
        trailing_config = get_trailing_sl_configuration()
        
        return {
            'enabled': True,
            'sl_type': 'percentage',
            'tp_type': 'percentage',
            'sl_value': sl_percent / 100,  # Convert to decimal
            'tp_value': tp_percent / 100,   # Convert to decimal
            'trailing_sl_enabled': trailing_config['enabled'],
            'trailing_sl_type': trailing_config['type'],
            'trailing_sl_value': trailing_config['value']
        }
    
    else:
        # Dollar-based
        print("\n💰 DOLLAR-BASED SL/TP:")
        
        while True:
            try:
                sl_input = input("Stop Loss dollar amount (e.g., 100 for $100 loss) [default: 50]: $").strip()
                sl_dollars = float(sl_input or "50")
                if sl_dollars > 0:
                    break
                else:
                    print("❌ Please enter a positive dollar amount")
            except ValueError:
                print("❌ Please enter a valid number")
        
        while True:
            try:
                tp_input = input("Take Profit dollar amount (e.g., 200 for $200 profit) [default: 100]: $").strip()
                tp_dollars = float(tp_input or "100")
                if tp_dollars > 0:
                    break
                else:
                    print("❌ Please enter a positive dollar amount")
            except ValueError:
                print("❌ Please enter a valid number")
        
        # Ask about trailing stop loss
        trailing_config = get_trailing_sl_configuration()
        
        return {
            'enabled': True,
            'sl_type': 'dollar',
            'tp_type': 'dollar',
            'sl_value': sl_dollars,
            'tp_value': tp_dollars,
            'trailing_sl_enabled': trailing_config['enabled'],
            'trailing_sl_type': trailing_config['type'],
            'trailing_sl_value': trailing_config['value']
        }

def get_trailing_sl_configuration():
    """Get trailing stop loss configuration from user"""
    print("\n" + "="*50)
    print("🔄 TRAILING STOP LOSS CONFIGURATION")
    print("="*50)
    print("💡 Trailing SL moves UP with profitable trades, locks in gains!")
    
    # Ask if user wants trailing SL
    while True:
        enable_trailing = input("Enable Trailing Stop Loss? (y/n) [default: n]: ").strip().lower()
        if not enable_trailing:  # Default to 'n' if empty
            enable_trailing = 'n'
        if enable_trailing in ['y', 'yes']:
            enable_trailing = True
            break
        elif enable_trailing in ['n', 'no']:
            enable_trailing = False
            break
        else:
            print("❌ Please enter 'y' or 'n'")
    
    if not enable_trailing:
        return {
            'enabled': False,
            'type': None,
            'value': 0
        }
    
    # Get trailing method
    print("\n📊 Choose Trailing SL Method:")
    print("1. Percentage-based (e.g., 3% trailing)")
    print("2. Dollar-based (e.g., $50 trailing)")
    
    while True:
        try:
            method_input = input("Select method (1 or 2) [default: 1]: ").strip()
            method = int(method_input or "1")
            if method in [1, 2]:
                break
            else:
                print("❌ Please enter 1 or 2")
        except ValueError:
            print("❌ Please enter a valid number")
    
    if method == 1:
        # Percentage-based trailing
        print("\n📊 PERCENTAGE-BASED TRAILING SL:")
        
        while True:
            try:
                percent_input = input("Trailing percentage (e.g., 3 for 3%) [default: 3]: ").strip()
                trailing_percent = float(percent_input or "3")
                if 0 < trailing_percent <= 50:
                    print(f"✅ Trailing SL: {trailing_percent}% (moves with profitable trades)")
                    break
                else:
                    print("❌ Please enter a percentage between 0 and 50")
            except ValueError:
                print("❌ Please enter a valid number")
        
        return {
            'enabled': True,
            'type': 'percentage',
            'value': trailing_percent / 100  # Convert to decimal
        }
    
    else:
        # Dollar-based trailing
        print("\n💰 DOLLAR-BASED TRAILING SL:")
        
        while True:
            try:
                amount_input = input("Trailing amount [default: $30]: $").strip()
                trailing_amount = float(amount_input or "30")
                if trailing_amount > 0:
                    print(f"✅ Trailing SL: ${trailing_amount:.2f} (moves with profitable trades)")
                    break
                else:
                    print("❌ Please enter a positive dollar amount")
            except ValueError:
                print("❌ Please enter a valid number")
        
        return {
            'enabled': True,
            'type': 'dollar',
            'value': trailing_amount
        }

def get_per_trade_allocation(total_capital):
    """Get per-trade allocation configuration from user"""
    print("\n" + "="*50)
    print("📊 PER-TRADE ALLOCATION CONFIGURATION")
    print("="*50)
    print(f"Total Capital: ${total_capital:,.2f}")
    
    # Get allocation method
    print("\n💰 Choose Per-Trade Allocation Method:")
    print("1. Percentage-based (e.g., 20% of total capital per trade)")
    print("2. Fixed dollar amount (e.g., $2,000 per trade)")
    
    while True:
        try:
            method_input = input("Select method (1 or 2) [default: 1]: ").strip()
            method = int(method_input or "1")
            if method in [1, 2]:
                break
            else:
                print("❌ Please enter 1 or 2")
        except ValueError:
            print("❌ Please enter a valid number")
    
    if method == 1:
        # Percentage-based allocation
        print(f"\n📊 PERCENTAGE-BASED ALLOCATION:")
        print(f"Total Capital: ${total_capital:,.2f}")
        
        while True:
            try:
                percent_input = input("Percentage per trade (e.g., 20 for 20%) [default: 20]: ").strip()
                percent_per_trade = float(percent_input or "20")
                if 0 < percent_per_trade <= 100:
                    amount_per_trade = total_capital * (percent_per_trade / 100)
                    print(f"✅ Per trade allocation: ${amount_per_trade:,.2f} ({percent_per_trade}% of ${total_capital:,.2f})")
                    break
                else:
                    print("❌ Please enter a percentage between 0 and 100")
            except ValueError:
                print("❌ Please enter a valid number")
        
        return {
            'method': 'percentage',
            'percentage': percent_per_trade,
            'amount_per_trade': amount_per_trade,
            'total_capital': total_capital
        }
    
    else:
        # Fixed dollar amount
        print(f"\n💰 FIXED DOLLAR ALLOCATION:")
        print(f"Total Capital: ${total_capital:,.2f}")
        
        while True:
            try:
                amount_input = input("Fixed amount per trade [default: $2,000]: $").strip()
                amount_per_trade = float(amount_input or "2000")
                if 0 < amount_per_trade <= total_capital:
                    percentage = (amount_per_trade / total_capital) * 100
                    print(f"✅ Per trade allocation: ${amount_per_trade:,.2f} ({percentage:.1f}% of ${total_capital:,.2f})")
                    break
                else:
                    print(f"❌ Please enter an amount between $0 and ${total_capital:,.2f}")
            except ValueError:
                print("❌ Please enter a valid number")
        
        return {
            'method': 'fixed',
            'percentage': (amount_per_trade / total_capital) * 100,
            'amount_per_trade': amount_per_trade,
            'total_capital': total_capital
        }


# ============================================================================
# MULTI-CONDITION STRATEGY INPUT FUNCTIONS
# ============================================================================

def get_multi_condition_count():
    """Ask user how many conditions they want for entry and exit"""
    print("\n" + "="*60)
    print("🔢 MULTI-CONDITION STRATEGY SETUP")
    print("="*60)
    print("💡 More conditions = Higher quality but fewer trades")
    print("💡 Recommended: 2-3 conditions for most strategies")
    
    while True:
        try:
            count_input = input("How many conditions per signal? (2-5) [default: 2]: ").strip()
            count = int(count_input or "2")
            if 2 <= count <= 5:
                print(f"✅ Will collect {count} conditions for entry and {count} for exit")
                return count
            else:
                print("❌ Please enter a number between 2 and 5")
        except ValueError:
            print("❌ Please enter a valid number")

def get_logic_type():
    """Ask user whether to use AND or OR logic"""
    print("\n" + "="*50)
    print("🧠 CONDITION LOGIC TYPE")
    print("="*50)
    print("💡 AND Logic: ALL conditions must be True (stricter, fewer trades)")
    print("💡 OR Logic: ANY condition can be True (flexible, more trades)")
    
    while True:
        logic_input = input("Choose logic type (AND/OR) [default: AND]: ").strip().upper()
        if not logic_input:
            logic_input = "AND"
        
        if logic_input in ["AND", "OR"]:
            print(f"✅ Using {logic_input} logic - ", end="")
            if logic_input == "AND":
                print("All conditions must be met")
            else:
                print("Any condition can trigger signal")
            return logic_input
        else:
            print("❌ Please enter 'AND' or 'OR'")

def get_single_condition_input(condition_num, signal_type="Entry"):
    """
    Get input for a single condition (reuses existing functions)
    Returns condition data in format expected by MultiConditionDetector
    """
    print(f"\n--- {signal_type.upper()} CONDITION {condition_num} ---")
    
    # Get comparison 1 (left side)
    print(f"\n{signal_type} Condition {condition_num} - Left Side:")
    comp1_type = get_comparison_type()
    
    if comp1_type == "INDICATOR":
        comp1_name = get_indicator_selection()
        comp1_params = get_indicator_params(comp1_name)
    elif comp1_type == "CONSTANT":
        comp1_name = "CONSTANT"
        comp1_value = get_constant_value()
        comp1_params = (comp1_value,)
    else:  # PRICE
        comp1_name = "PRICE"
        comp1_params = ()
    
    # Get candles ago for comparison 1
    comp1_candles_ago = get_candles_ago(f"{signal_type} Condition {condition_num} - Left Side")
    
    # Get strategy/comparison type
    strategy = get_strategy_selection()
    
    # Get comparison 2 (right side)
    print(f"\n{signal_type} Condition {condition_num} - Right Side:")
    comp2_type = get_comparison_type()
    
    if comp2_type == "INDICATOR":
        comp2_name = get_indicator_selection()
        comp2_params = get_indicator_params(comp2_name)
    elif comp2_type == "CONSTANT":
        comp2_name = "CONSTANT"
        comp2_value = get_constant_value()
        comp2_params = (comp2_value,)
    else:  # PRICE
        comp2_name = "PRICE"
        comp2_params = ()
    
    # Get candles ago for comparison 2
    comp2_candles_ago = get_candles_ago(f"{signal_type} Condition {condition_num} - Right Side")
    
    # Return structured condition data
    condition_data = {
        'comp1_type': comp1_type,
        'comp1_name': comp1_name,
        'comp1_params': comp1_params,
        'comp1_candles_ago': comp1_candles_ago,
        'strategy': strategy,
        'comp2_type': comp2_type,
        'comp2_name': comp2_name,
        'comp2_params': comp2_params,
        'comp2_candles_ago': comp2_candles_ago
    }
    
    # Show summary
    print(f"✅ Condition {condition_num}: {comp1_name} {strategy} {comp2_name}")
    
    return condition_data

def get_multi_condition_strategy_inputs():
    """
    Main function to collect multi-condition strategy inputs
    Returns all data needed for multi-condition strategy
    """
    print("\n" + "="*70)
    print("🚀 MULTI-CONDITION STRATEGY INPUT COLLECTION")
    print("="*70)
    
    # Get basic inputs (reuse existing functions)
    ticker = input("Enter ticker symbol [default: AAPL]: ").upper().strip()
    if not ticker: ticker = "AAPL"
    period, interval = get_time_interval_inputs()
    total_capital = get_total_capital()
    per_trade_config = get_per_trade_allocation(total_capital)
    
    # Get multi-condition specific inputs
    condition_count = get_multi_condition_count()
    entry_logic = get_logic_type()
    
    print(f"\n🎯 COLLECTING {condition_count} ENTRY CONDITIONS:")
    entry_conditions = []
    for i in range(condition_count):
        condition = get_single_condition_input(i + 1, "Entry")
        entry_conditions.append(condition)
    
    print(f"\n🎯 COLLECTING {condition_count} EXIT CONDITIONS:")
    # Ask if exit logic should be same as entry
    print(f"\nCurrent entry logic: {entry_logic}")
    use_same_logic = input("Use same logic for exit conditions? (y/n) [default: y]: ").strip().lower()
    if use_same_logic in ['', 'y', 'yes']:
        exit_logic = entry_logic
    else:
        print("\nExit logic:")
        exit_logic = get_logic_type()
    
    exit_conditions = []
    for i in range(condition_count):
        condition = get_single_condition_input(i + 1, "Exit")
        exit_conditions.append(condition)
    
    # Get SL/TP configuration
    sl_tp_config = get_sl_tp_configuration()
    
    # Create summary
    print(f"\n" + "="*70)
    print("📋 MULTI-CONDITION STRATEGY SUMMARY")
    print("="*70)
    print(f"📊 Ticker: {ticker}")
    print(f"💰 Total Capital: ${total_capital:,.2f}")
    print(f"📈 Per Trade: ${per_trade_config['amount_per_trade']:,.2f} ({per_trade_config['percentage']:.1f}%)")
    print(f"🔢 Conditions: {condition_count} entry, {condition_count} exit")
    print(f"🧠 Logic: Entry={entry_logic}, Exit={exit_logic}")
    print(f"🛡️ SL/TP: {'Enabled' if sl_tp_config['enabled'] else 'Disabled'}")
    
    print(f"\n📋 ENTRY CONDITIONS ({entry_logic} logic):")
    for i, condition in enumerate(entry_conditions):
        print(f"  {i+1}. {condition['comp1_name']} {condition['strategy']} {condition['comp2_name']}")
    
    print(f"\n📋 EXIT CONDITIONS ({exit_logic} logic):")
    for i, condition in enumerate(exit_conditions):
        print(f"  {i+1}. {condition['comp1_name']} {condition['strategy']} {condition['comp2_name']}")
    
    # Return all data in structured format
    return (
        ticker,                    # 0
        period,                    # 1  
        interval,                  # 2
        total_capital,             # 3
        per_trade_config,          # 4
        sl_tp_config,              # 5
        condition_count,           # 6
        entry_logic,               # 7
        exit_logic,                # 8
        entry_conditions,          # 9
        exit_conditions            # 10
    )
