#!/usr/bin/env python3
"""
Quick test with debug prints to verify all paths work
"""

def test_indicator_vs_constant_debug():
    """Test Indicator vs Constant with debug output"""
    print("🐛 DEBUG TEST: Indicator vs Constant")
    print("=" * 80)
    
    from inputs import get_multi_ticker_multi_strategy_inputs, download_multi_ticker_data
    from strategy import calculate_multi_ticker_multi_strategy_indicators, generate_multi_ticker_multi_strategy_signals
    from comparision_types import ComparisonType
    
    # Simulate strategy data for testing
    strategy_data = {
        'type': 'multi_ticker_multi_strategy',
        'tickers': ['AAPL'],
        'total_capital': 10000,
        'allocations': {'AAPL': 1.0},
        'trade_sizes': {'AAPL': {'percentage': 0.2, 'amount_per_trade': 2000}},
        'period': '1y',
        'interval': '1d',
        'ticker_strategies': {
            'AAPL': {
                'type': 'single',
                'entry_comp1_type': ComparisonType.INDICATOR,
                'entry_comp1_name': 'SMA',
                'entry_comp1_params': (20,),
                'entry_comp1_candles_ago': 0,
                'entry_comp2_type': ComparisonType.CONSTANT,
                'entry_comp2_name': 'CONSTANT',
                'entry_comp2_params': (200,),
                'entry_comp2_candles_ago': 0,
                'exit_comp1_type': ComparisonType.INDICATOR,
                'exit_comp1_name': 'SMA',
                'exit_comp1_params': (20,),
                'exit_comp1_candles_ago': 0,
                'exit_comp2_type': ComparisonType.CONSTANT,
                'exit_comp2_name': 'CONSTANT',
                'exit_comp2_params': (180,),
                'exit_comp2_candles_ago': 0,
                'entry_strategy': 'GREATER THAN',
                'exit_strategy': 'LESS THAN'
            }
        },
        'sl_tp_config': {'enabled': False}
    }
    
    print("\n1️⃣ Downloading data...")
    data = download_multi_ticker_data(['AAPL'], '1y', '1d')
    print(f"   Data shape: {data.shape}")
    print(f"   Columns: {list(data.columns)}")
    
    print("\n2️⃣ Finding actual tickers...")
    actual_tickers = []
    ticker_mapping = {}
    for ticker in ['AAPL']:
        ticker_columns = [col for col in data.columns if col.startswith(f'{ticker}_') and col.endswith('_Close')]
        for col in ticker_columns:
            actual_ticker = col.replace('_Close', '')
            if actual_ticker not in actual_tickers:
                actual_tickers.append(actual_ticker)
                ticker_mapping[actual_ticker] = ticker
    
    print(f"   Original: ['AAPL']")
    print(f"   Actual: {actual_tickers}")
    print(f"   Mapping: {ticker_mapping}")
    
    print("\n3️⃣ Updating strategy_data...")
    original_strategies = strategy_data['ticker_strategies'].copy()
    new_strategies = {}
    for actual_ticker, original_ticker in ticker_mapping.items():
        new_strategies[actual_ticker] = original_strategies[original_ticker]
        print(f"   {actual_ticker} -> {original_ticker} strategy")
    
    strategy_data['tickers'] = actual_tickers
    strategy_data['ticker_strategies'] = new_strategies
    
    print("\n4️⃣ Calculating indicators...")
    try:
        data = calculate_multi_ticker_multi_strategy_indicators(data, strategy_data, actual_tickers)
        print(f"   ✅ Success! New columns: {[c for c in data.columns if 'SMA' in c or 'CONSTANT' in c]}")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n5️⃣ Generating signals...")
    try:
        data = generate_multi_ticker_multi_strategy_signals(data, strategy_data, actual_tickers)
        signal_cols = [c for c in data.columns if 'Signal' in c]
        print(f"   ✅ Success! Signal columns: {signal_cols}")
        
        # Check signal counts
        for col in signal_cols:
            true_count = data[col].sum()
            print(f"   {col}: {true_count} True signals")
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n6️⃣ Checking specific rows...")
    print("   Sample data (first 5 rows with signals):")
    display_cols = [actual_tickers[0] + '_Close', 
                    actual_tickers[0] + '_SMA_entry1',
                    actual_tickers[0] + '_Entry_Signal',
                    actual_tickers[0] + '_Exit_Signal']
    
    # Find rows with signals
    signal_rows = data[data[actual_tickers[0] + '_Entry_Signal'] == True].head(5)
    if len(signal_rows) > 0:
        print(signal_rows[display_cols].to_string())
    else:
        print("   No entry signals found - check logic!")
        print("   Sample of SMA values:")
        print(data[[actual_tickers[0] + '_Close', actual_tickers[0] + '_SMA_entry1']].head(30).to_string())
    
    print("\n" + "=" * 80)
    print("✅ DEBUG TEST COMPLETE!")
    print("=" * 80)
    return True

def test_price_vs_constant_debug():
    """Test Price vs Constant with debug output"""
    print("\n\n🐛 DEBUG TEST: Price vs Constant")
    print("=" * 80)
    
    from inputs import download_multi_ticker_data
    from strategy import calculate_multi_ticker_multi_strategy_indicators, generate_multi_ticker_multi_strategy_signals
    from comparision_types import ComparisonType
    
    strategy_data = {
        'type': 'multi_ticker_multi_strategy',
        'tickers': ['AAPL'],
        'total_capital': 10000,
        'allocations': {'AAPL': 1.0},
        'trade_sizes': {'AAPL': {'percentage': 0.2, 'amount_per_trade': 2000}},
        'period': '1y',
        'interval': '1d',
        'ticker_strategies': {
            'AAPL': {
                'type': 'single',
                'entry_comp1_type': ComparisonType.PRICE,
                'entry_comp1_name': 'PRICE',
                'entry_comp1_params': ('Close',),
                'entry_comp1_candles_ago': 0,
                'entry_comp2_type': ComparisonType.CONSTANT,
                'entry_comp2_name': 'CONSTANT',
                'entry_comp2_params': (200,),
                'entry_comp2_candles_ago': 0,
                'exit_comp1_type': ComparisonType.PRICE,
                'exit_comp1_name': 'PRICE',
                'exit_comp1_params': ('Close',),
                'exit_comp1_candles_ago': 0,
                'exit_comp2_type': ComparisonType.CONSTANT,
                'exit_comp2_name': 'CONSTANT',
                'exit_comp2_params': (180,),
                'exit_comp2_candles_ago': 0,
                'entry_strategy': 'GREATER THAN',
                'exit_strategy': 'LESS THAN'
            }
        },
        'sl_tp_config': {'enabled': False}
    }
    
    print("\n1️⃣ Downloading data...")
    data = download_multi_ticker_data(['AAPL'], '1y', '1d')
    
    print("\n2️⃣ Finding actual tickers...")
    actual_tickers = []
    ticker_mapping = {}
    for ticker in ['AAPL']:
        ticker_columns = [col for col in data.columns if col.startswith(f'{ticker}_') and col.endswith('_Close')]
        for col in ticker_columns:
            actual_ticker = col.replace('_Close', '')
            if actual_ticker not in actual_tickers:
                actual_tickers.append(actual_ticker)
                ticker_mapping[actual_ticker] = ticker
    
    print(f"   Actual: {actual_tickers}")
    
    print("\n3️⃣ Updating strategy_data...")
    original_strategies = strategy_data['ticker_strategies'].copy()
    new_strategies = {}
    for actual_ticker, original_ticker in ticker_mapping.items():
        new_strategies[actual_ticker] = original_strategies[original_ticker]
    
    strategy_data['tickers'] = actual_tickers
    strategy_data['ticker_strategies'] = new_strategies
    
    print("\n4️⃣ Calculating indicators (should skip for Price vs Constant)...")
    try:
        data = calculate_multi_ticker_multi_strategy_indicators(data, strategy_data, actual_tickers)
        print(f"   ✅ Success!")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n5️⃣ Generating signals...")
    try:
        data = generate_multi_ticker_multi_strategy_signals(data, strategy_data, actual_tickers)
        signal_cols = [c for c in data.columns if 'Signal' in c]
        print(f"   ✅ Success! Signal columns: {signal_cols}")
        
        for col in signal_cols:
            true_count = data[col].sum()
            print(f"   {col}: {true_count} True signals")
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n6️⃣ Checking prices vs threshold...")
    close_col = actual_tickers[0] + '_Close'
    above_200 = (data[close_col] > 200).sum()
    below_180 = (data[close_col] < 180).sum()
    print(f"   Days with Close > 200: {above_200}")
    print(f"   Days with Close < 180: {below_180}")
    print(f"   Price range: ${data[close_col].min():.2f} to ${data[close_col].max():.2f}")
    
    print("\n" + "=" * 80)
    print("✅ DEBUG TEST COMPLETE!")
    print("=" * 80)
    return True

if __name__ == "__main__":
    print("🔍 RUNNING DEBUG TESTS")
    print("=" * 80)
    
    test1 = test_indicator_vs_constant_debug()
    test2 = test_price_vs_constant_debug()
    
    print("\n\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"Test 1 (Indicator vs Constant): {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Test 2 (Price vs Constant): {'✅ PASS' if test2 else '❌ FAIL'}")
    print("=" * 80)
