"""
Trade Executor - Orchestrates Portfolio Manager and Risk Manager
Handles trade execution, logging, and strategy flow control
"""

from portfolio_manager import PortfolioManager
from risk_manager import RiskManager

class TradeExecutor:
    """Executes trades and manages the interaction between portfolio and risk systems"""
    
    def __init__(self, initial_cash, sl_tp_config, per_trade_config=None):
        """Initialize trade executor with portfolio and risk managers"""
        self.portfolio = PortfolioManager(initial_cash, per_trade_config)
        self.risk = RiskManager(sl_tp_config)
        self.trades = []
        
        # portfolio, risk, trades
        print(f"Trade Executor initialized")
    
    def process_market_tick(self, current_price, entry_signal, exit_signal, strategy_type):
        """Process one market tick - handles all risk checks and signals"""
        # 🚨 HIGHEST PRIORITY: Risk Management Checks
        risk_result = self.risk.get_risk_check_result(current_price, self.portfolio)
        
        if risk_result['action'] == 'LIQUIDATION':
            return self._execute_liquidation(current_price, risk_result['info'])
        
        elif risk_result['action'] == 'STOP_LOSS':
            return self._execute_stop_loss(current_price, risk_result)
        
        elif risk_result['action'] == 'TAKE_PROFIT':
            return self._execute_take_profit(current_price, risk_result)
        
        # 📊 NORMAL TRADING SIGNALS (only if no risk action taken)
        if strategy_type == "long":
            return self._process_long_signals(current_price, entry_signal, exit_signal)
        elif strategy_type == "short":
            return self._process_short_signals(current_price, entry_signal, exit_signal)
        elif strategy_type == "reversal":
            return self._process_reversal_signals(current_price, entry_signal, exit_signal)
        
        return None  # No action taken
    
    def _execute_liquidation(self, current_price, liquidation_info):
        """Execute forced liquidation"""
        if not self.portfolio.is_short():
            return None
        
        # Force close short position
        result = self.portfolio.exit_short_position(current_price)
        
        print(f"🚨 LIQUIDATION TRIGGERED! Loss: ${liquidation_info['current_loss']:,.2f} <= ${liquidation_info['threshold_stop']:,.2f}")
        print(f"💥 FORCED SHORT COVER: Bought {result['shares']} shares at ${current_price:.2f}")
        print(f"  Money spent to cover: ${result['money_spent']:,.2f}")
        print(f"  Liquidation loss: ${result['profit_loss']:,.2f}")
        print(f"  Final cash: ${result['final_cash']:,.2f}")
        
        # Log trade
        trade = {
            'type': 'LIQUIDATION_SHORT',
            'price': current_price,
            'shares': result['shares'],
            'money_spent': result['money_spent'],
            'profit_loss': result['profit_loss'],
            'reason': f"Loss {liquidation_info['current_loss']:,.2f} exceeded threshold {liquidation_info['threshold_stop']:,.2f}"
        }
        self.trades.append(trade)
        
        # Reset risk manager
        self.risk.reset_levels()
        
        return trade
    
    def _execute_stop_loss(self, current_price, risk_result):
        """Execute stop loss exit"""
        if risk_result['position_type'] == 'LONG':
            result = self.portfolio.exit_long_position(current_price)
            action_name = "🚨 STOP LOSS"
        else:  # SHORT
            result = self.portfolio.exit_short_position(current_price)
            action_name = "🚨 STOP LOSS"
        
        print(f"{action_name}: Closed {result['shares']} shares at ${current_price:.2f}")
        print(f"  Entry price: ${risk_result['entry_price']:.2f}")
        print(f"  Loss: ${result['profit_loss']:,.2f}")
        print(f"  Final cash: ${result['final_cash']:,.2f}")
        
        # Log trade
        trade = {
            'type': f"STOP_LOSS_{risk_result['position_type']}",
            'price': current_price,
            'shares': result['shares'],
            'profit_loss': result['profit_loss'],
            'entry_price': risk_result['entry_price']
        }
        self.trades.append(trade)
        
        # Reset risk manager
        self.risk.reset_levels()
        
        return trade
    
    def _execute_take_profit(self, current_price, risk_result):
        """Execute take profit exit"""
        if risk_result['position_type'] == 'LONG':
            result = self.portfolio.exit_long_position(current_price)
            action_name = "💰 TAKE PROFIT"
        else:  # SHORT
            result = self.portfolio.exit_short_position(current_price)
            action_name = "💰 TAKE PROFIT"
        
        print(f"{action_name}: Closed {result['shares']} shares at ${current_price:.2f}")
        print(f"  Entry price: ${risk_result['entry_price']:.2f}")
        print(f"  Profit: ${result['profit_loss']:,.2f}")
        print(f"  Final cash: ${result['final_cash']:,.2f}")
        
        # Log trade
        trade = {
            'type': f"TAKE_PROFIT_{risk_result['position_type']}",
            'price': current_price,
            'shares': result['shares'],
            'profit_loss': result['profit_loss'],
            'entry_price': risk_result['entry_price']
        }
        self.trades.append(trade)
        
        # Reset risk manager
        self.risk.reset_levels()
        
        return trade
    
    def _process_long_signals(self, current_price, entry_signal, exit_signal):
        """Process long strategy signals"""
        # LONG ENTRY
        if entry_signal and self.portfolio.is_flat():
            result = self.portfolio.enter_long_position(current_price)
            
            # Set SL/TP levels
            self.risk.set_sl_tp_levels(current_price, result['shares'], result['money_spent'], 'LONG')
            
            print(f"LONG ENTRY: Bought {result['shares']} shares at ${current_price:.2f}")
            print(f"  Money spent: ${result['money_spent']:,.2f}")
            print(f"  Remaining: ${result['remaining']:,.2f}")
            if self.risk.is_sl_tp_enabled():
                print(f"  {self.risk.format_sl_tp_display()}")
            else:
                print(f"  ⚠️ No Stop Loss/Take Profit enabled")
            
            trade = {
                'type': 'BUY',
                'price': current_price,
                'shares': result['shares'],
                'money_spent': result['money_spent']
            }
            self.trades.append(trade)
            return trade
        
        # LONG EXIT
        elif exit_signal and self.portfolio.is_long():
            result = self.portfolio.exit_long_position(current_price)
            
            print(f"LONG EXIT: Sold {result['shares']} shares at ${current_price:.2f}")
            print(f"  Money received: ${result['selling_price']:,.2f}")
            print(f"  Profit/Loss: ${result['profit_loss']:,.2f}")
            print(f"  Final cash: ${result['final_cash']:,.2f}")
            
            trade = {
                'type': 'SELL',
                'price': current_price,
                'shares': result['shares'],
                'money_received': result['selling_price'],
                'profit_loss': result['profit_loss']
            }
            self.trades.append(trade)
            
            # Reset risk manager
            self.risk.reset_levels()
            return trade
        
        return None
    
    def _process_short_signals(self, current_price, entry_signal, exit_signal):
        """Process short strategy signals"""
        # SHORT ENTRY
        if entry_signal and self.portfolio.is_flat():
            result = self.portfolio.enter_short_position(current_price)
            
            # Set SL/TP levels
            self.risk.set_sl_tp_levels(current_price, -result['shares'], result['money_received'], 'SHORT')
            
            print(f"SHORT ENTRY: Sold {result['shares']} shares at ${current_price:.2f}")
            print(f"  Money received: ${result['money_received']:,.2f}")
            print(f"  Remaining: ${result['remaining']:,.2f}")
            if self.risk.is_sl_tp_enabled():
                print(f"  {self.risk.format_sl_tp_display()}")
            else:
                print(f"  ⚠️ No Stop Loss/Take Profit enabled")
            
            trade = {
                'type': 'SHORT',
                'price': current_price,
                'shares': result['shares'],
                'money_received': result['money_received']
            }
            self.trades.append(trade)
            return trade
        
        # SHORT EXIT
        elif exit_signal and self.portfolio.is_short():
            result = self.portfolio.exit_short_position(current_price)
            
            print(f"SHORT EXIT: Bought {result['shares']} shares at ${current_price:.2f}")
            print(f"  Money spent to cover: ${result['money_spent']:,.2f}")
            print(f"  Profit/Loss: ${result['profit_loss']:,.2f}")
            print(f"  Final cash: ${result['final_cash']:,.2f}")
            
            trade = {
                'type': 'COVER',
                'price': current_price,
                'shares': result['shares'],
                'money_spent': result['money_spent'],
                'profit_loss': result['profit_loss']
            }
            self.trades.append(trade)
            
            # Reset risk manager
            self.risk.reset_levels()
            return trade
        
        return None
    
    def _process_reversal_signals(self, current_price, entry_signal, exit_signal):
        """Process reversal strategy signals (always in market)"""
        # ENTRY SIGNAL: Go LONG
        if entry_signal:
            if self.portfolio.is_flat():  # Flat → Long
                result = self.portfolio.enter_long_position(current_price)
                self.risk.set_sl_tp_levels(current_price, result['shares'], result['money_spent'], 'LONG')
                
                print(f"📈 LONG ENTRY: Bought {result['shares']} shares at ${current_price:.2f}")
                print(f"  Money spent: ${result['money_spent']:,.2f}")
                print(f"  Remaining: ${result['remaining']:,.2f}")
                if self.risk.is_sl_tp_enabled():
                    print(f"  {self.risk.format_sl_tp_display()}")
                
                trade = {'type': 'LONG_ENTRY', 'price': current_price, 'shares': result['shares'], 'money_spent': result['money_spent']}
                self.trades.append(trade)
                return trade
                
            elif self.portfolio.is_short():  # Short → Long flip
                # Close short first
                short_result = self.portfolio.exit_short_position(current_price)
                # Enter long with proceeds
                long_result = self.portfolio.enter_long_position(current_price)
                self.risk.set_sl_tp_levels(current_price, long_result['shares'], long_result['money_spent'], 'LONG')
                
                short_profit = short_result['profit_loss']
                print(f"🔄 SHORT→LONG FLIP: Covered {short_result['shares']} shorts, bought {long_result['shares']} longs at ${current_price:.2f}")
                print(f"  Short profit: ${short_profit:,.2f}")
                print(f"  New long position: ${long_result['money_spent']:,.2f}")
                if self.risk.is_sl_tp_enabled():
                    print(f"  {self.risk.format_sl_tp_display()}")
                
                trade = {'type': 'FLIP_TO_LONG', 'price': current_price, 'shares_covered': short_result['shares'], 'shares_bought': long_result['shares'], 'short_profit': short_profit}
                self.trades.append(trade)
                return trade
        
        # EXIT SIGNAL: Go SHORT
        elif exit_signal:
            if self.portfolio.is_flat():  # Flat → Short
                result = self.portfolio.enter_short_position(current_price)
                self.risk.set_sl_tp_levels(current_price, -result['shares'], result['money_received'], 'SHORT')
                
                print(f"📉 SHORT ENTRY: Sold {result['shares']} shares at ${current_price:.2f}")
                print(f"  Money received: ${result['money_received']:,.2f}")
                print(f"  Remaining: ${result['remaining']:,.2f}")
                if self.risk.is_sl_tp_enabled():
                    print(f"  {self.risk.format_sl_tp_display()}")
                
                trade = {'type': 'SHORT_ENTRY', 'price': current_price, 'shares': result['shares'], 'money_received': result['money_received']}
                self.trades.append(trade)
                return trade
                
            elif self.portfolio.is_long():  # Long → Short flip
                # Close long first
                long_result = self.portfolio.exit_long_position(current_price)
                # Enter short with proceeds
                short_result = self.portfolio.enter_short_position(current_price)
                self.risk.set_sl_tp_levels(current_price, -short_result['shares'], short_result['money_received'], 'SHORT')
                
                long_profit = long_result['profit_loss']
                print(f"🔄 LONG→SHORT FLIP: Sold {long_result['shares']} longs, shorted {short_result['shares']} at ${current_price:.2f}")
                print(f"  Long profit: ${long_profit:,.2f}")
                print(f"  New short position: ${short_result['money_received']:,.2f}")
                if self.risk.is_sl_tp_enabled():
                    print(f"  {self.risk.format_sl_tp_display()}")
                
                trade = {'type': 'FLIP_TO_SHORT', 'price': current_price, 'shares_sold': long_result['shares'], 'shares_shorted': short_result['shares'], 'long_profit': long_profit}
                self.trades.append(trade)
                return trade
        
        return None
    
    def get_portfolio_tracking_data(self, current_price):
        """Get current portfolio data for DataFrame tracking"""
        portfolio_value = self.portfolio.get_portfolio_value(current_price)
        position_value = self.portfolio.get_position_value(current_price)
        info = self.portfolio.get_position_info()
        
        return {
            'Portfolio_Value': portfolio_value,
            'Invested_Amount': info['invested_amount'],
            'Remaining': info['remaining'],
            'Shares': info['shares_owned'],
            'Position_Value': position_value,
            'Final_Cash': info['final_cash']
        }
    
    def get_final_results(self):
        """Get final trading results"""
        results = self.portfolio.calculate_total_return()
        results['trades'] = self.trades
        results['num_trades'] = len(self.trades)
        
        return results
    
    def print_final_results(self):
        """Print final trading summary"""
        results = self.get_final_results()
        
        print(f"\n📊 FINAL RESULTS:")
        print(f"Started with: ${results['initial_cash']:,.2f}")
        print(f"Ended with: ${results['final_value']:,.2f}")
        print(f"Total Profit: ${results['total_profit']:,.2f}")
        print(f"Total Return: {results['total_return_percent']:.2f}%")
        print(f"Number of Trades: {results['num_trades']}")
        
        # Show final position
        if self.portfolio.is_long():
            print(f"Final Position: LONG {self.portfolio.shares_owned} shares")
        elif self.portfolio.is_short():
            print(f"Final Position: SHORT {abs(self.portfolio.shares_owned)} shares")
        else:
            print(f"Final Position: FLAT (no position)")
