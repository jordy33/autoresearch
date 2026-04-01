def evaluate_market(indicators, balance, rules, current_price):
    """
    Evaluate market conditions and return a trading decision.
    
    Args:
        indicators: Dict with RSI, MACD, and BollingerBands
        balance: Current portfolio balance
        rules: Binance symbol rules (min_notional, lot_size)
        current_price: Current price of the asset
    
    Returns:
        Dict with "action" ("BUY", "SELL", "HOLD") and "quantity"
    """
    # Placeholder baseline strategy: RSI-based mean reversion
    # Buy when RSI < 30 (oversold), Sell when RSI > 70 (overbought)
    
    rsi = indicators.get("RSI", 50.0)
    action = "HOLD"
    quantity = 0.0
    
    usdt_available = balance.get("USDT", {}).get("free", 0.0)
    btc_available = balance.get("BTC", {}).get("free", 0.0)
    
    min_notional = rules.get("min_notional", 5.0)
    lot_size = float(rules.get("lot_size", {}).get("stepSize", 0.00001))
    
    # BUY signal: RSI < 30 (oversold)
    if rsi < 30 and usdt_available >= min_notional:
        # Calculate maximum BTC we can buy with 20% of available USDT
        purchase_amount = usdt_available * 0.2
        if purchase_amount >= min_notional:
            quantity = purchase_amount / current_price
            # Round to lot size precision
            quantity = round(quantity / lot_size) * lot_size
            if quantity > 0:
                action = "BUY"
    
    # SELL signal: RSI > 70 (overbought)
    elif rsi > 70 and btc_available > 0:
        quantity = btc_available * 0.5  # Sell 50% of holdings
        # Round to lot size precision
        quantity = round(quantity / lot_size) * lot_size
        if quantity > 0:
            action = "SELL"
    
    return {"action": action, "quantity": quantity}