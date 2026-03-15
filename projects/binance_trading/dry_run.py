import asyncio
import json
import sys
import importlib
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

# Import the strategy dynamically so we can reload it if needed
import strategy

async def calculate_mock_rsi(closes, period=14):
    """Simple RSI calculation for the backtester."""
    if len(closes) < period + 1:
        return 50.0
    
    gains = 0
    losses = 0
    for i in range(1, period + 1):
        change = closes[-i] - closes[-(i+1)]
        if change > 0:
            gains += change
        else:
            losses -= change
            
    avg_gain = gains / period
    avg_loss = losses / period
    
    if avg_loss == 0:
        return 100.0
        
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

async def run_backtest():
    try:
        # Reload the strategy module to ensure we test the latest AI changes
        importlib.reload(strategy)
        
        async with sse_client("https://binance.armaddia.lat/sse") as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                await session.initialize()
                
                # 1. Fetch Historical Data (Last 500 hours)
                result = await session.call_tool("fetch_chart_data", {
                    "symbol": "BTCUSDT",
                    "interval": "1h",
                    "limit": 500
                })
                
                # Parse the data (assuming JSON string is returned in the text content)
                chart_data_str = result.content[0].text
                # Clean up formatting if it comes as a string representation of a list
                chart_data_str = chart_data_str.replace("'", '"')
                try:
                    chart_data = json.loads(chart_data_str)
                except json.JSONDecodeError:
                    # Fallback if the MCP server returns a slightly different format
                    # For a real robust system, we handle the specific MCP output format
                    print("Error parsing chart data from MCP.")
                    sys.exit(1)
                
                # 2. Get Rules to pass to strategy
                rules_result = await session.call_tool("get_symbol_rules", {"symbol": "BTCUSDT"})
                rules_str = rules_result.content[0].text.replace("'", '"')
                try:
                    rules = json.loads(rules_str)
                except:
                    # Mock rules if parsing fails for safety
                    rules = {"min_notional": 5.0, "lot_size": {"stepSize": 0.00001}}

                # 3. Initialize Mock Portfolio
                initial_usdt = 1000.0
                mock_balance = {
                    "USDT": {"free": initial_usdt, "locked": 0.0},
                    "BTC": {"free": 0.0, "locked": 0.0}
                }
                
                closes = []
                
                # 4. Run the simulation loop
                for candle in chart_data:
                    close_price = float(candle.get('close', 0))
                    if close_price == 0:
                        continue
                        
                    closes.append(close_price)
                    
                    # Mock indicators (Structured like real MCP results)
                    current_rsi = await calculate_mock_rsi(closes)
                    indicators = {
                        "RSI": current_rsi,
                        "MACD": {"macd": 0.0, "signal": 0.0, "histogram": 0.0},
                        "BollingerBands": {"upper": close_price * 1.02, "lower": close_price * 0.98}
                    } 
                    
                    # 5. Ask the AI strategy for a decision
                    try:
                        decision = strategy.evaluate_market(
                            indicators=indicators,
                            balance=mock_balance,
                            rules=rules,
                            current_price=close_price
                        )
                    except Exception as e:
                        # If the AI wrote broken code, it fails the backtest immediately
                        print(f"Strategy execution failed: {e}")
                        # Return a terrible score so the orchestrator discards this Challenger
                        print("PROFIT_LOSS_PCT: -100.00")
                        sys.exit(1)
                        
                    action = decision.get("action", "HOLD")
                    quantity = float(decision.get("quantity", 0.0))
                    
                    # 6. Execute Mock Trades
                    if action == "BUY" and quantity > 0:
                        cost = quantity * close_price
                        if mock_balance["USDT"]["free"] >= cost:
                            mock_balance["USDT"]["free"] -= cost
                            mock_balance["BTC"]["free"] += quantity
                            
                    elif action == "SELL" and quantity > 0:
                        if mock_balance["BTC"]["free"] >= quantity:
                            mock_balance["BTC"]["free"] -= quantity
                            revenue = quantity * close_price
                            mock_balance["USDT"]["free"] += revenue

                # 7. Calculate Final Value
                final_btc_value = mock_balance["BTC"]["free"] * closes[-1] if closes else 0
                final_total_value = mock_balance["USDT"]["free"] + final_btc_value
                
                profit_loss_pct = ((final_total_value - initial_usdt) / initial_usdt) * 100
                
                # 8. Output the EXACT format the orchestrator needs
                print(f"PROFIT_LOSS_PCT: {profit_loss_pct:.2f}")

    except Exception as e:
        print(f"Backtest error: {e}")
        # Negative massive score on infrastructural failure
        print("PROFIT_LOSS_PCT: -100.00")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(run_backtest())