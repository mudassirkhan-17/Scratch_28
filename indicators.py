
from ta_strategies_TVLibrary import *

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
            "MBB": momentum_breakout_bands
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
    """Generic function to calculate any indicator"""
    indicator_func = indicator_registry.get(indicator_name)
    if indicator_func is None:
        raise ValueError(f"Unknown indicator: {indicator_name}")
    
    if indicator_name in ["RSI", "RSI2"]:
        # RSI with defaults: period=14, upper=70, lower=30
        period = params[0] if len(params) >= 1 else 14
        upper = params[1] if len(params) >= 2 else 70
        lower = params[2] if len(params) >= 3 else 30
        return indicator_func(data, period, upper, lower)
    elif indicator_name in ["SSMA", "EMA2", "MOMENTUM"]:
        # Oscillators with defaults: period, upper=1.0, lower=-1.0
        period = params[0] if len(params) >= 1 else 14
        upper = params[1] if len(params) >= 2 else 1.0
        lower = params[2] if len(params) >= 3 else -1.0
        return indicator_func(data, period, upper, lower)
    elif indicator_name == "MARKET_MOMENTUM":
        # Market momentum with defaults: period=14, upper=0.05, lower=-0.05
        period = params[0] if len(params) >= 1 else 14
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
    else:
        # Handle both list and dict formats for params
        if isinstance(params, dict):
            period = params.get('period', 20)  # Default to 20 if not specified
            return indicator_func(data, period)
        else:
            return indicator_func(data, params[0])  # Only period

# Global registry instance - created after all functions are defined
indicator_registry = IndicatorRegistry()
