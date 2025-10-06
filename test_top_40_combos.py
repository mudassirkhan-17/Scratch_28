#!/usr/bin/env python3
"""
Test Top 40 Indicator Combinations
Tests various indicator pairs to ensure all work correctly
"""

def test_indicator_combinations():
    """Test top 40 popular indicator combinations"""
    
    from inputs import download_multi_ticker_data
    from strategy import calculate_multi_ticker_multi_strategy_indicators, generate_multi_ticker_multi_strategy_signals
    from comparision_types import ComparisonType
    
    # Top 40 indicator combinations to test
    test_cases = [
        # Moving Average Combinations
        ("SMA", (20,), "SMA", (50,), "Trend Following: SMA Crossover"),
        ("EMA", (12,), "EMA", (26,), "Trend Following: EMA Crossover"),
        ("SMA", (20,), "EMA", (20,), "Mixed MA: SMA vs EMA"),
        ("EMA", (9,), "SMA", (21,), "Mixed MA: Fast EMA vs Slow SMA"),
        
        # Oscillator vs MA
        ("RSI", (14, 30, 70), "SMA", (200,), "Momentum + Trend: RSI vs SMA"),
        ("RSI", (14, 30, 70), "EMA", (50,), "Momentum + Trend: RSI vs EMA"),
        
        # Price vs MA
        ("SMA", (20,), "CONSTANT", (200,), "Breakout: SMA > Level"),
        ("EMA", (50,), "CONSTANT", (0,), "Trend: EMA Direction"),
        
        # Volume Indicators
        ("OBV", (), "SMA", (20,), "Volume: OBV vs SMA"),
        ("VWAP", (), "SMA", (20,), "Volume: VWAP vs SMA"),
        
        # Advanced MAs
        ("DEMA", (20,), "DEMA", (50,), "Advanced: DEMA Crossover"),
        ("HULL_MA", (20,), "SMA", (50,), "Advanced: Hull MA vs SMA"),
        ("KAMA", (10, 2, 30), "SMA", (20,), "Adaptive: KAMA vs SMA"),
        ("T3_MA", (5, 0.7), "EMA", (20,), "Advanced: T3 vs EMA"),
        
        # Momentum Indicators
        ("MOMENTUM", (14,), "CONSTANT", (0,), "Momentum: Above/Below Zero"),
        
        # Multiple Timeframe MAs
        ("SMA", (10,), "SMA", (20,), "Fast Scalping: 10/20 SMA"),
        ("SMA", (50,), "SMA", (200,), "Golden Cross: 50/200 SMA"),
        ("EMA", (20,), "EMA", (100,), "Medium Term: 20/100 EMA"),
        
        # Weighted MAs
        ("WMA", (20,), "SMA", (20,), "Weighted vs Simple MA"),
        ("VWMA", (20,), "SMA", (20,), "Volume Weighted vs Simple"),
        
        # Trend Strength
        ("EMA", (12,), "SMA", (12,), "Lead/Lag: EMA vs SMA Same Period"),
        
        # Volatility Adapted
        ("ALMA", (9, 0.85, 6), "SMA", (20,), "Adaptive: ALMA vs SMA"),
        
        # Price Action
        ("TYPICAL_PRICE", (), "SMA", (20,), "Price: Typical Price vs SMA"),
        
        # More Volume
        ("PVO", (12, 26, 9), "CONSTANT", (0,), "Volume Oscillator"),
        ("VPT", (), "SMA", (20,), "Volume Price Trend"),
        
        # Multiple Fast MAs
        ("SMA", (5,), "SMA", (10,), "Very Fast: 5/10 SMA"),
        ("EMA", (5,), "EMA", (13,), "Fast EMA: 5/13"),
        ("EMA", (8,), "EMA", (21,), "Fibonacci EMA: 8/21"),
        
        # Exotic MAs
        ("ZLEMA", (20,), "SMA", (20,), "Zero Lag EMA vs SMA"),
        ("SINE_WMA", (14,), "SMA", (20,), "Sine WMA vs SMA"),
        ("FRAMA", (10,), "SMA", (20,), "Fractal Adaptive MA"),
        
        # More combinations
        ("EMA2", (20, 5), "SMA", (20,), "Double EMA vs SMA"),
        ("TRIANGULAR_MA", (20,), "SMA", (20,), "Triangular vs Simple"),
        ("MCGINLEY_DYNAMIC", (14,), "SMA", (20,), "McGinley Dynamic"),
        
        # Price vs Constant (Breakout strategies)
        ("SMA", (50,), "CONSTANT", (250,), "Breakout: MA > High Level"),
        ("EMA", (20,), "CONSTANT", (150,), "Breakout: EMA > Low Level"),
        
        # Volume breakouts
        ("OBV", (), "CONSTANT", (0,), "Volume: OBV Direction"),
        
        # Conservative vs Aggressive
        ("SMA", (100,), "SMA", (200,), "Conservative: Long Term"),
        ("SMA", (3,), "SMA", (5,), "Aggressive: Ultra Fast"),
        ("EMA", (3,), "EMA", (8,), "Aggressive: Fast EMA"),
    ]
    
    print("🧪 TESTING TOP 40 INDICATOR COMBINATIONS")
    print("=" * 80)
    print(f"Total test cases: {len(test_cases)}")
    print("=" * 80)
    
    # Download data once
    print("\n📥 Downloading AAPL data...")
    data = download_multi_ticker_data(['AAPL'], '1y', '1d')
    
    # Find actual ticker
    actual_ticker = 'AAPL_1' if 'AAPL_1_Close' in data.columns else 'AAPL'
    print(f"   Using ticker: {actual_ticker}")
    
    results = []
    passed = 0
    failed = 0
    
    for i, (ind1, params1, ind2, params2, description) in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}/{len(test_cases)}: {description}")
        print(f"   {ind1}{params1} vs {ind2}{params2}")
        print('-' * 80)
        
        try:
            # Create strategy data
            comp1_type = ComparisonType.INDICATOR if ind1 != 'CONSTANT' else ComparisonType.CONSTANT
            comp2_type = ComparisonType.INDICATOR if ind2 != 'CONSTANT' else ComparisonType.CONSTANT
            
            strategy_data = {
                'type': 'multi_ticker_multi_strategy',
                'tickers': [actual_ticker],
                'ticker_strategies': {
                    actual_ticker: {
                        'type': 'single',
                        'entry_comp1_type': comp1_type,
                        'entry_comp1_name': ind1,
                        'entry_comp1_params': params1,
                        'entry_comp1_candles_ago': 0,
                        'entry_comp2_type': comp2_type,
                        'entry_comp2_name': ind2,
                        'entry_comp2_params': params2,
                        'entry_comp2_candles_ago': 0,
                        'exit_comp1_type': comp1_type,
                        'exit_comp1_name': ind1,
                        'exit_comp1_params': params1,
                        'exit_comp1_candles_ago': 0,
                        'exit_comp2_type': comp2_type,
                        'exit_comp2_name': ind2,
                        'exit_comp2_params': params2,
                        'exit_comp2_candles_ago': 0,
                        'entry_strategy': 'CROSSED UP' if comp1_type == ComparisonType.INDICATOR and comp2_type == ComparisonType.INDICATOR else 'GREATER THAN',
                        'exit_strategy': 'CROSSED DOWN' if comp1_type == ComparisonType.INDICATOR and comp2_type == ComparisonType.INDICATOR else 'LESS THAN'
                    }
                }
            }
            
            # Make a copy of data for this test
            test_data = data.copy()
            
            # Calculate indicators
            test_data = calculate_multi_ticker_multi_strategy_indicators(test_data, strategy_data, [actual_ticker])
            
            # Generate signals
            test_data = generate_multi_ticker_multi_strategy_signals(test_data, strategy_data, [actual_ticker])
            
            # Check results
            entry_col = f'{actual_ticker}_Entry_Signal'
            exit_col = f'{actual_ticker}_Exit_Signal'
            
            entry_count = test_data[entry_col].sum() if entry_col in test_data.columns else 0
            exit_count = test_data[exit_col].sum() if exit_col in test_data.columns else 0
            
            print(f"   ✅ PASS")
            print(f"   Entry Signals: {entry_count}")
            print(f"   Exit Signals: {exit_count}")
            
            results.append({
                'test': i,
                'description': description,
                'ind1': f"{ind1}{params1}",
                'ind2': f"{ind2}{params2}",
                'status': 'PASS',
                'entry_signals': entry_count,
                'exit_signals': exit_count
            })
            passed += 1
            
        except Exception as e:
            print(f"   ❌ FAIL: {str(e)}")
            results.append({
                'test': i,
                'description': description,
                'ind1': f"{ind1}{params1}",
                'ind2': f"{ind2}{params2}",
                'status': 'FAIL',
                'error': str(e)
            })
            failed += 1
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {len(test_cases)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {(passed/len(test_cases)*100):.1f}%")
    
    if failed > 0:
        print("\n" + "=" * 80)
        print("❌ FAILED TESTS:")
        print("=" * 80)
        for r in results:
            if r['status'] == 'FAIL':
                print(f"\nTest {r['test']}: {r['description']}")
                print(f"   {r['ind1']} vs {r['ind2']}")
                print(f"   Error: {r.get('error', 'Unknown')}")
    
    print("\n" + "=" * 80)
    print("✅ TOP PERFORMERS (Most Signals):")
    print("=" * 80)
    successful_tests = [r for r in results if r['status'] == 'PASS']
    successful_tests.sort(key=lambda x: x['entry_signals'], reverse=True)
    
    for r in successful_tests[:10]:
        print(f"{r['test']:2d}. {r['description']:50s} - {r['entry_signals']:3d} entry, {r['exit_signals']:3d} exit")
    
    return passed == len(test_cases)

if __name__ == "__main__":
    success = test_indicator_combinations()
    exit(0 if success else 1)
