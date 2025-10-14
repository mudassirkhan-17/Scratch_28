"""
JSON Configuration Loader for Trading Strategy System
Converts JSON config files to strategy_data tuples
"""

import json
from comparision_types import ComparisonType


def load_json_config(filepath="config.json"):
    """
    Load JSON config and convert to strategy_data tuple
    
    Args:
        filepath: Path to JSON config file
        
    Returns:
        dict with keys:
            - strategy_data: tuple in format expected by execute_strategy()
            - strategy_direction: "long", "short", or "reversal"
            - strategy_complexity: "single", "multi_condition", "multi_ticker", etc.
            - sl_tp_config: SL/TP configuration dict
            - total_capital: Total capital amount
            - per_trade_config: Per trade configuration dict
    """
    
    print(f"📂 Loading configuration from: {filepath}")
    
    with open(filepath, 'r') as f:
        config = json.load(f)
    
    mode = config.get('mode', 'single')
    
    if mode == 'single':
        return load_single_strategy_config(config)
    elif mode == 'multi_condition':
        return load_multi_condition_config(config)
    elif mode == 'multi_ticker':
        return load_multi_ticker_config(config)
    elif mode == 'multi_ticker_multi':
        return load_multi_ticker_multi_config(config)
    else:
        raise ValueError(f"Unknown mode: {mode}")


def load_single_strategy_config(config):
    """Load single strategy configuration from JSON"""
    
    # Extract basic info
    ticker = config['basic']['ticker']
    period = config['basic']['period']
    interval = config['basic']['interval']
    total_capital = config['basic']['total_capital']
    
    # Per trade config
    per_trade_config = {
        'percentage': config['per_trade']['allocation_percent'],
        'amount_per_trade': config['per_trade']['amount_per_trade']
    }
    
    # Entry comparison 1
    entry_comp1_type = parse_comparison_type(config['entry']['comp1']['type'])
    entry_comp1_name = config['entry']['comp1']['name']
    entry_comp1_params = tuple(config['entry']['comp1']['params'])
    entry_comp1_candles_ago = config['entry']['comp1'].get('candles_ago', 0)
    
    # Entry comparison 2
    entry_comp2_type = parse_comparison_type(config['entry']['comp2']['type'])
    entry_comp2_name = config['entry']['comp2']['name']
    entry_comp2_params = tuple(config['entry']['comp2']['params'])
    entry_comp2_candles_ago = config['entry']['comp2'].get('candles_ago', 0)
    
    # Entry strategy
    entry_strategy = config['entry']['strategy']
    
    # Exit comparison 1
    exit_comp1_type = parse_comparison_type(config['exit']['comp1']['type'])
    exit_comp1_name = config['exit']['comp1']['name']
    exit_comp1_params = tuple(config['exit']['comp1']['params'])
    exit_comp1_candles_ago = config['exit']['comp1'].get('candles_ago', 0)
    
    # Exit comparison 2
    exit_comp2_type = parse_comparison_type(config['exit']['comp2']['type'])
    exit_comp2_name = config['exit']['comp2']['name']
    exit_comp2_params = tuple(config['exit']['comp2']['params'])
    exit_comp2_candles_ago = config['exit']['comp2'].get('candles_ago', 0)
    
    # Exit strategy
    exit_strategy = config['exit']['strategy']
    
    # Build strategy_data tuple (23 elements)
    strategy_data = (
        ticker,                     # 0
        period,                     # 1
        interval,                   # 2
        total_capital,              # 3
        per_trade_config,           # 4
        entry_comp1_type,           # 5
        entry_comp1_name,           # 6
        entry_comp1_params,         # 7
        entry_comp2_type,           # 8
        entry_comp2_name,           # 9
        entry_comp2_params,         # 10
        exit_comp1_type,            # 11
        exit_comp1_name,            # 12
        exit_comp1_params,          # 13
        exit_comp2_type,            # 14
        exit_comp2_name,            # 15
        exit_comp2_params,          # 16
        entry_strategy,             # 17
        exit_strategy,              # 18
        entry_comp1_candles_ago,    # 19
        entry_comp2_candles_ago,    # 20
        exit_comp1_candles_ago,     # 21
        exit_comp2_candles_ago      # 22
    )
    
    # SL/TP config - convert from JSON format to internal format
    sl_tp_config = {
        'enabled': config.get('sl_tp', {}).get('enabled', False),
        'sl_type': 'percentage',  # Always percentage for JSON configs
        'tp_type': 'percentage',
        'sl_value': config.get('sl_tp', {}).get('stop_loss_percent', 0) / 100,  # Convert % to decimal
        'tp_value': config.get('sl_tp', {}).get('take_profit_percent', 0) / 100,
        'trailing_sl_enabled': config.get('sl_tp', {}).get('trailing_sl_enabled', False),
        'trailing_sl_type': config.get('sl_tp', {}).get('trailing_sl_type', None),
        'trailing_sl_value': config.get('sl_tp', {}).get('trailing_sl_percent', 0) / 100
    }
    
    # Strategy direction
    strategy_direction = config.get('strategy_direction', 'long')
    
    return {
        'strategy_data': strategy_data,
        'strategy_direction': strategy_direction,
        'strategy_complexity': 'single',
        'sl_tp_config': sl_tp_config,
        'total_capital': total_capital,
        'per_trade_config': per_trade_config,
        'ticker': ticker,
        'period': period,
        'interval': interval
    }


def load_multi_condition_config(config):
    """Load multi-condition strategy configuration from JSON"""
    # TODO: Implement multi-condition loading
    raise NotImplementedError("Multi-condition JSON loading not yet implemented")


def load_multi_ticker_config(config):
    """Load multi-ticker strategy configuration from JSON"""
    # TODO: Implement multi-ticker loading
    raise NotImplementedError("Multi-ticker JSON loading not yet implemented")


def load_multi_ticker_multi_config(config):
    """Load multi-ticker multi-strategy configuration from JSON"""
    # TODO: Implement multi-ticker multi-strategy loading
    raise NotImplementedError("Multi-ticker multi-strategy JSON loading not yet implemented")


def parse_comparison_type(type_str):
    """
    Convert string to ComparisonType enum
    
    Args:
        type_str: "INDICATOR", "CONSTANT", or "PRICE"
        
    Returns:
        ComparisonType enum value
    """
    if type_str == "INDICATOR":
        return ComparisonType.INDICATOR
    elif type_str == "CONSTANT":
        return ComparisonType.CONSTANT
    elif type_str == "PRICE":
        return ComparisonType.PRICE
    else:
        raise ValueError(f"Unknown comparison type: {type_str}")

