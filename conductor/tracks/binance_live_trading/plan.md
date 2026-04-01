# Binance Live Trading - Implementation Plan

## Phase 1: Maturity Assessment
- [ ] Establish explicit maturity criteria based on dry run performance (e.g., >10-20% consistent PROFIT_LOSS_PCT over multiple days/weeks).
- [ ] Monitor the automated "Morning Summary" recommendation to approve a winning `strategy.py`.

## Phase 2: Live Infrastructure Setup (Using MCP)
- [ ] Duplicate the core logic into a new project `projects/binance_live_trading/`.
- [ ] Develop `live_trade.py` (replacing `dry_run.py`) to fully utilize the existing MCP server (`https://binance.armaddia.lat/sse`):
    - [ ] Use `get_account_balance` tool to fetch the *real* portfolio balance instead of maintaining a virtual one.
    - [ ] Use `get_market_price` and `fetch_chart_data` for real-time market data.
    - [ ] Connect to live Binance endpoints using the `place_order` tool (e.g., `place_order(symbol="BTCUSDT", side="BUY", quantity=X)`).
    - [ ] Add exception handling for live order rejections (e.g., API limits, insufficient funds, lot size errors).
- [ ] Set `config.json` for the live trading project to execute `live_trade.py`.

## Phase 3: Risk Management & Safeguards
- [ ] Implement a "circuit breaker" in `live_trade.py` to stop trading if the live PnL drops below a specific threshold (e.g., -5% in a day).
- [ ] Configure `strategy.py` limits to use only a small fraction of the live account balance per trade (e.g., maximum 5% of total USDT).

## Phase 4: Live Deployment & Monitoring
- [ ] Run the first live tests with minimal "test" amounts (respecting the `min_notional` rule from `get_symbol_rules`).
- [ ] Ensure Telegram notifications prominently display "🔴 LIVE TRADING" and report real transaction fees/slippage.
- [ ] Track the deviation between live PnL and simulated PnL to adjust future dry runs.