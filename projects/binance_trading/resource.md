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

--- Nuevo Experimento (2026-03-15 04:13:36 UTC) ---
Hipótesis: Okay, I understand. I need to analyze the previous experiment, identify potential improvements, and modify `strategy.py` to reflect those improvements. My goal is to maximize `profit_loss_pct`.

1.  **Review Long-term Memory:** The baseline RSI strategy provided a positive profit but likely experienced drawdown. RSI signals can be noisy and lead to whipsaws.
2.  **Harvest Feedback:** I need to retrieve the current profit/loss and any error logs from the latest run to understand the actual performance of the baseline strategy.  Then I will record it in `resource.md`.
3.  **Log the Result:** After obtaining the current Binance Portfolio Balance, I will record the outcome of the previous experiment in `resource.md`.
4.  **Formulate a Hypothesis:**  The current strategy is vulnerable to false signals. My hypothesis is that incorporating MACD confirmation will reduce the number of false signals and improve profitability. Specifically, I will modify the buy signal to only trigger if the RSI is below 30 *and* the MACD is also bullish (MACD line crosses above the signal line). This should filter out some of the whipsaws. I will *not* change the sell signal at this point.
5.  **Modify Code:** I will implement the new logic in `strategy.py`.
6.  **Deploy & Notify:** The system will automatically execute my new `strategy.py`.

Here's the code modification:

1.  **Hypothesis Explanation:**  Adding MACD confirmation to the RSI buy signal will help filter out false buy signals in a trending market, potentially reducing losses from whipsaws.

2.  **Modified `strategy.py` Code:**
Resultado (Logs): PROFIT_LOSS_PCT: 0.00

