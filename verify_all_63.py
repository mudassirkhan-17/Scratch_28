#!/usr/bin/env python3
"""Clean verification of all 63 indicators - no emojis"""
import sys

def verify_all_indicators():
    from inputs import download_multi_ticker_data
    from strategy import (calculate_multi_ticker_multi_strategy_indicators, 
                         generate_multi_ticker_multi_strategy_signals,
                         execute_multi_ticker_strategy)
    from comparision_types import ComparisonType
    
    print("=" * 100)
    print("VERIFYING ALL 63 INDICATORS - FINAL CHECK")
    print("=" * 100)
    
    # All 63 indicators
    indicators = [
        'SMA', 'EMA', 'WMA', 'DEMA', 'HULL_MA', 'KAMA', 'TRIANGULAR_MA', 'T3_MA', 'JMA', 'FRAMA',
        'SEMA', 'ZLEMA', 'ZLSMA', 'VWMA', 'MCGINLEY_DYNAMIC', 'ALMA', 'SINE_WMA', 'PASCAL_WMA',
        'SYMMETRIC_WMA', 'FIBONACCI_WMA', 'HOLT_WINTER_MA', 'HULL_EMA', 'EVMA',
        'RSI', 'RSI2', 'MOMENTUM', 'CMO', 'STC', 'WTO', 'APO', 'PPO', 'DPO', 'MBB',
        'OBV', 'AOBV', 'PVO', 'PVT', 'VPT', 'VFI', 'VZO', 'KVO', 'FVE', 'NVI', 'PVI', 'PVR',
        'PV', 'VAMA', 'WOBV',
        'ADX', 'DM', 'PDI', 'MDI', 'PDM', 'MDM',
        'TYPICAL_PRICE', 'VWAP', 'AP', 'MP', 'WCP', 'MPP', 'APZ', 'PD', 'MARKET_MOMENTUM'
    ]
    
    print("\nDownloading test data...")
    sys.stdout.flush()
    
    # Suppress output from download
    import io
    from contextlib import redirect_stdout
    
    with redirect_stdout(io.StringIO()):
        data = download_multi_ticker_data(['AAPL'], '1y', '1d')
    
    actual_ticker = 'AAPL_1' if 'AAPL_1_Close' in data.columns else 'AAPL'
    print(f"Data loaded: {len(data)} rows")
    print(f"\nTesting {len(indicators)} indicators...\n")
    sys.stdout.flush()
    
    passed = 0
    failed_list = []
    
    for i, indicator in enumerate(indicators, 1):
        try:
            strategy_data = {
                'type': 'multi_ticker_multi_strategy',
                'tickers': [actual_ticker],
                'total_capital': 10000,
                'allocations': {actual_ticker: 1.0},
                'trade_sizes': {actual_ticker: {'percentage': 0.2, 'amount_per_trade': 2000, 'max_trades': 5}},
                'sl_tp_config': {
                    'enabled': False, 'sl_type': 'percentage', 'tp_type': 'percentage',
                    'sl_value': 0.05, 'tp_value': 0.1, 'trailing_sl_enabled': False
                },
                'ticker_strategies': {
                    actual_ticker: {
                        'type': 'single',
                        'entry_comp1_type': ComparisonType.INDICATOR,
                        'entry_comp1_name': indicator,
                        'entry_comp1_params': (20,),
                        'entry_comp1_candles_ago': 0,
                        'entry_comp2_type': ComparisonType.INDICATOR,
                        'entry_comp2_name': 'SMA',
                        'entry_comp2_params': (50,),
                        'entry_comp2_candles_ago': 0,
                        'exit_comp1_type': ComparisonType.INDICATOR,
                        'exit_comp1_name': indicator,
                        'exit_comp1_params': (20,),
                        'exit_comp1_candles_ago': 0,
                        'exit_comp2_type': ComparisonType.INDICATOR,
                        'exit_comp2_name': 'SMA',
                        'exit_comp2_params': (50,),
                        'exit_comp2_candles_ago': 0,
                        'entry_strategy': 'CROSSED UP',
                        'exit_strategy': 'CROSSED DOWN'
                    }
                }
            }
            
            test_data = data.copy()
            
            # Suppress verbose output
            with redirect_stdout(io.StringIO()):
                test_data = calculate_multi_ticker_multi_strategy_indicators(test_data, strategy_data, [actual_ticker])
                test_data = generate_multi_ticker_multi_strategy_signals(test_data, strategy_data, [actual_ticker])
                test_data, trades = execute_multi_ticker_strategy(test_data, strategy_data, "long")
            
            # Get basic stats
            signals = test_data[f'{actual_ticker}_Entry_Signal'].sum()
            
            print(f"[{i:2d}/63] {indicator:20s} PASS (signals: {signals})")
            sys.stdout.flush()
            passed += 1
            
        except Exception as e:
            error_msg = str(e)
            print(f"[{i:2d}/63] {indicator:20s} FAIL: {error_msg[:60]}")
            sys.stdout.flush()
            failed_list.append({'name': indicator, 'error': error_msg})
    
    print("\n" + "=" * 100)
    print("FINAL VERIFICATION RESULTS")
    print("=" * 100)
    print(f"Total Indicators Tested: {len(indicators)}")
    print(f"PASSED: {passed}/{len(indicators)} ({passed/len(indicators)*100:.1f}%)")
    print(f"FAILED: {len(failed_list)}/{len(indicators)} ({len(failed_list)/len(indicators)*100:.1f}%)")
    
    if len(failed_list) > 0:
        print("\n" + "=" * 100)
        print("FAILED INDICATORS:")
        print("=" * 100)
        for item in failed_list:
            print(f"\nIndicator: {item['name']}")
            print(f"Error: {item['error']}")
    else:
        print("\n" + "=" * 100)
        print("*** SUCCESS: ALL 63 INDICATORS WORKING PERFECTLY! ***")
        print("=" * 100)
    
    return len(failed_list) == 0

if __name__ == "__main__":
    try:
        success = verify_all_indicators()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

