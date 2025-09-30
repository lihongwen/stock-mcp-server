# Stock MCP Server

<div align="center">

**Comprehensive Chinese A-share Market Data and Analysis for AI Assistants**

English | [简体中文](./README.md)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![MCP](https://img.shields.io/badge/MCP-Compatible-purple.svg)](https://modelcontextprotocol.io/)

</div>

## 📖 Introduction

Stock MCP Server is a Model Context Protocol (MCP) server that provides comprehensive Chinese A-share market data and analysis capabilities to AI assistants (like Claude Desktop). Get real-time quotes, technical indicators, market sentiment, news analysis, and investment recommendations through natural conversation.

### ✨ Key Features

- **🔴 Real-time Quotes**: Shanghai Composite Index data, volume, market breadth
- **📊 Technical Analysis**: 50+ indicators (MA, MACD, RSI, KDJ, etc.)
- **💰 Capital Flow**: Northbound capital, margin trading, main capital tracking
- **😊 Market Sentiment**: Multi-dimensional sentiment analysis (0-100 scale)
- **📰 News Analysis**: Financial news scraping, sentiment analysis, hot topics
- **🏢 Sector Analysis**: Sector performance, capital flows, leading stocks
- **🌍 Macro Data**: GDP, CPI, PMI and other macroeconomic indicators
- **💡 Investment Advice**: Strategy generation based on multi-dimensional analysis
- **📈 Market Overview**: One-click comprehensive market snapshot
- **🎯 Special Data**: Dragon-Tiger List, block trades, IPO data

## 🚀 Quick Start

### Installation

**Option 1: Using uvx (Recommended)**

```bash
uvx stock-mcp-server
```

**Option 2: Using pip**

```bash
pip install stock-mcp-server
stock-mcp-server
```

**Option 3: Development Mode**

```bash
git clone https://github.com/yourusername/stock-mcp-server.git
cd stock-mcp-server
uv sync
uv run stock-mcp-server
```

### Configure Claude Desktop

Edit your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "stock-mcp": {
      "command": "uvx",
      "args": ["stock-mcp-server"]
    }
  }
}
```

Restart Claude Desktop to activate.

### Usage Examples

Simply chat with Claude to get market data:

**Query Real-time Quotes**
> You: How is the Shanghai index performing today?
> 
> Claude: Shanghai Composite (000001) is at 3,245.67, up 0.33%...

**Technical Analysis**
> You: Show me technical indicators
> 
> Claude: Technical indicators show: MA5 crossed above MA10, MACD golden cross, RSI 65...

**Market Sentiment**
> You: What's the market sentiment today?
> 
> Claude: Market sentiment index is 62.5, optimistic range...

**Investment Advice**
> You: Give me investment advice
> 
> Claude: Based on current analysis: Bullish outlook, half position recommended...

## 🛠️ MCP Tools

This server provides 10 MCP tools:

1. **get_market_data** - Get market data (real-time/historical/breadth)
2. **calculate_indicators** - Calculate technical indicators (50+ indicators)
3. **get_money_flow** - Get capital flow data
4. **get_sentiment_analysis** - Market sentiment analysis
5. **get_news** - Get financial news with sentiment analysis
6. **get_sector_data** - Sector data and rotation analysis
7. **get_macro_data** - Macroeconomic data
8. **get_special_data** - Special data (Dragon-Tiger List, block trades, etc.)
9. **generate_advice** - Generate investment recommendations
10. **get_market_overview** - Get comprehensive market overview

## 📊 MCP Resources

Provides 10 read-only resources:

1. `market://summary/{date}` - Market summary
2. `market://analysis/technical/{date}` - Technical analysis report
3. `market://sentiment/{date}` - Sentiment report
4. `market://briefing/{date}` - Daily briefing
5. `market://news/{date}` - News digest
6. `market://moneyflow/{date}` - Money flow report
7. `market://sectors/heatmap/{date}` - Sector heatmap
8. `market://indicators/all/{date}` - All indicators
9. `market://risk/{date}` - Risk assessment
10. `market://macro/calendar` - Economic calendar

## 📦 Architecture

```
stock-mcp-server/
├── src/stock_mcp_server/
│   ├── server.py              # MCP server entry point
│   ├── tools/                 # 10 MCP tool implementations
│   ├── resources/             # 10 MCP resource implementations
│   ├── services/              # Business logic layer
│   │   ├── akshare_service.py # AKShare data fetching
│   │   ├── news_service.py    # News scraping
│   │   ├── cache_service.py   # Cache management
│   │   ├── indicator_service.py # Indicator calculation
│   │   └── sentiment_service.py # Sentiment analysis
│   ├── models/                # Data models (Pydantic)
│   └── utils/                 # Utility modules
└── tests/                     # Test suite
    ├── contract/              # Contract tests
    ├── integration/           # Integration tests
    └── unit/                  # Unit tests
```

## 🎯 Performance

- ⚡ Real-time queries: < 2s
- 📈 Indicator calculation: < 5s (50+ indicators)
- 📰 News scraping: < 10s
- 💡 Advice generation: < 5s
- 🔄 Cache hit rate: > 60%
- 🚀 Concurrent requests: 10+

## ⚙️ Configuration

Create a `config.yaml` file for customization:

```yaml
# Data refresh intervals (seconds)
refresh_intervals:
  realtime: 300      # Real-time data 5 min
  news: 1800         # News 30 min
  historical: 86400  # Historical 24 hours

# News sources
news_sources:
  - dongfang_fortune
  - sina_finance
  - securities_times

# Sentiment weights
sentiment_weights:
  volume: 0.25
  price: 0.35
  volatility: 0.15
  capital: 0.15
  news: 0.10

# Cache configuration
cache:
  max_size_mb: 500
  cleanup_interval: 86400
```

## 🧪 Development

### Install Development Dependencies

```bash
uv sync --all-extras
```

### Run Tests

```bash
# All tests
uv run pytest

# Unit tests
uv run pytest tests/unit/

# Integration tests
uv run pytest tests/integration/

# Coverage
uv run pytest --cov=stock_mcp_server --cov-report=html
```

### Code Quality

```bash
# Linting
uv run ruff check .

# Formatting
uv run black .

# Type checking
uv run mypy src/
```

## 📝 Documentation

- [Quickstart Guide](./specs/001-generate-mcp-server/quickstart.md)
- [API Documentation](./docs/api.md)
- [Data Models](./specs/001-generate-mcp-server/data-model.md)
- [Technical Plan](./specs/001-generate-mcp-server/plan.md)

## ⚠️ Disclaimer

All data and analysis provided by this tool are for reference only and do not constitute investment advice.

Investing involves risks. Please consult professional financial advisors before making investment decisions.

## 📄 License

[MIT License](./LICENSE)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📧 Contact

- GitHub Issues: [Submit Issues](https://github.com/yourusername/stock-mcp-server/issues)
- Email: your.email@example.com

---

<div align="center">
Made with ❤️ for the AI assistant community
</div>

