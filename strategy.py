from inputs import *

"""First function to run, will take all inputs from user and store in a variable"""

"""User selects strategy type (1-4) → Strategy class calls the corresponding input function from inputs.py
The input function then collects all detailed parameters (ticker, timeframe, indicators, conditions) through interactive prompts
How it works:
choice "1" → get_strategy_inputs() → asks for ticker, period, indicators, entry/exit conditions
choice "2" → get_multi_strategy_inputs() → asks for multiple conditions with AND/OR logic
choice "3" → get_multi_ticker_inputs() → asks for portfolio allocation across multiple tickers
choice "4" → get_multi_ticker_multi_strategy_inputs() → asks for different strategies per ticker"""


def calculate_indicators(data, strategy_data):
    """Step 3: Calculate all required indicators"""
    print(f"\nSTEP 3: Calculating indicators...")
    from indicators import calculate_indicator
    from comparision_types import ComparisonType
    
    # Extract indicator info from strategy_data (adjusted for per_trade_config at index 4)
    entry_comp1_type = strategy_data[5]
    entry_comp1_name = strategy_data[6]
    entry_comp1_params = strategy_data[7]
    
    entry_comp2_type = strategy_data[8]
    entry_comp2_name = strategy_data[9]
    entry_comp2_params = strategy_data[10]
    
    exit_comp1_type = strategy_data[11]
    exit_comp1_name = strategy_data[12]
    exit_comp1_params = strategy_data[13]
    
    exit_comp2_type = strategy_data[14]
    exit_comp2_name = strategy_data[15]
    exit_comp2_params = strategy_data[16]
    
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
    
    # Extract all strategy info (adjusted for per_trade_config at index 4)
    entry_comp1_type = strategy_data[5]
    entry_comp1_name = strategy_data[6] 
    entry_comp1_params = strategy_data[7]
    entry_comp2_type = strategy_data[8]
    entry_comp2_name = strategy_data[9]
    entry_comp2_params = strategy_data[10]
    
    exit_comp1_type = strategy_data[11]
    exit_comp1_name = strategy_data[12]
    exit_comp1_params = strategy_data[13]
    exit_comp2_type = strategy_data[14]
    exit_comp2_name = strategy_data[15]
    exit_comp2_params = strategy_data[16]
    
    entry_strategy = strategy_data[17]
    exit_strategy = strategy_data[18]
    
    entry_comp1_candles_ago = strategy_data[19]
    entry_comp2_candles_ago = strategy_data[20]
    exit_comp1_candles_ago = strategy_data[21]
    exit_comp2_candles_ago = strategy_data[22]
    
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


def calculate_multi_condition_indicators(data, entry_conditions, exit_conditions):
    """Calculate all indicators needed for multi-condition strategy"""
    print(f"\nSTEP 3: Calculating indicators for multi-condition strategy...")
    
    from indicators import calculate_indicator
    
    # Collect all unique indicators needed
    all_conditions = entry_conditions + exit_conditions
    indicators_needed = set()
    
    for condition in all_conditions:
        if condition['comp1_type'] == 'INDICATOR':
            indicators_needed.add((condition['comp1_name'], condition['comp1_params']))
        if condition['comp2_type'] == 'INDICATOR':
            indicators_needed.add((condition['comp2_name'], condition['comp2_params']))
    
    # Calculate each unique indicator - create separate columns for each unique combination
    condition_counter = 1
    for condition in all_conditions:
        if condition['comp1_type'] == 'INDICATOR':
            col_name = f"{condition['comp1_name']}_cond{condition_counter}_left"
            print(f"Calculating {condition['comp1_name']} with params {condition['comp1_params']} as {col_name}...")
            data[col_name] = calculate_indicator(data, condition['comp1_name'], condition['comp1_params'])
            condition['comp1_col'] = col_name  # Store the actual column name
            print(f"✅ {condition['comp1_name']} calculated as {col_name}")
        
        if condition['comp2_type'] == 'INDICATOR':
            col_name = f"{condition['comp2_name']}_cond{condition_counter}_right"
            print(f"Calculating {condition['comp2_name']} with params {condition['comp2_params']} as {col_name}...")
            data[col_name] = calculate_indicator(data, condition['comp2_name'], condition['comp2_params'])
            condition['comp2_col'] = col_name  # Store the actual column name
            print(f"✅ {condition['comp2_name']} calculated as {col_name}")
        
        condition_counter += 1
    
    print("✅ All multi-condition indicators calculated")
    return data


def generate_multi_condition_signals(data, entry_conditions, exit_conditions, entry_logic, exit_logic):
    """Generate entry and exit signals using MultiConditionDetector"""
    print(f"\nSTEP 4: Generating multi-condition signals...")
    
    from new12 import MultiConditionDetector
    
    # Create detector
    detector = MultiConditionDetector()
    detector.set_logic_type(entry_logic, exit_logic)
    
    # Add all conditions
    for condition in entry_conditions:
        detector.add_entry_condition(condition)
    
    for condition in exit_conditions:
        detector.add_exit_condition(condition)
    
    print(detector.get_condition_summary())
    
    # Generate signals for each row
    entry_signals = []
    exit_signals = []
    
    print("🔄 Evaluating conditions for each time period...")
    for i in range(len(data)):
        entry_signal = detector.evaluate_entry_conditions(data, i)
        exit_signal = detector.evaluate_exit_conditions(data, i)
        
        entry_signals.append(entry_signal)
        exit_signals.append(exit_signal)
    
    # Add signals to DataFrame
    data['Entry_Signal'] = entry_signals
    data['Exit_Signal'] = exit_signals
    
    # Count signals
    entry_count = sum(entry_signals)
    exit_count = sum(exit_signals)
    
    print(f"✅ Multi-condition signals generated:")
    print(f"  📈 Entry signals: {entry_count}")
    print(f"  📉 Exit signals: {exit_count}")
    print("📋 Next: Execute trades based on signals")
    
    return data


def execute_long_strategy(data, strategy_data, sl_tp_config, total_capital, per_trade_config):
    """Step 5: Execute Long Entry/Exit Strategy - Modular Version"""
    print(f"\nSTEP 5: Executing Long Entry/Exit Strategy...")
    
    from trade_executor import TradeExecutor
    executor = TradeExecutor(total_capital, sl_tp_config, per_trade_config)
    
    for i in range(len(data)):
        current_price = data['Close'].iloc[i]
        entry_signal = data['Entry_Signal'].iloc[i]
        exit_signal = data['Exit_Signal'].iloc[i]
        
        # Process market tick - handles all logic automatically
        executor.process_market_tick(current_price, entry_signal, exit_signal, "long")
        
        # Update DataFrame tracking
        tracking = executor.get_portfolio_tracking_data(current_price)
        for key, value in tracking.items():
            data.loc[data.index[i], key] = value
    
    # Print final results with advanced metrics
    executor.print_final_results(data)
    return data, executor.trades

def execute_short_strategy(data, strategy_data, sl_tp_config, total_capital, per_trade_config):
    """Step 5: Execute Short Entry/Exit Strategy - Modular Version"""
    print(f"\nSTEP 5: Executing Short Entry/Exit Strategy...")
    
    from trade_executor import TradeExecutor
    executor = TradeExecutor(total_capital, sl_tp_config, per_trade_config)
    
    for i in range(len(data)):
        current_price = data['Close'].iloc[i]
        entry_signal = data['Entry_Signal'].iloc[i]
        exit_signal = data['Exit_Signal'].iloc[i]
        
        # Process market tick - handles all logic automatically
        executor.process_market_tick(current_price, entry_signal, exit_signal, "short")
        
        # Update DataFrame tracking
        tracking = executor.get_portfolio_tracking_data(current_price)
        for key, value in tracking.items():
            data.loc[data.index[i], key] = value
    
    # Print final results with advanced metrics
    executor.print_final_results(data)
    return data, executor.trades

def execute_reversal_strategy(data, strategy_data, sl_tp_config, total_capital, per_trade_config):
    """Step 5: Execute Long/Short Reversal Strategy - Modular Version"""
    print(f"\nSTEP 5: Executing Long/Short Reversal Strategy...")
    print("🔄 REVERSAL STRATEGY: Always in market - Entry=Long, Exit=Short")
    
    from trade_executor import TradeExecutor
    executor = TradeExecutor(total_capital, sl_tp_config, per_trade_config)
    
    for i in range(len(data)):
        current_price = data['Close'].iloc[i]
        entry_signal = data['Entry_Signal'].iloc[i]
        exit_signal = data['Exit_Signal'].iloc[i]
        
        # Process market tick - handles all logic automatically
        executor.process_market_tick(current_price, entry_signal, exit_signal, "reversal")
        
        # Update DataFrame tracking
        tracking = executor.get_portfolio_tracking_data(current_price)
        for key, value in tracking.items():
            data.loc[data.index[i], key] = value
    
    # Print final results with advanced metrics
    executor.print_final_results(data)
    return data, executor.trades

def execute_strategy():
    """Execute the complete strategy step by step"""
    
    # Step 0: Choose Long or Short strategy using inputs.py function
    from inputs import (get_strategy_direction, get_strategy_inputs, 
                       get_multi_strategy_inputs, get_multi_ticker_inputs, 
                       get_multi_ticker_multi_strategy_inputs)
    

    strategy_direction = get_strategy_direction()
    
    if strategy_direction is None:
        print("❌ Strategy direction selection cancelled")
        return
    
    # Map the direction to our strategy type
    if strategy_direction == "Long Only":
        strategy_type = "long"
        print("✅ Selected: Long Strategy")
    elif strategy_direction == "Short Only":
        strategy_type = "short"
        print("✅ Selected: Short Strategy")
    else:  # Long/Short Reversal
        strategy_type = "reversal"
        print("✅ Selected: Long/Short Reversal Strategy")
    
    # Step 1: Choose strategy complexity and get inputs
    print("\nSTEP 1: Getting strategy inputs...")
    print("1. Single Strategy")
    print("2. Multi Strategy") 
    print("3. Multi Ticker")
    print("4. Multi Ticker Multi Strategy")
    
    choice = input("Choose (1-4) [default: 1]: ").strip() or "1"
    
    if choice == "1":
        strategy_data = get_strategy_inputs()
        strategy_complexity = "single"
    elif choice == "2":
        from inputs import get_multi_condition_strategy_inputs
        strategy_data = get_multi_condition_strategy_inputs()
        strategy_complexity = "multi_condition"
    elif choice == "3":
        strategy_data = get_multi_ticker_inputs()
        strategy_complexity = "multi_ticker"
    elif choice == "4":
        strategy_data = get_multi_ticker_multi_strategy_inputs()
        strategy_complexity = "multi_ticker_multi"
    else:
        print("❌ Invalid choice")
        return
    
    if strategy_data is None:
        print("❌ No strategy data collected")
        return
    
    # Extract the basic info based on strategy complexity
    if strategy_complexity == "single":
        # Single condition format: (ticker, period, interval, total_capital, per_trade_config, ...)
        ticker = strategy_data[0]
        period = strategy_data[1] 
        interval = strategy_data[2]
        total_capital = strategy_data[3]
        per_trade_config = strategy_data[4]
        
        print(f"✅ Strategy inputs collected for {ticker}")
        print(f"💰 Total Capital: ${total_capital:,.2f}")
        print(f"📊 Per Trade: ${per_trade_config['amount_per_trade']:,.2f} ({per_trade_config['percentage']:.1f}% allocation)")
        
        # Step 1.5: Get SL/TP Configuration
        from inputs import get_sl_tp_configuration
        sl_tp_config = get_sl_tp_configuration()
        print(f"✅ SL/TP configuration: {sl_tp_config}")
        
    elif strategy_complexity == "multi_condition":
        # Multi-condition format: (ticker, period, interval, total_capital, per_trade_config, sl_tp_config, condition_count, entry_logic, exit_logic, entry_conditions, exit_conditions)
        ticker = strategy_data[0]
        period = strategy_data[1] 
        interval = strategy_data[2]
        total_capital = strategy_data[3]
        per_trade_config = strategy_data[4]
        sl_tp_config = strategy_data[5]
        condition_count = strategy_data[6]
        entry_logic = strategy_data[7]
        exit_logic = strategy_data[8]
        entry_conditions = strategy_data[9]
        exit_conditions = strategy_data[10]
        
        print(f"✅ Multi-condition strategy inputs collected for {ticker}")
        print(f"💰 Total Capital: ${total_capital:,.2f}")
        print(f"📊 Per Trade: ${per_trade_config['amount_per_trade']:,.2f} ({per_trade_config['percentage']:.1f}% allocation)")
        print(f"🔢 Conditions: {condition_count} entry ({entry_logic}), {condition_count} exit ({exit_logic})")
        print(f"✅ SL/TP configuration: {sl_tp_config}")
        
    else:
        print("❌ Unsupported strategy complexity")
        return
    
    # Step 2: Download market data
    print(f"\nSTEP 2: Downloading market data...")
    from inputs import download_and_prepare_data
    
    data = download_and_prepare_data(ticker, period, interval)
    
    if data is None:
        print("❌ Failed to download data")
        return
        
    print(f"✅ Downloaded {len(data)} rows of data")
    
    # Step 3 & 4: Calculate indicators and generate signals based on strategy complexity
    if strategy_complexity == "single":
        # Single condition strategy
        data = calculate_indicators(data, strategy_data)
        data = generate_signals(data, strategy_data)
    elif strategy_complexity == "multi_condition":
        # Multi-condition strategy
        data = calculate_multi_condition_indicators(data, entry_conditions, exit_conditions)
        data = generate_multi_condition_signals(data, entry_conditions, exit_conditions, entry_logic, exit_logic)
    else:
        print("❌ Unsupported strategy complexity for execution")
        return
    
    # Step 5: Execute Strategy based on user choice
    if strategy_type == "long":
        data, trades = execute_long_strategy(data, strategy_data, sl_tp_config, total_capital, per_trade_config)
    elif strategy_type == "short":
        data, trades = execute_short_strategy(data, strategy_data, sl_tp_config, total_capital, per_trade_config)
    else:  # reversal
        data, trades = execute_reversal_strategy(data, strategy_data, sl_tp_config, total_capital, per_trade_config)
    
    return strategy_data, data, trades

if __name__ == "__main__":
    execute_strategy()
