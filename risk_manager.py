"""
Risk Manager - Handles all Stop Loss, Take Profit, and Liquidation logic
Eliminates code duplication and manages risk state properly
"""

class RiskManager:
    """Manages risk controls including SL/TP and liquidation checks"""
    
    def __init__(self, sl_tp_config):
        """Initialize risk manager with user's SL/TP configuration"""
        self.sl_tp_config = sl_tp_config
        
        # Risk state variables
        self.entry_price = 0          # Price per share when position entered
        self.stop_loss_price = 0      # SL trigger price
        self.take_profit_price = 0    # TP trigger price
        self.position_direction = ""  # "LONG", "SHORT", or ""
        
        # Position tracking for liquidation
        self.position_buying_price = 0  # Money involved in position
        self.position_shares = 0        # Number of shares in position

        # entry price, stop loss price, take profit price, position direction, position buying price, position shares
        
        print(f"Risk Manager initialized - SL/TP enabled: {self.sl_tp_config['enabled']}")
        if self.sl_tp_config['enabled']:
            if self.sl_tp_config['sl_type'] == 'percentage':
                print(f"  Mode: Percentage-based ({self.sl_tp_config['sl_value']*100:.1f}% SL, {self.sl_tp_config['tp_value']*100:.1f}% TP)")
            else:
                print(f"  Mode: Dollar-based (${self.sl_tp_config['sl_value']:.0f} SL, ${self.sl_tp_config['tp_value']:.0f} TP)")
    
    def set_sl_tp_levels(self, entry_price, shares_owned, buying_price, position_type):
        """Set Stop Loss and Take Profit levels after position entry"""
        if not self.sl_tp_config['enabled']:
            self.stop_loss_price = 0
            self.take_profit_price = 0
            return
        
        # Store position info
        self.entry_price = entry_price
        self.position_direction = position_type
        self.position_buying_price = buying_price
        self.position_shares = abs(shares_owned)
        
        # Calculate SL/TP levels based on user configuration
        if self.sl_tp_config['sl_type'] == 'percentage':
            # Percentage-based SL/TP
            if position_type == 'LONG':
                self.stop_loss_price = entry_price * (1 - self.sl_tp_config['sl_value'])
                self.take_profit_price = entry_price * (1 + self.sl_tp_config['tp_value'])
            else:  # SHORT
                self.stop_loss_price = entry_price * (1 + self.sl_tp_config['sl_value'])
                self.take_profit_price = entry_price * (1 - self.sl_tp_config['tp_value'])
        
        else:  # dollar-based
            # Dollar-based SL/TP
            if position_type == 'LONG':
                stop_loss_amount = buying_price - self.sl_tp_config['sl_value']
                take_profit_amount = buying_price + self.sl_tp_config['tp_value']
            else:  # SHORT
                stop_loss_amount = buying_price + self.sl_tp_config['sl_value']
                take_profit_amount = buying_price - self.sl_tp_config['tp_value']
            
            # Convert to per-share prices
            self.stop_loss_price = stop_loss_amount / abs(shares_owned)
            self.take_profit_price = take_profit_amount / abs(shares_owned)
    
    def check_stop_loss(self, current_price):
        """Check if Stop Loss should trigger"""
        if not self.sl_tp_config['enabled'] or self.position_direction == "":
            return False
        
        if self.position_direction == "LONG":
            return current_price <= self.stop_loss_price
        else:  # SHORT
            return current_price >= self.stop_loss_price
    
    def check_take_profit(self, current_price):
        """Check if Take Profit should trigger"""
        if not self.sl_tp_config['enabled'] or self.position_direction == "":
            return False
        
        if self.position_direction == "LONG":
            return current_price >= self.take_profit_price
        else:  # SHORT
            return current_price <= self.take_profit_price
    
    def check_liquidation(self, current_price, portfolio):
        """Check if liquidation should trigger (only for short positions)"""
        # Only check liquidation for short positions
        if not portfolio.is_short():
            return False
        
        # Get position data from portfolio
        shorting_price = portfolio.buying_price      # Money received from shorting
        buying_back = abs(portfolio.shares_owned) * current_price  # Cost to cover position
        threshold_stop = -(shorting_price * 1.0)     # 100% loss limit
        
        # Check if loss exceeds threshold
        current_loss = shorting_price - buying_back
        return current_loss <= threshold_stop
    
    def get_liquidation_info(self, current_price, portfolio):
        """Get liquidation details for logging"""
        if not portfolio.is_short():
            return None
        
        shorting_price = portfolio.buying_price
        buying_back = abs(portfolio.shares_owned) * current_price
        threshold_stop = -(shorting_price * 1.0)
        current_loss = shorting_price - buying_back
        
        return {
            'shorting_price': shorting_price,
            'buying_back': buying_back,
            'threshold_stop': threshold_stop,
            'current_loss': current_loss,
            'shares_to_cover': abs(portfolio.shares_owned)
        }
    
    def get_sl_tp_info(self):
        """Get current SL/TP levels for display"""
        if not self.sl_tp_config['enabled']:
            return None
        
        return {
            'entry_price': self.entry_price,
            'stop_loss_price': self.stop_loss_price,
            'take_profit_price': self.take_profit_price,
            'position_direction': self.position_direction,
            'sl_type': self.sl_tp_config['sl_type'],
            'sl_value': self.sl_tp_config['sl_value'],
            'tp_value': self.sl_tp_config['tp_value']
        }
    
    def reset_levels(self):
        """Reset all risk levels after position closes"""
        self.entry_price = 0
        self.stop_loss_price = 0
        self.take_profit_price = 0
        self.position_direction = ""
        self.position_buying_price = 0
        self.position_shares = 0
    
    def is_sl_tp_enabled(self):
        """Check if SL/TP is enabled"""
        return self.sl_tp_config['enabled']
    
    def has_position(self):
        """Check if risk manager is tracking a position"""
        return self.position_direction != ""
    
    def format_sl_tp_display(self):
        """Format SL/TP info for display"""
        if not self.sl_tp_config['enabled']:
            return "⚠️ No Stop Loss/Take Profit enabled"
        
        if self.sl_tp_config['sl_type'] == 'percentage':
            sl_pct = self.sl_tp_config['sl_value'] * 100
            tp_pct = self.sl_tp_config['tp_value'] * 100
            return f"🚨 Stop Loss: ${self.stop_loss_price:.2f} (-{sl_pct:.1f}%), 💰 Take Profit: ${self.take_profit_price:.2f} (+{tp_pct:.1f}%)"
        else:
            return f"🚨 Stop Loss: ${self.stop_loss_price:.2f} (-${self.sl_tp_config['sl_value']:.0f}), 💰 Take Profit: ${self.take_profit_price:.2f} (+${self.sl_tp_config['tp_value']:.0f})"
    
    def get_risk_check_result(self, current_price, portfolio):
        """Comprehensive risk check - returns action needed"""
        # Check liquidation first (highest priority)
        if self.check_liquidation(current_price, portfolio):
            return {
                'action': 'LIQUIDATION',
                'info': self.get_liquidation_info(current_price, portfolio)
            }
        
        # Check Stop Loss (second priority)
        if self.check_stop_loss(current_price):
            return {
                'action': 'STOP_LOSS',
                'position_type': self.position_direction,
                'entry_price': self.entry_price,
                'trigger_price': self.stop_loss_price
            }
        
        # Check Take Profit (third priority)
        if self.check_take_profit(current_price):
            return {
                'action': 'TAKE_PROFIT',
                'position_type': self.position_direction,
                'entry_price': self.entry_price,
                'trigger_price': self.take_profit_price
            }
        # action, position_type, entry_price, trigger_price
        # No risk action needed
        return {'action': 'NONE'}
