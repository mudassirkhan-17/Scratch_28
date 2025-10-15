#!/usr/bin/env python3
"""
Simple Results Analyzer
Takes JSON output file and provides precise LLM analysis
"""

import json
import os
import sys
from datetime import datetime

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Manual .env loading if python-dotenv not available
    env_file = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

from openai import OpenAI

def analyze_results(json_file_path, return_data=False):
    """
    Analyze trading results and provide precise LLM explanation
    
    Args:
        json_file_path: Path to the JSON results file
        return_data: If True, returns analysis data instead of printing
    
    Returns:
        dict: Analysis data if return_data=True, None otherwise
    """
    
    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        if return_data:
            return {"error": "OpenAI API key not found"}
        print("❌ OpenAI API key not found!")
        print("💡 Set OPENAI_API_KEY environment variable")
        return
    
    # Load JSON results
    try:
        with open(json_file_path, 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        if return_data:
            return {"error": f"File not found: {json_file_path}"}
        print(f"❌ File not found: {json_file_path}")
        return
    except json.JSONDecodeError:
        if return_data:
            return {"error": f"Invalid JSON file: {json_file_path}"}
        print(f"❌ Invalid JSON file: {json_file_path}")
        return
    
    # Extract key data
    config = results.get('configuration', {})
    performance = results.get('performance_metrics', {})
    results_data = results.get('results', {})
    trades = results.get('trades', [])
    
    # Create analysis prompt
    prompt = f"""
Analyze this trading strategy backtest results and provide a precise, clear explanation:

STRATEGY DETAILS:
- Ticker: {config.get('ticker', 'Unknown')}
- Strategy: {config.get('mode', 'Unknown')}
- Capital: ${results_data.get('initial_cash', 0):,.2f}
- Final Value: ${results_data.get('final_value', 0):,.2f}
- Total Return: {results_data.get('total_return_percent', 0):.2f}%

PERFORMANCE METRICS:
- Total Trades: {performance.get('total_trades', 0)}
- Win Rate: {performance.get('win_rate_percent', 0):.1f}%
- Profit Factor: {performance.get('profit_factor', 0)}
- Sharpe Ratio: {performance.get('sharpe_ratio', 0):.3f}
- Max Drawdown: {performance.get('max_drawdown_percent', 0):.2f}%

TRADES EXECUTED: {len(trades)}

Provide a concise analysis in exactly 5-6 lines covering:
1. Overall performance assessment (good/bad/neutral)
2. Key strength or weakness
3. Risk level assessment
4. One specific recommendation

Keep it brief and actionable.
"""
    
    # Get LLM analysis
    try:
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a trading strategy analyst. Provide precise, actionable analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        analysis = response.choices[0].message.content
        
        # Prepare metrics data
        metrics_data = {
            'total_return': results_data.get('total_return_percent', 0),
            'win_rate': performance.get('win_rate_percent', 0),
            'total_trades': performance.get('total_trades', 0),
            'max_drawdown': performance.get('max_drawdown_percent', 0),
            'sharpe_ratio': performance.get('sharpe_ratio', 0)
        }
        
        if return_data:
            # Return data for integration
            return {
                'success': True,
                'analysis': analysis,
                'metrics': metrics_data,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        
        # Display results (original behavior)
        print("="*60)
        print("TRADING STRATEGY ANALYSIS")
        print("="*60)
        print(f"File: {json_file_path}")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Key numbers at top
        print("KEY METRICS:")
        print(f"• Total Return: {metrics_data['total_return']:.2f}%")
        print(f"• Win Rate: {metrics_data['win_rate']:.1f}%")
        print(f"• Total Trades: {metrics_data['total_trades']}")
        print(f"• Max Drawdown: {metrics_data['max_drawdown']:.2f}%")
        print(f"• Sharpe Ratio: {metrics_data['sharpe_ratio']:.3f}")
        print("="*60)
        
        print("ANALYSIS:")
        print(analysis)
        print("="*60)
        
        # Save analysis to file (ensure it's in the correct location)
        if json_file_path.startswith('results/'):
            # If relative path, make it absolute from project root
            project_root = os.path.join(os.path.dirname(__file__), '..', '..')
            analysis_file = os.path.join(project_root, json_file_path.replace('.json', '_analysis.txt'))
        else:
            analysis_file = json_file_path.replace('.json', '_analysis.txt')
        with open(analysis_file, 'w', encoding='utf-8') as f:
            f.write(f"TRADING STRATEGY ANALYSIS\n")
            f.write(f"File: {json_file_path}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n")
            f.write(analysis)
            f.write("\n" + "="*60)
        
        print(f"💾 Analysis saved to: {analysis_file}")
        
    except Exception as e:
        if return_data:
            return {"error": f"LLM analysis failed: {e}"}
        print(f"❌ Error getting LLM analysis: {e}")

def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python analyze_results.py <results_file.json>")
        print("Example: python analyze_results.py ../../results/output/single_AAPL_results.json")
        return
    
    json_file = sys.argv[1]
    
    # Fix file path - if it's a relative path starting with 'results/', make it absolute
    if json_file.startswith('results/'):
        project_root = os.path.join(os.path.dirname(__file__), '..', '..')
        json_file = os.path.join(project_root, json_file)
    
    if not json_file.endswith('.json'):
        print("❌ Please provide a JSON file")
        return
    
    if not os.path.exists(json_file):
        print(f"❌ File not found: {json_file}")
        print(f"💡 Try: python analyze_results.py ../../results/output/single_AAPL_results.json")
        return
    
    print(f"🔍 Analyzing: {json_file}")
    analyze_results(json_file)

if __name__ == "__main__":
    main()
