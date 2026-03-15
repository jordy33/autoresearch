# Specification: Binance Automated Trading with MCP & Telegram

## Objective
Create an autonomous trading agent connected to a Model Context Protocol (MCP) Server for Binance to trade BTC/USDT.

## Requirements
1. Use the `binance_mcp_server` tools to fetch market data, get account balances, check rules, and place orders.
2. The agent will run on a 1-hour interval loop.
3. Target metric: `profit_loss_pct` (goal: maximize, feedback signal: Binance Portfolio Balance).
4. The agent must compile and send a **daily summary report** every morning via **Telegram**. This report should detail if strategies have improved, current balance, profit/loss metric, and a summary of recent actions (instead of notifying on every loop execution).
5. Record trade failures and rationales to build consolidated market knowledge.

## Tools (MCP)
- `get_account_balance`
- `get_market_price`
- `fetch_chart_data`
- `calculate_indicators`
- `get_symbol_rules`
- `adjust_leverage`
- `place_order`
- `read_bot_logs`

## Integration
- Telegram Bot API for notifications (requires `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` env vars).