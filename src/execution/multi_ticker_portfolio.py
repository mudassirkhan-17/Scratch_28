#!/usr/bin/env python3
"""
Multi-Ticker Portfolio Management System
Handles portfolio allocation, position tracking, and execution across multiple tickers
"""

class MultiTickerPortfolioManager:
    """Manages portfolio across multiple tickers with individual allocations"""
    
    def __init__(self, total_capital, allocations, trade_sizes, sl_tp_config):
        self.total_capital = total_capital
        self.allocations = allocations  # {'AAPL': 0.6, 'MSFT': 0.4}
        self.trade_sizes = trade_sizes  # Per-ticker trade configuration
        self.sl_tp_config = sl_tp_config
        
        # Initialize per-ticker portfolios
        self.ticker_portfolios = {}
        self.ticker_risk_managers = {}
        
        print(f"🎯 MULTI-TICKER PORTFOLIO INITIALIZED")
        print(f"💰 Total Capital: ${total_capital:,.2f}")
        
        for ticker, allocation in allocations.items():
            allocated_capital = total_capital * allocation
            trade_config = {
                'percentage': trade_sizes[ticker]['percentage'],
                'amount_per_trade': trade_sizes[ticker]['amount_per_trade']
            }
            
            # Create individual portfolio and risk manager for each ticker
            from portfolio_manager import PortfolioManager
            from risk_manager import RiskManager
            
            self.ticker_portfolios[ticker] = PortfolioManager(allocated_capital, trade_config)
            self.ticker_risk_managers[ticker] = RiskManager(sl_tp_config)
            
            print(f"  📈 {ticker}: ${allocated_capital:,.2f} ({allocation*100:.1f}%) - ${trade_config['amount_per_trade']:,.2f}/trade")
        
        # Portfolio tracking
        self.all_trades = []
        self.portfolio_history = []
        
        print(f"✅ Multi-ticker portfolio ready!")
    
    def get_total_portfolio_value(self, current_prices):
        """Calculate total portfolio value across all tickers"""
        total_value = 0
        
        for ticker, portfolio in self.ticker_portfolios.items():
            current_price = current_prices.get(ticker, 0)
            ticker_value = portfolio.get_portfolio_value(current_price)
            total_value += ticker_value
        
        return total_value
    
    def process_market_tick(self, current_prices, signals, strategy_type):
        """Process market tick for all tickers simultaneously"""
        total_portfolio_value = self.get_total_portfolio_value(current_prices)
        
        # Process each ticker independently
        for ticker in self.allocations.keys():
            current_price = current_prices.get(ticker, 0)
            entry_signal = signals.get(f'{ticker}_Entry_Signal', False)
            exit_signal = signals.get(f'{ticker}_Exit_Signal', False)
            
            portfolio = self.ticker_portfolios[ticker]
            risk_manager = self.ticker_risk_managers[ticker]
            
            # Process tick for this ticker
            self._process_ticker_tick(
                ticker, current_price, entry_signal, exit_signal, 
                portfolio, risk_manager, strategy_type
            )
        
        # Record portfolio snapshot
        self.portfolio_history.append({
            'total_value': total_portfolio_value,
            'prices': current_prices.copy(),
            'individual_values': {
                ticker: portfolio.get_portfolio_value(current_prices.get(ticker, 0))
                for ticker, portfolio in self.ticker_portfolios.items()
            }
        })
        
        return total_portfolio_value
    
    def _process_ticker_tick(self, ticker, current_price, entry_signal, exit_signal, 
                           portfolio, risk_manager, strategy_type):
        """Process a single ticker's market tick"""
        
        # Risk management checks first
        if risk_manager.is_sl_tp_enabled() and portfolio.shares_owned != 0:
            risk_result = risk_manager.get_risk_check_result(current_price, portfolio)
            action = risk_result.get('action', 'NONE')
            
            if action == 'STOP_LOSS':
                self._execute_sl_tp_exit(ticker, current_price, portfolio, risk_manager, "Stop Loss")
                return
            elif action == 'TAKE_PROFIT':
                self._execute_sl_tp_exit(ticker, current_price, portfolio, risk_manager, "Take Profit")
                return
            elif action == 'LIQUIDATION':
                self._execute_liquidation(ticker, current_price, portfolio, risk_manager)
                return
        
        # Liquidation is now handled in the risk management section above
        
        # Strategy-based execution
        if strategy_type == "long":
            self._execute_long_logic(ticker, current_price, entry_signal, exit_signal, portfolio, risk_manager)
        elif strategy_type == "short":
            self._execute_short_logic(ticker, current_price, entry_signal, exit_signal, portfolio, risk_manager)
        else:  # reversal
            self._execute_reversal_logic(ticker, current_price, entry_signal, exit_signal, portfolio, risk_manager)
    
    def _execute_long_logic(self, ticker, current_price, entry_signal, exit_signal, portfolio, risk_manager):
        """Execute long strategy logic for a ticker"""
        if portfolio.shares_owned == 0 and entry_signal:
            # Enter long position
            shares_before = portfolio.shares_owned
            portfolio.enter_long_position(current_price)
            shares_bought = portfolio.shares_owned - shares_before
            
            if shares_bought > 0:
                risk_manager.set_sl_tp_levels(current_price, shares_bought, portfolio.buying_price, "LONG")
                
                self.all_trades.append({
                    'ticker': ticker,
                    'action': 'BUY',
                    'price': current_price,
                    'shares': shares_bought,
                    'value': shares_bought * current_price,
                    'type': 'Entry'
                })
                
        elif portfolio.shares_owned > 0 and exit_signal:
            # Exit long position
            shares_sold = portfolio.shares_owned
            exit_result = portfolio.exit_long_position(current_price)
            profit_loss = exit_result['profit_loss'] if isinstance(exit_result, dict) else exit_result
            risk_manager.reset_levels()
            
            self.all_trades.append({
                'ticker': ticker,
                'action': 'SELL',
                'price': current_price,
                'shares': shares_sold,
                'value': shares_sold * current_price,
                'profit_loss': profit_loss,
                'type': 'Exit'
            })
    
    def _execute_short_logic(self, ticker, current_price, entry_signal, exit_signal, portfolio, risk_manager):
        """Execute short strategy logic for a ticker"""
        if portfolio.shares_owned == 0 and entry_signal:
            # Enter short position
            shares_before = portfolio.shares_owned
            portfolio.enter_short_position(current_price)
            shares_shorted = abs(portfolio.shares_owned - shares_before)
            
            if shares_shorted > 0:
                risk_manager.set_sl_tp_levels(current_price, -shares_shorted, portfolio.buying_price, "SHORT")
                
                self.all_trades.append({
                    'ticker': ticker,
                    'action': 'SHORT',
                    'price': current_price,
                    'shares': shares_shorted,
                    'value': shares_shorted * current_price,
                    'type': 'Entry'
                })
                
        elif portfolio.shares_owned < 0 and exit_signal:
            # Exit short position
            shares_covered = abs(portfolio.shares_owned)
            exit_result = portfolio.exit_short_position(current_price)
            profit_loss = exit_result['profit_loss'] if isinstance(exit_result, dict) else exit_result
            risk_manager.reset_levels()
            
            self.all_trades.append({
                'ticker': ticker,
                'action': 'COVER',
                'price': current_price,
                'shares': shares_covered,
                'value': shares_covered * current_price,
                'profit_loss': profit_loss,
                'type': 'Exit'
            })
    
    def _execute_reversal_logic(self, ticker, current_price, entry_signal, exit_signal, portfolio, risk_manager):
        """Execute reversal strategy logic for a ticker"""
        if entry_signal and portfolio.shares_owned <= 0:
            # Go long (exit short if needed, then enter long)
            if portfolio.shares_owned < 0:
                shares_covered = abs(portfolio.shares_owned)
                exit_result = portfolio.exit_short_position(current_price)
                profit_loss = exit_result['profit_loss'] if isinstance(exit_result, dict) else exit_result
                self.all_trades.append({
                    'ticker': ticker,
                    'action': 'COVER',
                    'price': current_price,
                    'shares': shares_covered,
                    'profit_loss': profit_loss,
                    'type': 'Reversal Exit'
                })
            
            # Enter long
            shares_before = portfolio.shares_owned
            portfolio.enter_long_position(current_price)
            shares_bought = portfolio.shares_owned - shares_before
            
            if shares_bought > 0:
                risk_manager.set_sl_tp_levels(current_price, shares_bought, portfolio.buying_price, "LONG")
                
                self.all_trades.append({
                    'ticker': ticker,
                    'action': 'BUY',
                    'price': current_price,
                    'shares': shares_bought,
                    'type': 'Reversal Entry'
                })
                
        elif exit_signal and portfolio.shares_owned >= 0:
            # Go short (exit long if needed, then enter short)
            if portfolio.shares_owned > 0:
                shares_sold = portfolio.shares_owned
                exit_result = portfolio.exit_long_position(current_price)
                profit_loss = exit_result['profit_loss'] if isinstance(exit_result, dict) else exit_result
                self.all_trades.append({
                    'ticker': ticker,
                    'action': 'SELL',
                    'price': current_price,
                    'shares': shares_sold,
                    'profit_loss': profit_loss,
                    'type': 'Reversal Exit'
                })
            
            # Enter short
            shares_before = portfolio.shares_owned
            portfolio.enter_short_position(current_price)
            shares_shorted = abs(portfolio.shares_owned - shares_before)
            
            if shares_shorted > 0:
                risk_manager.set_sl_tp_levels(current_price, -shares_shorted, portfolio.buying_price, "SHORT")
                
                self.all_trades.append({
                    'ticker': ticker,
                    'action': 'SHORT',
                    'price': current_price,
                    'shares': shares_shorted,
                    'type': 'Reversal Entry'
                })
    
    def _execute_sl_tp_exit(self, ticker, current_price, portfolio, risk_manager, reason):
        """Execute stop loss or take profit exit"""
        if portfolio.shares_owned > 0:  # Long position
            exit_result = portfolio.exit_long_position(current_price)
            profit_loss = exit_result['profit_loss'] if isinstance(exit_result, dict) else exit_result
            action = 'SELL'
        else:  # Short position
            exit_result = portfolio.exit_short_position(current_price)
            profit_loss = exit_result['profit_loss'] if isinstance(exit_result, dict) else exit_result
            action = 'COVER'
        
        risk_manager.reset_levels()
        
        self.all_trades.append({
            'ticker': ticker,
            'action': action,
            'price': current_price,
            'shares': abs(portfolio.shares_owned),
            'profit_loss': profit_loss,
            'type': reason
        })
    
    def _execute_liquidation(self, ticker, current_price, portfolio, risk_manager):
        """Execute forced liquidation"""
        exit_result = portfolio.exit_short_position(current_price)
        profit_loss = exit_result['profit_loss'] if isinstance(exit_result, dict) else exit_result
        risk_manager.reset_levels()
        
        self.all_trades.append({
            'ticker': ticker,
            'action': 'LIQUIDATE',
            'price': current_price,
            'shares': abs(portfolio.shares_owned),
            'profit_loss': profit_loss,
            'type': 'Liquidation'
        })
    
    def get_final_results(self, final_prices=None):
        """Get comprehensive final results with proper portfolio value calculation"""
        # Get final prices from the last portfolio history entry if not provided
        if final_prices is None and self.portfolio_history:
            final_prices = self.portfolio_history[-1]['prices']
        elif final_prices is None:
            # Fallback: use zeros (will use final_cash values)
            final_prices = {ticker: 0 for ticker in self.ticker_portfolios.keys()}
        
        # Calculate total final value using proper portfolio value calculation
        total_final_value = 0
        ticker_results = {}
        
        for ticker, portfolio in self.ticker_portfolios.items():
            # Get the final price for this ticker (handle unique ticker names)
            base_ticker = ticker.split('_')[0]  # Convert AAPL_1 -> AAPL
            final_price = final_prices.get(ticker, final_prices.get(base_ticker, 0))
            
            # Use the portfolio's get_portfolio_value method for accurate calculation
            ticker_final_value = portfolio.get_portfolio_value(final_price)
            ticker_profit = ticker_final_value - portfolio.original_capital
            ticker_return = (ticker_profit / portfolio.original_capital) * 100 if portfolio.original_capital != 0 else 0
            
            ticker_results[ticker] = {
                'initial_capital': portfolio.original_capital,
                'final_value': ticker_final_value,
                'profit_loss': ticker_profit,
                'return_percent': ticker_return,
                'trades': len([t for t in self.all_trades if t['ticker'] == ticker])
            }
            
            total_final_value += ticker_final_value
        
        total_profit = total_final_value - self.total_capital
        total_return_percent = (total_profit / self.total_capital) * 100 if self.total_capital != 0 else 0
        
        return {
            'total_initial_capital': self.total_capital,
            'total_final_value': total_final_value,
            'total_profit_loss': total_profit,
            'total_return_percent': total_return_percent,
            'total_trades': len(self.all_trades),
            'ticker_results': ticker_results,
            'all_trades': self.all_trades
        }
    
    def print_final_results(self, data=None):
        """Print comprehensive final results"""
        # Extract final prices from data if available
        final_prices = None
        if data is not None and not data.empty:
            final_prices = {}
            for ticker in self.ticker_portfolios.keys():
                base_ticker = ticker.split('_')[0]  # Convert AAPL_1 -> AAPL
                close_col = f'{ticker}_Close' if f'{ticker}_Close' in data.columns else f'{base_ticker}_Close'
                if close_col in data.columns:
                    final_prices[ticker] = data[close_col].iloc[-1]
        
        results = self.get_final_results(final_prices)
        
        print(f"\n📊 MULTI-TICKER PORTFOLIO RESULTS")
        print("="*60)
        print(f"💰 OVERALL PERFORMANCE:")
        print(f"  Started with: ${results['total_initial_capital']:,.2f}")
        print(f"  Ended with: ${results['total_final_value']:,.2f}")
        print(f"  Total Profit: ${results['total_profit_loss']:,.2f}")
        print(f"  Total Return: {results['total_return_percent']:.2f}%")
        print(f"  Total Trades: {results['total_trades']}")
        
        print(f"\n📈 PER-TICKER PERFORMANCE:")
        print("-"*60)
        for ticker, ticker_result in results['ticker_results'].items():
            print(f"📊 {ticker}:")
            print(f"  💰 Capital: ${ticker_result['initial_capital']:,.2f}")
            print(f"  📈 Final: ${ticker_result['final_value']:,.2f}")
            print(f"  💵 P&L: ${ticker_result['profit_loss']:,.2f}")
            print(f"  📊 Return: {ticker_result['return_percent']:.2f}%")
            print(f"  🔄 Trades: {ticker_result['trades']}")
            print()
        
        # Advanced metrics if data is available
        if data is not None and len(self.all_trades) > 0:
            try:
                from metrics import calculate_advanced_metrics
                
                # Create a mock portfolio manager for metrics calculation
                class MockPortfolio:
                    def __init__(self, initial_cash, final_value):
                        self.initial_cash = initial_cash
                        self.final_cash = final_value
                
                mock_portfolio = MockPortfolio(self.total_capital, results['total_final_value'])
                
                # Add portfolio value column to data
                if 'Portfolio_Value' not in data.columns:
                    # Ensure we have the right number of portfolio values
                    portfolio_values = [h['total_value'] for h in self.portfolio_history]
                    if len(portfolio_values) == len(data):
                        data['Portfolio_Value'] = portfolio_values
                    else:
                        # Pad or truncate to match data length
                        if len(portfolio_values) < len(data):
                            # Pad with the last value
                            last_value = portfolio_values[-1] if portfolio_values else self.total_capital
                            portfolio_values.extend([last_value] * (len(data) - len(portfolio_values)))
                        else:
                            # Truncate to match data length
                            portfolio_values = portfolio_values[:len(data)]
                        data['Portfolio_Value'] = portfolio_values
                
                metrics = calculate_advanced_metrics(mock_portfolio, data, self.all_trades)
                
                if metrics:
                    print(f"📈 ADVANCED PORTFOLIO METRICS:")
                    print("="*60)
                    print(f"📊 Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.3f}")
                    print(f"📊 Sortino Ratio: {metrics.get('sortino_ratio', 0):.3f}")
                    print(f"📊 Calmar Ratio: {metrics.get('calmar_ratio', 0):.3f}")
                    print(f"📉 Max Drawdown: {metrics.get('max_drawdown', 0):.2f}%")
                    print(f"📊 Volatility: {metrics.get('volatility', 0):.2f}%")
                    print(f"🎯 Win Rate: {metrics.get('win_rate', 0):.1f}%")
                    print(f"💰 Profit Factor: {metrics.get('profit_factor', 0):.2f}")
                    
            except Exception as e:
                print(f"⚠️ Advanced metrics calculation failed: {e}")
