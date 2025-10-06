#!/usr/bin/env python3
"""
TEST ALL INDICATORS IN THE SYSTEM
Tests every single indicator with logical parameters and crossover strategies
"""

def run_all_indicators_test():
    """Test all available indicators with proper parameters"""
    
    from inputs import download_multi_ticker_data
    from strategy import (calculate_multi_ticker_multi_strategy_indicators, 
                         generate_multi_ticker_multi_strategy_signals,
                         execute_multi_ticker_strategy)
    from comparision_types import ComparisonType
    
    print("🔬 TESTING ALL INDICATORS IN THE SYSTEM")
    print("=" * 120)
    
    # Define all indicators with logical parameters
    all_indicators = [
        # BASIC MOVING AVERAGES (proven to work)
        ('SMA', (20,), 'Simple Moving Average'),
        ('EMA', (20,), 'Exponential Moving Average'),
        ('WMA', (20,), 'Weighted Moving Average'),
        
        # ADVANCED MOVING AVERAGES
        ('DEMA', (20,), 'Double Exponential MA'),
        ('HULL_MA', (20,), 'Hull Moving Average'),
        ('KAMA', (20, 2, 30), 'Kaufman Adaptive MA'),
        ('TRIANGULAR_MA', (20,), 'Triangular MA'),
        ('ZLEMA', (20,), 'Zero Lag Exponential MA'),
        ('ZLSMA', (20,), 'Zero Lag Simple MA'),
        ('VWMA', (20,), 'Volume Weighted MA'),
        ('MCGINLEY_DYNAMIC', (20,), 'McGinley Dynamic'),
        ('ALMA', (20, 0.85, 6), 'Arnaud Legoux MA'),
        ('T3_MA', (20, 0.7), 'T3 Moving Average'),
        ('JMA', (20, 0), 'Jurik Moving Average'),
        ('FRAMA', (20,), 'Fractal Adaptive MA'),
        ('SEMA', (20,), 'Smoothed Exponential MA'),
        ('SINE_WMA', (20,), 'Sine Weighted MA'),
        ('PASCAL_WMA', (20,), 'Pascals Weighted MA'),
        ('SYMMETRIC_WMA', (20,), 'Symmetric Weighted MA'),
        ('FIBONACCI_WMA', (20,), 'Fibonacci Weighted MA'),
        ('HOLT_WINTER_MA', (20, 0.3, 0.1), 'Holt Winter MA'),
        ('HULL_EMA', (20,), 'Hull Exponential MA'),
        ('EVMA', (20,), 'Elastic Volume MA'),
        
        # MOMENTUM & OSCILLATORS
        ('RSI', (14,), 'Relative Strength Index'),
        ('RSI2', (14,), 'RSI Variant 2'),
        ('MOMENTUM', (10,), 'Momentum Indicator'),
        ('CMO', (14,), 'Chande Momentum Oscillator'),
        ('STC', (23, 50, 10, 3, 3), 'Schaff Trend Cycle'),
        ('WTO', (10, 3), 'Wave Trend Oscillator'),
        ('APO', (12, 26), 'Absolute Price Oscillator'),
        ('PPO', (12, 26, 9), 'Percentage Price Oscillator'),
        ('DPO', (20,), 'Detrended Price Oscillator'),
        ('MBB', (20, 2.0), 'Momentum Breakout Bands'),
        
        # VOLUME INDICATORS
        ('OBV', (), 'On Balance Volume'),
        ('AOBV', (5, 10, 20), 'Archer On Balance Volume'),
        ('PVO', (12, 26, 9), 'Percentage Volume Oscillator'),
        ('PVT', (), 'Price Volume Trend'),
        ('VPT', (), 'Volume Price Trend'),
        ('VFI', (130, 2.5, 3, 0.2), 'Volume Flow Indicator'),
        ('VZO', (14,), 'Volume Zone Oscillator'),
        ('KVO', (34, 55, 13), 'Klinger Volume Oscillator'),
        ('FVE', (22,), 'Finite Volume Element'),
        ('NVI', (), 'Negative Volume Index'),
        ('PVI', (), 'Positive Volume Index'),
        ('PVR', (20,), 'Price Volume Rank'),
        ('PV', (), 'Price Volume'),
        ('VAMA', (20,), 'Volume Adjusted MA'),
        ('WOBV', (20,), 'Weighted On Balance Volume'),
        
        # TREND INDICATORS
        ('ADX', (14,), 'Average Directional Index'),
        ('DM', (14,), 'Directional Movement'),
        ('PDI', (14,), 'Plus Directional Indicator'),
        ('MDI', (14,), 'Minus Directional Indicator'),
        ('PDM', (14,), 'Plus Directional Movement'),
        ('MDM', (14,), 'Minus Directional Movement'),
        
        # PRICE INDICATORS
        ('TYPICAL_PRICE', (), 'Typical Price (H+L+C)/3'),
        ('VWAP', (), 'Volume Weighted Average Price'),
        ('AP', (), 'Average Price'),
        ('MP', (), 'Median Price (H+L)/2'),
        ('WCP', (), 'Weighted Closing Price'),
        ('MPP', (14,), 'Midpoint Price Period'),
        ('APZ', (20, 2.0), 'Adaptive Price Zone'),
        ('PD', (14,), 'Price Distance'),
        
        # MARKET INDICATORS
        ('MARKET_MOMENTUM', (10,), 'Market Momentum'),
    ]
    
    print(f"📊 Total Indicators to Test: {len(all_indicators)}")
    print("=" * 120)
    
    # Download data once
    print("\n📥 Downloading market data (AAPL, 1 year, daily)...")
    data = download_multi_ticker_data(['AAPL'], '1y', '1d')
    actual_ticker = 'AAPL_1' if 'AAPL_1_Close' in data.columns else 'AAPL'
    print(f"   ✅ Data loaded: {data.shape[0]} rows, Ticker: {actual_ticker}")
    
    results = []
    passed = 0
    failed = 0
    
    for i, (indicator_name, params, description) in enumerate(all_indicators, 1):
        print(f"\n{'='*120}")
        print(f"TEST {i}/{len(all_indicators)}: {indicator_name} - {description}")
        print(f"   📊 Parameters: {params if params else 'None'}")
        print(f"   📈 Strategy: {indicator_name}{params} CROSSED UP SMA(50)")
        print(f"   📉 Exit: {indicator_name}{params} CROSSED DOWN SMA(50)")
        print('-' * 120)
        
        try:
            # Create strategy: Test indicator crossed with SMA(50)
            strategy_data = {
                'type': 'multi_ticker_multi_strategy',
                'tickers': [actual_ticker],
                'total_capital': 10000,
                'allocations': {actual_ticker: 1.0},
                'trade_sizes': {actual_ticker: {'percentage': 0.2, 'amount_per_trade': 2000, 'max_trades': 5}},
                'sl_tp_config': {
                    'enabled': True, 'sl_type': 'percentage', 'tp_type': 'percentage',
                    'sl_value': 0.05, 'tp_value': 0.1, 'trailing_sl_enabled': False
                },
                'ticker_strategies': {
                    actual_ticker: {
                        'type': 'single',
                        'entry_comp1_type': ComparisonType.INDICATOR,
                        'entry_comp1_name': indicator_name,
                        'entry_comp1_params': params,
                        'entry_comp1_candles_ago': 0,
                        'entry_comp2_type': ComparisonType.INDICATOR,
                        'entry_comp2_name': 'SMA',
                        'entry_comp2_params': (50,),
                        'entry_comp2_candles_ago': 0,
                        'exit_comp1_type': ComparisonType.INDICATOR,
                        'exit_comp1_name': indicator_name,
                        'exit_comp1_params': params,
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
            
            # Test data copy
            test_data = data.copy()
            
            # Calculate indicators
            print("   🔄 Calculating indicators...")
            test_data = calculate_multi_ticker_multi_strategy_indicators(test_data, strategy_data, [actual_ticker])
            
            # Generate signals
            print("   🔄 Generating signals...")
            test_data = generate_multi_ticker_multi_strategy_signals(test_data, strategy_data, [actual_ticker])
            
            # Execute strategy
            print("   🔄 Executing strategy...")
            test_data, trades = execute_multi_ticker_strategy(test_data, strategy_data, "long")
            
            # Get results
            entry_signals = test_data[f'{actual_ticker}_Entry_Signal'].sum()
            exit_signals = test_data[f'{actual_ticker}_Exit_Signal'].sum()
            final_value = test_data['Portfolio_Value'].iloc[-1]
            profit = final_value - 10000
            return_pct = (profit / 10000) * 100
            
            print(f"\n   ✅ SUCCESS!")
            print(f"   📊 Entry Signals: {entry_signals} | Exit Signals: {exit_signals} | Trades: {len(trades)}")
            print(f"   💰 Final: ${final_value:,.2f} | P&L: ${profit:,.2f} | Return: {return_pct:.2f}%")
            
            passed += 1
            results.append({
                'indicator': indicator_name,
                'description': description,
                'params': params,
                'status': 'PASS ✅',
                'entry_signals': entry_signals,
                'exit_signals': exit_signals,
                'trades': len(trades),
                'final_value': final_value,
                'profit': profit,
                'return_pct': return_pct
            })
            
        except Exception as e:
            error_msg = str(e)
            print(f"\n   ❌ FAILED: {error_msg[:100]}")
            failed += 1
            results.append({
                'indicator': indicator_name,
                'description': description,
                'params': params,
                'status': 'FAIL ❌',
                'error': error_msg
            })
    
    # Print comprehensive summary
    print("\n" + "=" * 120)
    print("🏆 ALL INDICATORS TEST RESULTS")
    print("=" * 120)
    
    print(f"\n📊 OVERALL STATISTICS:")
    print(f"   Total Indicators: {len(results)}")
    print(f"   ✅ Passed: {passed} ({passed/len(results)*100:.1f}%)")
    print(f"   ❌ Failed: {failed} ({failed/len(results)*100:.1f}%)")
    
    if passed > 0:
        successful = [r for r in results if r['status'] == 'PASS ✅']
        
        print(f"\n✅ SUCCESSFUL INDICATORS ({passed}):")
        print("-" * 120)
        print(f"{'#':<4} {'Indicator':<20} {'Description':<35} {'Signals':<12} {'Trades':<7} {'Return':<10}")
        print("-" * 120)
        for idx, r in enumerate(successful, 1):
            signals_str = f"{r['entry_signals']}↑/{r['exit_signals']}↓"
            print(f"{idx:<4} {r['indicator']:<20} {r['description']:<35} {signals_str:<12} {r['trades']:<7} {r['return_pct']:>6.2f}%")
        
        # Profitability analysis
        profitable = [r for r in successful if r['profit'] > 0]
        if profitable:
            print(f"\n💰 PROFITABILITY:")
            print(f"   Profitable: {len(profitable)}/{len(successful)} ({len(profitable)/len(successful)*100:.1f}%)")
            print(f"   Avg Profit: ${sum(r['profit'] for r in profitable)/len(profitable):,.2f}")
            print(f"   Best: {max(profitable, key=lambda x: x['return_pct'])['indicator']} "
                  f"({max(profitable, key=lambda x: x['return_pct'])['return_pct']:.2f}%)")
        
        # Signal generation
        print(f"\n📈 SIGNAL GENERATION:")
        print(f"   Total Entry Signals: {sum(r['entry_signals'] for r in successful):,}")
        print(f"   Total Exit Signals: {sum(r['exit_signals'] for r in successful):,}")
        print(f"   Total Trades: {sum(r['trades'] for r in successful):,}")
        
        # Most active
        most_active = max(successful, key=lambda x: x['entry_signals'])
        print(f"   Most Active: {most_active['indicator']} ({most_active['entry_signals']} entry signals)")
    
    if failed > 0:
        print(f"\n❌ FAILED INDICATORS ({failed}):")
        print("-" * 120)
        failed_tests = [r for r in results if r['status'] == 'FAIL ❌']
        for idx, r in enumerate(failed_tests, 1):
            error_preview = r.get('error', 'Unknown')[:80]
            print(f"{idx:<4} {r['indicator']:<20} {r['description']:<35}")
            print(f"      Error: {error_preview}")
    
    print("\n" + "=" * 120)
    print("🎯 INDICATOR CATEGORIES SUMMARY:")
    print("=" * 120)
    
    categories = {
        'Moving Averages': ['SMA', 'EMA', 'WMA', 'DEMA', 'HULL_MA', 'KAMA', 'TRIANGULAR_MA', 'ZLEMA', 'ZLSMA', 
                           'VWMA', 'MCGINLEY_DYNAMIC', 'ALMA', 'T3_MA', 'JMA', 'FRAMA', 'SEMA', 'SINE_WMA',
                           'PASCAL_WMA', 'SYMMETRIC_WMA', 'FIBONACCI_WMA', 'HOLT_WINTER_MA', 'HULL_EMA', 'EVMA'],
        'Momentum & Oscillators': ['RSI', 'RSI2', 'MOMENTUM', 'CMO', 'STC', 'WTO', 'APO', 'PPO', 'DPO', 'MBB'],
        'Volume Indicators': ['OBV', 'AOBV', 'PVO', 'PVT', 'VPT', 'VFI', 'VZO', 'KVO', 'FVE', 'NVI', 'PVI', 
                             'PVR', 'PV', 'VAMA', 'WOBV'],
        'Trend Indicators': ['ADX', 'DM', 'PDI', 'MDI', 'PDM', 'MDM'],
        'Price Indicators': ['TYPICAL_PRICE', 'VWAP', 'AP', 'MP', 'WCP', 'MPP', 'APZ', 'PD'],
        'Market Indicators': ['MARKET_MOMENTUM']
    }
    
    for category, indicators in categories.items():
        cat_results = [r for r in results if r['indicator'] in indicators]
        cat_passed = sum(1 for r in cat_results if r['status'] == 'PASS ✅')
        cat_total = len(cat_results)
        status = "✅" if cat_passed == cat_total else "⚠️" if cat_passed > 0 else "❌"
        print(f"{status} {category:<25} {cat_passed}/{cat_total} passed ({cat_passed/cat_total*100:.0f}%)")
    
    print("\n" + "=" * 120)
    success_rate = (passed / len(results)) * 100
    if success_rate >= 90:
        print(f"🎉 EXCELLENT! {success_rate:.1f}% of all indicators working perfectly!")
    elif success_rate >= 70:
        print(f"✅ GOOD! {success_rate:.1f}% of indicators functional. Some need parameter fixes.")
    else:
        print(f"⚠️  {success_rate:.1f}% success rate. Multiple indicators need attention.")
    print("=" * 120)
    
    return passed == len(results)

if __name__ == "__main__":
    success = run_all_indicators_test()
    exit(0 if success else 1)

