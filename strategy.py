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
    print("📋 Next: Calculate indicators and generate signals")
    
    return strategy_data, data

if __name__ == "__main__":
    execute_strategy()
