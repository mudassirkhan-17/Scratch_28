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
    elif entry_strategy == "INCREASED":
        data['Entry_Signal'] = comp.increased(data, 'entry_comp1_shifted', 'entry_comp2_shifted')
    elif entry_strategy == "DECREASED":
        data['Entry_Signal'] = comp.decreased(data, 'entry_comp1_shifted', 'entry_comp2_shifted')
    elif entry_strategy == "CROSSED":
        data['Entry_Signal'] = comp.crossed(data, 'entry_comp1_shifted', 'entry_comp2_shifted')
    elif entry_strategy == "EQUAL":
        data['Entry_Signal'] = comp.equal_comparison(data, 'entry_comp1_shifted', 'entry_comp2_shifted')
    elif entry_strategy == "GREATER OR EQUAL":
        data['Entry_Signal'] = comp.greater_or_equal(data, 'entry_comp1_shifted', 'entry_comp2_shifted')
    elif entry_strategy == "LESS OR EQUAL":
        data['Entry_Signal'] = comp.less_or_equal(data, 'entry_comp1_shifted', 'entry_comp2_shifted')
    elif entry_strategy == "WITHIN RANGE":
        data['Entry_Signal'] = comp.within_range(data, 'entry_comp1_shifted', 'entry_comp2_shifted')
    
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
    elif exit_strategy == "INCREASED":
        data['Exit_Signal'] = comp.increased(data, 'exit_comp1_shifted', 'exit_comp2_shifted')
    elif exit_strategy == "DECREASED":
        data['Exit_Signal'] = comp.decreased(data, 'exit_comp1_shifted', 'exit_comp2_shifted')
    elif exit_strategy == "CROSSED":
        data['Exit_Signal'] = comp.crossed(data, 'exit_comp1_shifted', 'exit_comp2_shifted')
    elif exit_strategy == "EQUAL":
        data['Exit_Signal'] = comp.equal_comparison(data, 'exit_comp1_shifted', 'exit_comp2_shifted')
    elif exit_strategy == "GREATER OR EQUAL":
        data['Exit_Signal'] = comp.greater_or_equal(data, 'exit_comp1_shifted', 'exit_comp2_shifted')
    elif exit_strategy == "LESS OR EQUAL":
        data['Exit_Signal'] = comp.less_or_equal(data, 'exit_comp1_shifted', 'exit_comp2_shifted')
    elif exit_strategy == "WITHIN RANGE":
        data['Exit_Signal'] = comp.within_range(data, 'exit_comp1_shifted', 'exit_comp2_shifted')
    
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


def calculate_multi_ticker_indicators(data, strategy_data, tickers):
    """Calculate indicators for each ticker in multi-ticker strategy"""
    print(f"\nSTEP 3: Calculating multi-ticker indicators...")
    from indicators import calculate_indicator
    from comparision_types import ComparisonType
    
    # Extract strategy data (single strategy applied to all tickers)
    entry_comp1_type = strategy_data['entry_comp1_type']
    entry_comp1_name = strategy_data['entry_comp1_name']
    entry_comp1_params = strategy_data['entry_comp1_params']
    
    entry_comp2_type = strategy_data['entry_comp2_type']
    entry_comp2_name = strategy_data['entry_comp2_name']
    entry_comp2_params = strategy_data['entry_comp2_params']
    
    exit_comp1_type = strategy_data['exit_comp1_type']
    exit_comp1_name = strategy_data['exit_comp1_name']
    exit_comp1_params = strategy_data['exit_comp1_params']
    
    exit_comp2_type = strategy_data['exit_comp2_type']
    exit_comp2_name = strategy_data['exit_comp2_name']
    exit_comp2_params = strategy_data['exit_comp2_params']
    
    print(f"📊 Strategy: {strategy_data['entry_strategy']} / {strategy_data['exit_strategy']}")
    print(f"📈 Applying to tickers: {', '.join(tickers)}")
    
    # Calculate indicators for each ticker
    for ticker in tickers:
        print(f"\n📊 Calculating indicators for {ticker}...")
        
        # Create ticker-specific price data for indicator calculation
        ticker_data = data[['Date', f'{ticker}_Open', f'{ticker}_High', f'{ticker}_Low', f'{ticker}_Close', f'{ticker}_Volume']].copy()
        ticker_data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']  # Rename for indicator functions
        
        # Calculate entry comparison 1 indicator
        if entry_comp1_type == ComparisonType.INDICATOR:
            print(f"  📈 Calculating {entry_comp1_name}{entry_comp1_params} for entry comparison 1...")
            indicator_values = calculate_indicator(ticker_data, entry_comp1_name, entry_comp1_params)
            data[f'{ticker}_{entry_comp1_name}_entry1'] = indicator_values
            print(f"  ✅ {ticker}_{entry_comp1_name}_entry1 calculated")
        
        # Calculate entry comparison 2 indicator
        if entry_comp2_type == ComparisonType.INDICATOR:
            print(f"  📈 Calculating {entry_comp2_name}{entry_comp2_params} for entry comparison 2...")
            indicator_values = calculate_indicator(ticker_data, entry_comp2_name, entry_comp2_params)
            data[f'{ticker}_{entry_comp2_name}_entry2'] = indicator_values
            print(f"  ✅ {ticker}_{entry_comp2_name}_entry2 calculated")
        
        # Calculate exit comparison 1 indicator
        if exit_comp1_type == ComparisonType.INDICATOR:
            print(f"  📈 Calculating {exit_comp1_name}{exit_comp1_params} for exit comparison 1...")
            indicator_values = calculate_indicator(ticker_data, exit_comp1_name, exit_comp1_params)
            data[f'{ticker}_{exit_comp1_name}_exit1'] = indicator_values
            print(f"  ✅ {ticker}_{exit_comp1_name}_exit1 calculated")
        
        # Calculate exit comparison 2 indicator
        if exit_comp2_type == ComparisonType.INDICATOR:
            print(f"  📈 Calculating {exit_comp2_name}{exit_comp2_params} for exit comparison 2...")
            indicator_values = calculate_indicator(ticker_data, exit_comp2_name, exit_comp2_params)
            data[f'{ticker}_{exit_comp2_name}_exit2'] = indicator_values
            print(f"  ✅ {ticker}_{exit_comp2_name}_exit2 calculated")
        
        print(f"✅ {ticker} indicators complete")
    
    print(f"\n✅ All multi-ticker indicators calculated")
    print(f"📊 New columns added: {[col for col in data.columns if any(ticker in col for ticker in tickers) and ('_SMA_' in col or '_EMA_' in col or '_RSI_' in col)]}")
    
    return data

def calculate_multi_ticker_multi_strategy_indicators(data, strategy_data, tickers):
    """Calculate different indicators for each ticker based on their unique strategies"""
    print(f"\nSTEP 3: Calculating multi-ticker multi-strategy indicators...")
    from indicators import calculate_indicator
    from comparision_types import ComparisonType
    
    print(f"📊 Each ticker has its own unique strategy")
    print(f"📈 Processing tickers: {', '.join(tickers)}")
    
    # Process each ticker with its own strategy
    for ticker in tickers:
        ticker_strategy = strategy_data['ticker_strategies'][ticker]
        
        print(f"\n📊 Calculating indicators for {ticker}...")
        print(f"  Strategy type: {ticker_strategy['type']}")
        
        # Get ticker-specific data columns and rename them for indicator calculation
        ticker_cols = [col for col in data.columns if col.startswith(f'{ticker}_')]
        ticker_data = data[['Date'] + ticker_cols].copy()
        
        # Rename columns: AAPL_1_Close -> Close, AAPL_1_Open -> Open, etc.
        rename_map = {}
        for col in ticker_cols:
            # Remove ticker prefix: AAPL_1_Close -> Close
            new_name = col.replace(f'{ticker}_', '')
            rename_map[col] = new_name
        ticker_data = ticker_data.rename(columns=rename_map)
        
        if ticker_strategy['type'] == 'single':
            # Single condition strategy for this ticker
            entry_comp1_type = ticker_strategy['entry_comp1_type']
            entry_comp1_name = ticker_strategy['entry_comp1_name']
            entry_comp1_params = ticker_strategy['entry_comp1_params']
            
            entry_comp2_type = ticker_strategy['entry_comp2_type']
            entry_comp2_name = ticker_strategy['entry_comp2_name']
            entry_comp2_params = ticker_strategy['entry_comp2_params']
            
            exit_comp1_type = ticker_strategy['exit_comp1_type']
            exit_comp1_name = ticker_strategy['exit_comp1_name']
            exit_comp1_params = ticker_strategy['exit_comp1_params']
            
            exit_comp2_type = ticker_strategy['exit_comp2_type']
            exit_comp2_name = ticker_strategy['exit_comp2_name']
            exit_comp2_params = ticker_strategy['exit_comp2_params']
            
            # Calculate entry indicators
            if entry_comp1_type == ComparisonType.INDICATOR:
                print(f"  📈 Calculating {entry_comp1_name}{entry_comp1_params} for entry comparison 1...")
                indicator_values = calculate_indicator(ticker_data, entry_comp1_name, entry_comp1_params)
                data[f'{ticker}_{entry_comp1_name}_entry1'] = indicator_values
                print(f"  ✅ {ticker}_{entry_comp1_name}_entry1 calculated")
            
            if entry_comp2_type == ComparisonType.INDICATOR:
                print(f"  📈 Calculating {entry_comp2_name}{entry_comp2_params} for entry comparison 2...")
                indicator_values = calculate_indicator(ticker_data, entry_comp2_name, entry_comp2_params)
                data[f'{ticker}_{entry_comp2_name}_entry2'] = indicator_values
                print(f"  ✅ {ticker}_{entry_comp2_name}_entry2 calculated")
            
            # Calculate exit indicators
            if exit_comp1_type == ComparisonType.INDICATOR:
                print(f"  📈 Calculating {exit_comp1_name}{exit_comp1_params} for exit comparison 1...")
                indicator_values = calculate_indicator(ticker_data, exit_comp1_name, exit_comp1_params)
                data[f'{ticker}_{exit_comp1_name}_exit1'] = indicator_values
                print(f"  ✅ {ticker}_{exit_comp1_name}_exit1 calculated")
            
            if exit_comp2_type == ComparisonType.INDICATOR:
                print(f"  📈 Calculating {exit_comp2_name}{exit_comp2_params} for exit comparison 2...")
                indicator_values = calculate_indicator(ticker_data, exit_comp2_name, exit_comp2_params)
                data[f'{ticker}_{exit_comp2_name}_exit2'] = indicator_values
                print(f"  ✅ {ticker}_{exit_comp2_name}_exit2 calculated")
        
        elif ticker_strategy['type'] == 'multi':
            # Multi-condition strategy for this ticker
            entry_conditions = ticker_strategy['entry_conditions']
            exit_conditions = ticker_strategy['exit_conditions']
            all_conditions = entry_conditions + exit_conditions
            
            condition_counter = 1
            for condition in all_conditions:
                if condition['comp1_type'] == 'INDICATOR':
                    col_name = f"{ticker}_{condition['comp1_name']}_cond{condition_counter}_left"
                    print(f"  📈 Calculating {condition['comp1_name']} as {col_name}...")
                    data[col_name] = calculate_indicator(ticker_data, condition['comp1_name'], condition['comp1_params'])
                    condition['comp1_col'] = col_name
                    print(f"  ✅ {col_name} calculated")
                
                if condition['comp2_type'] == 'INDICATOR':
                    col_name = f"{ticker}_{condition['comp2_name']}_cond{condition_counter}_right"
                    print(f"  📈 Calculating {condition['comp2_name']} as {col_name}...")
                    data[col_name] = calculate_indicator(ticker_data, condition['comp2_name'], condition['comp2_params'])
                    condition['comp2_col'] = col_name
                    print(f"  ✅ {col_name} calculated")
                
                condition_counter += 1
        
        print(f"✅ {ticker} indicators complete")
    
    print(f"\n✅ All multi-ticker multi-strategy indicators calculated")
    
    return data

def generate_multi_ticker_signals(data, strategy_data, tickers):
    """Generate entry and exit signals for each ticker in multi-ticker strategy"""
    print(f"\nSTEP 4: Generating multi-ticker signals...")
    
    # Import comparison functions
    from comparisons import (crossed_up, crossed_down, greater_than, less_than, 
                           equal_comparison, increased, decreased, crossed,
                           greater_or_equal, less_or_equal, within_range)
    from comparision_types import ComparisonType
    
    # Extract strategy data
    entry_strategy = strategy_data['entry_strategy']
    exit_strategy = strategy_data['exit_strategy']
    
    entry_comp1_candles_ago = strategy_data['entry_comp1_candles_ago']
    entry_comp2_candles_ago = strategy_data['entry_comp2_candles_ago']
    exit_comp1_candles_ago = strategy_data['exit_comp1_candles_ago']
    exit_comp2_candles_ago = strategy_data['exit_comp2_candles_ago']
    
    # Strategy mapping
    strategy_map = {
        "CROSSED UP": crossed_up,
        "CROSSED DOWN": crossed_down,
        "GREATER THAN": greater_than,
        "LESS THAN": less_than,
        "EQUAL": equal_comparison,
        "GREATER OR EQUAL": greater_or_equal,
        "LESS OR EQUAL": less_or_equal,
        "WITHIN RANGE": within_range,
        "INCREASED": increased,
        "DECREASED": decreased,
        "CROSSED": crossed
    }
    
    print(f"📊 Entry Strategy: {entry_strategy}")
    print(f"📊 Exit Strategy: {exit_strategy}")
    
    # Generate signals for each ticker
    for ticker in tickers:
        print(f"\n📊 Generating signals for {ticker}...")
        
        # Prepare comparison columns for entry
        entry_col1 = get_comparison_column(data, strategy_data, ticker, 'entry', 1, entry_comp1_candles_ago)
        entry_col2 = get_comparison_column(data, strategy_data, ticker, 'entry', 2, entry_comp2_candles_ago)
        
        # Prepare comparison columns for exit
        exit_col1 = get_comparison_column(data, strategy_data, ticker, 'exit', 1, exit_comp1_candles_ago)
        exit_col2 = get_comparison_column(data, strategy_data, ticker, 'exit', 2, exit_comp2_candles_ago)
        
        # Generate entry signals
        entry_func = strategy_map.get(entry_strategy)
        if entry_func:
            print(f"  📈 Generating entry signals: {entry_col1} {entry_strategy} {entry_col2}")
            data[f'{ticker}_Entry_Signal'] = entry_func(data, entry_col1, entry_col2)
            print(f"  ✅ {ticker}_Entry_Signal generated")
        
        # Generate exit signals
        exit_func = strategy_map.get(exit_strategy)
        if exit_func:
            print(f"  📉 Generating exit signals: {exit_col1} {exit_strategy} {exit_col2}")
            data[f'{ticker}_Exit_Signal'] = exit_func(data, exit_col1, exit_col2)
            print(f"  ✅ {ticker}_Exit_Signal generated")
        
        print(f"✅ {ticker} signals complete")
    
    # Summary
    entry_signals = [col for col in data.columns if '_Entry_Signal' in col]
    exit_signals = [col for col in data.columns if '_Exit_Signal' in col]
    
    print(f"\n✅ All multi-ticker signals generated")
    print(f"📈 Entry signals: {entry_signals}")
    print(f"📉 Exit signals: {exit_signals}")
    
    return data

def generate_multi_ticker_multi_strategy_signals(data, strategy_data, tickers):
    """Generate signals for each ticker using their unique strategies"""
    print(f"\nSTEP 4: Generating multi-ticker multi-strategy signals...")
    
    # Import comparison functions
    from comparisons import (crossed_up, crossed_down, greater_than, less_than, 
                           equal_comparison, increased, decreased, crossed,
                           greater_or_equal, less_or_equal, within_range)
    from comparision_types import ComparisonType
    
    # Strategy mapping
    strategy_map = {
        "CROSSED UP": crossed_up,
        "CROSSED DOWN": crossed_down,
        "GREATER THAN": greater_than,
        "LESS THAN": less_than,
        "EQUAL": equal_comparison,
        "GREATER OR EQUAL": greater_or_equal,
        "LESS OR EQUAL": less_or_equal,
        "WITHIN RANGE": within_range,
        "INCREASED": increased,
        "DECREASED": decreased,
        "CROSSED": crossed
    }
    
    print(f"📊 Each ticker uses its own unique strategy")
    
    # Generate signals for each ticker
    for ticker in tickers:
        ticker_strategy = strategy_data['ticker_strategies'][ticker]
        
        print(f"\n📊 Generating signals for {ticker}...")
        print(f"  Strategy type: {ticker_strategy['type']}")
        
        if ticker_strategy['type'] == 'single':
            # Single condition strategy
            entry_strategy = ticker_strategy['entry_strategy']
            exit_strategy = ticker_strategy['exit_strategy']
            
            entry_comp1_candles_ago = ticker_strategy['entry_comp1_candles_ago']
            entry_comp2_candles_ago = ticker_strategy['entry_comp2_candles_ago']
            exit_comp1_candles_ago = ticker_strategy['exit_comp1_candles_ago']
            exit_comp2_candles_ago = ticker_strategy['exit_comp2_candles_ago']
            
            # Prepare comparison columns for entry
            entry_col1 = get_ticker_comparison_column(data, ticker_strategy, ticker, 'entry', 1, entry_comp1_candles_ago)
            entry_col2 = get_ticker_comparison_column(data, ticker_strategy, ticker, 'entry', 2, entry_comp2_candles_ago)
            
            # Prepare comparison columns for exit
            exit_col1 = get_ticker_comparison_column(data, ticker_strategy, ticker, 'exit', 1, exit_comp1_candles_ago)
            exit_col2 = get_ticker_comparison_column(data, ticker_strategy, ticker, 'exit', 2, exit_comp2_candles_ago)
            
            # Generate entry signals
            entry_func = strategy_map.get(entry_strategy)
            if entry_func:
                print(f"  📈 Generating entry signals: {entry_col1} {entry_strategy} {entry_col2}")
                data[f'{ticker}_Entry_Signal'] = entry_func(data, entry_col1, entry_col2)
                print(f"  ✅ {ticker}_Entry_Signal generated")
            
            # Generate exit signals
            exit_func = strategy_map.get(exit_strategy)
            if exit_func:
                print(f"  📉 Generating exit signals: {exit_col1} {exit_strategy} {exit_col2}")
                data[f'{ticker}_Exit_Signal'] = exit_func(data, exit_col1, exit_col2)
                print(f"  ✅ {ticker}_Exit_Signal generated")
        
        elif ticker_strategy['type'] == 'multi':
            # Multi-condition strategy
            entry_conditions = ticker_strategy['entry_conditions']
            exit_conditions = ticker_strategy['exit_conditions']
            entry_logic = ticker_strategy['entry_logic']
            exit_logic = ticker_strategy['exit_logic']
            
            # Generate entry signals using multi-condition logic
            entry_results = []
            for condition in entry_conditions:
                col1 = get_ticker_multi_condition_column(data, ticker, condition, 'comp1')
                col2 = get_ticker_multi_condition_column(data, ticker, condition, 'comp2')
                strategy = condition['strategy']
                
                strategy_func = strategy_map.get(strategy)
                if strategy_func:
                    result = strategy_func(data, col1, col2)
                    entry_results.append(result)
            
            # Combine entry signals based on logic
            if entry_logic == 'AND':
                data[f'{ticker}_Entry_Signal'] = entry_results[0]
                for result in entry_results[1:]:
                    data[f'{ticker}_Entry_Signal'] = data[f'{ticker}_Entry_Signal'] & result
            else:  # OR
                data[f'{ticker}_Entry_Signal'] = entry_results[0]
                for result in entry_results[1:]:
                    data[f'{ticker}_Entry_Signal'] = data[f'{ticker}_Entry_Signal'] | result
            
            print(f"  ✅ {ticker}_Entry_Signal generated ({entry_logic} logic)")
            
            # Generate exit signals using multi-condition logic
            exit_results = []
            for condition in exit_conditions:
                col1 = get_ticker_multi_condition_column(data, ticker, condition, 'comp1')
                col2 = get_ticker_multi_condition_column(data, ticker, condition, 'comp2')
                strategy = condition['strategy']
                
                strategy_func = strategy_map.get(strategy)
                if strategy_func:
                    result = strategy_func(data, col1, col2)
                    exit_results.append(result)
            
            # Combine exit signals based on logic
            if exit_logic == 'AND':
                data[f'{ticker}_Exit_Signal'] = exit_results[0]
                for result in exit_results[1:]:
                    data[f'{ticker}_Exit_Signal'] = data[f'{ticker}_Exit_Signal'] & result
            else:  # OR
                data[f'{ticker}_Exit_Signal'] = exit_results[0]
                for result in exit_results[1:]:
                    data[f'{ticker}_Exit_Signal'] = data[f'{ticker}_Exit_Signal'] | result
            
            print(f"  ✅ {ticker}_Exit_Signal generated ({exit_logic} logic)")
        
        print(f"✅ {ticker} signals complete")
    
    # Summary
    entry_signals = [col for col in data.columns if '_Entry_Signal' in col]
    exit_signals = [col for col in data.columns if '_Exit_Signal' in col]
    
    print(f"\n✅ All multi-ticker multi-strategy signals generated")
    print(f"📈 Entry signals: {entry_signals}")
    print(f"📉 Exit signals: {exit_signals}")
    
    return data

def get_ticker_comparison_column(data, ticker_strategy, ticker, signal_type, comp_num, candles_ago):
    """Helper function to get comparison column for ticker-specific strategy"""
    from comparision_types import ComparisonType
    
    comp_type = ticker_strategy[f'{signal_type}_comp{comp_num}_type']
    comp_name = ticker_strategy[f'{signal_type}_comp{comp_num}_name']
    comp_params = ticker_strategy[f'{signal_type}_comp{comp_num}_params']
    
    if comp_type == ComparisonType.INDICATOR:
        base_col = f'{ticker}_{comp_name}_{signal_type}{comp_num}'
        if candles_ago > 0:
            shifted_col = f'{base_col}_shifted_{candles_ago}'
            if shifted_col not in data.columns:
                data[shifted_col] = data[base_col].shift(candles_ago)
            return shifted_col
        return base_col
    elif comp_type == ComparisonType.CONSTANT:
        const_col = f'{ticker}_CONSTANT_{comp_params[0]}'
        if const_col not in data.columns:
            data[const_col] = comp_params[0]
        return const_col
    else:  # PRICE
        price_col = f'{ticker}_{comp_params[0]}'
        if candles_ago > 0:
            shifted_col = f'{price_col}_shifted_{candles_ago}'
            if shifted_col not in data.columns:
                data[shifted_col] = data[price_col].shift(candles_ago)
            return shifted_col
        return price_col

def get_ticker_multi_condition_column(data, ticker, condition, comp_key):
    """Helper function to get column for multi-condition ticker strategy"""
    comp_type = condition[f'{comp_key}_type']
    
    if comp_type == 'INDICATOR':
        # Use the stored column name from indicator calculation
        return condition[f'{comp_key}_col']
    elif comp_type == 'CONSTANT':
        const_value = condition[f'{comp_key}_value']
        const_col = f'{ticker}_CONSTANT_{const_value}'
        if const_col not in data.columns:
            data[const_col] = const_value
        return const_col
    else:  # PRICE
        price_type = condition[f'{comp_key}_price']
        price_col = f'{ticker}_{price_type}'
        candles_ago = condition[f'{comp_key}_candles_ago']
        if candles_ago > 0:
            shifted_col = f'{price_col}_shifted_{candles_ago}'
            if shifted_col not in data.columns:
                data[shifted_col] = data[price_col].shift(candles_ago)
            return shifted_col
        return price_col

def get_comparison_column(data, strategy_data, ticker, signal_type, comp_num, candles_ago):
    """Helper function to get the correct comparison column name with candles ago logic"""
    from comparision_types import ComparisonType
    
    # Get comparison info
    comp_type = strategy_data[f'{signal_type}_comp{comp_num}_type']
    comp_name = strategy_data[f'{signal_type}_comp{comp_num}_name']
    comp_params = strategy_data[f'{signal_type}_comp{comp_num}_params']
    
    if comp_type == ComparisonType.INDICATOR:
        # Use ticker-prefixed indicator column
        base_col = f'{ticker}_{comp_name}_{signal_type}{comp_num}'
        
        # Apply candles ago logic if needed
        if candles_ago > 0:
            shifted_col = f'{base_col}_shifted_{candles_ago}'
            if shifted_col not in data.columns:
                data[shifted_col] = data[base_col].shift(candles_ago)
            return shifted_col
        else:
            return base_col
            
    elif comp_type == ComparisonType.CONSTANT:
        # Create constant column
        const_col = f'{ticker}_CONSTANT_{comp_params[0]}'
        if const_col not in data.columns:
            data[const_col] = comp_params[0]
        return const_col
        
    else:  # PRICE
        # Use ticker-prefixed price column
        price_col = f'{ticker}_Close'
        
        # Apply candles ago logic if needed
        if candles_ago > 0:
            shifted_col = f'{price_col}_shifted_{candles_ago}'
            if shifted_col not in data.columns:
                data[shifted_col] = data[price_col].shift(candles_ago)
            return shifted_col
        else:
            return price_col

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

def execute_multi_ticker_strategy(data, strategy_data, strategy_type):
    """Execute multi-ticker strategy with portfolio allocation management"""
    print(f"\nSTEP 5: Executing Multi-Ticker {strategy_type.title()} Strategy...")
    
    from multi_ticker_portfolio import MultiTickerPortfolioManager
    
    # Extract strategy parameters
    tickers = strategy_data['tickers']
    total_capital = strategy_data['total_capital']
    allocations = strategy_data['allocations']
    trade_sizes = strategy_data['trade_sizes']
    sl_tp_config = strategy_data['sl_tp_config']
    
    # Initialize multi-ticker portfolio manager
    portfolio_manager = MultiTickerPortfolioManager(
        total_capital, allocations, trade_sizes, sl_tp_config
    )
    
    print(f"📊 Processing {len(data)} market periods...")
    
    # Process each market period
    for i in range(len(data)):
        # Get current prices for all tickers
        current_prices = {}
        for ticker in tickers:
            current_prices[ticker] = data[f'{ticker}_Close'].iloc[i]
        
        # Get signals for all tickers
        signals = {}
        for ticker in tickers:
            signals[f'{ticker}_Entry_Signal'] = data[f'{ticker}_Entry_Signal'].iloc[i]
            signals[f'{ticker}_Exit_Signal'] = data[f'{ticker}_Exit_Signal'].iloc[i]
        
        # Process market tick for all tickers
        total_portfolio_value = portfolio_manager.process_market_tick(
            current_prices, signals, strategy_type
        )
        
        # Update data with portfolio tracking
        data.loc[data.index[i], 'Portfolio_Value'] = total_portfolio_value
        
        # Add per-ticker values for tracking
        for ticker in tickers:
            ticker_portfolio = portfolio_manager.ticker_portfolios[ticker]
            ticker_value = ticker_portfolio.get_portfolio_value(current_prices[ticker])
            data.loc[data.index[i], f'{ticker}_Portfolio_Value'] = ticker_value
    
    # Print final results
    portfolio_manager.print_final_results(data)
    
    return data, portfolio_manager.all_trades

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
        print("⚠️  LIQUIDATION PROTECTION: Enabled at 100% loss on position value")
        print("💡 If price doubles from entry, position will be auto-liquidated")
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
        
    elif strategy_complexity == "multi_ticker":
        # Multi-ticker format: dictionary with tickers, allocations, strategy_data, etc.
        tickers = strategy_data['tickers']
        total_capital = strategy_data['total_capital']
        allocations = strategy_data['allocations']
        trade_sizes = strategy_data['trade_sizes']
        period = strategy_data['period']
        interval = strategy_data['interval']
        sl_tp_config = strategy_data['sl_tp_config']
        
        print(f"✅ Multi-ticker strategy inputs collected")
        print(f"📈 Tickers: {', '.join(tickers)}")
        print(f"💰 Total Capital: ${total_capital:,.2f}")
        print(f"📊 Allocations: {', '.join([f'{t}:{a*100:.1f}%' for t, a in allocations.items()])}")
        print(f"✅ SL/TP configuration: {sl_tp_config}")
        
    elif strategy_complexity == "multi_ticker_multi":
        # Multi-ticker multi-strategy format
        tickers = strategy_data['tickers']
        total_capital = strategy_data['total_capital']
        allocations = strategy_data['allocations']
        trade_sizes = strategy_data['trade_sizes']
        period = strategy_data['period']
        interval = strategy_data['interval']
        sl_tp_config = strategy_data['sl_tp_config']
        ticker_strategies = strategy_data['ticker_strategies']
        
        print(f"✅ Multi-ticker multi-strategy inputs collected")
        print(f"📈 Tickers: {', '.join(tickers)}")
        print(f"💰 Total Capital: ${total_capital:,.2f}")
        print(f"📊 Each ticker has unique strategy")
        print(f"✅ SL/TP configuration: {sl_tp_config}")
        
    else:
        print("❌ Unsupported strategy complexity")
        return
    
    # Step 2: Download market data
    print(f"\nSTEP 2: Downloading market data...")
    
    if strategy_complexity in ["multi_ticker", "multi_ticker_multi"]:
        from inputs import download_multi_ticker_data
        data = download_multi_ticker_data(tickers, period, interval)
    else:
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
    elif strategy_complexity == "multi_ticker":
        # Multi-ticker strategy - use actual column names from data
        actual_tickers = []
        for ticker in tickers:
            # Find the actual ticker names in the data columns (e.g., AAPL_1, AAPL_2)
            ticker_columns = [col for col in data.columns if col.startswith(f'{ticker}_') and col.endswith('_Close')]
            for col in ticker_columns:
                actual_ticker = col.replace('_Close', '')
                if actual_ticker not in actual_tickers:  # Avoid duplicates
                    actual_tickers.append(actual_ticker)
        
        print(f"📊 Original tickers: {tickers}")
        print(f"📊 Actual ticker columns: {actual_tickers}")
        
        data = calculate_multi_ticker_indicators(data, strategy_data, actual_tickers)
        data = generate_multi_ticker_signals(data, strategy_data, actual_tickers)
    elif strategy_complexity == "multi_ticker_multi":
        # Multi-ticker multi-strategy - each ticker has unique strategy
        actual_tickers = []
        ticker_mapping = {}
        
        for ticker in tickers:
            # Find the actual ticker names in the data columns (e.g., AAPL_1, AAPL_2)
            ticker_columns = [col for col in data.columns if col.startswith(f'{ticker}_') and col.endswith('_Close')]
            for col in ticker_columns:
                actual_ticker = col.replace('_Close', '')
                if actual_ticker not in actual_tickers:  # Avoid duplicates
                    actual_tickers.append(actual_ticker)
                    ticker_mapping[actual_ticker] = ticker  # Map AAPL_1 -> AAPL
        
        print(f"📊 Original tickers: {tickers}")
        print(f"📊 Actual ticker columns: {actual_tickers}")
        print(f"📊 Ticker mapping: {ticker_mapping}")
        
        # Update ticker_strategies dictionary to use actual ticker names
        original_strategies = strategy_data['ticker_strategies'].copy()
        new_strategies = {}
        for actual_ticker, original_ticker in ticker_mapping.items():
            new_strategies[actual_ticker] = original_strategies[original_ticker]
        
        # Update strategy_data with actual tickers and mapped strategies
        strategy_data['tickers'] = actual_tickers
        strategy_data['ticker_strategies'] = new_strategies
        
        data = calculate_multi_ticker_multi_strategy_indicators(data, strategy_data, actual_tickers)
        data = generate_multi_ticker_multi_strategy_signals(data, strategy_data, actual_tickers)
    else:
        print("❌ Unsupported strategy complexity for execution")
        return
    
    # Step 5: Execute Strategy based on user choice
    if strategy_complexity in ["multi_ticker", "multi_ticker_multi"]:
        # Multi-ticker execution - update strategy_data with actual tickers
        # Create proper allocations and trade_sizes for actual tickers
        original_allocations = strategy_data['allocations'].copy()
        original_trade_sizes = strategy_data['trade_sizes'].copy()
        
        # Create new allocations and trade_sizes for actual tickers
        new_allocations = {}
        new_trade_sizes = {}
        ticker_mapping = {}
        
        original_ticker_list = list(original_allocations.keys())
        
        for i, actual_ticker in enumerate(actual_tickers):
            # Map to original ticker (cycling through if more actual than original)
            original_ticker = original_ticker_list[i % len(original_ticker_list)]
            ticker_mapping[actual_ticker] = original_ticker
            
            # Copy allocation and trade size
            new_allocations[actual_ticker] = original_allocations[original_ticker]
            new_trade_sizes[actual_ticker] = original_trade_sizes[original_ticker]
        
        print(f"📊 Ticker mapping: {ticker_mapping}")
        print(f"📊 New allocations: {new_allocations}")
        
        # Update strategy_data
        strategy_data['tickers'] = actual_tickers
        strategy_data['allocations'] = new_allocations
        strategy_data['trade_sizes'] = new_trade_sizes
        strategy_data['ticker_mapping'] = ticker_mapping
        data, trades = execute_multi_ticker_strategy(data, strategy_data, strategy_type)
    elif strategy_type == "long":
        data, trades = execute_long_strategy(data, strategy_data, sl_tp_config, total_capital, per_trade_config)
    elif strategy_type == "short":
        data, trades = execute_short_strategy(data, strategy_data, sl_tp_config, total_capital, per_trade_config)
    else:  # reversal
        data, trades = execute_reversal_strategy(data, strategy_data, sl_tp_config, total_capital, per_trade_config)
    
    return strategy_data, data, trades

if __name__ == "__main__":
    execute_strategy()
