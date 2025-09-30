# Stock MCP Server

<div align="center">

**为 AI 助手提供全面的中国 A 股市场数据和分析能力**

[English](./README_EN.md) | 简体中文

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![MCP](https://img.shields.io/badge/MCP-Compatible-purple.svg)](https://modelcontextprotocol.io/)

</div>

## 📖 简介

Stock MCP Server 是一个基于 Model Context Protocol (MCP) 的服务器，为 AI 助手（如 Claude Desktop）提供全面的中国 A 股市场数据和分析能力。通过自然对话即可获取实时行情、技术指标、市场情绪、新闻分析和投资建议。

### ✨ 核心功能

- **🔴 实时行情**：上证指数实时数据、成交量、市场宽度统计
- **📊 技术分析**：50+ 技术指标（均线、MACD、RSI、KDJ 等）
- **💰 资金流向**：北向资金、融资融券、主力资金追踪
- **😊 市场情绪**：多维度情绪分析（0-100 量化指标）
- **📰 新闻分析**：财经新闻抓取、情感分析、热点聚合
- **🏢 板块分析**：行业板块表现、资金流向、龙头股识别
- **🌍 宏观数据**：GDP、CPI、PMI 等宏观经济指标
- **💡 投资建议**：基于多维分析生成投资策略和风险提示
- **📈 市场总览**：一键获取市场全景快照
- **🎯 特色数据**：龙虎榜、大宗交易、IPO 数据

## 🚀 快速开始

### 安装

**方式 1：使用 uvx（推荐）**

```bash
uvx stock-mcp-server
```

**方式 2：使用 pip**

```bash
pip install stock-mcp-server
stock-mcp-server
```

**方式 3：开发模式**

```bash
git clone https://github.com/yourusername/stock-mcp-server.git
cd stock-mcp-server
uv sync
uv run stock-mcp-server
```

### 配置 Claude Desktop

编辑 Claude Desktop 配置文件：

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

重启 Claude Desktop 即可使用。

### 使用示例

与 Claude 对话即可获取市场数据：

**查询实时行情**
> 你：上证指数今天表现如何？
> 
> Claude：上证指数（000001）当前 3,245.67 点，上涨 0.33%...

**技术分析**
> 你：帮我分析一下技术指标
> 
> Claude：技术指标显示：MA5 上穿 MA10，MACD 金叉，RSI 65...

**市场情绪**
> 你：今天市场情绪怎么样？
> 
> Claude：市场情绪指数 62.5，处于偏乐观区间...

**投资建议**
> 你：给我一些投资建议
> 
> Claude：基于当前市场分析：看多，建议半仓操作...

## 🛠️ MCP 工具

本服务器提供 10 个 MCP 工具：

1. **get_market_data** - 获取市场数据（实时/历史/市场宽度）
2. **calculate_indicators** - 计算技术指标（50+ 指标）
3. **get_money_flow** - 获取资金流向数据
4. **get_sentiment_analysis** - 市场情绪分析
5. **get_news** - 获取财经新闻和情感分析
6. **get_sector_data** - 板块数据和轮动分析
7. **get_macro_data** - 宏观经济数据
8. **get_special_data** - 特色数据（龙虎榜、大宗交易等）
9. **generate_advice** - 生成投资建议
10. **get_market_overview** - 获取市场总览

## 📊 MCP 资源

提供 10 个只读资源：

1. `market://summary/{date}` - 市场摘要
2. `market://analysis/technical/{date}` - 技术分析报告
3. `market://sentiment/{date}` - 情绪报告
4. `market://briefing/{date}` - 每日简报
5. `market://news/{date}` - 新闻摘要
6. `market://moneyflow/{date}` - 资金流向报告
7. `market://sectors/heatmap/{date}` - 板块热力图
8. `market://indicators/all/{date}` - 全部指标
9. `market://risk/{date}` - 风险评估
10. `market://macro/calendar` - 经济日历

## 📦 架构

```
stock-mcp-server/
├── src/stock_mcp_server/
│   ├── server.py              # MCP 服务器入口
│   ├── tools/                 # 10 个 MCP 工具实现
│   ├── resources/             # 10 个 MCP 资源实现
│   ├── services/              # 业务逻辑层
│   │   ├── akshare_service.py # AKShare 数据获取
│   │   ├── news_service.py    # 新闻抓取
│   │   ├── cache_service.py   # 缓存管理
│   │   ├── indicator_service.py # 指标计算
│   │   └── sentiment_service.py # 情绪分析
│   ├── models/                # 数据模型（Pydantic）
│   └── utils/                 # 工具模块
└── tests/                     # 测试套件
    ├── contract/              # 契约测试
    ├── integration/           # 集成测试
    └── unit/                  # 单元测试
```

## 🎯 性能指标

- ⚡ 实时数据查询：< 2 秒
- 📈 技术指标计算：< 5 秒（50+ 指标）
- 📰 新闻抓取：< 10 秒
- 💡 投资建议生成：< 5 秒
- 🔄 缓存命中率：> 60%
- 🚀 并发支持：10+ 并发请求

## ⚙️ 配置

创建 `config.yaml` 文件自定义配置：

```yaml
# 数据刷新间隔（秒）
refresh_intervals:
  realtime: 300      # 实时数据 5 分钟
  news: 1800         # 新闻 30 分钟
  historical: 86400  # 历史数据 24 小时

# 新闻源
news_sources:
  - dongfang_fortune
  - sina_finance
  - securities_times

# 情绪计算权重
sentiment_weights:
  volume: 0.25
  price: 0.35
  volatility: 0.15
  capital: 0.15
  news: 0.10

# 缓存配置
cache:
  max_size_mb: 500
  cleanup_interval: 86400
```

## 🧪 开发

### 安装开发依赖

```bash
uv sync --all-extras
```

### 运行测试

```bash
# 所有测试
uv run pytest

# 单元测试
uv run pytest tests/unit/

# 集成测试
uv run pytest tests/integration/

# 测试覆盖率
uv run pytest --cov=stock_mcp_server --cov-report=html
```

### 代码质量检查

```bash
# Linting
uv run ruff check .

# 格式化
uv run black .

# 类型检查
uv run mypy src/
```

## 📝 文档

- [快速开始指南](./specs/001-generate-mcp-server/quickstart.md)
- [API 文档](./docs/api.md)
- [数据模型](./specs/001-generate-mcp-server/data-model.md)
- [技术方案](./specs/001-generate-mcp-server/plan.md)

## ⚠️ 免责声明

本工具提供的所有数据和分析仅供参考，不构成投资建议。

投资有风险，入市需谨慎。请在做出投资决策前咨询专业的金融顾问。

## 📄 许可证

[MIT License](./LICENSE)

## 🤝 贡献

欢迎贡献代码、报告问题或提出改进建议！

## 📧 联系

- GitHub Issues: [提交问题](https://github.com/yourusername/stock-mcp-server/issues)
- Email: your.email@example.com

---

<div align="center">
Made with ❤️ for the AI assistant community
</div>

