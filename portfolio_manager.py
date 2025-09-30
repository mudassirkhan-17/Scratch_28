"""
Portfolio Manager - Handles all money and position tracking
Using your exact variable names and formulas
"""

class PortfolioManager:
    """Manages portfolio state including cash, positions, and calculations"""
    
    def __init__(self, initial_cash=1000, per_trade_config=None):
        """Initialize portfolio with starting cash and per-trade allocation"""
        # Your exact variables
        self.initial_cash = initial_cash           # Money we start with
        self.original_capital = initial_cash       # Store original starting capital (never changes)
        
        # Per-trade allocation setup
        if per_trade_config:
            self.per_trade_config = per_trade_config  # Store original config
            self.invested_amount = per_trade_config['amount_per_trade']  # Amount per trade
            self.allocation_percentage = per_trade_config['percentage']   # Percentage for display
        else:
            self.per_trade_config = None
            self.invested_amount = initial_cash * 1.0  # Fallback: 100% (old behavior)
            self.allocation_percentage = 100.0
            
        self.remaining = 0                         # Unused investment money
        self.shares_owned = 0                      # How many shares we own (positive=long, negative=short)
        self.buying_price = 0                      # Actual money spent/received
        self.final_cash = 0                        # Money from selling/covering
        
        print(f"Portfolio initialized with: ${self.initial_cash:,.2f}")
        print(f"Available to invest: ${self.invested_amount:,.2f} ({self.allocation_percentage:.1f}%)")
    
    def enter_long_position(self, current_price):
        """Enter a long position - buy shares"""
        if self.shares_owned != 0:
            raise ValueError("Cannot enter long position - already have position")
        
        # Calculate how many shares we can buy
        max_shares = int(self.invested_amount / current_price)  # Whole shares only
        self.buying_price = max_shares * current_price          # Actual money spent
        self.shares_owned = max_shares                          # Shares we own
        self.remaining = self.initial_cash - self.buying_price  # Money left in account
        self.final_cash = 0                                     # Reset for calculation
        
        return {
            'shares': self.shares_owned,
            'money_spent': self.buying_price,
            'remaining': self.remaining
        }
    
    def exit_long_position(self, current_price):
        """Exit a long position - sell shares"""
        if self.shares_owned <= 0:
            raise ValueError("Cannot exit long position - no long position exists")
        
        selling_price = self.shares_owned * current_price  # Money received from selling
        
        # Your Formula: final_cash = remaining + buying_price + (selling_price - buying_price)
        self.final_cash = self.remaining + self.buying_price + (selling_price - self.buying_price)
        
        profit_loss = selling_price - self.buying_price  # Profit or loss on shares
        
        result = {
            'shares': self.shares_owned,
            'selling_price': selling_price,
            'profit_loss': profit_loss,
            'final_cash': self.final_cash
        }
        
        # Reset for next trade
        # Keep consistent per-trade amount instead of using all cash
        self.initial_cash = self.final_cash  # Update initial cash to current value
        if self.per_trade_config:
            # Use original per-trade amount (e.g., $2,000), not all available cash
            self.invested_amount = self.per_trade_config['amount_per_trade']
        else:
            # Fallback: use all available cash (old behavior)
            self.invested_amount = self.final_cash
        self.remaining = 0
        self.shares_owned = 0
        self.buying_price = 0
        
        return result
    
    def enter_short_position(self, current_price):
        """Enter a short position - borrow and sell shares"""
        if self.shares_owned != 0:
            raise ValueError("Cannot enter short position - already have position")
        
        # Calculate how many shares we can short
        max_shares = int(self.invested_amount / current_price)  # Whole shares only
        self.buying_price = max_shares * current_price          # Money received from shorting
        self.shares_owned = -max_shares                         # Negative shares (we owe them)
        self.remaining = self.initial_cash - self.buying_price  # Money left in account
        self.final_cash = 0                                     # Reset for calculation
        
        return {
            'shares': max_shares,  # Return positive number for display
            'money_received': self.buying_price,
            'remaining': self.remaining
        }
    
    def exit_short_position(self, current_price):
        """Exit a short position - buy back to cover"""
        if self.shares_owned >= 0:
            raise ValueError("Cannot exit short position - no short position exists")
        
        shares_to_cover = abs(self.shares_owned)             # How many shares to buy back
        selling_price = shares_to_cover * current_price      # Money spent to cover
        
        # Your Formula: final_cash = remaining + buying_price + (buying_price - selling_price)
        # Note: For shorts, profit is when selling_price < buying_price
        self.final_cash = self.remaining + self.buying_price + (self.buying_price - selling_price)
        
        profit_loss = self.buying_price - selling_price  # Profit when positive (sold high, bought low)
        
        result = {
            'shares': shares_to_cover,
            'money_spent': selling_price,
            'profit_loss': profit_loss,
            'final_cash': self.final_cash
        }
        
        # Reset for next trade
        # Keep consistent per-trade amount instead of using all cash
        self.initial_cash = self.final_cash  # Update initial cash to current value
        if self.per_trade_config:
            # Use original per-trade amount (e.g., $2,000), not all available cash
            self.invested_amount = self.per_trade_config['amount_per_trade']
        else:
            # Fallback: use all available cash (old behavior)
            self.invested_amount = self.final_cash
        self.remaining = 0
        self.shares_owned = 0
        self.buying_price = 0
        
        return result
    
    def get_portfolio_value(self, current_price):
        """Calculate current total portfolio value (real trading platform style)"""
        if self.shares_owned != 0:  # Any position (long or short)
            current_position_value = abs(self.shares_owned) * current_price
            return self.remaining + current_position_value
        else:  # No position
            return self.final_cash if self.final_cash > 0 else self.initial_cash
    
    def get_position_value(self, current_price):
        """Get current position value (for tracking)"""
        if self.shares_owned != 0:
            return abs(self.shares_owned) * current_price
        return 0
    
    def reset_for_next_trade(self, new_cash):
        """Reset portfolio state for next trade (used after SL/TP/Liquidation)"""
        self.invested_amount = new_cash
        self.remaining = 0
        self.shares_owned = 0
        self.buying_price = 0
        self.final_cash = 0
    
    def is_long(self):
        """Check if currently in long position"""
        return self.shares_owned > 0
    
    def is_short(self):
        """Check if currently in short position"""
        return self.shares_owned < 0
    
    def is_flat(self):
        """Check if currently have no position"""
        return self.shares_owned == 0
    
    def get_position_info(self):
        """Get current position information for display"""
        return {
            'initial_cash': self.initial_cash,
            'invested_amount': self.invested_amount,
            'remaining': self.remaining,
            'shares_owned': self.shares_owned,
            'buying_price': self.buying_price,
            'final_cash': self.final_cash
        }
    
    def calculate_total_return(self):
        """Calculate final results"""
        current_value = self.final_cash if self.final_cash > 0 else self.invested_amount
        total_profit = current_value - self.initial_cash
        total_return_percent = (total_profit / self.initial_cash) * 100
        
        return {
            'initial_cash': self.initial_cash,
            'final_value': current_value,
            'total_profit': total_profit,
            'total_return_percent': total_return_percent
        }