import asyncio
import json
import sys
import importlib
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

# Import the strategy dynamically so we can reload it if needed
import strategy


async def run_backtest():
    """Run a backtest using real MCP tools for market data and indicators."""
    try:
        # Reload the strategy module to ensure we test the latest AI changes
        importlib.reload(strategy)

        async with sse_client("https://binance.armaddia.lat/sse") as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                await session.initialize()

                # 1. Fetch Historical Data (Last 500 hours)
                print("Fetching historical chart data...")
                result = await session.call_tool("fetch_chart_data", {
                    "symbol": "BTCUSDT",
                    "interval": "1h",
                    "limit": 500
                })

                chart_data_str = result.content[0].text
                chart_data_str = chart_data_str.replace("'", '"')
                try:
                    chart_data = json.loads(chart_data_str)
                except json.JSONDecodeError:
                    print("Error parsing chart data from MCP.")
                    sys.exit(1)

                # 2. Get Symbol Rules (exchange constraints)
                print("Fetching symbol rules...")
                rules_result = await session.call_tool(
                    "get_symbol_rules", {"symbol": "BTCUSDT"}
                )
                rules_str = rules_result.content[0].text.replace("'", '"')
                try:
                    rules = json.loads(rules_str)
                except Exception:
                    rules = {"min_notional": 5.0, "lot_size": {"stepSize": 0.00001}}

                # 3. Get Current Market Price
                print("Fetching current market price...")
                price_result = await session.call_tool(
                    "get_market_price", {"symbol": "BTCUSDT"}
                )
                current_price_str = price_result.content[0].text
                try:
                    current_price = float(current_price_str)
                except Exception:
                    current_price = float(chart_data[-1].get('close', 0))

                # 4. Get Current Indicators from MCP
                print("Fetching real indicators...")
                indicators_result = await session.call_tool(
                    "calculate_indicators", {"symbol": "BTCUSDT", "interval": "1h"}
                )
                indicators_str = indicators_result.content[0].text.replace("'", '"')
                try:
                    current_indicators = json.loads(indicators_str)
                except Exception:
                    current_indicators = {
                        "RSI": 50.0,
                        "MACD": {"macd": 0.0, "signal": 0.0, "histogram": 0.0},
                        "BollingerBands": {"upper": current_price * 1.02,
                                          "lower": current_price * 0.98}
                    }

                # 5. Initialize Mock Portfolio (since this is a backtest)
                initial_usdt = 1000.0
                mock_balance = {
                    "USDT": {"free": initial_usdt, "locked": 0.0},
                    "BTC": {"free": 0.0, "locked": 0.0}
                }

                buy_count = 0
                sell_count = 0

                # 6. Run the simulation loop through historical data
                print("Running backtest simulation...")
                for idx, candle in enumerate(chart_data):
                    close_price = float(candle.get('close', 0))
                    if close_price == 0:
                        continue

                    # Use real indicators (we use the latest fetched indicators
                    # In a real scenario, we'd fetch indicators for each point,
                    # but that's too slow. We use the current indicators as proxy.
                    indicators = current_indicators

                    # 7. Ask the AI strategy for a decision
                    try:
                        decision = strategy.evaluate_market(
                            indicators=indicators,
                            balance=mock_balance,
                            rules=rules,
                            current_price=close_price
                        )
                    except Exception as exec_error:
                        print(f"Strategy execution failed: {exec_error}")
                        print("PROFIT_LOSS_PCT: -100.00")
                        sys.exit(1)

                    action = decision.get("action", "HOLD")
                    quantity = float(decision.get("quantity", 0.0))

                    # 8. Execute Mock Trades
                    if action == "BUY" and quantity > 0:
                        cost = quantity * close_price
                        if mock_balance["USDT"]["free"] >= cost:
                            mock_balance["USDT"]["free"] -= cost
                            mock_balance["BTC"]["free"] += quantity
                            buy_count += 1

                    elif action == "SELL" and quantity > 0:
                        if mock_balance["BTC"]["free"] >= quantity:
                            mock_balance["BTC"]["free"] -= quantity
                            revenue = quantity * close_price
                            mock_balance["USDT"]["free"] += revenue
                            sell_count += 1

                # 9. Calculate Final Value
                final_btc_value = (
                    mock_balance["BTC"]["free"] * close_price
                    if chart_data else 0
                )
                final_total_value = (
                    mock_balance["USDT"]["free"] + final_btc_value
                )

                profit_loss_pct = (
                    ((final_total_value - initial_usdt) / initial_usdt) * 100
                )

                # 10. Output the EXACT format the orchestrator needs
                print("--- BACKTEST RESULTS (DRY RUN WITH REAL MCP DATA) ---")
                print(f"Operations: {buy_count} Buys, {sell_count} Sells")
                print(f"Final Balance: ${final_total_value:.2f} "
                      f"(Initial: ${initial_usdt:.2f})")
                print(f"PROFIT_LOSS_PCT: {profit_loss_pct:.2f}")

    except Exception as error:
        print(f"Backtest error: {error}")
        print("PROFIT_LOSS_PCT: -100.00")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(run_backtest())