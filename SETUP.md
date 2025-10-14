# Trading Strategy System

## Setup Instructions

### 1. Install Dependencies
```bash
pip install yfinance pandas numpy openai
```

### 2. Set up OpenAI API Key (for AI mode)
The AI-powered strategy parsing requires an OpenAI API key:

**Option A: Environment Variable (Recommended)**
```bash
# Windows
set OPENAI_API_KEY=your_api_key_here

# Linux/Mac
export OPENAI_API_KEY=your_api_key_here
```

**Option B: Enter when prompted**
The system will ask for your API key when using AI mode if not set as environment variable.

### 3. Run the System
```bash
python src/execution/strategy3.py
```

## Features

✅ **Immediate Ticker Validation** - Catches invalid tickers instantly  
✅ **Smart Input Validation** - Prevents common configuration errors  
✅ **Multiple Strategy Types** - Single, Multi-condition, Multi-ticker  
✅ **AI-Powered Parsing** - Natural language to strategy conversion  
✅ **Risk Management** - Stop loss, take profit, trailing stops  

## Security Note
- Never commit API keys to version control
- Use environment variables for sensitive data
- The system will prompt for API keys if not found in environment
