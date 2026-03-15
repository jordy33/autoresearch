# Experiment Log: Bitcoin Binance Automated Trading

This file serves as the long-term memory for the trading agent. Each iteration (experiment) must be recorded here with its hypothesis, changes, and the resulting metric (profit_loss_pct).

## Base Metrics
- **Initial Balance:** 1000 USDT (Simulated)
- **Target Asset:** BTC/USDT
- **Iteration Interval:** 1 Hour

---

## Experiment History

### Experiment #0: Baseline RSI Strategy
- **Date:** 2026-03-15
- **Hypothesis:** A simple RSI-based mean reversion strategy (Buy < 30, Sell > 70) will provide a stable baseline for further optimization.
- **Changes:** Initial implementation of `strategy.py`.
- **Status:** Completed.
- **Result (profit_loss_pct):** 7.18
- **Reasoning/Findings:** Baseline established using 500h of historical data. Standard RSI signals work but are prone to high drawdown.

--- Nuevo Experimento ---
Hipótesis: 1.  **Hypothesis:** The baseline RSI strategy proved successful, but is prone to whipsaws. Adding MACD confirmation to the RSI signals should filter out some false signals, leading to fewer losing trades and a higher profit. Specifically, I will buy only when RSI is below 30 *and* MACD is below its signal line (bullish divergence confirmation), and sell only when RSI is above 70 *and* MACD is above its signal line (bearish divergence confirmation).

2.
Resultado (Logs): PROFIT_LOSS_PCT: 0.00

