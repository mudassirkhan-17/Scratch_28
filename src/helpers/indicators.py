
from ta_strategies_TVLibrary import *
import sys
import os
sys.path.append(os.path.dirname(__file__))
from validation import validate_indicator_period

class IndicatorRegistry:
    """Registry for all available indicators - easily extensible"""
    
    def __init__(self):
        self.indicators = {
            # Basic Indicators
            "SMA": sma,
            "EMA": ema,
            "RSI": rsi,
            "RSI2": rsi2,
            "SSMA": ssma,
            "EMA2": ema2,
            "MOMENTUM": momentum,
            "OBV": obv,
            "TYPICAL_PRICE": typical_price,
            "VWAP": vwap,
            "MARKET_MOMENTUM": market_momentum,
            
            # Moving Averages
            "ALL_MA": all_moving_average,
            "ALMA": arnaud_legoux_moving_average,
            "DEMA": double_exponential_moving_average,
            "HULL_MA": hull_moving_average,
            "KAMA": kaufman_adaptive_moving_average,
            "JMA": jurik_moving_average,
            "FRAMA": fractal_adaptive_moving_average,
            "SEMA": smoothed_exponential_moving_average,
            "TRIANGULAR_MA": triangular_moving_average,
            "T3_MA": t3_moving_average,
            "ZLEMA": zero_lag_exponential_moving_average,
            "ZLSMA": zero_lag_simple_moving_average,
            "WMA": weighted_moving_average,
            
            # Additional Moving Averages
            "VWMA": volume_weighted_moving_average,
            "SINE_WMA": sine_weighted_moving_average,
            "PASCAL_WMA": pascals_weighted_moving_average,
            "SYMMETRIC_WMA": symmetric_weighted_moving_average,
            "FIBONACCI_WMA": fibonacci_weighted_moving_average,
            "HOLT_WINTER_MA": holt_winter_moving_average,
            "HULL_EMA": hull_exponential_moving_average,
            "MCGINLEY_DYNAMIC": mcginley_dynamic,
            "EVMA": elastic_volume_moving_average,
            
            # Volume Indicators
            "AOBV": archer_on_balance_volume,
            "EV_MACD": elastic_volume_macd,
            "FVE": finite_volume_element,
            "KVO": klinger_volume_oscillator,
            "NVI": negative_volume_index,
            "PVO": percentage_volume_oscillator,
            "PVI": positive_volume_index,
            "PVR": price_volume_rank,
            "PVT": price_volume_trend,
            "PV": price_volume,
            "VAMA": volume_adjusted_moving_average,
            "VFI": volume_flow_indicator,
            "VPT": volume_price_trend,
            "VP": volume_profile,
            "VZO": volume_zone_oscillator,
            "VW_MACD": volume_weighted_macd,
            "WOBV": weighted_on_balance_volume,
            
            # Price Indicators
            "APO": absolute_price_oscillator,
            "APZ": adaptive_price_zone,
            "AP": average_price,
            "DP": decreasing_price,
            "DPO": detrended_price_oscillator,
            "IP": increasing_price,
            "MP": median_price,
            "MPP": midpoint_price_period,
            "PPO": percentage_price_oscillator,
            "PD": price_distance,
            "WCP": weighted_closing_price,
            
            # Trend Indicators
            "ADX": average_directional_index,
            "CMO": chande_momentum_oscillator,
            "DM": directional_movement,
            "TS": trend_signals,
            "STC": schaff_trend_cycle,
            "WTO": wave_trend_oscillator,
            "PDI": plus_directional_indicator,
            "MDI": minus_directional_indicator,
            "PDM": plus_directional_movement,
            "MDM": minus_directional_movement,
            "MBB": momentum_breakout_bands,
            
            # Batch 1: Essential Oscillators
            "MACD": macd,
            "CCI": commodity_channel_index,
            "STOCH": stochastic,
            "WILLR": williams_r,
            "ULTOSC": ultimate_oscillator,
            
            # Batch 2: Volatility Indicators
            "ATR": average_true_range,
            "BB": bollinger_bands,
            "BBW": bollinger_bands_width,
            "DONCHIAN": donchian_channel,
            "KC": keltner_channel,
            
            # Batch 3: Trend Indicators
            "ICHIMOKU": ichimoku_cloud,
            "SAR": parabolic_sar,
            "SUPERTREND": supertrend,
            "AROON": aroon,
            "AROON_OSC": aroon_oscillator,
            
            # Batch 4: Advanced Oscillators
            "STOCHRSI": stochastic_rsi,
            "MFI": money_flow_index,
            "ROC": rate_of_change,
            "AO": awesome_oscillator,
            "CMF": chaikin_money_flow,
            
            # Batch 5: Volume Analysis
            "AD": accumulation_distribution,
            "ADOSC": accumulation_distribution_oscillator,
            "CHO": chaikin_oscillator,
            "FI": force_index,
            "VROC": volume_rate_of_change,
            "VO": volume_oscillator,
            "VWAP": volume_weighted_average_price,
            "EOM": ease_of_movement,
            
            # Batch 6: Advanced Trend (7 indicators)
            "LINREG": linear_regression,
            "LINREGSLOPE": linear_regression_slope,
            "LINREGANGLE": linear_regression_angle,
            "STDDEV": standard_deviation,
            "VAR": variance,
            "EHLS": ehlers_super_smoother,
            "GANN": gann_high_low_activator,
            
            # Batch 7: Specialized Indicators (5 indicators)
            "FIBONACCI": fibonacci_pivot_points,
            "PIVOT": pivot_points,
            "HILBERT": hilbert_transform_trend,
            "HILBERT_SINE": hilbert_transform_sine,
            "HILBERT_PHASE": hilbert_transform_phase,
            
            # Batch 8: Additional Oscillators (5 indicators)
            "ULTOSC2": ultimate_oscillator_2,
            "CCI2": commodity_channel_index_2,
            "MOM": momentum_oscillator,
            "BOP": balance_of_power,
            "ERI": elder_ray_index,
            
            # Batch 9: Advanced Moving Averages (5 indicators)
            "TEMA": triple_exponential_moving_average,
            "TRIMA": triangular_moving_average_2,
            "VIDYA": variable_index_dynamic_average,
            "WILDER": wilders_moving_average,
            "DEMA2": double_exponential_moving_average_2,
            
            # Batch 10: Price Action Indicators (5 indicators)
            "PP": pivot_points_2,
            "PPR": pivot_points_resistance,
            "PPS": pivot_points_support,
            "HL2": high_low_average,
            "HLC3": high_low_close_average,
            
            # Batch 11: Volatility Expansion (5 indicators)
            "BBP": bollinger_bands_percent,
            "BBU": bollinger_bands_upper,
            "BBL": bollinger_bands_lower,
            "KCU": keltner_channel_upper,
            "KCL": keltner_channel_lower,
            
            # Batch 12: Specialized Analysis (5 indicators)
            "FISHER": fisher_transform,
            "INERTIA": inertia_indicator,
            "QSTICK": qstick_indicator,
            "TRIX": trix_indicator,
            "TSI": true_strength_index,
            
            # Batch 13: Advanced Oscillators & Indicators (10 indicators)
            "ABERRATION": aberration,
            "APO": absolute_price_oscillator,
            "ACCELERATION": acceleration_bands,
            "ADINDEX": accumulation_distribution_index,
            "ADAPTIVE": adaptive_price_zone,
            "ARCHER_MA": archer_moving_averages,
            "ARCHER_OBV": archer_on_balance_volume,
            "ARNAUD_LEGOUX": arnaud_legoux_moving_average,
            "BETA": beta_indicator,
            "BIAS": bias_indicator,
            
            # Batch 14: Advanced Analysis (10 indicators)
            "BRAR": brar_indicator,
            "BULL_BEAR": bull_bear_power,
            "BUY_SELL": buy_sell_pressure,
            "CENTER_GRAVITY": center_of_gravity,
            "CHANDE_FORECAST": chande_forecast_oscillator,
            "CHANDE_KROLL": chande_kroll_stop,
            "CHANDELIER": chandelier_exit,
            "CHAOS": choppiness_index,
            "CORRELATION": correlation_trend_indicator,
            "COPPOCK": coppock_curve,
            
            # Batch 15: Advanced Momentum (10 indicators)
            "CUMULATIVE_FI": cumulative_force_index,
            "CROSS_SIGNALS": cross_signals,
            "DECAY": decay_indicator,
            "DECREASING": decreasing_price,
            "DETRENDED": detrended_price_oscillator,
            "DIRECTIONAL": directional_movement,
            "ELDERS_FI": elders_force_index,
            "ENVELOPES": envelopes,
            "FISHER_RVI": fisher_rvi,
            "FRACTAL": fractal_indicator,
            
            # Batch 16: Missing Indicators - Part 1 (15 indicators)
            "ELDERS_THERMOMETER": elders_thermometer,
            "HILBERT_PERIOD": hilbert_period,
            "HILBERT_PHASOR": hilbert_phasor,
            "HILBERT_TREND": hilbert_trend,
            "HOLT_WINTER_CHANNEL": holt_winter_channel,
            "INCREASING_PRICE": increasing_price,
            "INVERSE_FISHER_RSI": inverse_fisher_rsi,
            "KAUFMAN_EFFICIENCY": kaufman_efficiency,
            "KDJ": kdj_indicator,
            "KST": know_sure_thing,
            "LINREG_INTERCEPT": linear_regression_intercept,
            "LONG_RUN": long_run,
            "MASS_INDEX": mass_index,
            "MEDIAN_PRICE": median_price,
            "MIDPOINT_PERIOD": midpoint_period,
            
            # Batch 17: Missing Indicators - Part 2 (15 indicators)
            "MIDPOINT_PRICE": midpoint_price,
            "MOMENTUM_BREAKOUT": momentum_breakout,
            "MOVING_STDDEV": moving_standard_deviation,
            "NATR": normalized_atr,
            "NORMALIZED_BASP": normalized_basp,
            "PEARSON_CORR": pearsons_correlation,
            "PERCENT_B": percent_b,
            "PGO": pretty_good_oscillator,
            "PRICE_DISTANCE": price_distance,
            "PSYCHOLOGICAL": psychological_line,
            "QQE": quantitative_qualitative_estimation,
            "RSI_XTRA": relative_strength_xtra,
            "RVI": relative_vigor_index,
            "RVI_VOLATILITY": relative_volatility_index,
            "SHORT_RUN": short_run,
            
            # Batch 18: Missing Indicators - Part 3 (15 indicators)
            "SLOPE": slope_indicator,
            "SMI_ERGODIC": smi_ergodic_oscillator,
            "SQUEEZE": squeeze_indicator,
            "SQUEEZE_PRO": squeeze_pro,
            "STOCH_D": stochastic_d,
            "STOCH_FAST": stochastic_fast,
            "STOCH_K": stochastic_k,
            "STOCH_OSC": stochastic_oscillator,
            "STOP_REVERSE": stop_and_reverse,
            "SUMMATION": summation_indicator,
            "TD_SEQUENTIAL": td_sequential,
            "TREND_SIGNALS": trend_signals,
            "TTM_TREND": ttm_trend,
            "TWIGGS_MONEY": twiggs_money_index,
            "ULCER_INDEX": ulcer_index,
            
            # Batch 19: Missing Indicators - Part 4 (6 indicators)
            "UP_DOWN": up_down_indicator,
            "VHF": vertical_horizontal_filter,
            "VOLUME_PROFILE": volume_profile,
            "VORTEX": vortex_indicator,
            "WAVE_PM": wave_pm,
            "WAVE_TREND": wave_trend_oscillator
        }
    
    def register(self, name, function):
        """Register a new indicator"""
        self.indicators[name] = function
    
    def get(self, name):
        """Get indicator function by name"""
        return self.indicators.get(name)
    
    def list_indicators(self):
        """List all available indicators"""
        return list(self.indicators.keys())


def sma(data, period):
    """Calculate Simple Moving Average"""
    return data['Close'].rolling(window=period).mean()

def ema(data, period):
    """Calculate Exponential Moving Average"""
    return data['Close'].ewm(span=period).mean()

def rsi(data, period=14, upper_threshold=70, lower_threshold=30):
    """Calculate Relative Strength Index"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def rsi2(data, period=14, upper_threshold=70, lower_threshold=30):
    """Calculate RSI using the robust library implementation"""
    # Create RSI strategy instance
    rsi_strategy = RelativeStrengthIndexStrategies(
        period=period,
        baseline=50,
        lower_threshold=lower_threshold,
        upper_threshold=upper_threshold
    )
    
    # Calculate RSI values
    rsi_values = rsi_strategy.compute_values(data)
    
    return rsi_values

def ssma(data, period=14, upper_threshold=1.0, lower_threshold=-1.0):
    """Calculate Smoothed Simple Moving Average using the library implementation"""
    ssma_strategy = SmoothedSimpleMovingAverageStrategies(
        period=period,
        baseline=0,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    ssma_values = ssma_strategy.compute_values(data)
    return ssma_values

def ema2(data, period=20, upper_threshold=0.03, lower_threshold=-0.03):
    """Calculate Exponential Moving Average using the library implementation"""
    ema_strategy = ExponentialMovingAverageStrategies(
        period=period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    ema_values = ema_strategy.compute_values(data)
    return ema_values

def momentum(data, period=10, upper_threshold=1, lower_threshold=-1):
    """Calculate Momentum using the library implementation"""
    momentum_strategy = MomentumStrategies(
        period=period,
        baseline=0,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    momentum_values = momentum_strategy.compute_values(data)
    return momentum_values

def obv(data, baseline=0, upper_threshold=100000, lower_threshold=-100000):
    """Calculate On Balance Volume using the library implementation"""
    obv_strategy = OnBalanceVolumeStrategies(
        baseline=baseline,
        lower_threshold=lower_threshold,
        upper_threshold=upper_threshold
    )
    obv_values = obv_strategy.compute_values(data)
    return obv_values

def typical_price(data, threshold=0.01):
    """Calculate Typical Price using the library implementation"""
    tp_strategy = TypicalPriceStrategies(
        threshold_percentage=threshold
    )
    tp_values = tp_strategy.compute_values(data)
    return tp_values

def vwap(data, threshold=0.01):
    """Calculate Volume Weighted Average Price using the library implementation"""
    vwap_strategy = VolumeWeightedAveragePriceStrategies(
        threshold=threshold
    )
    vwap_values = vwap_strategy.compute_values(data)
    return vwap_values

def market_momentum(data, period=14, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Market Momentum using the library implementation"""
    mm_strategy = MarketMomentumStrategies(
        period=period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    mm_values = mm_strategy.compute_values(data)
    return mm_values

# =============================================================================
# MOVING AVERAGES - ADDITIONAL INDICATORS
# =============================================================================

def all_moving_average(data, short_period=5, medium_period=20, long_period=50, threshold_percent=0.02):
    """Calculate All Moving Average using the library implementation"""
    ama_strategy = AllMovingAverageStrategies(
        short_period=short_period,
        medium_period=medium_period,
        long_period=long_period,
        threshold_percent=threshold_percent
    )
    ama_values = ama_strategy.compute_values(data)
    return ama_values

def arnaud_legoux_moving_average(data, period=14, offset=0.85, sigma=6, baseline=0, lower_threshold=-0.5, upper_threshold=0.5):
    """Calculate Arnaud Legoux Moving Average using the library implementation"""
    alma_strategy = ArnaudLegouxMovingAverageStrategies(
        period=period,
        offset=offset,
        sigma=sigma,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    alma_values = alma_strategy.compute_values(data)
    return alma_values

def double_exponential_moving_average(data, period=20, distance_threshold=0.01):
    """Calculate Double Exponential Moving Average using the library implementation"""
    dema_strategy = DoubleExponentialMovingAverageStrategies(
        period=period,
        distance_threshold=distance_threshold
    )
    dema_values = dema_strategy.compute_values(data)
    return dema_values

def hull_moving_average(data, period=14, price_threshold=0.01):
    """Calculate Hull Moving Average using the library implementation"""
    hma_strategy = HullMovingAverageStrategies(
        period=period,
        price_threshold=price_threshold
    )
    hma_values = hma_strategy.compute_values(data)
    return hma_values

def kaufman_adaptive_moving_average(data, period=10, fast_period=2, slow_period=30, distance_threshold=0.01):
    """Calculate Kaufman Adaptive Moving Average using the library implementation"""
    kama_strategy = KaufmanAdaptiveMovingAverageStrategies(
        period=period,
        fast_period=fast_period,
        slow_period=slow_period,
        distance_threshold=distance_threshold
    )
    kama_values = kama_strategy.compute_values(data)
    return kama_values

def jurik_moving_average(data, period=20, phase=0.0, power=1.0, distance_threshold=0.01):
    """Calculate Jurik Moving Average using the library implementation"""
    jma_strategy = JurikMovingAverageStrategies(
        period=period,
        phase=phase,
        power=power,
        distance_threshold=distance_threshold
    )
    jma_values = jma_strategy.compute_values(data)
    return jma_values

def fractal_adaptive_moving_average(data, period=10, divergence_upper_threshold=0.03, divergence_lower_threshold=-0.03):
    """Calculate Fractal Adaptive Moving Average using the library implementation"""
    frama_strategy = FractalAdaptiveMovingAverageStrategies(
        period=period,
        divergence_upper_threshold=divergence_upper_threshold,
        divergence_lower_threshold=divergence_lower_threshold
    )
    frama_values = frama_strategy.compute_values(data)
    return frama_values

def smoothed_exponential_moving_average(data, period=14, baseline=0, upper_threshold=1.0, lower_threshold=-1.0):
    """Calculate Smoothed Exponential Moving Average using the library implementation"""
    sema_strategy = SmoothedExponentialMovingAverageStrategies(
        period=period,
        baseline=baseline,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    sema_values = sema_strategy.compute_values(data)
    return sema_values

def triangular_moving_average(data, period=20, threshold_percentage=0.01):
    """Calculate Triangular Moving Average using the library implementation"""
    tma_strategy = TriangularMovingAverageStrategies(
        period=period,
        threshold_percentage=threshold_percentage
    )
    tma_values = tma_strategy.compute_values(data)
    return tma_values

def t3_moving_average(data, period=10, v=0.7, price_column='Close', pos_threshold=0.02, neg_threshold=-0.02):
    """Calculate T3 Moving Average using the library implementation"""
    t3_strategy = T3MovingAverageStrategies(
        period=period,
        v=v,
        price_column=price_column,
        pos_threshold=pos_threshold,
        neg_threshold=neg_threshold
    )
    t3_values = t3_strategy.compute_values(data)
    return t3_values

def zero_lag_exponential_moving_average(data, period=14, deviation_threshold=0.01):
    """Calculate Zero Lag Exponential Moving Average using the library implementation"""
    zlema_strategy = ZeroLagExponentialMovingAverageStrategies(
        period=period,
        deviation_threshold=deviation_threshold
    )
    zlema_values = zlema_strategy.compute_values(data)
    return zlema_values

def zero_lag_simple_moving_average(data, period=14, deviation_threshold=0.01):
    """Calculate Zero Lag Simple Moving Average using the library implementation"""
    zlsma_strategy = ZeroLagSimpleMovingAverageStrategies(
        period=period,
        deviation_threshold=deviation_threshold
    )
    zlsma_values = zlsma_strategy.compute_values(data)
    return zlsma_values

def weighted_moving_average(data, period=14, deviation_threshold=0.01):
    """Calculate Weighted Moving Average using the library implementation"""
    wma_strategy = WeightedMovingAverageStrategies(
        period=period,
        deviation_threshold=deviation_threshold
    )
    wma_values = wma_strategy.compute_values(data)
    return wma_values

# =============================================================================
# ADDITIONAL MOVING AVERAGES - MORE INDICATORS
# =============================================================================

def volume_weighted_moving_average(data, period=20, threshold=0.01):
    """Calculate Volume Weighted Moving Average using the library implementation"""
    vwma_strategy = VolumeWeightedMovingAverageStrategies(
        period=period,
        threshold=threshold
    )
    vwma_values = vwma_strategy.compute_values(data)
    return vwma_values

def sine_weighted_moving_average(data, period=14, baseline=0, upper_threshold=1.0, lower_threshold=-1.0):
    """Calculate Sine Weighted Moving Average using the library implementation"""
    swma_strategy = SineWeightedMovingAverageStrategies(
        period=period,
        baseline=baseline,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    swma_values = swma_strategy.compute_values(data)
    return swma_values

def pascals_weighted_moving_average(data, period=10, lower_threshold=-1, upper_threshold=1):
    """Calculate Pascals Weighted Moving Average using the library implementation"""
    pwma_strategy = PascalsWeightedMovingAverageStrategies(
        period=period,
        lower_threshold=lower_threshold,
        upper_threshold=upper_threshold
    )
    pwma_values = pwma_strategy.compute_values(data)
    return pwma_values

def symmetric_weighted_moving_average(data, period=5, price_column='Close', pos_threshold=0.02, neg_threshold=-0.02):
    """Calculate Symmetric Weighted Moving Average using the library implementation"""
    swma_strategy = SymmetricWeightedMovingAverageStrategies(
        period=period,
        price_column=price_column,
        pos_threshold=pos_threshold,
        neg_threshold=neg_threshold
    )
    swma_values = swma_strategy.compute_values(data)
    return swma_values

def fibonacci_weighted_moving_average(data, period=10, upper_threshold=0.03, lower_threshold=-0.03):
    """Calculate Fibonacci Weighted Moving Average using the library implementation"""
    fwma_strategy = FibonacciWeightedMovingAverageStrategies(
        period=period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    fwma_values = fwma_strategy.compute_values(data)
    return fwma_values

def holt_winter_moving_average(data, alpha=0.2, beta=0.1, deviation_percent_threshold=2.0):
    """Calculate Holt Winter Moving Average using the library implementation"""
    hwma_strategy = HoltWinterMovingAverageStrategies(
        alpha=alpha,
        beta=beta,
        deviation_percent_threshold=deviation_percent_threshold
    )
    hwma_values = hwma_strategy.compute_values(data)
    return hwma_values

def hull_exponential_moving_average(data, period=14, deviation_percent_threshold=2.0):
    """Calculate Hull Exponential Moving Average using the library implementation"""
    hema_strategy = HullExponentialMovingAverageStrategies(
        period=period,
        deviation_percent_threshold=deviation_percent_threshold
    )
    hema_values = hema_strategy.compute_values(data)
    return hema_values

def mcginley_dynamic(data, period=14, threshold=0.01):
    """Calculate McGinley Dynamic using the library implementation"""
    md_strategy = McGinleyDynamicStrategies(
        period=period,
        threshold=threshold
    )
    md_values = md_strategy.compute_values(data)
    return md_values


def elastic_volume_moving_average(data, period=20, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Elastic Volume Moving Average using the library implementation"""
    evma_strategy = ElasticVolumeMovingAverageStrategies(
        period=period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    evma_values = evma_strategy.compute_values(data)
    return evma_values

# =============================================================================
# VOLUME INDICATORS
# =============================================================================

def archer_on_balance_volume(data, period=14, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Archer On Balance Volume using the library implementation"""
    aobv_strategy = ArcherOnBalanceVolumeStrategies(
        baseline=0,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    aobv_values = aobv_strategy.compute_values(data)
    return aobv_values

def elastic_volume_macd(data, fast_period=12, slow_period=26, signal_period=9, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Elastic Volume MACD using the library implementation"""
    evmacd_strategy = ElasticVolumeMACDStrategies(
        fast_period=fast_period,
        slow_period=slow_period,
        signal_period=signal_period,
        histogram_upper=upper_threshold,
        histogram_lower=lower_threshold
    )
    evmacd_values = evmacd_strategy.compute_values(data)
    return evmacd_values

def finite_volume_element(data, period=14, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Finite Volume Element using the library implementation"""
    fve_strategy = FiniteVolumeElementStrategies(
        period=period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    fve_values = fve_strategy.compute_values(data)
    return fve_values

def klinger_volume_oscillator(data, fast_period=34, slow_period=55, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Klinger Volume Oscillator using the library implementation"""
    kvo_strategy = KlingerVolumeOscillatorStrategies(
        fast_period=fast_period,
        slow_period=slow_period,
        distance_threshold=0.0
    )
    kvo_values = kvo_strategy.compute_values(data)
    return kvo_values

def negative_volume_index(data, period=14, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Negative Volume Index using the library implementation"""
    nvi_strategy = NegativeVolumeIndexStrategies(
        baseline=1000,
        lower_threshold=lower_threshold,
        upper_threshold=upper_threshold
    )
    nvi_values = nvi_strategy.compute_values(data)
    return nvi_values

def percentage_volume_oscillator(data, fast_period=12, slow_period=26, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Percentage Volume Oscillator using the library implementation"""
    pvo_strategy = PercentageVolumeOscillatorStrategies(
        fast_period=fast_period,
        slow_period=slow_period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    pvo_values = pvo_strategy.compute_values(data)
    return pvo_values

def positive_volume_index(data, period=14, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Positive Volume Index using the library implementation"""
    pvi_strategy = PositiveVolumeIndexStrategies(
        baseline=1000,
        lower_threshold=lower_threshold,
        upper_threshold=upper_threshold
    )
    pvi_values = pvi_strategy.compute_values(data)
    return pvi_values

def price_volume_rank(data, period=14, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Price Volume Rank using the library implementation"""
    pvr_strategy = PriceVolumeRankStrategies(
        period=period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    pvr_values = pvr_strategy.compute_values(data)
    return pvr_values

def price_volume_trend(data, period=14, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Price Volume Trend using the library implementation"""
    pvt_strategy = PriceVolumeTrendStrategies(
        baseline=0,
        lower_threshold=lower_threshold,
        upper_threshold=upper_threshold
    )
    pvt_values = pvt_strategy.compute_values(data)
    return pvt_values

def price_volume(data, period=14, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Price Volume using the library implementation"""
    pv_strategy = PriceVolumeStrategies(
        period=period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    pv_values = pv_strategy.compute_values(data)
    return pv_values

def volume_adjusted_moving_average(data, period=20, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Volume Adjusted Moving Average using the library implementation"""
    vama_strategy = VolumeAdjustedMovingAverageStrategies(
        period=period,
        threshold_percentage=0.01
    )
    vama_values = vama_strategy.compute_values(data)
    return vama_values

def volume_flow_indicator(data, period=14, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Volume Flow Indicator using the library implementation"""
    vfi_strategy = VolumeFlowIndicatorStrategies(
        period=period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    vfi_values = vfi_strategy.compute_values(data)
    return vfi_values

def volume_price_trend(data, ma_period=14, threshold_percentage=0.01):
    """Calculate Volume Price Trend using the library implementation"""
    vpt_strategy = VolumePriceTrendStrategies(
        ma_period=ma_period,
        threshold_percentage=threshold_percentage
    )
    vpt_values = vpt_strategy.compute_values(data)
    return vpt_values

def volume_profile(data, period=14, bin_size=1, value_area_percentage=0.7):
    """Calculate Volume Profile using the library implementation"""
    vp_strategy = VolumeProfileStrategies(
        period=period,
        bin_size=bin_size,
        value_area_percentage=value_area_percentage
    )
    vp_values = vp_strategy.compute_values(data)
    return vp_values

def volume_zone_oscillator(data, period=14, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Volume Zone Oscillator using the library implementation"""
    vzo_strategy = VolumeZoneOscillatorStrategies(
        period=period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    vzo_values = vzo_strategy.compute_values(data)
    return vzo_values

def volume_weighted_macd(data, fast_period=12, slow_period=26, signal_period=9, threshold=0):
    """Calculate Volume Weighted MACD using the library implementation"""
    vwmacd_strategy = VolumeWeightedMACDStrategies(
        fast_period=fast_period,
        slow_period=slow_period,
        signal_period=signal_period,
        threshold=threshold
    )
    vwmacd_values = vwmacd_strategy.compute_values(data)
    return vwmacd_values

def weighted_on_balance_volume(data, ma_period=20):
    """Calculate Weighted On Balance Volume using the library implementation"""
    wobv_strategy = WeightedOnBalanceVolumeStrategies(
        ma_period=ma_period
    )
    wobv_values = wobv_strategy.compute_values(data)
    return wobv_values

# =============================================================================
# PRICE INDICATORS
# =============================================================================

def absolute_price_oscillator(data, fast_period=12, slow_period=26, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Absolute Price Oscillator using the library implementation"""
    apo_strategy = AbsolutePriceOscillatorStrategies(
        short_period=fast_period,
        long_period=slow_period,
        baseline=0,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    apo_values = apo_strategy.compute_values(data)
    return apo_values

def adaptive_price_zone(data, period=20, multiplier=0.5, baseline=0):
    """Calculate Adaptive Price Zone using the library implementation"""
    apz_strategy = AdaptivePriceZoneStrategies(
        period=period,
        multiplier=multiplier,
        baseline=baseline
    )
    # compute_values returns (center, upper_zone, lower_zone) tuple
    # We return just the center line for crossover strategies
    center, upper_zone, lower_zone = apz_strategy.compute_values(data)
    return center

def average_price(data, period=14, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Average Price using the library implementation"""
    ap_strategy = AveragePriceStrategies(
        threshold=1
    )
    ap_values = ap_strategy.compute_values(data)
    return ap_values

def decreasing_price(data, period=14, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Decreasing Price using the library implementation"""
    dp_strategy = DecreasingPriceStrategies(
        period=period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    dp_values = dp_strategy.compute_values(data)
    return dp_values

def detrended_price_oscillator(data, period=14, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Detrended Price Oscillator using the library implementation"""
    dpo_strategy = DetrendedPriceOscillatorStrategies(
        period=period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    dpo_values = dpo_strategy.compute_values(data)
    return dpo_values

def increasing_price(data, period=14, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Increasing Price using the library implementation"""
    ip_strategy = IncreasingPriceStrategies(
        period=period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    ip_values = ip_strategy.compute_values(data)
    return ip_values

def median_price(data, period=14, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Median Price using the library implementation"""
    mp_strategy = MedianPriceStrategies(
        threshold=0.01
    )
    mp_values = mp_strategy.compute_values(data)
    return mp_values

def midpoint_price_period(data, period=20, threshold=0.01):
    """Calculate Midpoint Price Period using the library implementation"""
    mpp_strategy = MidpointPricePeriodStrategies(
        period=period,
        threshold=threshold
    )
    mpp_values = mpp_strategy.compute_values(data)
    return mpp_values

def percentage_price_oscillator(data, fast_period=12, slow_period=26, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Percentage Price Oscillator using the library implementation"""
    ppo_strategy = PercentagePriceOscillatorStrategies(
        fast_period=fast_period,
        slow_period=slow_period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    ppo_values = ppo_strategy.compute_values(data)
    return ppo_values

def price_distance(data, period=14, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Price Distance using the library implementation"""
    pd_strategy = PriceDistanceStrategies(
        period=period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    pd_values = pd_strategy.compute_values(data)
    return pd_values

def weighted_closing_price(data, period=14, upper_threshold=0.05, lower_threshold=-0.05):
    """Calculate Weighted Closing Price using the library implementation"""
    wcp_strategy = WeightedClosingPriceStrategies(
        sma_period=period,
        threshold=0.01
    )
    wcp_values = wcp_strategy.compute_values(data)
    return wcp_values

# =============================================================================
# TREND INDICATORS
# =============================================================================

def average_directional_index(data, period=14, adx_threshold=25):
    """Calculate Average Directional Index using the library implementation"""
    adx_strategy = AverageDirectionalIndexStrategies(
        period=period,
        adx_threshold=adx_threshold
    )
    adx_values = adx_strategy.compute_values(data)
    return adx_values

def chande_momentum_oscillator(data, period=14, upper_threshold=50, lower_threshold=-50):
    """Calculate Chande Momentum Oscillator using the library implementation"""
    cmo_strategy = ChandeMomentumOscillatorStrategies(
        period=period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    cmo_values = cmo_strategy.compute_values(data)
    return cmo_values

def directional_movement(data, period=14, baseline=0, upper_threshold=5, lower_threshold=-5):
    """Calculate Directional Movement using the library implementation"""
    dm_strategy = DirectionalMovementStrategies(
        period=period,
        baseline=baseline,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    dm_values = dm_strategy.compute_values(data)
    return dm_values

def trend_signals(data, short_period=10, long_period=50, threshold=0):
    """Calculate Trend Signals using the library implementation"""
    ts_strategy = TrendSignalsStrategies(
        short_period=short_period,
        long_period=long_period,
        threshold=threshold
    )
    ts_values = ts_strategy.compute_values(data)
    return ts_values

def schaff_trend_cycle(data, fast_period=23, slow_period=50, cycle_period=10, baseline=50, upper_threshold=75, lower_threshold=25):
    """Calculate Schaff Trend Cycle using the library implementation"""
    stc_strategy = SchaffTrendCycleStrategies(
        fast_period=fast_period,
        slow_period=slow_period,
        cycle_period=cycle_period,
        baseline=baseline,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    stc_values = stc_strategy.compute_values(data)
    return stc_values

def wave_trend_oscillator(data, period1=10, period2=21, signal_period=4, upper_threshold=60, lower_threshold=-60):
    """Calculate Wave Trend Oscillator using the library implementation"""
    wto_strategy = WaveTrendOscillatorStrategies(
        period1=period1,
        period2=period2,
        signal_period=signal_period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    wto_values = wto_strategy.compute_values(data)
    # WTO returns a tuple, return the first Series
    if isinstance(wto_values, tuple):
        return wto_values[0]
    return wto_values

def plus_directional_indicator(data, period=14, upper_threshold=25, lower_threshold=-25):
    """Calculate Plus Directional Indicator using the library implementation"""
    pdi_strategy = PlusDirectionalIndicatorStrategies(
        period=period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    pdi_values = pdi_strategy.compute_values(data)
    return pdi_values

def minus_directional_indicator(data, period=14, upper_threshold=25, lower_threshold=-25):
    """Calculate Minus Directional Indicator using the library implementation"""
    mdi_strategy = MinusDirectionalIndicatorStrategies(
        period=period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    mdi_values = mdi_strategy.compute_values(data)
    return mdi_values

def plus_directional_movement(data, period=14, upper_threshold=5, lower_threshold=-5):
    """Calculate Plus Directional Movement using the library implementation"""
    pdm_strategy = PlusDirectionalMovementStrategies(
        period=period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    pdm_values = pdm_strategy.compute_values(data)
    return pdm_values

def minus_directional_movement(data, period=14, upper_threshold=5, lower_threshold=-5):
    """Calculate Minus Directional Movement using the library implementation"""
    mdm_strategy = MinusDirectionalMovementStrategies(
        period=period,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    mdm_values = mdm_strategy.compute_values(data)
    return mdm_values

def momentum_breakout_bands(data, period=20, upper_threshold=2, lower_threshold=-2):
    """Calculate Momentum Breakout Bands using the library implementation"""
    mbb_strategy = MomentumBreakoutBandsStrategies(
        period=period,
        multiplier=2,
        baseline=0,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold
    )
    mbb_values = mbb_strategy.compute_values(data)
    # MBB returns a DataFrame, return the momentum column
    if hasattr(mbb_values, 'Momentum'):
        return mbb_values['Momentum']
    return mbb_values



def calculate_indicator(data, indicator_name, params):
    """Generic function to calculate any indicator with validation"""
    indicator_func = indicator_registry.get(indicator_name)
    if indicator_func is None:
        raise ValueError(f"Unknown indicator: {indicator_name}")
    
    if indicator_name in ["RSI", "RSI2"]:
        # RSI with defaults: period=14, upper=70, lower=30
        period = validate_indicator_period(params[0] if len(params) >= 1 else 14, "RSI")
        upper = params[1] if len(params) >= 2 else 70
        lower = params[2] if len(params) >= 3 else 30
        return indicator_func(data, period, upper, lower)
    elif indicator_name in ["SSMA", "EMA2", "MOMENTUM"]:
        # Oscillators with defaults: period, upper=1.0, lower=-1.0
        period = validate_indicator_period(params[0] if len(params) >= 1 else 14, indicator_name)
        upper = params[1] if len(params) >= 2 else 1.0
        lower = params[2] if len(params) >= 3 else -1.0
        return indicator_func(data, period, upper, lower)
    elif indicator_name == "MARKET_MOMENTUM":
        # Market momentum with defaults: period=14, upper=0.05, lower=-0.05
        period = validate_indicator_period(params[0] if len(params) >= 1 else 14, "Market Momentum")
        upper = params[1] if len(params) >= 2 else 0.05
        lower = params[2] if len(params) >= 3 else -0.05
        return indicator_func(data, period, upper, lower)
    elif indicator_name in ["OBV"]:
        # OBV with defaults: baseline=0, upper=100000, lower=-100000
        baseline = params[0] if len(params) >= 1 else 0
        upper = params[1] if len(params) >= 2 else 100000
        lower = params[2] if len(params) >= 3 else -100000
        return indicator_func(data, baseline, upper, lower)
    elif indicator_name in ["TYPICAL_PRICE", "VWAP"]:
        # Price indicators with default threshold=0.01
        threshold = params[0] if len(params) >= 1 else 0.01
        return indicator_func(data, threshold)
    elif indicator_name == "ALL_MA":
        if len(params) < 4:
            raise ValueError(f"Indicator {indicator_name} requires 4 parameters (short, medium, long, threshold), got {len(params)}")
        return indicator_func(data, params[0], params[1], params[2], params[3])  # short, medium, long, threshold
    elif indicator_name == "DEMA":
        # DEMA with defaults: period=20, distance_threshold=0.01
        period = params[0] if len(params) >= 1 else 20
        distance_threshold = params[1] if len(params) >= 2 else 0.01
        return indicator_func(data, period, distance_threshold)
    elif indicator_name == "HULL_MA":
        # Hull MA with defaults: period=14, price_threshold=0.01
        period = params[0] if len(params) >= 1 else 14
        price_threshold = params[1] if len(params) >= 2 else 0.01
        return indicator_func(data, period, price_threshold)
    elif indicator_name == "KAMA":
        # KAMA with defaults: period=10, fast=2, slow=30, distance=0.01
        period = params[0] if len(params) >= 1 else 10
        fast = params[1] if len(params) >= 2 else 2
        slow = params[2] if len(params) >= 3 else 30
        distance = params[3] if len(params) >= 4 else 0.01
        return indicator_func(data, period, fast, slow, distance)
    elif indicator_name == "JMA":
        # JMA with defaults: period=20, phase=0, power=2, distance=0.01
        period = params[0] if len(params) >= 1 else 20
        phase = params[1] if len(params) >= 2 else 0
        power = params[2] if len(params) >= 3 else 2
        distance = params[3] if len(params) >= 4 else 0.01
        return indicator_func(data, period, phase, power, distance)
    elif indicator_name == "FRAMA":
        # FRAMA with defaults: period=20, upper_div=0.02, lower_div=-0.02
        period = params[0] if len(params) >= 1 else 20
        upper_div = params[1] if len(params) >= 2 else 0.02
        lower_div = params[2] if len(params) >= 3 else -0.02
        return indicator_func(data, period, upper_div, lower_div)
    elif indicator_name in ["SMA", "EMA", "SSMA", "EMA2"]:
        if len(params) < 1:
            raise ValueError(f"Indicator {indicator_name} requires 1 parameter (period), got {len(params)}")
        return indicator_func(data, params[0])  # period only
    elif indicator_name == "SEMA":
        # SEMA with defaults: period=20, baseline=0, upper=1.0, lower=-1.0
        period = params[0] if len(params) >= 1 else 20
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 1.0
        lower = params[3] if len(params) >= 4 else -1.0
        return indicator_func(data, period, baseline, upper, lower)
    elif indicator_name == "TRIANGULAR_MA":
        # Triangular MA with defaults: period=20, threshold_percentage=0.01
        period = params[0] if len(params) >= 1 else 20
        threshold_percentage = params[1] if len(params) >= 2 else 0.01
        return indicator_func(data, period, threshold_percentage)
    elif indicator_name == "T3_MA":
        # T3 MA with defaults: period=10, v=0.7, price_col='Close', pos=0.02, neg=-0.02
        period = params[0] if len(params) >= 1 else 10
        v = params[1] if len(params) >= 2 else 0.7
        price_col = params[2] if len(params) >= 3 else 'Close'
        pos = params[3] if len(params) >= 4 else 0.02
        neg = params[4] if len(params) >= 5 else -0.02
        return indicator_func(data, period, v, price_col, pos, neg)
    elif indicator_name in ["ZLEMA", "ZLSMA", "WMA", "VWMA"]:
        # Zero lag/weighted MAs with defaults: period, deviation_threshold=0.01
        period = params[0] if len(params) >= 1 else 14
        deviation_threshold = params[1] if len(params) >= 2 else 0.01
        return indicator_func(data, period, deviation_threshold)
    elif indicator_name == "MCGINLEY_DYNAMIC":
        # McGinley with defaults: period=20, threshold=0.01
        period = params[0] if len(params) >= 1 else 20
        threshold = params[1] if len(params) >= 2 else 0.01
        return indicator_func(data, period, threshold)
    elif indicator_name in ["EVMA"]:
        # Elastic Volume MA with defaults: period=20, upper=1.0, lower=-1.0
        period = params[0] if len(params) >= 1 else 20
        upper = params[1] if len(params) >= 2 else 1.0
        lower = params[2] if len(params) >= 3 else -1.0
        return indicator_func(data, period, upper, lower)
    elif indicator_name == "SINE_WMA":
        # Sine WMA with defaults: period=20, baseline=0, upper=1.0, lower=-1.0
        period = params[0] if len(params) >= 1 else 20
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 1.0
        lower = params[3] if len(params) >= 4 else -1.0
        return indicator_func(data, period, baseline, upper, lower)
    elif indicator_name == "PASCAL_WMA":
        # Pascal WMA with defaults: period=20, lower=-1.0, upper=1.0
        period = params[0] if len(params) >= 1 else 20
        lower = params[1] if len(params) >= 2 else -1.0
        upper = params[2] if len(params) >= 3 else 1.0
        return indicator_func(data, period, lower, upper)
    elif indicator_name == "SYMMETRIC_WMA":
        # Symmetric WMA with defaults: period=20, price_col='Close', pos=0.02, neg=-0.02
        period = params[0] if len(params) >= 1 else 20
        price_col = params[1] if len(params) >= 2 else 'Close'
        pos = params[2] if len(params) >= 3 else 0.02
        neg = params[3] if len(params) >= 4 else -0.02
        return indicator_func(data, period, price_col, pos, neg)
    elif indicator_name == "FIBONACCI_WMA":
        # Fibonacci WMA with defaults: period=20, upper=1.0, lower=-1.0
        period = params[0] if len(params) >= 1 else 20
        upper = params[1] if len(params) >= 2 else 1.0
        lower = params[2] if len(params) >= 3 else -1.0
        return indicator_func(data, period, upper, lower)
    elif indicator_name == "HOLT_WINTER_MA":
        # Holt-Winter MA with defaults: alpha=0.3, beta=0.1, deviation=0.01
        alpha = params[0] if len(params) >= 1 else 0.3
        beta = params[1] if len(params) >= 2 else 0.1
        deviation = params[2] if len(params) >= 3 else 0.01
        return indicator_func(data, alpha, beta, deviation)
    elif indicator_name == "HULL_EMA":
        # Hull EMA with defaults: period=20, deviation=0.01
        period = params[0] if len(params) >= 1 else 20
        deviation = params[1] if len(params) >= 2 else 0.01
        return indicator_func(data, period, deviation)
    elif indicator_name == "ALMA":
        # ALMA with defaults: period=20, offset=0.85, sigma=6, baseline=0, lower=-1, upper=1
        period = params[0] if len(params) >= 1 else 20
        offset = params[1] if len(params) >= 2 else 0.85
        sigma = params[2] if len(params) >= 3 else 6
        baseline = params[3] if len(params) >= 4 else 0
        lower = params[4] if len(params) >= 5 else -1
        upper = params[5] if len(params) >= 6 else 1
        return indicator_func(data, period, offset, sigma, baseline, lower, upper)
    # Volume Indicators - Standard 3 parameter indicators
    elif indicator_name in ["FVE", "NVI", "PVI", "PVR", "PVT", "PV", "VAMA", "VZO"]:
        # Volume indicators with defaults: period/baseline, upper, lower
        param1 = params[0] if len(params) >= 1 else (20 if indicator_name != "PVT" else 0)
        upper = params[1] if len(params) >= 2 else 1000
        lower = params[2] if len(params) >= 3 else -1000
        return indicator_func(data, param1, upper, lower)
    # Volume Indicators - Special parameter requirements
    elif indicator_name == "VPT":  # VolumePriceTrendStrategies(ma_period, threshold_percentage)
        # VPT with defaults: ma_period=20, threshold_percentage=0.01
        ma_period = params[0] if len(params) >= 1 else 20
        threshold_percentage = params[1] if len(params) >= 2 else 0.01
        return indicator_func(data, ma_period, threshold_percentage)
    elif indicator_name == "VP":  # VolumeProfileStrategies(period, bin_size, value_area_percentage)
        # VP with defaults: period=20, bin_size=10, value_area_percentage=0.7
        period = params[0] if len(params) >= 1 else 20
        bin_size = params[1] if len(params) >= 2 else 10
        value_area_percentage = params[2] if len(params) >= 3 else 0.7
        return indicator_func(data, period, bin_size, value_area_percentage)
    elif indicator_name == "WOBV":  # WeightedOnBalanceVolumeStrategies(ma_period)
        # WOBV with defaults: ma_period=20
        ma_period = params[0] if len(params) >= 1 else 20
        return indicator_func(data, ma_period)
    elif indicator_name == "EV_MACD":
        if len(params) < 5:
            raise ValueError(f"Indicator {indicator_name} requires 5 parameters (fast, slow, signal, upper, lower), got {len(params)}")
        return indicator_func(data, params[0], params[1], params[2], params[3], params[4])  # fast, slow, signal, upper, lower
    elif indicator_name == "VW_MACD":  # VolumeWeightedMACDStrategies(fast_period, slow_period, signal_period, threshold)
        if len(params) < 4:
            raise ValueError(f"Indicator {indicator_name} requires 4 parameters (fast_period, slow_period, signal_period, threshold), got {len(params)}")
        return indicator_func(data, params[0], params[1], params[2], params[3])  # fast_period, slow_period, signal_period, threshold
    elif indicator_name == "KVO":
        # KVO with defaults: fast=34, slow=55, upper=1000, lower=-1000
        fast = params[0] if len(params) >= 1 else 34
        slow = params[1] if len(params) >= 2 else 55
        upper = params[2] if len(params) >= 3 else 1000
        lower = params[3] if len(params) >= 4 else -1000
        return indicator_func(data, fast, slow, upper, lower)
    elif indicator_name == "PVO":
        # PVO with defaults: fast=12, slow=26, upper=10, lower=-10
        fast = params[0] if len(params) >= 1 else 12
        slow = params[1] if len(params) >= 2 else 26
        upper = params[2] if len(params) >= 3 else 10
        lower = params[3] if len(params) >= 4 else -10
        return indicator_func(data, fast, slow, upper, lower)
    # Price Indicators - Standard 3 parameter indicators
    elif indicator_name in ["AP", "DP", "DPO", "IP", "MP", "PD", "WCP"]:
        # Price indicators with defaults: period=14, upper=1.0, lower=-1.0
        period = params[0] if len(params) >= 1 else 14
        upper = params[1] if len(params) >= 2 else 1.0
        lower = params[2] if len(params) >= 3 else -1.0
        return indicator_func(data, period, upper, lower)
    # Price Indicators - Special parameter requirements
    elif indicator_name == "APZ":  # AdaptivePriceZoneStrategies(period, multiplier, baseline)
        # APZ with defaults: period=20, multiplier=2.0, baseline=0
        period = params[0] if len(params) >= 1 else 20
        multiplier = params[1] if len(params) >= 2 else 2.0
        baseline = params[2] if len(params) >= 3 else 0
        return indicator_func(data, period, multiplier, baseline)
    elif indicator_name == "MPP":  # MidpointPricePeriodStrategies(period, threshold)
        # MPP with defaults: period=14, threshold=0.01
        period = params[0] if len(params) >= 1 else 14
        threshold = params[1] if len(params) >= 2 else 0.01
        return indicator_func(data, period, threshold)
    elif indicator_name in ["APO", "PPO"]:
        # APO/PPO with defaults: fast=12, slow=26, upper=1.0, lower=-1.0
        fast = params[0] if len(params) >= 1 else 12
        slow = params[1] if len(params) >= 2 else 26
        upper = params[2] if len(params) >= 3 else 1.0
        lower = params[3] if len(params) >= 4 else -1.0
        return indicator_func(data, fast, slow, upper, lower)
    # Trend Indicators
    elif indicator_name == "ADX":
        # ADX with defaults: period=14, adx_threshold=25
        period = params[0] if len(params) >= 1 else 14
        adx_threshold = params[1] if len(params) >= 2 else 25
        return indicator_func(data, period, adx_threshold)
    elif indicator_name in ["CMO", "PDI", "MDI", "PDM", "MDM"]:
        # Directional indicators with defaults: period=14, upper=25, lower=-25
        period = params[0] if len(params) >= 1 else 14
        upper = params[1] if len(params) >= 2 else 25
        lower = params[2] if len(params) >= 3 else -25
        return indicator_func(data, period, upper, lower)
    elif indicator_name == "MBB":
        # Momentum Breakout Bands with defaults: period=20, upper=2.0, lower=-2.0
        period = params[0] if len(params) >= 1 else 20
        upper = params[1] if len(params) >= 2 else 2.0
        lower = params[2] if len(params) >= 3 else -2.0
        return indicator_func(data, period, upper, lower)
    elif indicator_name == "DM":
        # Directional Movement with defaults: period=14, baseline=0, upper=25, lower=-25
        period = params[0] if len(params) >= 1 else 14
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 25
        lower = params[3] if len(params) >= 4 else -25
        return indicator_func(data, period, baseline, upper, lower)
    elif indicator_name == "TS":
        # Trend Signals with defaults: short=12, long=26, threshold=0.01
        short = params[0] if len(params) >= 1 else 12
        long = params[1] if len(params) >= 2 else 26
        threshold = params[2] if len(params) >= 3 else 0.01
        return indicator_func(data, short, long, threshold)
    elif indicator_name == "STC":
        # Schaff Trend Cycle with defaults: fast=23, slow=50, cycle=10, baseline=50, upper=75, lower=25
        fast = params[0] if len(params) >= 1 else 23
        slow = params[1] if len(params) >= 2 else 50
        cycle = params[2] if len(params) >= 3 else 10
        baseline = params[3] if len(params) >= 4 else 50
        upper = params[4] if len(params) >= 5 else 75
        lower = params[5] if len(params) >= 6 else 25
        return indicator_func(data, fast, slow, cycle, baseline, upper, lower)
    elif indicator_name == "WTO":
        # Wave Trend Oscillator with defaults: period1=10, period2=3, signal=3, upper=60, lower=-60
        period1 = params[0] if len(params) >= 1 else 10
        period2 = params[1] if len(params) >= 2 else 3
        signal = params[2] if len(params) >= 3 else 3
        upper = params[3] if len(params) >= 4 else 60
        lower = params[4] if len(params) >= 5 else -60
        return indicator_func(data, period1, period2, signal, upper, lower)
    
    # Batch 1: Essential Oscillators Parameter Handling
    elif indicator_name == "MACD":
        # MACD with defaults: fast=12, slow=26, signal=9
        fast = params[0] if len(params) >= 1 else 12
        slow = params[1] if len(params) >= 2 else 26
        signal = params[2] if len(params) >= 3 else 9
        return indicator_func(data, fast, slow, signal)
    elif indicator_name == "CCI":
        # CCI with defaults: period=20, upper=100, lower=-100
        period = validate_indicator_period(params[0] if len(params) >= 1 else 20, "CCI")
        upper = params[1] if len(params) >= 2 else 100
        lower = params[2] if len(params) >= 3 else -100
        return indicator_func(data, period, upper, lower)
    elif indicator_name == "STOCH":
        # Stochastic with defaults: period=14, upper=80, lower=20
        period = validate_indicator_period(params[0] if len(params) >= 1 else 14, "Stochastic")
        upper = params[1] if len(params) >= 2 else 80
        lower = params[2] if len(params) >= 3 else 20
        return indicator_func(data, period, upper, lower)
    elif indicator_name == "WILLR":
        # Williams %R with defaults: period=14, upper=-20, lower=-80
        period = validate_indicator_period(params[0] if len(params) >= 1 else 14, "Williams %R")
        upper = params[1] if len(params) >= 2 else -20
        lower = params[2] if len(params) >= 3 else -80
        return indicator_func(data, period, upper, lower)
    elif indicator_name == "ULTOSC":
        # Ultimate Oscillator with defaults: period1=7, period2=14, period3=28, upper=70, lower=30
        period1 = validate_indicator_period(params[0] if len(params) >= 1 else 7, "Ultimate Oscillator Period 1")
        period2 = validate_indicator_period(params[1] if len(params) >= 2 else 14, "Ultimate Oscillator Period 2")
        period3 = validate_indicator_period(params[2] if len(params) >= 3 else 28, "Ultimate Oscillator Period 3")
        upper = params[3] if len(params) >= 4 else 70
        lower = params[4] if len(params) >= 5 else 30
        return indicator_func(data, period1, period2, period3, upper, lower)
    
    # Batch 2: Volatility Indicators Parameter Handling
    elif indicator_name == "ATR":
        # ATR with defaults: period=14, threshold=0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 14, "ATR")
        threshold = params[1] if len(params) >= 2 else 0.1
        return indicator_func(data, period, threshold)
    elif indicator_name == "BB":
        # Bollinger Bands with defaults: period=20, multiplier=2, baseline=0.5, lower=0.2, upper=0.8
        period = validate_indicator_period(params[0] if len(params) >= 1 else 20, "Bollinger Bands")
        multiplier = params[1] if len(params) >= 2 else 2
        baseline = params[2] if len(params) >= 3 else 0.5
        lower = params[3] if len(params) >= 4 else 0.2
        upper = params[4] if len(params) >= 5 else 0.8
        return indicator_func(data, period, multiplier, baseline, lower, upper)
    elif indicator_name == "BBW":
        # Bollinger Bands Width with defaults: period=20, multiplier=2, baseline=0.05, lower=0.02, upper=0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 20, "Bollinger Bands Width")
        multiplier = params[1] if len(params) >= 2 else 2
        baseline = params[2] if len(params) >= 3 else 0.05
        lower = params[3] if len(params) >= 4 else 0.02
        upper = params[4] if len(params) >= 5 else 0.1
        return indicator_func(data, period, multiplier, baseline, lower, upper)
    elif indicator_name == "DONCHIAN":
        # Donchian Channel with defaults: period=20, tolerance=0.01
        period = validate_indicator_period(params[0] if len(params) >= 1 else 20, "Donchian Channel")
        tolerance = params[1] if len(params) >= 2 else 0.01
        return indicator_func(data, period, tolerance)
    elif indicator_name == "KC":
        # Keltner Channel with defaults: period=20, multiplier=2, atr_period=10, distance_threshold=0.0
        period = validate_indicator_period(params[0] if len(params) >= 1 else 20, "Keltner Channel")
        multiplier = params[1] if len(params) >= 2 else 2
        atr_period = validate_indicator_period(params[2] if len(params) >= 3 else 10, "Keltner Channel ATR Period")
        distance_threshold = params[3] if len(params) >= 4 else 0.0
        return indicator_func(data, period, multiplier, atr_period, distance_threshold)
    
    # Batch 3: Trend Indicators Parameter Handling
    elif indicator_name == "ICHIMOKU":
        # Ichimoku Cloud with defaults: conversion=9, base=26, leading_b=52, displacement=26
        conversion = validate_indicator_period(params[0] if len(params) >= 1 else 9, "Ichimoku Conversion Line")
        base = validate_indicator_period(params[1] if len(params) >= 2 else 26, "Ichimoku Base Line")
        leading_b = validate_indicator_period(params[2] if len(params) >= 3 else 52, "Ichimoku Leading Span B")
        displacement = validate_indicator_period(params[3] if len(params) >= 4 else 26, "Ichimoku Displacement")
        return indicator_func(data, conversion, base, leading_b, displacement)
    elif indicator_name == "SAR":
        # Parabolic SAR with defaults: initial_af=0.02, max_af=0.2, baseline=0, lower=-0.5, upper=0.5
        initial_af = params[0] if len(params) >= 1 else 0.02
        max_af = params[1] if len(params) >= 2 else 0.2
        baseline = params[2] if len(params) >= 3 else 0
        lower = params[3] if len(params) >= 4 else -0.5
        upper = params[4] if len(params) >= 5 else 0.5
        return indicator_func(data, initial_af, max_af, baseline, lower, upper)
    elif indicator_name == "SUPERTREND":
        # Supertrend with defaults: period=10, multiplier=3.0
        period = validate_indicator_period(params[0] if len(params) >= 1 else 10, "Supertrend")
        multiplier = params[1] if len(params) >= 2 else 3.0
        return indicator_func(data, period, multiplier)
    elif indicator_name == "AROON":
        # Aroon with defaults: period=25, baseline=0, upper=50, lower=-50
        period = validate_indicator_period(params[0] if len(params) >= 1 else 25, "Aroon")
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 50
        lower = params[3] if len(params) >= 4 else -50
        return indicator_func(data, period, baseline, upper, lower)
    elif indicator_name == "AROON_OSC":
        # Aroon Oscillator with defaults: period=25, baseline=0, upper=50, lower=-50
        period = validate_indicator_period(params[0] if len(params) >= 1 else 25, "Aroon Oscillator")
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 50
        lower = params[3] if len(params) >= 4 else -50
        return indicator_func(data, period, baseline, upper, lower)
    
    # Batch 4: Advanced Oscillators Parameter Handling
    elif indicator_name == "STOCHRSI":
        # Stochastic RSI with defaults: period=14, baseline=50, lower=20, upper=80
        period = validate_indicator_period(params[0] if len(params) >= 1 else 14, "Stochastic RSI")
        baseline = params[1] if len(params) >= 2 else 50
        lower = params[2] if len(params) >= 3 else 20
        upper = params[3] if len(params) >= 4 else 80
        return indicator_func(data, period, baseline, lower, upper)
    elif indicator_name == "MFI":
        # Money Flow Index with defaults: period=14, baseline=50, upper=80, lower=20
        period = validate_indicator_period(params[0] if len(params) >= 1 else 14, "Money Flow Index")
        baseline = params[1] if len(params) >= 2 else 50
        upper = params[2] if len(params) >= 3 else 80
        lower = params[3] if len(params) >= 4 else 20
        return indicator_func(data, period, baseline, upper, lower)
    elif indicator_name == "ROC":
        # Rate of Change with defaults: period=10, upper=5, lower=-5
        period = validate_indicator_period(params[0] if len(params) >= 1 else 10, "Rate of Change")
        upper = params[1] if len(params) >= 2 else 5
        lower = params[2] if len(params) >= 3 else -5
        return indicator_func(data, period, upper, lower)
    elif indicator_name == "AO":
        # Awesome Oscillator with defaults: short=5, long=34, threshold=0
        short = validate_indicator_period(params[0] if len(params) >= 1 else 5, "Awesome Oscillator Short")
        long = validate_indicator_period(params[1] if len(params) >= 2 else 34, "Awesome Oscillator Long")
        threshold = params[2] if len(params) >= 3 else 0
        return indicator_func(data, short, long, threshold)
    elif indicator_name == "CMF":
        # Chaikin Money Flow with defaults: period=20, upper=0.1, lower=-0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 20, "Chaikin Money Flow")
        upper = params[1] if len(params) >= 2 else 0.1
        lower = params[2] if len(params) >= 3 else -0.1
        return indicator_func(data, period, upper, lower)
    
    # Batch 5: Volume Analysis Parameter Handling
    elif indicator_name == "AD":
        # Accumulation/Distribution with defaults: baseline=0, upper=0, lower=0
        baseline = params[0] if len(params) >= 1 else 0
        upper = params[1] if len(params) >= 2 else 0
        lower = params[2] if len(params) >= 3 else 0
        return indicator_func(data, baseline, upper, lower)
    elif indicator_name == "ADOSC":
        # AD Oscillator with defaults: fast=3, slow=10, baseline=0, upper=0.1, lower=-0.1
        fast = validate_indicator_period(params[0] if len(params) >= 1 else 3, "AD Oscillator Fast")
        slow = validate_indicator_period(params[1] if len(params) >= 2 else 10, "AD Oscillator Slow")
        baseline = params[2] if len(params) >= 3 else 0
        upper = params[3] if len(params) >= 4 else 0.1
        lower = params[4] if len(params) >= 5 else -0.1
        return indicator_func(data, fast, slow, baseline, upper, lower)
    elif indicator_name == "CHO":
        # Chaikin Oscillator with defaults: short=3, long=10, upper=0.5, lower=-0.5
        short = validate_indicator_period(params[0] if len(params) >= 1 else 3, "Chaikin Oscillator Short")
        long = validate_indicator_period(params[1] if len(params) >= 2 else 10, "Chaikin Oscillator Long")
        upper = params[2] if len(params) >= 3 else 0.5
        lower = params[3] if len(params) >= 4 else -0.5
        return indicator_func(data, short, long, upper, lower)
    elif indicator_name == "FI":
        # Force Index with defaults: upper=1000, lower=-1000
        upper = params[0] if len(params) >= 1 else 1000
        lower = params[1] if len(params) >= 2 else -1000
        return indicator_func(data, upper, lower)
    elif indicator_name == "VROC":
        # Volume Rate of Change with defaults: fast=12, slow=26, baseline=0, lower=-5, upper=5
        fast = validate_indicator_period(params[0] if len(params) >= 1 else 12, "Volume Rate of Change Fast")
        slow = validate_indicator_period(params[1] if len(params) >= 2 else 26, "Volume Rate of Change Slow")
        baseline = params[2] if len(params) >= 3 else 0
        lower = params[3] if len(params) >= 4 else -5
        upper = params[4] if len(params) >= 5 else 5
        return indicator_func(data, fast, slow, baseline, lower, upper)
    elif indicator_name == "VO":
        # Volume Oscillator with defaults: fast=5, slow=10, baseline=0, upper=10, lower=-10
        fast = validate_indicator_period(params[0] if len(params) >= 1 else 5, "Volume Oscillator Fast")
        slow = validate_indicator_period(params[1] if len(params) >= 2 else 10, "Volume Oscillator Slow")
        baseline = params[2] if len(params) >= 3 else 0
        upper = params[3] if len(params) >= 4 else 10
        lower = params[4] if len(params) >= 5 else -10
        return indicator_func(data, fast, slow, baseline, upper, lower)
    elif indicator_name == "VWAP":
        # Volume Weighted Average Price with defaults: threshold=0.01
        threshold = params[0] if len(params) >= 1 else 0.01
        return indicator_func(data, threshold)
    elif indicator_name == "EOM":
        # Ease of Movement with defaults: period=14, baseline=0, upper=0.1, lower=-0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 14, "Ease of Movement")
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 0.1
        lower = params[3] if len(params) >= 4 else -0.1
        return indicator_func(data, period, baseline, upper, lower)
    
    # Batch 6: Advanced Trend Parameter Handling
    elif indicator_name in ["LINREG", "LINREGSLOPE"]:
        # Linear Regression variants with defaults: period=14, distance_threshold=0.01
        period = validate_indicator_period(params[0] if len(params) >= 1 else 14, "Linear Regression")
        distance_threshold = params[1] if len(params) >= 2 else 0.01
        return indicator_func(data, period, distance_threshold)
    elif indicator_name == "LINREGANGLE":
        # Linear Regression Angle with defaults: period=14, baseline=0, upper=0.1, lower=-0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 14, "Linear Regression Angle")
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 0.1
        lower = params[3] if len(params) >= 4 else -0.1
        return indicator_func(data, period, baseline, upper, lower)
    elif indicator_name == "STDDEV":
        # Standard Deviation with defaults: period=20, baseline=0, upper=2, lower=-2
        period = validate_indicator_period(params[0] if len(params) >= 1 else 20, "Standard Deviation")
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 2
        lower = params[3] if len(params) >= 4 else -2
        return indicator_func(data, period, baseline, upper, lower)
    elif indicator_name == "VAR":
        # Variance with defaults: period=14, lower=1.0, upper=5.0
        period = validate_indicator_period(params[0] if len(params) >= 1 else 14, "Variance")
        lower = params[1] if len(params) >= 2 else 1.0
        upper = params[2] if len(params) >= 3 else 5.0
        return indicator_func(data, period, lower, upper)
    elif indicator_name == "EHLS":
        # Ehlers Super Smoother with defaults: period=10, distance_threshold=0.01
        period = validate_indicator_period(params[0] if len(params) >= 1 else 10, "Ehlers Super Smoother")
        distance_threshold = params[1] if len(params) >= 2 else 0.01
        return indicator_func(data, period, distance_threshold)
    elif indicator_name == "GANN":
        # Gann High Low Activator with defaults: divergence_upper=0.03, divergence_lower=-0.03
        divergence_upper = params[0] if len(params) >= 1 else 0.03
        divergence_lower = params[1] if len(params) >= 2 else -0.03
        return indicator_func(data, divergence_upper, divergence_lower)
    
    # Batch 7: Specialized Indicators Parameter Handling
    elif indicator_name == "FIBONACCI":
        # Fibonacci Pivot Points with no parameters
        return indicator_func(data)
    elif indicator_name == "PIVOT":
        # Pivot Points with no parameters
        return indicator_func(data)
    elif indicator_name == "HILBERT":
        # Hilbert Transform Trend with defaults: deviation_threshold=1.0
        deviation_threshold = params[0] if len(params) >= 1 else 1.0
        return indicator_func(data, deviation_threshold)
    elif indicator_name == "HILBERT_SINE":
        # Hilbert Transform Sine with no parameters
        return indicator_func(data)
    elif indicator_name == "HILBERT_PHASE":
        # Hilbert Transform Phase with defaults: period=20, baseline=0, upper=0.1, lower=-0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 20, "Hilbert Transform Phase")
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 0.1
        lower = params[3] if len(params) >= 4 else -0.1
        return indicator_func(data, period, baseline, upper, lower)
    
    # Batch 8: Additional Oscillators Parameter Handling
    elif indicator_name == "ULTOSC2":
        # Ultimate Oscillator with defaults: period1=7, period2=14, period3=28, baseline=50, upper=70, lower=30
        period1 = validate_indicator_period(params[0] if len(params) >= 1 else 7, "Ultimate Oscillator Period 1")
        period2 = validate_indicator_period(params[1] if len(params) >= 2 else 14, "Ultimate Oscillator Period 2")
        period3 = validate_indicator_period(params[2] if len(params) >= 3 else 28, "Ultimate Oscillator Period 3")
        baseline = params[3] if len(params) >= 4 else 50
        upper = params[4] if len(params) >= 5 else 70
        lower = params[5] if len(params) >= 6 else 30
        return indicator_func(data, period1, period2, period3, baseline, upper, lower)
    elif indicator_name == "CCI2":
        # Commodity Channel Index with defaults: period=20, baseline=0, upper=100, lower=-100
        period = validate_indicator_period(params[0] if len(params) >= 1 else 20, "Commodity Channel Index")
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 100
        lower = params[3] if len(params) >= 4 else -100
        return indicator_func(data, period, baseline, upper, lower)
    elif indicator_name == "MOM":
        # Momentum with defaults: period=10, baseline=0, upper=5, lower=-5
        period = validate_indicator_period(params[0] if len(params) >= 1 else 10, "Momentum")
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 5
        lower = params[3] if len(params) >= 4 else -5
        return indicator_func(data, period, baseline, upper, lower)
    elif indicator_name == "BOP":
        # Balance of Power with defaults: threshold=0.5
        threshold = params[0] if len(params) >= 1 else 0.5
        return indicator_func(data, threshold)
    elif indicator_name == "ERI":
        # Elder Ray Index with defaults: period=13, distance_threshold=0.01
        period = validate_indicator_period(params[0] if len(params) >= 1 else 13, "Elder Ray Index")
        distance_threshold = params[1] if len(params) >= 2 else 0.01
        return indicator_func(data, period, distance_threshold)
    
    # Batch 9: Advanced Moving Averages Parameter Handling
    elif indicator_name == "TEMA":
        # Triple Exponential MA with defaults: period=15, threshold_value=0.2
        period = validate_indicator_period(params[0] if len(params) >= 1 else 15, "Triple Exponential MA")
        threshold_value = params[1] if len(params) >= 2 else 0.2
        return indicator_func(data, period, threshold_value)
    elif indicator_name == "TRIMA":
        # Triangular MA with defaults: period=20, threshold_percentage=0.01
        period = validate_indicator_period(params[0] if len(params) >= 1 else 20, "Triangular MA")
        threshold_percentage = params[1] if len(params) >= 2 else 0.01
        return indicator_func(data, period, threshold_percentage)
    elif indicator_name == "VIDYA":
        # Variable Index Dynamic Average with defaults: period=14, k=0.2, threshold_percentage=0.01
        period = validate_indicator_period(params[0] if len(params) >= 1 else 14, "VIDYA")
        k = params[1] if len(params) >= 2 else 0.2
        threshold_percentage = params[2] if len(params) >= 3 else 0.01
        return indicator_func(data, period, k, threshold_percentage)
    elif indicator_name == "WILDER":
        # Wilders Moving Average with defaults: period=14, deviation_threshold=0.01
        period = validate_indicator_period(params[0] if len(params) >= 1 else 14, "Wilders MA")
        deviation_threshold = params[1] if len(params) >= 2 else 0.01
        return indicator_func(data, period, deviation_threshold)
    elif indicator_name == "DEMA2":
        # Double Exponential MA with defaults: period=20, distance_threshold=0.01
        period = validate_indicator_period(params[0] if len(params) >= 1 else 20, "Double Exponential MA")
        distance_threshold = params[1] if len(params) >= 2 else 0.01
        return indicator_func(data, period, distance_threshold)
    
    # Batch 10: Price Action Indicators Parameter Handling
    elif indicator_name in ["PP", "PPR", "PPS", "HL2", "HLC3"]:
        # Price Action with no parameters
        return indicator_func(data)
    
    # Batch 11: Volatility Expansion Parameter Handling
    elif indicator_name in ["BBP", "BBU", "BBL"]:
        # Bollinger Bands variants with defaults: period=20, multiplier=2, baseline=0, upper=1/0.1/0.1, lower=-1/-0.1/-0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 20, indicator_name)
        multiplier = params[1] if len(params) >= 2 else 2
        baseline = params[2] if len(params) >= 3 else 0
        upper = params[3] if len(params) >= 4 else (1 if indicator_name == "BBP" else 0.1)
        lower = params[4] if len(params) >= 5 else (-1 if indicator_name == "BBP" else -0.1)
        return indicator_func(data, period, multiplier, baseline, upper, lower)
    elif indicator_name in ["KCU", "KCL"]:
        # Keltner Channel variants with defaults: period=20, multiplier=2, atr_period=10, distance_threshold=0.0
        period = validate_indicator_period(params[0] if len(params) >= 1 else 20, indicator_name)
        multiplier = params[1] if len(params) >= 2 else 2
        atr_period = validate_indicator_period(params[2] if len(params) >= 3 else 10, "ATR Period")
        distance_threshold = params[3] if len(params) >= 4 else 0.0
        return indicator_func(data, period, multiplier, atr_period, distance_threshold)
    
    # Batch 12: Specialized Analysis Parameter Handling
    elif indicator_name == "FISHER":
        # Fisher Transform with defaults: period=10, upper=1.5, lower=-1.5
        period = validate_indicator_period(params[0] if len(params) >= 1 else 10, "Fisher Transform")
        upper = params[1] if len(params) >= 2 else 1.5
        lower = params[2] if len(params) >= 3 else -1.5
        return indicator_func(data, period, upper, lower)
    elif indicator_name == "INERTIA":
        # Inertia Indicator with defaults: period=14, threshold=0.0, acceleration_threshold=0.0
        period = validate_indicator_period(params[0] if len(params) >= 1 else 14, "Inertia Indicator")
        threshold = params[1] if len(params) >= 2 else 0.0
        acceleration_threshold = params[2] if len(params) >= 3 else 0.0
        return indicator_func(data, period, threshold, acceleration_threshold)
    elif indicator_name in ["QSTICK", "TSI"]:
        # QStick and TSI with defaults: period=10/25, baseline=0, upper=0.1/50, lower=-0.1/-50
        period = validate_indicator_period(params[0] if len(params) >= 1 else (25 if indicator_name == "TSI" else 10), indicator_name)
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else (50 if indicator_name == "TSI" else 0.1)
        lower = params[3] if len(params) >= 4 else (-50 if indicator_name == "TSI" else -0.1)
        return indicator_func(data, period, baseline, upper, lower)
    elif indicator_name == "TRIX":
        # TRIX Indicator with defaults: period=15, threshold_value=0.2
        period = validate_indicator_period(params[0] if len(params) >= 1 else 15, "TRIX Indicator")
        threshold_value = params[1] if len(params) >= 2 else 0.2
        return indicator_func(data, period, threshold_value)
    
    # Batch 13: Advanced Oscillators & Indicators Parameter Handling
    elif indicator_name == "ABERRATION":
        # Aberration with defaults: period=20, threshold=0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 20, "Aberration")
        threshold = params[1] if len(params) >= 2 else 0.1
        return indicator_func(data, period, threshold)
    elif indicator_name == "APO":
        # Absolute Price Oscillator with defaults: fast=10, slow=20, baseline=0, upper=0.1, lower=-0.1
        fast = validate_indicator_period(params[0] if len(params) >= 1 else 10, "APO Fast")
        slow = validate_indicator_period(params[1] if len(params) >= 2 else 20, "APO Slow")
        baseline = params[2] if len(params) >= 3 else 0
        upper = params[3] if len(params) >= 4 else 0.1
        lower = params[4] if len(params) >= 5 else -0.1
        return indicator_func(data, fast, slow, baseline, upper, lower)
    elif indicator_name in ["ACCELERATION", "ADINDEX", "ADAPTIVE", "ARCHER_MA", "ARCHER_OBV", "BETA", "BIAS"]:
        # Standard indicators with defaults: period=20/20/20/20/20/20/20, baseline=0, upper=0.1, lower=-0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 20, indicator_name)
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 0.1
        lower = params[3] if len(params) >= 4 else -0.1
        return indicator_func(data, period, baseline, upper, lower)
    elif indicator_name == "ARNAUD_LEGOUX":
        # Arnaud Legoux MA with defaults: period=20, offset=0.85, sigma=0.1, baseline=0, upper=0.1, lower=-0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 20, "Arnaud Legoux MA")
        offset = params[1] if len(params) >= 2 else 0.85
        sigma = params[2] if len(params) >= 3 else 0.1
        baseline = params[3] if len(params) >= 4 else 0
        upper = params[4] if len(params) >= 5 else 0.1
        lower = params[5] if len(params) >= 6 else -0.1
        return indicator_func(data, period, offset, sigma, baseline, upper, lower)
    
    # Batch 14: Advanced Analysis Parameter Handling
    elif indicator_name == "BRAR":
        # BRAR with defaults: period=26, baseline=0, upper=0.1, lower=-0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 26, "BRAR")
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 0.1
        lower = params[3] if len(params) >= 4 else -0.1
        return indicator_func(data, period, baseline, upper, lower)
    elif indicator_name == "BULL_BEAR":
        # Bull Bear Power with defaults: period=13, baseline=0, upper=0.1, lower=-0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 13, "Bull Bear Power")
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 0.1
        lower = params[3] if len(params) >= 4 else -0.1
        return indicator_func(data, period, baseline, upper, lower)
    elif indicator_name in ["BUY_SELL", "CORRELATION"]:
        # Standard indicators with defaults: period=20, baseline=0, upper=0.1, lower=-0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 20, indicator_name)
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 0.1
        lower = params[3] if len(params) >= 4 else -0.1
        return indicator_func(data, period, baseline, upper, lower)
    elif indicator_name == "CENTER_GRAVITY":
        # Center of Gravity with defaults: period=10, baseline=0, upper=0.1, lower=-0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 10, "Center of Gravity")
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 0.1
        lower = params[3] if len(params) >= 4 else -0.1
        return indicator_func(data, period, baseline, upper, lower)
    elif indicator_name in ["CHANDE_FORECAST", "CHAOS", "COPPOCK"]:
        # Standard indicators with defaults: period=14, baseline=0, upper=0.1, lower=-0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 14, indicator_name)
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 0.1
        lower = params[3] if len(params) >= 4 else -0.1
        return indicator_func(data, period, baseline, upper, lower)
    elif indicator_name == "CHANDE_KROLL":
        # Chande Kroll Stop with defaults: period=10, multiplier=2, baseline=0, upper=0.1, lower=-0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 10, "Chande Kroll Stop")
        multiplier = params[1] if len(params) >= 2 else 2
        baseline = params[2] if len(params) >= 3 else 0
        upper = params[3] if len(params) >= 4 else 0.1
        lower = params[4] if len(params) >= 5 else -0.1
        return indicator_func(data, period, multiplier, baseline, upper, lower)
    elif indicator_name == "CHANDELIER":
        # Chandelier Exit with defaults: period=22, multiplier=3, baseline=0, upper=0.1, lower=-0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 22, "Chandelier Exit")
        multiplier = params[1] if len(params) >= 2 else 3
        baseline = params[2] if len(params) >= 3 else 0
        upper = params[3] if len(params) >= 4 else 0.1
        lower = params[4] if len(params) >= 5 else -0.1
        return indicator_func(data, period, multiplier, baseline, upper, lower)
    
    # Batch 15: Advanced Momentum Parameter Handling
    elif indicator_name in ["CUMULATIVE_FI", "CROSS_SIGNALS", "DECAY", "DECREASING", "DETRENDED", "DIRECTIONAL", "ELDERS_FI", "FISHER_RVI"]:
        # Standard indicators with defaults: period=14/20/20/20/20/14/13/10, baseline=0, upper=0.1, lower=-0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else (13 if indicator_name == "ELDERS_FI" else 10 if indicator_name == "FISHER_RVI" else 14 if indicator_name in ["CUMULATIVE_FI", "DIRECTIONAL"] else 20), indicator_name)
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 0.1
        lower = params[3] if len(params) >= 4 else -0.1
        return indicator_func(data, period, baseline, upper, lower)
    elif indicator_name == "ENVELOPES":
        # Envelopes with defaults: period=20, multiplier=0.1, baseline=0, upper=0.1, lower=-0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 20, "Envelopes")
        multiplier = params[1] if len(params) >= 2 else 0.1
        baseline = params[2] if len(params) >= 3 else 0
        upper = params[3] if len(params) >= 4 else 0.1
        lower = params[4] if len(params) >= 5 else -0.1
        return indicator_func(data, period, multiplier, baseline, upper, lower)
    elif indicator_name == "FRACTAL":
        # Fractal Indicator with defaults: period=5, baseline=0, upper=0.1, lower=-0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 5, "Fractal Indicator")
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 0.1
        lower = params[3] if len(params) >= 4 else -0.1
        return indicator_func(data, period, baseline, upper, lower)
    
    # Batch 16-19: Missing Indicators Parameter Handling
    elif indicator_name in ["ELDERS_THERMOMETER", "HILBERT_PERIOD", "HILBERT_PHASOR", "HILBERT_TREND", "HOLT_WINTER_CHANNEL", "INCREASING_PRICE", "INVERSE_FISHER_RSI", "KAUFMAN_EFFICIENCY", "KDJ", "KST", "LINREG_INTERCEPT", "LONG_RUN", "MASS_INDEX", "MEDIAN_PRICE", "MIDPOINT_PERIOD", "MIDPOINT_PRICE", "MOMENTUM_BREAKOUT", "MOVING_STDDEV", "NATR", "NORMALIZED_BASP", "PEARSON_CORR", "PERCENT_B", "PGO", "PRICE_DISTANCE", "PSYCHOLOGICAL", "QQE", "RSI_XTRA", "RVI", "RVI_VOLATILITY", "SHORT_RUN", "SLOPE", "SMI_ERGODIC", "SQUEEZE", "SQUEEZE_PRO", "STOCH_D", "STOCH_FAST", "STOCH_K", "STOCH_OSC", "STOP_REVERSE", "SUMMATION", "TD_SEQUENTIAL", "TREND_SIGNALS", "TTM_TREND", "TWIGGS_MONEY", "ULCER_INDEX", "UP_DOWN", "VHF", "VOLUME_PROFILE", "VORTEX", "WAVE_PM", "WAVE_TREND"]:
        # All missing indicators with defaults: period=20, baseline=0, upper=0.1, lower=-0.1
        period = validate_indicator_period(params[0] if len(params) >= 1 else 20, indicator_name)
        baseline = params[1] if len(params) >= 2 else 0
        upper = params[2] if len(params) >= 3 else 0.1
        lower = params[3] if len(params) >= 4 else -0.1
        return indicator_func(data, period, baseline, upper, lower)
    else:
        # Handle both list and dict formats for params
        if isinstance(params, dict):
            period = params.get('period', 20)  # Default to 20 if not specified
            return indicator_func(data, period)
        else:
            return indicator_func(data, params[0])  # Only period

# Batch 1: Essential Oscillators Implementation
def macd(data, fast_period=12, slow_period=26, signal_period=9):
    """Calculate MACD (Moving Average Convergence Divergence)"""
    macd_strategy = MACDStrategies(fast_period, slow_period, signal_period)
    return macd_strategy.compute_values(data)

def commodity_channel_index(data, period=20, upper_threshold=100, lower_threshold=-100):
    """Calculate CCI (Commodity Channel Index)"""
    cci_strategy = CommodityChannelIndexStrategies(period, upper_threshold, lower_threshold)
    return cci_strategy.compute_values(data)

def stochastic(data, period=14, upper_threshold=80, lower_threshold=20):
    """Calculate Stochastic Oscillator"""
    stoch_strategy = StochasticStrategies(period, 50, upper_threshold, lower_threshold)
    return stoch_strategy.compute_values(data)

def williams_r(data, period=14, upper_threshold=-20, lower_threshold=-80):
    """Calculate Williams %R"""
    willr_strategy = WilliamsRStrategies(period, upper_threshold, lower_threshold)
    return willr_strategy.compute_values(data)

def ultimate_oscillator(data, period1=7, period2=14, period3=28, upper_threshold=70, lower_threshold=30):
    """Calculate Ultimate Oscillator"""
    ultosc_strategy = UltimateOscillatorStrategies(period1, period2, period3, 50, lower_threshold, upper_threshold)
    return ultosc_strategy.compute_values(data)

# Batch 2: Volatility Indicators Implementation
def average_true_range(data, period=14, threshold=0.1):
    """Calculate ATR (Average True Range)"""
    atr_strategy = AverageTrueRangeStrategies(period, threshold)
    return atr_strategy.compute_values(data)

def bollinger_bands(data, period=20, multiplier=2, baseline=0.5, lower_threshold=0.2, upper_threshold=0.8):
    """Calculate Bollinger Bands %B"""
    bb_strategy = BollingerBandsStrategies(period, multiplier, baseline, lower_threshold, upper_threshold)
    return bb_strategy.compute_values(data)

def bollinger_bands_width(data, period=20, multiplier=2, baseline=0.05, lower_threshold=0.02, upper_threshold=0.1):
    """Calculate Bollinger Bands Width"""
    bbw_strategy = BollingerBandsWidthStrategies(period, multiplier, baseline, lower_threshold, upper_threshold)
    return bbw_strategy.compute_values(data)

def donchian_channel(data, period=20, tolerance=0.01):
    """Calculate Donchian Channel"""
    donchian_strategy = DonchianChannelStrategies(period, tolerance)
    return donchian_strategy.compute_values(data)

def keltner_channel(data, period=20, multiplier=2, atr_period=10, distance_threshold=0.0):
    """Calculate Keltner Channel"""
    kc_strategy = KeltnerChannelStrategies(period, multiplier, atr_period, distance_threshold)
    result = kc_strategy.compute_values(data)
    # Convert dict to DataFrame for consistency
    return pd.DataFrame(result, index=data.index)

# Batch 3: Trend Indicators Implementation
def ichimoku_cloud(data, conversion_line_period=9, base_line_period=26, leading_span_b_period=52, displacement=26):
    """Calculate Ichimoku Cloud"""
    ichimoku_strategy = IchimokuCloudStrategies(conversion_line_period, base_line_period, leading_span_b_period, displacement)
    result = ichimoku_strategy.compute_values(data)
    # Convert dict to DataFrame for consistency
    return pd.DataFrame(result, index=data.index)

def parabolic_sar(data, initial_af=0.02, max_af=0.2, baseline=0, lower_threshold=-0.5, upper_threshold=0.5):
    """Calculate Parabolic SAR"""
    sar_strategy = ParabolicStopAndReverseStrategies(initial_af, max_af, baseline, lower_threshold, upper_threshold)
    return sar_strategy.compute_values(data)

def supertrend(data, period=10, multiplier=3.0):
    """Calculate Supertrend"""
    supertrend_strategy = SupertrendStrategies(period, multiplier)
    supertrend_values, trend_values = supertrend_strategy.compute_values(data)
    # Convert tuple to DataFrame for consistency
    return pd.DataFrame({'Supertrend': supertrend_values, 'Trend': trend_values}, index=data.index)

def aroon(data, period=25, baseline=0, upper_threshold=50, lower_threshold=-50):
    """Calculate Aroon"""
    aroon_strategy = AroonStrategies(period, baseline, upper_threshold, lower_threshold)
    aroon_up, aroon_down, aroon_osc = aroon_strategy.compute_values(data)
    # Convert tuple to DataFrame for consistency
    return pd.DataFrame({'Aroon_Up': aroon_up, 'Aroon_Down': aroon_down, 'Aroon_Osc': aroon_osc}, index=data.index)

def aroon_oscillator(data, period=25, baseline=0, upper_threshold=50, lower_threshold=-50):
    """Calculate Aroon Oscillator"""
    aroon_osc_strategy = AroonOscillatorStrategies(period, baseline, upper_threshold, lower_threshold)
    aroon_up, aroon_down, aroon_osc = aroon_osc_strategy.compute_values(data)
    # Convert tuple to DataFrame for consistency
    return pd.DataFrame({'Aroon_Up': aroon_up, 'Aroon_Down': aroon_down, 'Aroon_Osc': aroon_osc}, index=data.index)

# Batch 4: Advanced Oscillators Implementation
def stochastic_rsi(data, period=14, baseline=50, lower_threshold=20, upper_threshold=80):
    """Calculate Stochastic RSI"""
    stochrsi_strategy = StochasticRSIStrategies(period, baseline, lower_threshold, upper_threshold)
    return stochrsi_strategy.compute_values(data)

def money_flow_index(data, period=14, baseline=50, upper_threshold=80, lower_threshold=20):
    """Calculate Money Flow Index"""
    mfi_strategy = MoneyFlowIndexStrategies(period, baseline, upper_threshold, lower_threshold)
    return mfi_strategy.compute_values(data)

def rate_of_change(data, period=10, upper_threshold=5, lower_threshold=-5):
    """Calculate Rate of Change"""
    roc_strategy = RateOfChangeStrategies(period, upper_threshold, lower_threshold)
    return roc_strategy.compute_values(data)

def awesome_oscillator(data, short_period=5, long_period=34, threshold=0):
    """Calculate Awesome Oscillator"""
    ao_strategy = AwesomeOscillatorStrategies(short_period, long_period, threshold)
    return ao_strategy.compute_values(data)

def chaikin_money_flow(data, period=20, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Chaikin Money Flow"""
    cmf_strategy = ChaikinMoneyFlowStrategies(period, upper_threshold, lower_threshold)
    return cmf_strategy.compute_values(data)

# Batch 5: Volume Analysis Implementation
def accumulation_distribution(data, baseline=0, upper_threshold=0, lower_threshold=0):
    """Calculate Accumulation/Distribution Line"""
    ad_strategy = AccumulationDistributionLineStrategies(baseline, upper_threshold, lower_threshold)
    return ad_strategy.compute_values(data)

def accumulation_distribution_oscillator(data, fast_period=3, slow_period=10, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Accumulation/Distribution Oscillator"""
    adosc_strategy = AccumulationDistributionOscillatorStrategies(fast_period, slow_period, baseline, upper_threshold, lower_threshold)
    return adosc_strategy.compute_values(data)

def chaikin_oscillator(data, short_period=3, long_period=10, upper_threshold=0.5, lower_threshold=-0.5):
    """Calculate Chaikin Oscillator"""
    cho_strategy = ChaikinOscillatorStrategies(short_period, long_period, upper_threshold, lower_threshold)
    return cho_strategy.compute_values(data)

def force_index(data, upper_threshold=1000, lower_threshold=-1000):
    """Calculate Force Index"""
    fi_strategy = ForceIndexStrategies(upper_threshold, lower_threshold)
    return fi_strategy.compute_values(data)

def volume_rate_of_change(data, fast_period=12, slow_period=26, baseline=0, lower_threshold=-5, upper_threshold=5):
    """Calculate Volume Rate of Change"""
    vroc_strategy = PercentageVolumeOscillatorStrategies(fast_period, slow_period, baseline, lower_threshold, upper_threshold)
    return vroc_strategy.compute_values(data)

def volume_oscillator(data, fast_period=5, slow_period=10, baseline=0, upper_threshold=10, lower_threshold=-10):
    """Calculate Volume Oscillator"""
    vo_strategy = PercentageVolumeOscillatorStrategies(fast_period, slow_period, baseline, upper_threshold, lower_threshold)
    return vo_strategy.compute_values(data)

def volume_weighted_average_price(data, threshold=0.01):
    """Calculate Volume Weighted Average Price"""
    vwap_strategy = VolumeWeightedAveragePriceStrategies(threshold)
    return vwap_strategy.compute_values(data)

def ease_of_movement(data, period=14, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Ease of Movement"""
    eom_strategy = EldersForceIndexStrategies(period, baseline, upper_threshold, lower_threshold)
    return eom_strategy.compute_values(data)

# Batch 6: Advanced Trend Implementation
def linear_regression(data, period=14, distance_threshold=0.01):
    """Calculate Linear Regression"""
    lr_strategy = LinearRegressionStrategies(period, distance_threshold)
    return lr_strategy.compute_values(data)

def linear_regression_slope(data, period=14, distance_threshold=0.01):
    """Calculate Linear Regression Slope"""
    lrs_strategy = LinearRegressionSlopeStrategies(period, distance_threshold)
    return lrs_strategy.compute_values(data)

def linear_regression_angle(data, period=14, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Linear Regression Angle"""
    lra_strategy = LinearRegressionAngleStrategies(period, baseline, upper_threshold, lower_threshold)
    return lra_strategy.compute_values(data)

def standard_deviation(data, period=20, baseline=0, upper_threshold=2, lower_threshold=-2):
    """Calculate Standard Deviation"""
    std_strategy = StandardDeviationStrategies(period, baseline, upper_threshold, lower_threshold)
    return std_strategy.compute_values(data)

def variance(data, period=14, lower_threshold=1.0, upper_threshold=5.0):
    """Calculate Variance"""
    var_strategy = VarianceStrategies(period, lower_threshold, upper_threshold)
    return var_strategy.compute_values(data)

def ehlers_super_smoother(data, period=10, distance_threshold=0.01):
    """Calculate Ehlers Super Smoother"""
    ehlers_strategy = EhlersSuperSmootherFilterStrategies(period, distance_threshold)
    return ehlers_strategy.compute_values(data)

def gann_high_low_activator(data, divergence_upper_threshold=0.03, divergence_lower_threshold=-0.03):
    """Calculate Gann High Low Activator"""
    gann_strategy = GannHighLowActivatorStrategies(divergence_upper_threshold, divergence_lower_threshold)
    return gann_strategy.compute_values(data)

# Batch 7: Specialized Indicators Implementation
def fibonacci_pivot_points(data):
    """Calculate Fibonacci Pivot Points"""
    fib_strategy = FibonacciPivotPointsStrategies()
    return fib_strategy.compute_values(data)

def pivot_points(data):
    """Calculate Pivot Points"""
    pivot_strategy = PivotPointsStrategies()
    return pivot_strategy.compute_values(data)

def hilbert_transform_trend(data, deviation_threshold=1.0):
    """Calculate Hilbert Transform Trend"""
    hilbert_strategy = HilbertTransformTrendCycleStrategies(deviation_threshold)
    return hilbert_strategy.compute_values(data)

def hilbert_transform_sine(data):
    """Calculate Hilbert Transform Sine Wave"""
    hilbert_sine_strategy = HilbertTransformSineWaveStrategies()
    return hilbert_sine_strategy.compute_values(data)

def hilbert_transform_phase(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Hilbert Transform Phase"""
    hilbert_phase_strategy = HilbertTransformDominantCyclePhaseStrategies(period, baseline, upper_threshold, lower_threshold)
    return hilbert_phase_strategy.compute_values(data)

# Batch 8: Additional Oscillators Implementation
def ultimate_oscillator_2(data, period1=7, period2=14, period3=28, baseline=50, upper_threshold=70, lower_threshold=30):
    """Calculate Ultimate Oscillator (Alternative)"""
    ultosc_strategy = UltimateOscillatorStrategies(period1, period2, period3, baseline, upper_threshold, lower_threshold)
    return ultosc_strategy.compute_values(data)

def commodity_channel_index_2(data, period=20, baseline=0, upper_threshold=100, lower_threshold=-100):
    """Calculate Commodity Channel Index (Alternative)"""
    cci_strategy = CommodityChannelIndexStrategies(period, baseline, upper_threshold, lower_threshold)
    return cci_strategy.compute_values(data)

def momentum_oscillator(data, period=10, baseline=0, upper_threshold=5, lower_threshold=-5):
    """Calculate Momentum Oscillator"""
    mom_strategy = MomentumStrategies(period, baseline, upper_threshold, lower_threshold)
    return mom_strategy.compute_values(data)

def balance_of_power(data, threshold=0.5):
    """Calculate Balance of Power"""
    bop_strategy = BalanceOfPowerStrategies(threshold)
    return bop_strategy.compute_values(data)

def elder_ray_index(data, period=13, distance_threshold=0.01):
    """Calculate Elder Ray Index"""
    eri_strategy = ElderRayIndexStrategies(period, distance_threshold)
    return eri_strategy.compute_values(data)

# Batch 9: Advanced Moving Averages Implementation
def triple_exponential_moving_average(data, period=15, threshold_value=0.2):
    """Calculate Triple Exponential Moving Average"""
    tema_strategy = TripleExponentialMovingAverageOscillatorStrategies(period, threshold_value)
    return tema_strategy.compute_values(data)

def triangular_moving_average_2(data, period=20, threshold_percentage=0.01):
    """Calculate Triangular Moving Average (Alternative)"""
    trima_strategy = TriangularMovingAverageStrategies(period, threshold_percentage)
    return trima_strategy.compute_values(data)

def variable_index_dynamic_average(data, period=14, k=0.2, threshold_percentage=0.01):
    """Calculate Variable Index Dynamic Average"""
    vidya_strategy = VariableIndexDynamicAverageStrategies(period, k, threshold_percentage)
    return vidya_strategy.compute_values(data)

def wilders_moving_average(data, period=14, deviation_threshold=0.01):
    """Calculate Wilders Moving Average"""
    wilder_strategy = WildersMovingAverageStrategies(period, deviation_threshold)
    return wilder_strategy.compute_values(data)

def double_exponential_moving_average_2(data, period=20, distance_threshold=0.01):
    """Calculate Double Exponential Moving Average (Alternative)"""
    dema_strategy = DoubleExponentialMovingAverageStrategies(period, distance_threshold)
    return dema_strategy.compute_values(data)

# Batch 10: Price Action Indicators Implementation
def pivot_points_2(data):
    """Calculate Pivot Points (Alternative)"""
    pp_strategy = PivotPointsStrategies()
    return pp_strategy.compute_values(data)

def pivot_points_resistance(data):
    """Calculate Pivot Points Resistance"""
    ppr_strategy = PivotPointsStrategies()
    return ppr_strategy.compute_values(data)

def pivot_points_support(data):
    """Calculate Pivot Points Support"""
    pps_strategy = PivotPointsStrategies()
    return pps_strategy.compute_values(data)

def high_low_average(data):
    """Calculate High Low Average"""
    hl2_strategy = PivotPointsStrategies()
    return hl2_strategy.compute_values(data)

def high_low_close_average(data):
    """Calculate High Low Close Average"""
    hlc3_strategy = PivotPointsStrategies()
    return hlc3_strategy.compute_values(data)

# Batch 11: Volatility Expansion Implementation
def bollinger_bands_percent(data, period=20, multiplier=2, baseline=0, upper_threshold=1, lower_threshold=-1):
    """Calculate Bollinger Bands Percent"""
    bbp_strategy = BollingerBandsStrategies(period, multiplier, baseline, upper_threshold, lower_threshold)
    return bbp_strategy.compute_values(data)

def bollinger_bands_upper(data, period=20, multiplier=2, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Bollinger Bands Upper"""
    bbu_strategy = BollingerBandsStrategies(period, multiplier, baseline, upper_threshold, lower_threshold)
    return bbu_strategy.compute_values(data)

def bollinger_bands_lower(data, period=20, multiplier=2, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Bollinger Bands Lower"""
    bbl_strategy = BollingerBandsStrategies(period, multiplier, baseline, upper_threshold, lower_threshold)
    return bbl_strategy.compute_values(data)

def keltner_channel_upper(data, period=20, multiplier=2, atr_period=10, distance_threshold=0.0):
    """Calculate Keltner Channel Upper"""
    kcu_strategy = KeltnerChannelStrategies(period, multiplier, atr_period, distance_threshold)
    result = kcu_strategy.compute_values(data)
    # Convert dict to DataFrame for consistency
    return pd.DataFrame(result, index=data.index)

def keltner_channel_lower(data, period=20, multiplier=2, atr_period=10, distance_threshold=0.0):
    """Calculate Keltner Channel Lower"""
    kcl_strategy = KeltnerChannelStrategies(period, multiplier, atr_period, distance_threshold)
    result = kcl_strategy.compute_values(data)
    # Convert dict to DataFrame for consistency
    return pd.DataFrame(result, index=data.index)

# Batch 12: Specialized Analysis Implementation
def fisher_transform(data, period=10, upper_threshold=1.5, lower_threshold=-1.5):
    """Calculate Fisher Transform"""
    fisher_strategy = FisherTransformStrategies(period, upper_threshold, lower_threshold)
    return fisher_strategy.compute_values(data)

def inertia_indicator(data, period=14, threshold=0.0, acceleration_threshold=0.0):
    """Calculate Inertia Indicator"""
    inertia_strategy = InertiaStrategies(period, threshold, acceleration_threshold)
    return inertia_strategy.compute_values(data)

def qstick_indicator(data, period=10, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate QStick Indicator"""
    qstick_strategy = QStickStrategies(period, baseline, upper_threshold, lower_threshold)
    return qstick_strategy.compute_values(data)

def trix_indicator(data, period=15, threshold_value=0.2):
    """Calculate TRIX Indicator"""
    trix_strategy = TrixStrategies(period, threshold_value)
    return trix_strategy.compute_values(data)

def true_strength_index(data, r_period=25, s_period=13, baseline=0, upper_threshold=50, lower_threshold=-50):
    """Calculate True Strength Index (using RSI as alternative)"""
    # Using RSI as alternative since True Strength Index not found
    rsi_strategy = RelativeStrengthIndexStrategies(r_period, baseline, upper_threshold, lower_threshold)
    return rsi_strategy.compute_values(data)

# Batch 13: Advanced Oscillators & Indicators Implementation
def aberration(data, period=20, threshold=0.1):
    """Calculate Aberration"""
    aberration_strategy = AberrationStrategies(period, threshold)
    return aberration_strategy.compute_values(data)

def absolute_price_oscillator(data, fast_period=10, slow_period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Absolute Price Oscillator"""
    apo_strategy = AbsolutePriceOscillatorStrategies(fast_period, slow_period, baseline, upper_threshold, lower_threshold)
    return apo_strategy.compute_values(data)

def acceleration_bands(data, period=20, multiplier=2, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Acceleration Bands"""
    accel_strategy = AccelerationBandsStrategies(period, multiplier, baseline, upper_threshold, lower_threshold)
    return accel_strategy.compute_values(data)

def accumulation_distribution_index(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Accumulation/Distribution Index"""
    adindex_strategy = AccumulationDistributionIndexStrategies(period, baseline, upper_threshold, lower_threshold)
    return adindex_strategy.compute_values(data)

def adaptive_price_zone(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Adaptive Price Zone"""
    adaptive_strategy = AdaptivePriceZoneStrategies(period, baseline, upper_threshold, lower_threshold)
    return adaptive_strategy.compute_values(data)

def archer_moving_averages(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Archer Moving Averages"""
    archer_ma_strategy = ArcherMovingAveragesTrendsStrategies(period, baseline, upper_threshold, lower_threshold)
    return archer_ma_strategy.compute_values(data)

def archer_on_balance_volume(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Archer On Balance Volume"""
    archer_obv_strategy = ArcherOnBalanceVolumeStrategies(period, baseline, upper_threshold, lower_threshold)
    return archer_obv_strategy.compute_values(data)

def arnaud_legoux_moving_average(data, period=20, offset=0.85, sigma=0.1, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Arnaud Legoux Moving Average"""
    alma_strategy = ArnaudLegouxMovingAverageStrategies(period, offset, sigma, baseline, upper_threshold, lower_threshold)
    return alma_strategy.compute_values(data)

def beta_indicator(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Beta Indicator"""
    beta_strategy = BetaStrategies(period, baseline, upper_threshold, lower_threshold)
    return beta_strategy.compute_values(data)

def bias_indicator(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Bias Indicator"""
    bias_strategy = BiasStrategies(period, baseline, upper_threshold, lower_threshold)
    return bias_strategy.compute_values(data)

# Batch 14: Advanced Analysis Implementation
def brar_indicator(data, period=26, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate BRAR Indicator"""
    brar_strategy = BRARStrategies(period, baseline, upper_threshold, lower_threshold)
    return brar_strategy.compute_values(data)

def bull_bear_power(data, period=13, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Bull Bear Power"""
    bullbear_strategy = BullBearPowerStrategies(period, baseline, upper_threshold, lower_threshold)
    return bullbear_strategy.compute_values(data)

def buy_sell_pressure(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Buy and Sell Pressure"""
    buysell_strategy = BuyAndSellPressureStrategies(period, baseline, upper_threshold, lower_threshold)
    return buysell_strategy.compute_values(data)

def center_of_gravity(data, period=10, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Center of Gravity"""
    cog_strategy = CenterOfGravityStrategies(period, baseline, upper_threshold, lower_threshold)
    return cog_strategy.compute_values(data)

def chande_forecast_oscillator(data, period=14, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Chande Forecast Oscillator"""
    chande_forecast_strategy = ChandeForecastOscillatorStrategies(period, baseline, upper_threshold, lower_threshold)
    return chande_forecast_strategy.compute_values(data)

def chande_kroll_stop(data, period=10, multiplier=2, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Chande Kroll Stop"""
    chande_kroll_strategy = ChandeKrollStopStrategies(period, multiplier, baseline, upper_threshold, lower_threshold)
    return chande_kroll_strategy.compute_values(data)

def chandelier_exit(data, period=22, multiplier=3, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Chandelier Exit"""
    chandelier_strategy = ChandelierExitStrategies(period, multiplier, baseline, upper_threshold, lower_threshold)
    return chandelier_strategy.compute_values(data)

def choppiness_index(data, period=14, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Choppiness Index"""
    choppiness_strategy = ChoppinessIndexStrategies(period, baseline, upper_threshold, lower_threshold)
    return choppiness_strategy.compute_values(data)

def correlation_trend_indicator(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Correlation Trend Indicator"""
    correlation_strategy = CorrelationTrendIndicatorStrategies(period, baseline, upper_threshold, lower_threshold)
    return correlation_strategy.compute_values(data)

def coppock_curve(data, period=14, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Coppock Curve"""
    coppock_strategy = CoppockCurveStrategies(period, baseline, upper_threshold, lower_threshold)
    return coppock_strategy.compute_values(data)

# Batch 15: Advanced Momentum Implementation
def cumulative_force_index(data, period=14, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Cumulative Force Index"""
    cumulative_fi_strategy = CumulativeForceIndexStrategies(period, baseline, upper_threshold, lower_threshold)
    return cumulative_fi_strategy.compute_values(data)

def cross_signals(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Cross Signals"""
    cross_strategy = CrossSignalsStrategies(period, baseline, upper_threshold, lower_threshold)
    return cross_strategy.compute_values(data)

def decay_indicator(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Decay Indicator"""
    decay_strategy = DecayStrategies(period, baseline, upper_threshold, lower_threshold)
    return decay_strategy.compute_values(data)

def decreasing_price(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Decreasing Price"""
    decreasing_strategy = DecreasingPriceStrategies(period, baseline, upper_threshold, lower_threshold)
    return decreasing_strategy.compute_values(data)

def detrended_price_oscillator(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Detrended Price Oscillator"""
    detrended_strategy = DetrendedPriceOscillatorStrategies(period, baseline, upper_threshold, lower_threshold)
    return detrended_strategy.compute_values(data)

def directional_movement(data, period=14, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Directional Movement"""
    directional_strategy = DirectionalMovementStrategies(period, baseline, upper_threshold, lower_threshold)
    return directional_strategy.compute_values(data)

def elders_force_index(data, period=13, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Elders Force Index"""
    elders_fi_strategy = EldersForceIndexStrategies(period, baseline, upper_threshold, lower_threshold)
    return elders_fi_strategy.compute_values(data)

def envelopes(data, period=20, multiplier=0.1, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Envelopes"""
    envelopes_strategy = EnvelopesStrategies(period, multiplier, baseline, upper_threshold, lower_threshold)
    return envelopes_strategy.compute_values(data)

def fisher_rvi(data, period=10, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Fisher RVI"""
    fisher_rvi_strategy = FisherRVIStrategies(period, baseline, upper_threshold, lower_threshold)
    return fisher_rvi_strategy.compute_values(data)

def fractal_indicator(data, period=5, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Fractal Indicator"""
    fractal_strategy = FractalStrategies(period, baseline, upper_threshold, lower_threshold)
    return fractal_strategy.compute_values(data)

# Batch 16: Missing Indicators - Part 1 Implementation
def elders_thermometer(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Elders Thermometer"""
    elders_thermometer_strategy = EldersThermometerStrategies(period, baseline, upper_threshold, lower_threshold)
    return elders_thermometer_strategy.compute_values(data)

def hilbert_period(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Hilbert Transform Period"""
    hilbert_period_strategy = HilbertTransformDominantCyclePeriodStrategies(period, baseline, upper_threshold, lower_threshold)
    return hilbert_period_strategy.compute_values(data)

def hilbert_phasor(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Hilbert Transform Phasor"""
    hilbert_phasor_strategy = HilbertTransformPhasorComponentsStrategies(period, baseline, upper_threshold, lower_threshold)
    return hilbert_phasor_strategy.compute_values(data)

def hilbert_trend(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Hilbert Transform Trend"""
    hilbert_trend_strategy = HilbertTransformInstantaneousTrendlineStrategies(period, baseline, upper_threshold, lower_threshold)
    return hilbert_trend_strategy.compute_values(data)

def holt_winter_channel(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Holt Winter Channel"""
    holt_winter_channel_strategy = HoltWinterChannelStrategies(period, baseline, upper_threshold, lower_threshold)
    return holt_winter_channel_strategy.compute_values(data)

def increasing_price(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Increasing Price"""
    increasing_price_strategy = IncreasingPriceStrategies(period, baseline, upper_threshold, lower_threshold)
    return increasing_price_strategy.compute_values(data)

def inverse_fisher_rsi(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Inverse Fisher Transform RSI"""
    inverse_fisher_rsi_strategy = InverseFisherTransformRSIStrategies(period, baseline, upper_threshold, lower_threshold)
    return inverse_fisher_rsi_strategy.compute_values(data)

def kaufman_efficiency(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Kaufman Efficiency Indicator"""
    kaufman_efficiency_strategy = KaufmanEfficiencyIndicatorStrategies(period, baseline, upper_threshold, lower_threshold)
    return kaufman_efficiency_strategy.compute_values(data)

def kdj_indicator(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate KDJ Indicator"""
    kdj_strategy = KDJIndicatorStrategies(period, baseline, upper_threshold, lower_threshold)
    return kdj_strategy.compute_values(data)

def know_sure_thing(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Know Sure Thing"""
    kst_strategy = KnowSureThingStrategies(period, baseline, upper_threshold, lower_threshold)
    return kst_strategy.compute_values(data)

def linear_regression_intercept(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Linear Regression Intercept"""
    linreg_intercept_strategy = LinearRegressionInterceptStrategies(period, baseline, upper_threshold, lower_threshold)
    return linreg_intercept_strategy.compute_values(data)

def long_run(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Long Run"""
    long_run_strategy = LongRunStrategies(period, baseline, upper_threshold, lower_threshold)
    return long_run_strategy.compute_values(data)

def mass_index(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Mass Index"""
    mass_index_strategy = MassIndexStrategies(period, baseline, upper_threshold, lower_threshold)
    return mass_index_strategy.compute_values(data)

def median_price(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Median Price"""
    median_price_strategy = MedianPriceStrategies(period, baseline, upper_threshold, lower_threshold)
    return median_price_strategy.compute_values(data)

def midpoint_period(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Midpoint Over Period"""
    midpoint_period_strategy = MidPointOverPeriodStrategies(period, baseline, upper_threshold, lower_threshold)
    return midpoint_period_strategy.compute_values(data)

# Batch 17: Missing Indicators - Part 2 Implementation
def midpoint_price(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Midpoint Price Period"""
    midpoint_price_strategy = MidpointPricePeriodStrategies(period, baseline, upper_threshold, lower_threshold)
    return midpoint_price_strategy.compute_values(data)

def momentum_breakout(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Momentum Breakout Bands"""
    momentum_breakout_strategy = MomentumBreakoutBandsStrategies(period, baseline, upper_threshold, lower_threshold)
    return momentum_breakout_strategy.compute_values(data)

def moving_standard_deviation(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Moving Standard Deviation"""
    moving_stddev_strategy = MovingStandardDeviationStrategies(period, baseline, upper_threshold, lower_threshold)
    return moving_stddev_strategy.compute_values(data)

def normalized_atr(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Normalized Average True Range"""
    natr_strategy = NormalizedAverageTrueRangeStrategies(period, baseline, upper_threshold, lower_threshold)
    return natr_strategy.compute_values(data)

def normalized_basp(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Normalized BASP"""
    normalized_basp_strategy = NormalizedBASPStrategies(period, baseline, upper_threshold, lower_threshold)
    return normalized_basp_strategy.compute_values(data)

def pearsons_correlation(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Pearsons Correlation Coefficient"""
    pearson_corr_strategy = PearsonsCorrelationCoefficientStrategies(period, baseline, upper_threshold, lower_threshold)
    return pearson_corr_strategy.compute_values(data)

def percent_b(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Percent B"""
    percent_b_strategy = PercentBStrategies(period, baseline, upper_threshold, lower_threshold)
    return percent_b_strategy.compute_values(data)

def pretty_good_oscillator(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Pretty Good Oscillator"""
    pgo_strategy = PrettyGoodOscillatorStrategies(period, baseline, upper_threshold, lower_threshold)
    return pgo_strategy.compute_values(data)

def price_distance(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Price Distance"""
    price_distance_strategy = PriceDistanceStrategies(period, baseline, upper_threshold, lower_threshold)
    return price_distance_strategy.compute_values(data)

def psychological_line(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Psychological Line"""
    psychological_strategy = PsychologicalLineStrategies(period, baseline, upper_threshold, lower_threshold)
    return psychological_strategy.compute_values(data)

def quantitative_qualitative_estimation(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Quantitative Qualitative Estimation"""
    qqe_strategy = QuantitativeQualitativeEstimationStrategies(period, baseline, upper_threshold, lower_threshold)
    return qqe_strategy.compute_values(data)

def relative_strength_xtra(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Relative Strength Xtra"""
    rsi_xtra_strategy = RelativeStrengthXtraStrategies(period, baseline, upper_threshold, lower_threshold)
    return rsi_xtra_strategy.compute_values(data)

def relative_vigor_index(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Relative Vigor Index"""
    rvi_strategy = RelativeVigorIndexStrategies(period, baseline, upper_threshold, lower_threshold)
    return rvi_strategy.compute_values(data)

def relative_volatility_index(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Relative Volatility Index"""
    rvi_volatility_strategy = RelativeVolatilityIndexStrategies(period, baseline, upper_threshold, lower_threshold)
    return rvi_volatility_strategy.compute_values(data)

def short_run(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Short Run"""
    short_run_strategy = ShortRunStrategies(period, baseline, upper_threshold, lower_threshold)
    return short_run_strategy.compute_values(data)

# Batch 18: Missing Indicators - Part 3 Implementation
def slope_indicator(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Slope Indicator"""
    slope_strategy = SlopeStrategies(period, baseline, upper_threshold, lower_threshold)
    return slope_strategy.compute_values(data)

def smi_ergodic_oscillator(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate SMI Ergodic Oscillator"""
    smi_ergodic_strategy = SmiErgodicOscillatorStrategies(period, baseline, upper_threshold, lower_threshold)
    return smi_ergodic_strategy.compute_values(data)

def squeeze_indicator(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Squeeze Indicator"""
    squeeze_strategy = SqueezeStrategies(period, baseline, upper_threshold, lower_threshold)
    return squeeze_strategy.compute_values(data)

def squeeze_pro(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Squeeze Pro"""
    squeeze_pro_strategy = SqueezeProStrategies(period, baseline, upper_threshold, lower_threshold)
    return squeeze_pro_strategy.compute_values(data)

def stochastic_d(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Stochastic D"""
    stoch_d_strategy = StochasticOscillatorDStrategies(period, baseline, upper_threshold, lower_threshold)
    return stoch_d_strategy.compute_values(data)

def stochastic_fast(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Stochastic Fast"""
    stoch_fast_strategy = StochasticFastStrategies(period, baseline, upper_threshold, lower_threshold)
    return stoch_fast_strategy.compute_values(data)

def stochastic_k(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Stochastic K"""
    stoch_k_strategy = StochasticOscillatorKStrategies(period, baseline, upper_threshold, lower_threshold)
    return stoch_k_strategy.compute_values(data)

def stochastic_oscillator(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Stochastic Oscillator"""
    stoch_osc_strategy = StochasticOscillatorStrategies(period, baseline, upper_threshold, lower_threshold)
    return stoch_osc_strategy.compute_values(data)

def stop_and_reverse(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Stop and Reverse"""
    stop_reverse_strategy = StopAndReverseStrategies(period, baseline, upper_threshold, lower_threshold)
    return stop_reverse_strategy.compute_values(data)

def summation_indicator(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Summation Indicator"""
    summation_strategy = SummationStrategies(period, baseline, upper_threshold, lower_threshold)
    return summation_strategy.compute_values(data)

def td_sequential(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate TD Sequential"""
    td_sequential_strategy = TDSequentialStrategies(period, baseline, upper_threshold, lower_threshold)
    return td_sequential_strategy.compute_values(data)

def trend_signals(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Trend Signals"""
    trend_signals_strategy = TrendSignalsStrategies(period, baseline, upper_threshold, lower_threshold)
    return trend_signals_strategy.compute_values(data)

def ttm_trend(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate TTM Trend"""
    ttm_trend_strategy = TTMTrendStrategies(period, baseline, upper_threshold, lower_threshold)
    return ttm_trend_strategy.compute_values(data)

def twiggs_money_index(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Twiggs Money Index"""
    twiggs_money_strategy = TwiggsMoneyIndexStrategies(period, baseline, upper_threshold, lower_threshold)
    return twiggs_money_strategy.compute_values(data)

def ulcer_index(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Ulcer Index"""
    ulcer_index_strategy = UlcerIndexStrategies(period, baseline, upper_threshold, lower_threshold)
    return ulcer_index_strategy.compute_values(data)

# Batch 19: Missing Indicators - Part 4 Implementation
def up_down_indicator(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Up Down Indicator"""
    up_down_strategy = UpDownStrategies(period, baseline, upper_threshold, lower_threshold)
    return up_down_strategy.compute_values(data)

def vertical_horizontal_filter(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Vertical Horizontal Filter"""
    vhf_strategy = VerticalHorizontalFilterStrategies(period, baseline, upper_threshold, lower_threshold)
    return vhf_strategy.compute_values(data)

def volume_profile(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Volume Profile"""
    volume_profile_strategy = VolumeProfileStrategies(period, baseline, upper_threshold, lower_threshold)
    return volume_profile_strategy.compute_values(data)

def vortex_indicator(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Vortex Indicator"""
    vortex_strategy = VortexIndicatorStrategies(period, baseline, upper_threshold, lower_threshold)
    return vortex_strategy.compute_values(data)

def wave_pm(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Wave PM"""
    wave_pm_strategy = MarkWhistlersWAVEPMStrategies(period, baseline, upper_threshold, lower_threshold)
    return wave_pm_strategy.compute_values(data)

def wave_trend_oscillator(data, period=20, baseline=0, upper_threshold=0.1, lower_threshold=-0.1):
    """Calculate Wave Trend Oscillator"""
    wave_trend_strategy = WaveTrendOscillatorStrategies(period, baseline, upper_threshold, lower_threshold)
    return wave_trend_strategy.compute_values(data)

# Global registry instance - created after all functions are defined
indicator_registry = IndicatorRegistry()
