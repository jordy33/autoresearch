def evaluate_market(indicators: dict, balance: dict, rules: dict, current_price: float) -> dict:
        """
        Evaluates market conditions and returns a trading decision.
        """

        # 1. Extract indicators (Safe handling)
        rsi = indicators.get("RSI", 50)
        macd_data = indicators.get("MACD", {"macd": 0.0, "signal": 0.0})
        macd = macd_data.get("macd", 0.0)
        signal = macd_data.get("signal", 0.0)

        action = "HOLD"
        quantity = 0.0
        reason = "No signal"

        # 2. Add MACD confirmation
        if rsi < 30 and macd < signal:  # Buy signal: RSI oversold AND MACD bullish
            action = "BUY"
            usdt_free = float(balance.get("USDT", {}).get("free", 0))
            investment = usdt_free * 0.10
            min_notional = float(rules.get("min_notional", 5.0))
            if investment > min_notional:
                quantity = round(investment / current_price, 5)
                reason = f"RSI undersold: {rsi:.2f}, MACD bullish confirmation"

        elif rsi > 70 and macd > signal:  # Sell signal: RSI overbought AND MACD bearish
            action = "SELL"
            btc_free = float(balance.get("BTC", {}).get("free", 0))
            if btc_free > 0:
                quantity = round(btc_free * 0.5, 5)
                reason = f"RSI overbought: {rsi:.2f}, MACD bearish confirmation"

        return {"action": action, "quantity": quantity, "reason": reason}