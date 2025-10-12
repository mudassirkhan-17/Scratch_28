"""
Test script to verify JSON config save for all 4 modes
Creates sample configs without user interaction
"""

import json
import os
from comparision_types import ComparisonType
from inputs import (
    save_strategy_to_json, 
    save_multi_condition_to_json,
    save_multi_ticker_to_json,
    save_multi_ticker_multi_to_json
)

def test_mode_1_single_strategy():
    """Test Mode 1: Single Strategy JSON save"""
    print("\n" + "="*60)
    print("🧪 TESTING MODE 1: SINGLE STRATEGY")
    print("="*60)
    
    # Create a sample single strategy tuple (23 elements)
    strategy_data = (
        "AAPL",                          # 0: ticker
        "1y",                            # 1: period
        "1d",                            # 2: interval
        10000,                           # 3: total_capital
        {'amount_per_trade': 2000, 'percentage': 20},  # 4: per_trade_config
        
        ComparisonType.INDICATOR,        # 5: entry_comp1_type
        "SMA",                           # 6: entry_comp1_name
        (20,),                           # 7: entry_comp1_params
        ComparisonType.INDICATOR,        # 8: entry_comp2_type
        "SMA",                           # 9: entry_comp2_name
        (50,),                           # 10: entry_comp2_params
        
        ComparisonType.INDICATOR,        # 11: exit_comp1_type
        "SMA",                           # 12: exit_comp1_name
        (20,),                           # 13: exit_comp1_params
        ComparisonType.INDICATOR,        # 14: exit_comp2_type
        "SMA",                           # 15: exit_comp2_name
        (50,),                           # 16: exit_comp2_params
        
        "CROSSED UP",                    # 17: entry_strategy
        "CROSSED DOWN",                  # 18: exit_strategy
        0,                               # 19: entry_comp1_candles_ago
        0,                               # 20: entry_comp2_candles_ago
        0,                               # 21: exit_comp1_candles_ago
        0                                # 22: exit_comp2_candles_ago
    )
    
    sl_tp_config = {
        'enabled': True,
        'sl_type': 'percentage',
        'sl_value': 0.05,
        'tp_type': 'percentage',
        'tp_value': 0.10,
        'trailing_sl_enabled': True,
        'trailing_sl_type': 'percentage',
        'trailing_sl_value': 0.03
    }
    
    filename = "config_test_single.json"
    save_strategy_to_json(strategy_data, filename, "long", sl_tp_config)
    print(f"✅ Created: {filename}")
    return filename


def test_mode_2_multi_condition():
    """Test Mode 2: Multi-Condition JSON save"""
    print("\n" + "="*60)
    print("🧪 TESTING MODE 2: MULTI-CONDITION")
    print("="*60)
    
    # Create sample conditions (stored as dicts)
    entry_conditions = [
        {
            'comp1_type': ComparisonType.INDICATOR,
            'comp1_name': 'SMA',
            'comp1_params': (20,),
            'comp1_candles_ago': 0,
            'comp2_type': ComparisonType.INDICATOR,
            'comp2_name': 'SMA',
            'comp2_params': (50,),
            'comp2_candles_ago': 0,
            'strategy': 'CROSSED UP'
        },
        {
            'comp1_type': ComparisonType.INDICATOR,
            'comp1_name': 'RSI',
            'comp1_params': (14,),
            'comp1_candles_ago': 0,
            'comp2_type': ComparisonType.CONSTANT,
            'comp2_name': 'CONSTANT',
            'comp2_params': (30,),
            'comp2_candles_ago': 0,
            'strategy': 'GREATER THAN'
        }
    ]
    
    exit_conditions = [
        {
            'comp1_type': ComparisonType.INDICATOR,
            'comp1_name': 'SMA',
            'comp1_params': (20,),
            'comp1_candles_ago': 0,
            'comp2_type': ComparisonType.INDICATOR,
            'comp2_name': 'SMA',
            'comp2_params': (50,),
            'comp2_candles_ago': 0,
            'strategy': 'CROSSED DOWN'
        },
        {
            'comp1_type': ComparisonType.INDICATOR,
            'comp1_name': 'RSI',
            'comp1_params': (14,),
            'comp1_candles_ago': 0,
            'comp2_type': ComparisonType.CONSTANT,
            'comp2_name': 'CONSTANT',
            'comp2_params': (70,),
            'comp2_candles_ago': 0,
            'strategy': 'LESS THAN'
        }
    ]
    
    # Create multi-condition tuple (11 elements)
    strategy_data = (
        "AAPL",                                              # 0: ticker
        "1y",                                                # 1: period
        "1d",                                                # 2: interval
        10000,                                               # 3: total_capital
        {'amount_per_trade': 2000, 'percentage': 20},       # 4: per_trade_config
        {'enabled': True, 'sl_value': 0.05, 'tp_value': 0.1},  # 5: sl_tp_config
        2,                                                   # 6: condition_count
        "AND",                                               # 7: entry_logic
        "AND",                                               # 8: exit_logic
        entry_conditions,                                    # 9: entry_conditions
        exit_conditions                                      # 10: exit_conditions
    )
    
    sl_tp_config = {
        'enabled': True,
        'sl_type': 'percentage',
        'sl_value': 0.05,
        'tp_type': 'percentage',
        'tp_value': 0.10,
        'trailing_sl_enabled': False,
        'trailing_sl_type': None,
        'trailing_sl_value': 0
    }
    
    filename = "config_test_multi_condition.json"
    save_multi_condition_to_json(strategy_data, filename, "short", sl_tp_config)
    print(f"✅ Created: {filename}")
    return filename


def test_mode_3_multi_ticker():
    """Test Mode 3: Multi-Ticker JSON save"""
    print("\n" + "="*60)
    print("🧪 TESTING MODE 3: MULTI-TICKER")
    print("="*60)
    
    # Create shared strategy data (23-element tuple)
    shared_strategy = (
        "AAPL",                          # 0: ticker (placeholder)
        "1y",                            # 1: period
        "1d",                            # 2: interval
        10000,                           # 3: total_capital
        {'amount_per_trade': 1000, 'percentage': 10},  # 4: per_trade_config
        
        ComparisonType.INDICATOR,        # 5: entry_comp1_type
        "EMA",                           # 6: entry_comp1_name
        (12,),                           # 7: entry_comp1_params
        ComparisonType.INDICATOR,        # 8: entry_comp2_type
        "EMA",                           # 9: entry_comp2_name
        (26,),                           # 10: entry_comp2_params
        
        ComparisonType.INDICATOR,        # 11: exit_comp1_type
        "EMA",                           # 12: exit_comp1_name
        (12,),                           # 13: exit_comp1_params
        ComparisonType.INDICATOR,        # 14: exit_comp2_type
        "EMA",                           # 15: exit_comp2_name
        (26,),                           # 16: exit_comp2_params
        
        "CROSSED UP",                    # 17: entry_strategy
        "CROSSED DOWN",                  # 18: exit_strategy
        0,                               # 19: entry_comp1_candles_ago
        0,                               # 20: entry_comp2_candles_ago
        0,                               # 21: exit_comp1_candles_ago
        0                                # 22: exit_comp2_candles_ago
    )
    
    # Create multi-ticker dict
    strategy_data = {
        'tickers': ['AAPL', 'MSFT', 'GOOGL'],
        'total_capital': 30000,
        'allocations': {'AAPL': 0.4, 'MSFT': 0.35, 'GOOGL': 0.25},
        'trade_sizes': {
            'AAPL': {'amount_per_trade': 2400, 'percentage': 20},
            'MSFT': {'amount_per_trade': 2100, 'percentage': 20},
            'GOOGL': {'amount_per_trade': 1500, 'percentage': 20}
        },
        'period': '1y',
        'interval': '1d',
        'sl_tp_config': {
            'enabled': True,
            'sl_type': 'percentage',
            'sl_value': 0.05,
            'tp_type': 'percentage',
            'tp_value': 0.10,
            'trailing_sl_enabled': True,
            'trailing_sl_type': 'percentage',
            'trailing_sl_value': 0.02
        },
        'strategy_data': shared_strategy
    }
    
    filename = "config_test_multi_ticker.json"
    save_multi_ticker_to_json(strategy_data, filename, "long")
    print(f"✅ Created: {filename}")
    return filename


def test_mode_4_multi_ticker_multi():
    """Test Mode 4: Multi-Ticker Multi-Strategy JSON save"""
    print("\n" + "="*60)
    print("🧪 TESTING MODE 4: MULTI-TICKER MULTI-STRATEGY")
    print("="*60)
    
    # Create unique strategy for AAPL (single-condition)
    aapl_strategy = {
        'type': 'single',
        'entry_comp1_type': ComparisonType.INDICATOR,
        'entry_comp1_name': 'SMA',
        'entry_comp1_params': (20,),
        'entry_comp1_candles_ago': 0,
        'entry_comp2_type': ComparisonType.INDICATOR,
        'entry_comp2_name': 'SMA',
        'entry_comp2_params': (50,),
        'entry_comp2_candles_ago': 0,
        'exit_comp1_type': ComparisonType.INDICATOR,
        'exit_comp1_name': 'SMA',
        'exit_comp1_params': (20,),
        'exit_comp1_candles_ago': 0,
        'exit_comp2_type': ComparisonType.INDICATOR,
        'exit_comp2_name': 'SMA',
        'exit_comp2_params': (50,),
        'exit_comp2_candles_ago': 0,
        'entry_strategy': 'CROSSED UP',
        'exit_strategy': 'CROSSED DOWN'
    }
    
    # Create unique strategy for MSFT (multi-condition)
    msft_entry_conditions = [
        {
            'comp1_type': ComparisonType.INDICATOR,
            'comp1_name': 'EMA',
            'comp1_params': (12,),
            'comp1_candles_ago': 0,
            'comp2_type': ComparisonType.INDICATOR,
            'comp2_name': 'EMA',
            'comp2_params': (26,),
            'comp2_candles_ago': 0,
            'strategy': 'CROSSED UP'
        },
        {
            'comp1_type': ComparisonType.INDICATOR,
            'comp1_name': 'RSI',
            'comp1_params': (14,),
            'comp1_candles_ago': 0,
            'comp2_type': ComparisonType.CONSTANT,
            'comp2_name': 'CONSTANT',
            'comp2_params': (50,),
            'comp2_candles_ago': 0,
            'strategy': 'GREATER THAN'
        }
    ]
    
    msft_exit_conditions = [
        {
            'comp1_type': ComparisonType.INDICATOR,
            'comp1_name': 'EMA',
            'comp1_params': (12,),
            'comp1_candles_ago': 0,
            'comp2_type': ComparisonType.INDICATOR,
            'comp2_name': 'EMA',
            'comp2_params': (26,),
            'comp2_candles_ago': 0,
            'strategy': 'CROSSED DOWN'
        },
        {
            'comp1_type': ComparisonType.INDICATOR,
            'comp1_name': 'RSI',
            'comp1_params': (14,),
            'comp1_candles_ago': 0,
            'comp2_type': ComparisonType.CONSTANT,
            'comp2_name': 'CONSTANT',
            'comp2_params': (50,),
            'comp2_candles_ago': 0,
            'strategy': 'LESS THAN'
        }
    ]
    
    msft_strategy = {
        'type': 'multi',
        'entry_conditions': msft_entry_conditions,
        'exit_conditions': msft_exit_conditions,
        'entry_logic': 'AND',
        'exit_logic': 'AND'
    }
    
    # Create multi-ticker multi-strategy dict
    strategy_data = {
        'tickers': ['AAPL', 'MSFT'],
        'total_capital': 30000,
        'allocations': {'AAPL': 0.6, 'MSFT': 0.4},
        'trade_sizes': {
            'AAPL': {'amount_per_trade': 3600, 'percentage': 20},
            'MSFT': {'amount_per_trade': 2400, 'percentage': 20}
        },
        'period': '1y',
        'interval': '1d',
        'sl_tp_config': {
            'enabled': True,
            'sl_type': 'percentage',
            'sl_value': 0.05,
            'tp_type': 'percentage',
            'tp_value': 0.10,
            'trailing_sl_enabled': False,
            'trailing_sl_type': None,
            'trailing_sl_value': 0
        },
        'ticker_strategies': {
            'AAPL': aapl_strategy,
            'MSFT': msft_strategy
        }
    }
    
    filename = "config_test_multi_ticker_multi.json"
    save_multi_ticker_multi_to_json(strategy_data, filename, "reversal")
    print(f"✅ Created: {filename}")
    return filename


def verify_json_file(filename):
    """Verify JSON file is valid and display summary"""
    print(f"\n🔍 Verifying {filename}...")
    
    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        return False
    
    try:
        with open(filename, 'r') as f:
            config = json.load(f)
        
        print(f"✅ Valid JSON")
        print(f"   Mode: {config.get('mode', 'N/A')}")
        print(f"   Direction: {config.get('strategy_direction', 'N/A')}")
        
        if 'basic' in config:
            if 'ticker' in config['basic']:
                print(f"   Ticker: {config['basic']['ticker']}")
            elif 'tickers' in config['basic']:
                print(f"   Tickers: {', '.join(config['basic']['tickers'])}")
        
        print(f"   SL/TP: {'Enabled' if config.get('sl_tp', {}).get('enabled') else 'Disabled'}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🚀 TESTING JSON CONFIG SAVE FOR ALL 4 MODES")
    print("="*70)
    
    results = []
    
    # Test each mode
    try:
        file1 = test_mode_1_single_strategy()
        results.append(('Mode 1: Single', file1, verify_json_file(file1)))
    except Exception as e:
        print(f"❌ Mode 1 failed: {e}")
        results.append(('Mode 1: Single', None, False))
    
    try:
        file2 = test_mode_2_multi_condition()
        results.append(('Mode 2: Multi-Condition', file2, verify_json_file(file2)))
    except Exception as e:
        print(f"❌ Mode 2 failed: {e}")
        results.append(('Mode 2: Multi-Condition', None, False))
    
    try:
        file3 = test_mode_3_multi_ticker()
        results.append(('Mode 3: Multi-Ticker', file3, verify_json_file(file3)))
    except Exception as e:
        print(f"❌ Mode 3 failed: {e}")
        results.append(('Mode 3: Multi-Ticker', None, False))
    
    try:
        file4 = test_mode_4_multi_ticker_multi()
        results.append(('Mode 4: Multi-Ticker Multi', file4, verify_json_file(file4)))
    except Exception as e:
        print(f"❌ Mode 4 failed: {e}")
        results.append(('Mode 4: Multi-Ticker Multi', None, False))
    
    # Summary
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    
    for mode_name, filename, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {mode_name}")
        if filename:
            print(f"         File: {filename}")
    
    print("\n" + "="*70)
    passed = sum(1 for _, _, success in results if success)
    total = len(results)
    print(f"RESULT: {passed}/{total} modes passed")
    print("="*70)


if __name__ == "__main__":
    main()

