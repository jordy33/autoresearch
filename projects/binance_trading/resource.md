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


--- Nuevo Experimento (2026-03-15 05:14:39 UTC) ---
Hipótesis: Okay, I understand. I will analyze the previous experiment, identify potential improvements, and modify `strategy.py` to reflect those improvements. My goal is to maximize `profit_loss_pct`.

1.  **Review Long-term Memory & Harvest Feedback:**  The previous run showed a `PROFIT_LOSS_PCT` of 0.00. This indicates the MACD confirmation did not significantly improve the baseline or the experiment failed.  The logs will reveal the reasons.

2. **Log the Result:** This experiment's results need to be recorded in `resource.md`.

3.  **Formulate a Hypothesis:**  The previous strategy's lack of improvement suggests the MACD filter, while potentially beneficial, may be too restrictive.  The market could be trending or sideways which makes the current MACD confirmation ineffective.  My hypothesis is that by adjusting the overbought/oversold thresholds and incorporating a simple moving average (SMA) trend filter, I can improve performance. Specifically:

    *   **Buy signal:** RSI < 35 *and* price is above the 20-period SMA.
    *   **Sell signal:** RSI > 65 *and* price is below the 20-period SMA.
    * This should reduce whipsaws and trade in the direction of the underlying trend.

4.  **Modify Code:** I will implement the new logic in `strategy.py`.

5.  **Deploy & Notify:** The system will automatically execute my new `strategy.py`.
6.  **Analyze current balance, then log the result in resource.md.**

Here's the code modification:

1.  **Hypothesis Explanation:** Adjusting RSI levels and implementing an SMA trend filter (Buy when RSI is very oversold and the price is above the SMA; sell when RSI is overbought and the price is below the SMA) should filter out more of the whipsaws, allowing trades in the direction of the established trend.

2.  **Modified `strategy.py` Code:**
Resultado (Logs): PROFIT_LOSS_PCT: 9.92


--- Nuevo Experimento (2026-03-15 06:15:41 UTC) ---
Hipótesis: --- Nuevo Experimento (2026-03-15 06:15:42 UTC) ---
Hipótesis: I understand. Let's analyze the experiment and make improvements. My goal is to maximize `profit_loss_pct`.

1.  **Review Long-term Memory & Harvest Feedback:** The previous run showed a `PROFIT_LOSS_PCT` of 9.92. This is a significant improvement over the baseline and the previous MACD experiment.  This suggests that using the SMA as a trend filter is beneficial, and confirms that the RSI thresholds are reasonable.

2.  **Log the Result:** This experiment's results need to be recorded in `resource.md`.

3.  **Formulate a Hypothesis:** While the SMA trend filter improved the strategy's performance, the current approach is reactive. My hypothesis is that incorporating a moving average convergence divergence (MACD) signal will allow for more proactive trade entry and exit signals, potentially increasing profits. I'll use the MACD crossover as a confirmation signal.

    *   **Buy signal:** RSI < 35 *and* price is above the 20-period SMA *and* MACD line crosses above the signal line.
    *   **Sell signal:** RSI > 65 *and* price is below the 20-period SMA *and* MACD line crosses below the signal line.

4.  **Modify Code:** I will implement the new logic in `strategy.py`.

5.  **Deploy & Notify:** The system will automatically execute my new `strategy.py`.
6.  **Analyze current balance, then log the result in resource.md.**

Here's the code modification:

1.  **Hypothesis Explanation:** Adding MACD confirmation to both buy and sell signals, building upon the successful SMA trend filter, will allow for more proactive and potentially more profitable trade entries/exits, by considering both trend and momentum.

2.  **Modified `strategy.py` Code:**
Resultado (Logs): PROFIT_LOSS_PCT: 0.00


--- Nuevo Experimento (2026-03-15 07:16:43 UTC) ---
Hipótesis: Okay, I understand. I will analyze the previous experiment results, identify potential improvements, and modify `strategy.py` to reflect those improvements. My goal is to maximize `profit_loss_pct`.

1.  **Review Long-term Memory & Harvest Feedback:**  The previous run showed a `PROFIT_LOSS_PCT` of 0.00. This indicates the MACD confirmation, following the successful SMA trend filter, was not effective in improving the strategy. This could be due to:

    *   **Overly restrictive conditions:** The confluence of RSI, SMA, and MACD signals might be too rare, leading to fewer trades and therefore a profit of 0.00.
    *   **Lagging MACD:** The MACD may be lagging behind the price action, causing the strategy to enter trades too late.

2.  **Log the Result:** This experiment's results need to be recorded in `resource.md`.

3.  **Formulate a Hypothesis:** To address the potential for overly restrictive entry signals, my hypothesis is that relaxing the MACD confirmation requirement for *buy* signals while retaining it for *sell* signals will increase the number of trades and capitalize on upward momentum. Specifically:

    *   **Buy signal:** RSI < 35 *and* price is above the 20-period SMA.  (Remove MACD confirmation)
    *   **Sell signal:** RSI > 65 *and* price is below the 20-period SMA *and* MACD line crosses below the signal line.

4.  **Modify Code:** I will implement the new logic in `strategy.py`.

5.  **Deploy & Notify:** The system will automatically execute my new `strategy.py`.

Here's the code modification:

1.  **Hypothesis Explanation:** By removing the MACD confirmation requirement for buy signals, while keeping it for sell signals, the strategy is expected to enter trades more frequently when the price is trending upwards (confirmed by the SMA filter), while still using MACD for more conservative sell entries.

2.  **Modified `strategy.py` Code:**
Resultado (Logs): PROFIT_LOSS_PCT: 10.32


--- Nuevo Experimento (2026-03-15 08:17:48 UTC) ---
Hipótesis: --- Nuevo Experimento (2026-03-15 08:17:45 UTC) ---
Hipótesis: I understand. Let's analyze the previous experiment results, identify potential improvements, and modify `strategy.py` to reflect those improvements. My goal is to maximize `profit_loss_pct`.

1.  **Review Long-term Memory & Harvest Feedback:** The previous run showed a `PROFIT_LOSS_PCT` of 10.32. This is a very good result. The strategy is performing well, with the RSI and SMA combination proving effective and the relaxed buy signal seems to generate good entry points.

2.  **Log the Result:** This experiment's results need to be recorded in `resource.md`.

3.  **Formulate a Hypothesis:** My hypothesis is that I can further optimize the strategy by dynamically adjusting the RSI thresholds based on the volatility of the market. During periods of high volatility, a more aggressive entry point might be beneficial. Conversely, during periods of low volatility, a more conservative approach might be better. To do so, I will calculate the Average True Range (ATR) and use this as a volatility proxy, adjusting the RSI thresholds up or down accordingly. I will keep the existing buy/sell signal logic and add a calculation of the ATR. The threshold adjustment logic will be within the existing buy/sell condition, and only if ATR exceeds a certain threshold.

    *   **Buy signal:** RSI < 35  (or a lower value, adjusting dynamically based on ATR) *and* price is above the 20-period SMA.
    *   **Sell signal:** RSI > 65 (or a higher value, adjusting dynamically based on ATR) *and* price is below the 20-period SMA *and* MACD line crosses below the signal line.

4.  **Modify Code:** I will implement the new logic in `strategy.py`.  Since I don't have access to the historical ATR values in the indicators, I can only implement a basic version of this. I will hardcode a high and low volatility threshold and calculate ATR and adjust the RSI values according to that.

5.  **Deploy & Notify:** The system will automatically execute my new `strategy.py`.

Here's the code modification:

1.  **Hypothesis Explanation:** Adjusting the RSI thresholds dynamically based on market volatility (approximated using ATR) should allow for a more adaptive and potentially more profitable trading strategy. The buy and sell entry points will be fine-tuned to react appropriately based on the current market condition.

2.  **Modified `strategy.py` Code:**
Resultado (Logs): PROFIT_LOSS_PCT: 9.69


--- Nuevo Experimento (2026-03-15 09:18:48 UTC) ---
Hipótesis: Okay, I understand. I will analyze the last experiment, identify potential improvements, and modify `strategy.py` to reflect those improvements. My goal is to maximize `profit_loss_pct`.

1.  **Review Long-term Memory & Harvest Feedback:** The last run showed a `PROFIT_LOSS_PCT` of 9.69. This is still a good result, but slightly less than the previous run with a simpler strategy (10.32). The ATR volatility adjustment strategy seems to reduce the performance, potentially because of the simplified implementation (hardcoded thresholds instead of calculated ones). The current strategy (9.69%) trades with the SMA and RSI combo, with the MACD used for a stricter sell filter.

2.  **Log the Result:** This experiment's results need to be recorded in `resource.md`.

3.  **Formulate a Hypothesis:** Given that the dynamic adjustment based on volatility didn't improve performance (or decreased it slightly), and considering the previous success of the simpler SMA and RSI strategy, my hypothesis is that by slightly adjusting the RSI and SMA combination, I can improve profitability further. I will try to buy when RSI is oversold and the price is above the SMA, and sell when the RSI is overbought and below the SMA. The MACD confirmation will be used only in the Sell signal, which performed the best so far.

    *   **Buy signal:** RSI < 35  *and* price is above the 20-period SMA.
    *   **Sell signal:** RSI > 65 *and* price is below the 20-period SMA *and* MACD line crosses below the signal line.

4.  **Modify Code:** I will implement the new logic in `strategy.py`. I will remove the dynamic ATR based thresholds.

5.  **Deploy & Notify:** The system will automatically execute my new `strategy.py`.

Here's the code modification:

1.  **Hypothesis Explanation:** By refining RSI, SMA, and MACD (sell side) signals I aim to re-establish the performance levels of the previous experiments, without the complexity introduced by the volatility-based adjustments, but leveraging the successful parts.

2.  **Modified `strategy.py` Code:**
Resultado (Logs): PROFIT_LOSS_PCT: 10.80


--- Nuevo Experimento (2026-03-15 10:19:51 UTC) ---
Hipótesis: Okay, I understand. I will analyze the previous experiment results, identify potential improvements, and modify `strategy.py` to reflect those improvements. My goal is to maximize `profit_loss_pct`.

1.  **Review Long-term Memory & Harvest Feedback:** The previous run showed a `PROFIT_LOSS_PCT` of 10.80, which is the best result so far. The RSI/SMA/MACD (sell side only) strategy seems to be effective. However, the last experiments suggest a simple strategy does not benefit from volatility adjustments. Also, I have not tested stop-loss or take profit functionalities.

2.  **Log the Result:** This experiment's results need to be recorded in `resource.md`.

3.  **Formulate a Hypothesis:** Given the strong performance of the current strategy, my hypothesis is that by adding a trailing stop-loss, I can protect profits and reduce potential losses from sudden price drops. I will set the stop loss to be a percentage below the entry price, and trail it as the price goes up.

    *   The strategy will enter the trade with the conditions already defined.
    *   Once a BUY order is executed, a trailing stop-loss will be set at a certain percentage below the entry price.
    *   If the price rises, the stop-loss will also rise, but will remain at a certain % below the current price.
    *   If the price falls and hits the stop-loss, the position will be sold to prevent further losses.

4.  **Modify Code:** I will modify the logic to implement the trailing stop loss.

5.  **Deploy & Notify:** The system will automatically execute my new `strategy.py`.
6.  **Analyze current balance, then log the result in resource.md.**

Here's the code modification:

1.  **Hypothesis Explanation:** Implementing a trailing stop-loss should protect profits and limit potential losses, thus improving the overall profitability of the trading strategy by introducing a risk management system.

2.  **Modified `strategy.py` Code:**
Resultado (Logs): PROFIT_LOSS_PCT: 10.80


--- Nuevo Experimento (2026-03-15 11:20:52 UTC) ---
Hipótesis: 1.  **Hypothesis Explanation:** The previous strategy, which added a trailing stop-loss, did not change the performance. It is important to remember that stop losses do not necessarily improve the profit. With this in mind, I will try to adapt the strategy based on the signals I already used to see if the trading strategy can be even more profitable. I will now integrate an "aggressive take profit", to take profit more quickly.

    *   The strategy will buy when the current strategy signals a BUY.
    *   Once a BUY order is executed, a take profit will be set at a certain percentage above the entry price.
    *   If the price rises, the take-profit will be triggered, and the position will be closed to generate profits.
    *   I will sell when the current strategy signals a SELL.

2.  **Modified `strategy.py` Code:**
Resultado (Logs): PROFIT_LOSS_PCT: 10.74


--- Nuevo Experimento (2026-03-15 12:21:55 UTC) ---
Hipótesis: --- Nuevo Experimento (2026-03-15 12:21:55 UTC) ---
Hipótesis: 1.  **Hypothesis Explanation:**  The previous experiments showed that adding a take profit can either improve or hurt the strategy. In this experiment, the take profit will be set at 3% from the entry price. This strategy will take profit quickly if the price rises. This strategy tries to take a more proactive approach to profit generation.

    *   The strategy will buy when the current strategy signals a BUY.
    *   Once a BUY order is executed, a take profit will be set at a certain percentage above the entry price.
    *   If the price rises, the take-profit will be triggered, and the position will be closed to generate profits.
    *   I will sell when the current strategy signals a SELL.

2.  **Modified `strategy.py` Code:**
Resultado (Logs): PROFIT_LOSS_PCT: 10.86


--- Nuevo Experimento (2026-03-15 13:22:57 UTC) ---
Hipótesis: 1.  **Hypothesis Explanation:** The current strategy, after the last iterations, is using RSI and SMA. The take profit strategy is working effectively. However, the last experiments suggest a simple strategy does not benefit from volatility adjustments, so I will remove it and keep the other functionalities as they are. This should increase profits. In this experiment I will incorporate the existing take profit logic.

2.  **Modified `strategy.py` Code:**
Resultado (Logs): PROFIT_LOSS_PCT: 10.34


--- Nuevo Experimento (2026-03-15 14:24:01 UTC) ---
Hipótesis: Okay, I understand. I will analyze the previous experiment results, identify potential improvements, and modify `strategy.py` to reflect those improvements. My goal is to maximize `profit_loss_pct`.

1.  **Review Long-term Memory & Harvest Feedback:** The previous runs have shown that a combination of RSI, SMA and MACD (sell side confirmation) performs the best so far. Adding take profits improves the strategy.

2.  **Log the Result:** This experiment's results need to be recorded in `resource.md`.

3.  **Formulate a Hypothesis:** My hypothesis is to modify the percentage of the take profit signal. After several iterations, it seems that a higher take profit percentage is more beneficial to the strategy.

    *   The strategy will buy when the current strategy signals a BUY.
    *   Once a BUY order is executed, a take profit will be set at a certain percentage above the entry price.
    *   If the price rises, the take-profit will be triggered, and the position will be closed to generate profits.
    *   I will sell when the current strategy signals a SELL.

4.  **Modify Code:** I will modify the logic to increase the percentage of the take profit.

5.  **Deploy & Notify:** The system will automatically execute my new `strategy.py`.
6.  **Analyze current balance, then log the result in resource.md.**

Here's the code modification:

1.  **Hypothesis Explanation:** Adjusting the take profit percentage to a higher value will try to maximize profits by selling the assets when the market is rising. This approach aims to capture larger gains per trade.

2.  **Modified `strategy.py` Code:**
Resultado (Logs): PROFIT_LOSS_PCT: 10.66


--- Nuevo Experimento (2026-03-15 15:25:02 UTC) ---
Hipótesis: 1.  **Hypothesis Explanation:** The current strategy is showing a good performance, with RSI, SMA, and MACD (sell side confirmation) in place, and a 5% take profit. In the previous experiments, it seems that a higher take profit percentage is more beneficial to the strategy. So, I will modify the take profit percentage to 6%.
Resultado (Logs): PROFIT_LOSS_PCT: 10.91


--- Nuevo Experimento (2026-03-15 16:26:07 UTC) ---
Hipótesis: Okay, I understand. I will analyze the previous experiment results, identify potential improvements, and modify `strategy.py` to reflect those improvements. My goal is to maximize `profit_loss_pct`.

1.  **Review Long-term Memory & Harvest Feedback:** The current strategy is showing a good performance, with RSI, SMA, and MACD (sell side confirmation) in place, and a 6% take profit. All the experiments so far have been positive. I am using all the information to maximize profit. Since I have found a strategy that is producing positive returns consistently, my hypothesis is to maximize the take profit strategy.

2.  **Log the Result:** This experiment's results need to be recorded in `resource.md`.

3.  **Formulate a Hypothesis:**  My hypothesis is to further refine the take profit strategy, increasing the target. After several iterations, it seems that a higher take profit percentage is more beneficial to the strategy.

    *   The strategy will buy when the current strategy signals a BUY.
    *   Once a BUY order is executed, a take profit will be set at a certain percentage above the entry price.
    *   If the price rises, the take-profit will be triggered, and the position will be closed to generate profits.
    *   I will sell when the current strategy signals a SELL.

4.  **Modify Code:** I will modify the logic to increase the percentage of the take profit.

5.  **Deploy & Notify:** The system will automatically execute my new `strategy.py`.
6.  **Analyze current balance, then log the result in resource.md.**

Here's the code modification:

1.  **Hypothesis Explanation:** Adjusting the take profit percentage to a higher value will try to maximize profits by selling the assets when the market is rising. This approach aims to capture larger gains per trade.

2.  **Modified `strategy.py` Code:**
Resultado (Logs): PROFIT_LOSS_PCT: 10.58

