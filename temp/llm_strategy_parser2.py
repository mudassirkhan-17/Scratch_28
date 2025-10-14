"""
LLM Strategy Parser - Converts natural language strategy descriptions to JSON config

This module uses an LLM to parse user's natural language strategy descriptions
and generate valid JSON configuration files that can be loaded by the backtesting system.
"""

import json
import os
from typing import Dict, Any, Optional


class StrategyParser:
    """
    Converts natural language strategy descriptions into JSON configs
    """
    
    def __init__(self, api_key=None):
        """
        Initialize the strategy parser
        
        Args:
            api_key: OpenAI API key (or None to read from OPENAI_API_KEY env variable)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OpenAI API key required. Provide it as argument or set OPENAI_API_KEY environment variable.")
    
    def parse_strategy(self, natural_language: str) -> Dict[str, Any]:
        """
        Parse natural language strategy description into JSON config
        
        Args:
            natural_language: User's strategy description in plain English
            
        Returns:
            Dictionary representing the strategy configuration
            
        Example:
            >>> parser = StrategyParser()
            >>> config = parser.parse_strategy(
            ...     "Backtest AAPL with 20-day SMA crossing above 50-day SMA for long entry, "
            ...     "exit when it crosses below. Use $10,000 capital with 20% per trade and 5% stop loss."
            ... )
        """
        # Get the system prompt that explains our JSON schema
        system_prompt = self._get_system_prompt()
        
        # Call OpenAI to parse the strategy
        llm_response = self._call_openai(system_prompt, natural_language)
        
        # Extract and validate JSON from response
        config = self._extract_json(llm_response)
        
        # Validate the config structure
        self._validate_config(config)
        
        return config
    
    def save_config(self, config: Dict[str, Any], filename: str = "config.json"):
        """Save the parsed config to a JSON file"""
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Strategy config saved to {filename}")
    
    def _get_system_prompt(self) -> str:
        """
        Returns the system prompt that teaches the LLM about our JSON schema
        """
        return """You are a trading strategy configuration expert. Your job is to convert natural language strategy descriptions into valid JSON configuration files for a backtesting system.

## JSON Schema for Different Strategy Modes:

### MODE 1: Single Strategy (Basic)
```json
{
  "mode": "single",
  "strategy_direction": "long" | "short" | "reversal",
  "basic": {
    "ticker": "AAPL",
    "period": "1y" | "2y" | "5y" | "10y",
    "interval": "1d" | "1h" | "1m",
    "total_capital": 10000
  },
  "per_trade": {
    "allocation_percent": 20.0,
    "amount_per_trade": 2000.0
  },
  "entry": {
    "comp1": {
      "type": "INDICATOR" | "PRICE" | "CONSTANT",
      "name": "SMA" | "EMA" | "RSI" | "Close" | "Open",
      "params": [20],
      "candles_ago": 0
    },
    "strategy": "CROSSED UP" | "CROSSED DOWN" | "GREATER THAN" | "LESS THAN" | "INCREASED" | "DECREASED",
    "comp2": {
      "type": "INDICATOR" | "PRICE" | "CONSTANT",
      "name": "SMA" | "Close",
      "params": [50],
      "candles_ago": 0
    }
  },
  "exit": {
    "comp1": {...},
    "strategy": "CROSSED DOWN",
    "comp2": {...}
  },
  "sl_tp": {
    "enabled": true,
    "stop_loss_percent": 5.0,
    "take_profit_percent": 10.0,
    "trailing_sl_enabled": false,
    "trailing_sl_type": null,
    "trailing_sl_percent": 0.0
  }
}
```

### MODE 2: Multi-Condition Strategy
Similar to Mode 1 but with multiple conditions combined with AND/OR logic.

### MODE 3: Multi-Ticker (Same Strategy)
```json
{
  "mode": "multi_ticker",
  "strategy_direction": "long",
  "basic": {
    "tickers": ["AAPL", "MSFT", "GOOGL"],
    "period": "1y",
    "interval": "1d",
    "total_capital": 10000
  },
  "allocations": {
    "AAPL": 0.4,
    "MSFT": 0.3,
    "GOOGL": 0.3
  },
  "trade_sizes": {
    "AAPL": {"percentage": 0.2, "amount_per_trade": 800, "max_trades": 5},
    "MSFT": {"percentage": 0.2, "amount_per_trade": 600, "max_trades": 5},
    "GOOGL": {"percentage": 0.2, "amount_per_trade": 600, "max_trades": 5}
  },
  "shared_strategy": {
    "entry": {...},
    "exit": {...}
  },
  "sl_tp": {...}
}
```

## Available Indicators:
SMA, EMA, RSI, MACD, VWAP, MOMENTUM, ADX, ATR, BOLLINGER_BANDS, and 60+ more.

## Strategy Types:
- CROSSED UP / CROSSED DOWN (for crossover strategies)
- GREATER THAN / LESS THAN (for threshold comparisons)
- INCREASED / DECREASED (for momentum)
- EQUAL, WITHIN RANGE, etc.

## Important Rules:
1. ALWAYS include these top-level keys: "mode", "strategy_direction", "basic", "per_trade", "entry", "exit", "sl_tp"
2. "type" must be UPPERCASE: "INDICATOR", "PRICE", or "CONSTANT"
3. For indicator params, use arrays: [20] not just 20
4. For constant values, params should be a single number: 100 or 50.5
5. "per_trade" is a SEPARATE top-level key with "allocation_percent" and "amount_per_trade"
6. Calculate "amount_per_trade" = total_capital * (allocation_percent / 100)
7. Percentages in sl_tp: use 5.0 for 5%
8. Default period: "1y", interval: "1d"
9. If user doesn't specify SL/TP, set enabled: false
10. For price comparisons, params is array with one element: ["Close"] or ["Open"]

## Example Calculation:
If total_capital=10000 and user says "20% per trade":
- allocation_percent: 20.0
- amount_per_trade: 2000.0 (calculated as 10000 * 0.20)

## Your Task:
Parse the user's natural language description and output ONLY valid JSON. No explanations, no markdown code blocks, just raw JSON."""

    def _call_openai(self, system_prompt: str, user_input: str) -> str:
        """Call OpenAI API"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Using gpt-4o-mini for cost efficiency
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.1  # Low temperature for consistent JSON output
            )
            
            return response.choices[0].message.content
        except ImportError:
            raise ImportError("OpenAI library not installed. Run: pip install openai")
        except Exception as e:
            raise Exception(f"OpenAI API error: {e}")
    
    def _extract_json(self, llm_response: str) -> Dict[str, Any]:
        """
        Extract JSON from LLM response (handles markdown code blocks)
        """
        # Remove markdown code blocks if present
        response = llm_response.strip()
        
        if response.startswith("```json"):
            response = response[7:]  # Remove ```json
        elif response.startswith("```"):
            response = response[3:]  # Remove ```
        
        if response.endswith("```"):
            response = response[:-3]  # Remove trailing ```
        
        response = response.strip()
        
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM did not return valid JSON. Error: {e}\n\nResponse:\n{response}")
    
    def _validate_config(self, config: Dict[str, Any]):
        """
        Validate that the config has required fields
        """
        required_fields = ["mode", "strategy_direction"]
        
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field: {field}")
        
        # Mode-specific validation
        mode = config["mode"]
        
        if mode == "single":
            if "basic" not in config or "ticker" not in config["basic"]:
                raise ValueError("Single mode requires 'basic.ticker'")
        
        elif mode == "multi_ticker" or mode == "multi_ticker_multi":
            if "basic" not in config or "tickers" not in config["basic"]:
                raise ValueError("Multi-ticker mode requires 'basic.tickers'")
        
        print("✅ Config validation passed")


def interactive_parse():
    """
    Interactive command-line interface for parsing strategies
    """
    print("\n" + "="*70)
    print("🤖 LLM STRATEGY PARSER (OpenAI GPT-4o-mini)")
    print("="*70)
    print("Convert your trading strategy from plain English to JSON config!")
    print()
    
    # Get API key
    api_key = input("Enter your OpenAI API key (or press Enter to use OPENAI_API_KEY env var): ").strip()
    if not api_key:
        api_key = None  # Will use environment variable
    
    # Initialize parser
    try:
        parser = StrategyParser(api_key=api_key)
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    print(f"\n✅ OpenAI API key configured")
    print("\n" + "="*70)
    print("Describe your trading strategy in plain English:")
    print("Example: 'Backtest AAPL with 20-day SMA crossing above 50-day SMA'")
    print("="*70)
    print()
    
    # Get user input
    strategy_description = input("Your strategy: ").strip()
    
    if not strategy_description:
        print("❌ No strategy provided")
        return
    
    print("\n🤔 Parsing strategy with LLM...")
    
    try:
        # Parse the strategy
        config = parser.parse_strategy(strategy_description)
        
        # Show the generated config
        print("\n" + "="*70)
        print("📋 GENERATED CONFIG:")
        print("="*70)
        print(json.dumps(config, indent=2))
        
        # Ask to save
        save = input("\n💾 Save this config? (y/n) [default: y]: ").strip().lower()
        
        if save != 'n':
            filename = input("Filename [default: config.json]: ").strip() or "config.json"
            parser.save_config(config, filename)
            print(f"\n✅ You can now run: python strategy2.py")
            print(f"   and load this config by typing 'y' when prompted!")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    interactive_parse()

