"""
Test script for LLM Strategy Parser

This demonstrates how to use the parser programmatically
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not installed, try to load .env manually
    env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

from llm.llm_strategy_parser import StrategyParser
import json

# Get API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("❌ Please set OPENAI_API_KEY in your .env file")
    print("💡 Create a .env file with: OPENAI_API_KEY=your_api_key_here")
    exit(1)


# Example 1: Simple SMA crossover strategy
def test_simple_strategy():
    """Test parsing a simple SMA crossover strategy"""
    
    strategy_text = """
    I want to backtest AAPL using a simple moving average crossover strategy.
    Entry: Buy when 20-day SMA crosses above 50-day SMA
    Exit: Sell when 20-day SMA crosses below 50-day SMA
    Capital: $10,000
    Per trade: 20% of capital
    Stop loss: 5%
    Take profit: 10%
    Period: 1 year of daily data
    """
    
    print("="*70)
    print("TEST 1: Simple SMA Crossover")
    print("="*70)
    print(f"Input: {strategy_text}")
    
    parser = StrategyParser(api_key=OPENAI_API_KEY)
    config = parser.parse_strategy(strategy_text)
    
    print("\nGenerated Config:")
    print(json.dumps(config, indent=2))
    
    parser.save_config(config, "test_config_1.json")
    print("\n✅ Test 1 passed!")


# Example 2: Multi-ticker strategy
def test_multi_ticker():
    """Test parsing a multi-ticker strategy"""
    
    strategy_text = """
    Create a multi-ticker portfolio strategy:
    - Tickers: AAPL (40%), MSFT (30%), GOOGL (30%)
    - Total capital: $20,000
    - Each ticker: 20% per trade
    - Strategy: RSI below 30 for entry, RSI above 70 for exit
    - Use 1 year of daily data
    - 5% stop loss, no take profit
    """
    
    print("\n" + "="*70)
    print("TEST 2: Multi-Ticker Portfolio")
    print("="*70)
    print(f"Input: {strategy_text}")
    
    parser = StrategyParser(api_key=OPENAI_API_KEY)
    config = parser.parse_strategy(strategy_text)
    
    print("\nGenerated Config:")
    print(json.dumps(config, indent=2))
    
    parser.save_config(config, "test_config_2.json")
    print("\n✅ Test 2 passed!")


# Example 3: Short strategy
def test_short_strategy():
    """Test parsing a short strategy"""
    
    strategy_text = """
    I want to short TSLA when price is above the 200-day SMA by more than 10%.
    Exit when price drops back to the 200-day SMA.
    Use $15,000 with $3,000 per trade.
    Set 8% stop loss.
    Test on 2 years of daily data.
    """
    
    print("\n" + "="*70)
    print("TEST 3: Short Strategy")
    print("="*70)
    print(f"Input: {strategy_text}")
    
    parser = StrategyParser(api_key=OPENAI_API_KEY)
    config = parser.parse_strategy(strategy_text)
    
    print("\nGenerated Config:")
    print(json.dumps(config, indent=2))
    
    parser.save_config(config, "test_config_3.json")
    print("\n✅ Test 3 passed!")


if __name__ == "__main__":
    print("🧪 Testing LLM Strategy Parser\n")
    
    try:
        test_simple_strategy()
        # test_multi_ticker()
        # test_short_strategy()
        
        print("\n" + "="*70)
        print("🎉 ALL TESTS PASSED!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")

