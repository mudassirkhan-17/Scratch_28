from inputs import *

"""First function to run, will take all inputs from user and store in a variable"""

"""User selects strategy type (1-4) → Strategy class calls the corresponding input function from inputs.py
The input function then collects all detailed parameters (ticker, timeframe, indicators, conditions) through interactive prompts
How it works:
choice "1" → get_strategy_inputs() → asks for ticker, period, indicators, entry/exit conditions
choice "2" → get_multi_strategy_inputs() → asks for multiple conditions with AND/OR logic
choice "3" → get_multi_ticker_inputs() → asks for portfolio allocation across multiple tickers
choice "4" → get_multi_ticker_multi_strategy_inputs() → asks for different strategies per ticker"""

class Strategy:
    def __init__(self):
        self.strategy_data = None
        
    def get_inputs(self):
        print("1. Single Strategy")
        print("2. Multi Strategy") 
        print("3. Multi Ticker")
        print("4. Multi Ticker Multi Strategy")
        
        choice = input("Choose (1-4): ")
        
        if choice == "1":
            self.strategy_data = get_strategy_inputs()
        elif choice == "2":
            self.strategy_data = get_multi_strategy_inputs()
        elif choice == "3":
            self.strategy_data = get_multi_ticker_inputs()
        elif choice == "4":
            self.strategy_data = get_multi_ticker_multi_strategy_inputs()
            
        return self.strategy_data

def calculate_indicators(data, strategy_data):
    """Step 3: Calculate all required indicators"""
    print(f"\nSTEP 3: Calculating indicators...")
    from indicators import calculate_indicator
    from comparision_types import ComparisonType
    
    # Extract indicator info from strategy_data
    entry_comp1_type = strategy_data[3]
    entry_comp1_name = strategy_data[4]
    entry_comp1_params = strategy_data[5]
    
    entry_comp2_type = strategy_data[6]
    entry_comp2_name = strategy_data[7]
    entry_comp2_params = strategy_data[8]
    
    exit_comp1_type = strategy_data[9]
    exit_comp1_name = strategy_data[10]
    exit_comp1_params = strategy_data[11]
    
    exit_comp2_type = strategy_data[12]
    exit_comp2_name = strategy_data[13]
    exit_comp2_params = strategy_data[14]
    
    # Calculate indicators for entry comparison 1
    if entry_comp1_type == ComparisonType.INDICATOR:
        print(f"Calculating {entry_comp1_name} for entry comparison 1...")
        data[f'{entry_comp1_name}_entry1'] = calculate_indicator(data, entry_comp1_name, entry_comp1_params)
        print(f"✅ {entry_comp1_name} calculated")
    
    # Calculate indicators for entry comparison 2  
    if entry_comp2_type == ComparisonType.INDICATOR:
        print(f"Calculating {entry_comp2_name} for entry comparison 2...")
        data[f'{entry_comp2_name}_entry2'] = calculate_indicator(data, entry_comp2_name, entry_comp2_params)
        print(f"✅ {entry_comp2_name} calculated")
    
    # Calculate indicators for exit comparison 1
    if exit_comp1_type == ComparisonType.INDICATOR:
        print(f"Calculating {exit_comp1_name} for exit comparison 1...")
        data[f'{exit_comp1_name}_exit1'] = calculate_indicator(data, exit_comp1_name, exit_comp1_params)
        print(f"✅ {exit_comp1_name} calculated")
    
    # Calculate indicators for exit comparison 2
    if exit_comp2_type == ComparisonType.INDICATOR:
        print(f"Calculating {exit_comp2_name} for exit comparison 2...")
        data[f'{exit_comp2_name}_exit2'] = calculate_indicator(data, exit_comp2_name, exit_comp2_params)
        print(f"✅ {exit_comp2_name} calculated")
    
    print("✅ All indicators calculated")
    print("📋 Next: Generate buy/sell signals")
    
    return data

def generate_signals(data, strategy_data):
    """Step 4: Generate buy/sell signals with candles ago logic"""
    print(f"\nSTEP 4: Generating signals...")
    from comparision_types import ComparisonType
    import comparisons as comp
    
    # Extract all strategy info
    entry_comp1_type = strategy_data[3]
    entry_comp1_name = strategy_data[4] 
    entry_comp1_params = strategy_data[5]
    entry_comp2_type = strategy_data[6]
    entry_comp2_name = strategy_data[7]
    entry_comp2_params = strategy_data[8]
    
    exit_comp1_type = strategy_data[9]
    exit_comp1_name = strategy_data[10]
    exit_comp1_params = strategy_data[11]
    exit_comp2_type = strategy_data[12]
    exit_comp2_name = strategy_data[13]
    exit_comp2_params = strategy_data[14]
    
    entry_strategy = strategy_data[15]
    exit_strategy = strategy_data[16]
    
    entry_comp1_candles_ago = strategy_data[17]
    entry_comp2_candles_ago = strategy_data[18]
    exit_comp1_candles_ago = strategy_data[19]
    exit_comp2_candles_ago = strategy_data[20]
    
    # Add shifted columns to data for comparison functions
    if entry_comp1_type == ComparisonType.INDICATOR:
        data[f'entry_comp1_shifted'] = data[f'{entry_comp1_name}_entry1'].shift(entry_comp1_candles_ago)
    elif entry_comp1_type == ComparisonType.CONSTANT:
        data[f'entry_comp1_shifted'] = entry_comp1_params[0]  # Just the constant value
    else:  # PRICE
        price_col = entry_comp1_params[0]  # e.g., "Close"
        data[f'entry_comp1_shifted'] = data[price_col].shift(entry_comp1_candles_ago)
    
    if entry_comp2_type == ComparisonType.INDICATOR:
        data[f'entry_comp2_shifted'] = data[f'{entry_comp2_name}_entry2'].shift(entry_comp2_candles_ago)
    elif entry_comp2_type == ComparisonType.CONSTANT:
        data[f'entry_comp2_shifted'] = entry_comp2_params[0]
    else:  # PRICE
        price_col = entry_comp2_params[0]
        data[f'entry_comp2_shifted'] = data[price_col].shift(entry_comp2_candles_ago)
    
    # Generate entry signals using existing comparison functions
    if entry_strategy == "CROSSED UP":
        data['Entry_Signal'] = comp.crossed_up(data, 'entry_comp1_shifted', 'entry_comp2_shifted')
    elif entry_strategy == "CROSSED DOWN":
        data['Entry_Signal'] = comp.crossed_down(data, 'entry_comp1_shifted', 'entry_comp2_shifted')
    elif entry_strategy == "GREATER THAN":
        data['Entry_Signal'] = comp.greater_than(data, 'entry_comp1_shifted', 'entry_comp2_shifted')
    elif entry_strategy == "LESS THAN":
        data['Entry_Signal'] = comp.less_than(data, 'entry_comp1_shifted', 'entry_comp2_shifted')
    # Add more comparison types as needed...
    
    # Add shifted columns for exit comparisons
    if exit_comp1_type == ComparisonType.INDICATOR:
        data[f'exit_comp1_shifted'] = data[f'{exit_comp1_name}_exit1'].shift(exit_comp1_candles_ago)
    elif exit_comp1_type == ComparisonType.CONSTANT:
        data[f'exit_comp1_shifted'] = exit_comp1_params[0]
    else:  # PRICE
        price_col = exit_comp1_params[0]
        data[f'exit_comp1_shifted'] = data[price_col].shift(exit_comp1_candles_ago)
    
    if exit_comp2_type == ComparisonType.INDICATOR:
        data[f'exit_comp2_shifted'] = data[f'{exit_comp2_name}_exit2'].shift(exit_comp2_candles_ago)
    elif exit_comp2_type == ComparisonType.CONSTANT:
        data[f'exit_comp2_shifted'] = exit_comp2_params[0]
    else:  # PRICE
        price_col = exit_comp2_params[0]
        data[f'exit_comp2_shifted'] = data[price_col].shift(exit_comp2_candles_ago)
    
    # Generate exit signals using existing comparison functions
    if exit_strategy == "CROSSED UP":
        data['Exit_Signal'] = comp.crossed_up(data, 'exit_comp1_shifted', 'exit_comp2_shifted')
    elif exit_strategy == "CROSSED DOWN":
        data['Exit_Signal'] = comp.crossed_down(data, 'exit_comp1_shifted', 'exit_comp2_shifted')
    elif exit_strategy == "GREATER THAN":
        data['Exit_Signal'] = comp.greater_than(data, 'exit_comp1_shifted', 'exit_comp2_shifted')
    elif exit_strategy == "LESS THAN":
        data['Exit_Signal'] = comp.less_than(data, 'exit_comp1_shifted', 'exit_comp2_shifted')
    
    print("✅ Entry and exit signals generated")
    print("📋 Next: Execute trades based on signals")
    
    return data

def execute_strategy():
    """Execute the complete strategy step by step"""
    
    # Step 1: Get strategy inputs
    print("STEP 1: Getting strategy inputs...")
    strategy = Strategy()
    strategy_data = strategy.get_inputs()
    
    if strategy_data is None:
        print("❌ No strategy data collected")
        return
    
    # Extract the basic info we need
    ticker = strategy_data[0]
    period = strategy_data[1] 
    interval = strategy_data[2]
    
    print(f"✅ Strategy inputs collected for {ticker}")
    
    # Step 2: Download market data
    print(f"\nSTEP 2: Downloading market data...")
    from inputs import download_and_prepare_data
    
    data = download_and_prepare_data(ticker, period, interval)
    
    if data is None:
        print("❌ Failed to download data")
        return
        
    print(f"✅ Downloaded {len(data)} rows of data")
    
    # Step 3: Calculate indicators
    data = calculate_indicators(data, strategy_data)
    
    # Step 4: Generate signals
    data = generate_signals(data, strategy_data)
    
    # Show the final DataFrame
    print(f"\n📊 FINAL DATAFRAME:")
    print(f"Columns: {list(data.columns)}")
    print(f"\nLast 5 rows:")
    print(data.tail())
    
    return strategy_data, data

if __name__ == "__main__":
    execute_strategy()
