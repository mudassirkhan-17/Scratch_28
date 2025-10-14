"""
Multi-Condition Strategy Detector
Handles multiple conditions with AND/OR logic for entry and exit signals
"""

class MultiConditionDetector:
    """
    Manages multiple trading conditions and evaluates them with AND/OR logic
    """
    
    def __init__(self):
        """Initialize the multi-condition detector"""
        self.entry_conditions = []  # List of entry conditions
        self.exit_conditions = []   # List of exit conditions
        self.entry_logic_type = "AND"  # "AND" or "OR" for entry
        self.exit_logic_type = "AND"   # "AND" or "OR" for exit
        
        print("🔧 MultiConditionDetector initialized")
    
    def clear_conditions(self):
        """Clear all conditions"""
        self.entry_conditions = []
        self.exit_conditions = []
        print("🧹 All conditions cleared")
    
    def set_logic_type(self, entry_logic="AND", exit_logic="AND"):
        """Set the logic type for combining conditions"""
        self.entry_logic_type = entry_logic.upper()
        self.exit_logic_type = exit_logic.upper()
        print(f"⚙️ Logic set - Entry: {self.entry_logic_type}, Exit: {self.exit_logic_type}")
    
    def add_entry_condition(self, condition_data):
        """
        Add an entry condition
        condition_data = {
            'comp1_type': 'INDICATOR',
            'comp1_name': 'SMA', 
            'comp1_params': (20,),
            'comp1_candles_ago': 0,
            'strategy': 'CROSSED UP',
            'comp2_type': 'INDICATOR',
            'comp2_name': 'SMA',
            'comp2_params': (50,),
            'comp2_candles_ago': 0
        }
        """
        self.entry_conditions.append(condition_data)
        print(f"➕ Entry condition {len(self.entry_conditions)} added: {condition_data['comp1_name']} {condition_data['strategy']} {condition_data['comp2_name']}")
    
    def add_exit_condition(self, condition_data):
        """Add an exit condition (same format as entry)"""
        self.exit_conditions.append(condition_data)
        print(f"➕ Exit condition {len(self.exit_conditions)} added: {condition_data['comp1_name']} {condition_data['strategy']} {condition_data['comp2_name']}")
    
    def evaluate_single_condition(self, data, condition, index):
        """
        Evaluate a single condition at given index
        Returns True/False
        """
        try:
            # Import comparison functions
            from comparisons import (crossed_up, crossed_down, greater_than, less_than, 
                                   equal_comparison, increased, decreased, crossed)
            
            # Get the comparison function
            strategy_map = {
                "CROSSED UP": crossed_up,
                "CROSSED DOWN": crossed_down, 
                "GREATER THAN": greater_than,
                "LESS THAN": less_than,
                "EQUAL": equal_comparison,
                "INCREASED": increased,
                "DECREASED": decreased,
                "CROSSED": crossed
            }
            
            comparison_func = strategy_map.get(condition['strategy'])
            if not comparison_func:
                print(f"❌ Unknown strategy: {condition['strategy']}")
                return False
            
            # Get column names for comparison 1 and 2
            if condition['comp1_type'] == 'INDICATOR':
                comp1_col = condition.get('comp1_col', f"{condition['comp1_name']}_entry1")  # Use stored column name
            elif condition['comp1_type'] == 'CONSTANT':
                # Create temporary constant column
                comp1_col = f"CONSTANT_1_{condition['comp1_params'][0]}"
                if comp1_col not in data.columns:
                    data[comp1_col] = condition['comp1_params'][0]
            else:  # PRICE
                comp1_col = 'Close'  # Use Close price
            
            if condition['comp2_type'] == 'INDICATOR':
                comp2_col = condition.get('comp2_col', f"{condition['comp2_name']}_entry1")  # Use stored column name
            elif condition['comp2_type'] == 'CONSTANT':
                # Create temporary constant column
                comp2_col = f"CONSTANT_2_{condition['comp2_params'][0]}"
                if comp2_col not in data.columns:
                    data[comp2_col] = condition['comp2_params'][0]
            else:  # PRICE
                comp2_col = 'Close'  # Use Close price
            
            # Handle candles ago by creating shifted columns if needed
            if condition['comp1_candles_ago'] > 0:
                comp1_shifted_col = f"{comp1_col}_shifted"
                if comp1_shifted_col not in data.columns:
                    data[comp1_shifted_col] = data[comp1_col].shift(condition['comp1_candles_ago'])
                comp1_col = comp1_shifted_col
            
            if condition['comp2_candles_ago'] > 0:
                comp2_shifted_col = f"{comp2_col}_shifted"
                if comp2_shifted_col not in data.columns:
                    data[comp2_shifted_col] = data[comp2_col].shift(condition['comp2_candles_ago'])
                comp2_col = comp2_shifted_col
            
            # Evaluate the condition - comparison functions return Series, we need specific index
            result_series = comparison_func(data, comp1_col, comp2_col)
            result = result_series.iloc[index] if index < len(result_series) else False
            return bool(result)
            
        except Exception as e:
            print(f"❌ Error evaluating condition: {e}")
            return False
    
    def evaluate_entry_conditions(self, data, index):
        """
        Evaluate all entry conditions with specified logic (AND/OR)
        Returns True if conditions are met, False otherwise
        """
        if not self.entry_conditions:
            return False
        
        results = []
        for i, condition in enumerate(self.entry_conditions):
            result = self.evaluate_single_condition(data, condition, index)
            results.append(result)
            # Debug output
            # print(f"🔍 Entry Condition {i+1}: {result}")
        
        # Apply logic
        if self.entry_logic_type == "AND":
            final_result = all(results)  # All must be True
        else:  # OR
            final_result = any(results)  # At least one must be True
        
        return final_result
    
    def evaluate_exit_conditions(self, data, index):
        """
        Evaluate all exit conditions with specified logic (AND/OR)
        Returns True if conditions are met, False otherwise
        """
        if not self.exit_conditions:
            return False
        
        results = []
        for i, condition in enumerate(self.exit_conditions):
            result = self.evaluate_single_condition(data, condition, index)
            results.append(result)
            # Debug output
            # print(f"🔍 Exit Condition {i+1}: {result}")
        
        # Apply logic
        if self.exit_logic_type == "AND":
            final_result = all(results)  # All must be True
        else:  # OR
            final_result = any(results)  # At least one must be True
        
        return final_result
    
    def get_condition_summary(self):
        """Get a summary of all conditions"""
        summary = f"""
📋 MULTI-CONDITION SUMMARY:
Entry Conditions: {len(self.entry_conditions)} ({self.entry_logic_type} logic)
Exit Conditions: {len(self.exit_conditions)} ({self.exit_logic_type} logic)

Entry Details:"""
        
        for i, condition in enumerate(self.entry_conditions):
            summary += f"\n  {i+1}. {condition['comp1_name']} {condition['strategy']} {condition['comp2_name']}"
        
        summary += "\n\nExit Details:"
        for i, condition in enumerate(self.exit_conditions):
            summary += f"\n  {i+1}. {condition['comp1_name']} {condition['strategy']} {condition['comp2_name']}"
        
        return summary


# Create global instances for easy access
entry_multi_detector = MultiConditionDetector()
exit_multi_detector = MultiConditionDetector()

print("✅ MultiConditionDetector class created successfully!")
print("🎯 Ready for multi-condition strategy implementation")