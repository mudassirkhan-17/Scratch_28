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

def execute_long_strategy(data, strategy_data):
    """Step 5: Execute Long Entry/Exit Strategy - Using Your Exact Variables"""
    print(f"\nSTEP 5: Executing Long Entry/Exit Strategy...")
    
    # Your exact variables
    initial_cash = 1000  # Money we start with
    invested_amount = initial_cash * 0.8  # 80% available for investment
    remaining = 0  # Unused investment money
    shares_owned = 0  # How many shares we own
    buying_price = 0  # Actual money spent on shares
    final_cash = 0  # Money from selling
    trades = []
    
    print(f"Starting with: ${initial_cash:,.2f}")
    print(f"Available to invest: ${invested_amount:,.2f} (80%)")
    
    for i in range(len(data)):
        current_price = data['Close'].iloc[i]
        entry_signal = data['Entry_Signal'].iloc[i]
        exit_signal = data['Exit_Signal'].iloc[i]
        
        # LONG ENTRY: Buy shares when signal says BUY
        if entry_signal and shares_owned == 0:
            # Calculate how many shares we can buy with invested_amount
            max_shares = int(invested_amount / current_price)  # Whole shares only
            buying_price = max_shares * current_price  # Actual money spent
            shares_owned = max_shares  # Shares we own
            remaining = invested_amount - buying_price  # Leftover investment money
            final_cash = 0  # Reset for calculation
            
            print(f"LONG ENTRY: Bought {shares_owned} shares at ${current_price:.2f}")
            print(f"  Money spent (buying_price): ${buying_price:,.2f}")
            print(f"  Leftover investment money (remaining): ${remaining:,.2f}")
            
            trades.append({
                'type': 'BUY',
                'price': current_price,
                'shares': shares_owned,
                'money_spent': buying_price
            })
        
        # LONG EXIT: Sell shares when signal says SELL
        elif exit_signal and shares_owned > 0:
            selling_price = shares_owned * current_price  # Money received from selling
            
            # Your Formula: final_cash = remaining + buying_price + (selling_price - buying_price)
            final_cash = remaining + buying_price + (selling_price - buying_price)
            
            profit_loss = selling_price - buying_price  # Profit or loss on shares
            
            print(f"LONG EXIT: Sold {shares_owned} shares at ${current_price:.2f}")
            print(f"  Money received (selling_price): ${selling_price:,.2f}")
            print(f"  Profit/Loss on shares: ${profit_loss:,.2f}")
            print(f"  Final cash (your formula): ${final_cash:,.2f}")
            
            trades.append({
                'type': 'SELL',
                'price': current_price,
                'shares': shares_owned,
                'money_received': selling_price,
                'profit_loss': profit_loss
            })
            
            # Reset for next trade - final_cash becomes new invested_amount
            invested_amount = final_cash
            remaining = 0
            shares_owned = 0
            buying_price = 0
        
        # Calculate current total portfolio value (only your variables)
        if shares_owned > 0:
            current_position_value = shares_owned * current_price
            total_portfolio = remaining + current_position_value
        else:
            total_portfolio = final_cash
        
        # Store in DataFrame (only your variables)
        data.loc[data.index[i], 'Portfolio_Value'] = total_portfolio
        data.loc[data.index[i], 'Invested_Amount'] = invested_amount
        data.loc[data.index[i], 'Remaining'] = remaining
        data.loc[data.index[i], 'Shares'] = shares_owned
        data.loc[data.index[i], 'Position_Value'] = shares_owned * current_price if shares_owned > 0 else 0
        data.loc[data.index[i], 'Final_Cash'] = final_cash
    
    # Final Results
    final_portfolio_value = data['Portfolio_Value'].iloc[-1]
    total_profit = final_portfolio_value - initial_cash
    total_return_percent = (total_profit / initial_cash) * 100
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"Started with: ${initial_cash:,.2f}")
    print(f"Ended with: ${final_portfolio_value:,.2f}")
    print(f"Total Profit: ${total_profit:,.2f}")
    print(f"Total Return: {total_return_percent:.2f}%")
    print(f"Number of Trades: {len(trades)}")
    
    return data, trades

def execute_short_strategy(data, strategy_data):
    """Step 5: Execute Short Entry/Exit Strategy - Using Your Exact Variables"""
    print(f"\nSTEP 5: Executing Short Entry/Exit Strategy...")
    
    # Your exact variables
    initial_cash = 1000  # Money we start with
    invested_amount = initial_cash * 0.8  # 80% available for investment
    remaining = 0  # Unused investment money
    shares_owned = 0  # How many shares we own (negative for short)
    buying_price = 0  # Actual money spent on shares
    final_cash = 0  # Money from selling
    trades = []
    
    print(f"Starting with: ${initial_cash:,.2f}")
    print(f"Available to invest: ${invested_amount:,.2f} (80%)")
    
    for i in range(len(data)):
        current_price = data['Close'].iloc[i]
        entry_signal = data['Entry_Signal'].iloc[i]
        exit_signal = data['Exit_Signal'].iloc[i]
        
        # SHORT ENTRY: Sell shares when signal says SELL (borrow and sell)
        if entry_signal and shares_owned == 0:
            # Calculate how many shares we can short with invested_amount
            max_shares = int(invested_amount / current_price)  # Whole shares only
            buying_price = max_shares * current_price  # Money received from shorting
            shares_owned = -max_shares  # Negative shares (we owe them)
            remaining = invested_amount - buying_price  # Leftover investment money
            final_cash = 0  # Reset for calculation
            
            print(f"SHORT ENTRY: Sold {max_shares} shares at ${current_price:.2f}")
            print(f"  Money received (buying_price): ${buying_price:,.2f}")
            print(f"  Leftover investment money (remaining): ${remaining:,.2f}")
            
            trades.append({
                'type': 'SHORT',
                'price': current_price,
                'shares': max_shares,
                'money_received': buying_price
            })
        
        # SHORT EXIT: Buy shares when signal says BUY (buy back to cover)
        elif exit_signal and shares_owned < 0:
            shares_to_cover = abs(shares_owned)  # How many shares to buy back
            selling_price = shares_to_cover * current_price  # Money spent to cover
            
            # Your Formula: final_cash = remaining + buying_price + (buying_price - selling_price)
            # Note: For shorts, profit is when selling_price < buying_price
            final_cash = remaining + buying_price + (buying_price - selling_price)
            
            profit_loss = buying_price - selling_price  # Profit when positive (sold high, bought low)
            
            print(f"SHORT EXIT: Bought {shares_to_cover} shares at ${current_price:.2f}")
            print(f"  Money spent to cover (selling_price): ${selling_price:,.2f}")
            print(f"  Profit/Loss on shares: ${profit_loss:,.2f}")
            print(f"  Final cash (your formula): ${final_cash:,.2f}")
            
            trades.append({
                'type': 'COVER',
                'price': current_price,
                'shares': shares_to_cover,
                'money_spent': selling_price,
                'profit_loss': profit_loss
            })
            
            # Reset for next trade - final_cash becomes new invested_amount
            invested_amount = final_cash
            remaining = 0
            shares_owned = 0
            buying_price = 0
        
        # Calculate current total portfolio value (only your variables)
        if shares_owned < 0:  # Short position
            current_position_liability = abs(shares_owned) * current_price
            total_portfolio = remaining + buying_price - current_position_liability
        else:
            total_portfolio = final_cash
        
        # Store in DataFrame (only your variables)
        data.loc[data.index[i], 'Portfolio_Value'] = total_portfolio
        data.loc[data.index[i], 'Invested_Amount'] = invested_amount
        data.loc[data.index[i], 'Remaining'] = remaining
        data.loc[data.index[i], 'Shares'] = shares_owned
        data.loc[data.index[i], 'Position_Value'] = abs(shares_owned) * current_price if shares_owned != 0 else 0
        data.loc[data.index[i], 'Final_Cash'] = final_cash
    
    # Final Results
    final_portfolio_value = data['Portfolio_Value'].iloc[-1]
    total_profit = final_portfolio_value - initial_cash
    total_return_percent = (total_profit / initial_cash) * 100
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"Started with: ${initial_cash:,.2f}")
    print(f"Ended with: ${final_portfolio_value:,.2f}")
    print(f"Total Profit: ${total_profit:,.2f}")
    print(f"Total Return: {total_return_percent:.2f}%")
    print(f"Number of Trades: {len(trades)}")
    
    return data, trades

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
    
    # Step 5: Execute Long Entry/Exit Strategy
    data, trades = execute_long_strategy(data, strategy_data)
    
    return strategy_data, data, trades

if __name__ == "__main__":
    execute_strategy()
