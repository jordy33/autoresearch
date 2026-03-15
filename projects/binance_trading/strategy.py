def evaluate_market(indicators: dict, balance: dict, rules: dict, current_price: float) -> dict:
    """
    Evaluates market conditions and returns a trading decision.
    """

    # 1. Extract indicators (Safe handling)
    rsi = indicators.get("RSI", 50)
    sma = indicators.get("SMA", {}).get("20", 0.0)
    macd_line = indicators.get("MACD", {}).get("MACD", 0.0)
    signal_line = indicators.get("MACD", {}).get("signal", 0.0)
    previous_macd_line = indicators.get("MACD", {}).get("previous_macd", 0.0)
    previous_signal_line = indicators.get("MACD", {}).get("previous_signal", 0.0)
    atr = indicators.get("ATR", 0.0)

    action = "HOLD"
    quantity = 0.0
    reason = "No signal"
    take_profit_pct = 0.07  # 7% take-profit

    # 2. RSI, SMA, and MACD Strategy

    if (
        rsi < 35
        and current_price > sma
    ):
        action = "BUY"
        usdt_free = float(balance.get("USDT", {}).get("free", 0))
        investment = usdt_free * 0.10  # Invest 10% of available USDT
        min_notional = float(rules.get("min_notional", 5.0))
        if investment > min_notional:
            quantity = round(investment / current_price, 5)
            reason = f"BUY Signal: RSI oversold {rsi:.2f}, Price above SMA {sma:.2f}"

    elif (
        rsi > 65
        and current_price < sma
        and macd_line < signal_line
        and previous_macd_line >= previous_signal_line
    ):
        action = "SELL"
        btc_free = float(balance.get("BTC", {}).get("free", 0))
        if btc_free > 0:
            quantity = round(btc_free * 0.5, 5)  # Sell 50% of BTC holdings
            reason = f"SELL Signal: RSI overbought {rsi:.2f}, Price below SMA {sma:.2f}, MACD cross"

    return {"action": action, "quantity": quantity, "reason": reason}