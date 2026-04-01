# Binance Autopilot (Sim-to-Live Automation) - Specification

## Objective
Fully automate the lifecycle of the trading strategy by building an autonomous pipeline that promotes a winning strategy from the simulation environment (`binance_trading`) to live execution (`binance_live_trading`), and demotes it back to simulation if live performance degrades (Circuit Breaker).

## Scope
- **Promotion Engine:** A script that evaluates if the dry-run strategy meets the maturity criteria (e.g., >15% consistent profit over X days). If met, it automatically copies `strategy.py` from the lab to the live project and starts the live daemon.
- **Demotion Engine (Circuit Breaker Trigger):** A live PnL monitor. If the live strategy hits a maximum drawdown limit (e.g., -5% daily), it automatically stops the live project and notifies the auto-researcher that the market regime has changed and it needs to adapt.
- **Telegram Alerts:** Notify the user of autonomous state changes (e.g., "🟢 STRATEGY PROMOTED TO LIVE", "🔴 CIRCUIT BREAKER TRIPPED - REVERTING TO LAB").

## Out of Scope
- Modifying the underlying AI research logic (handled by the base `binance_trading` track).
- Modifying the live execution logic (handled by the `binance_live_trading` track). This track focuses purely on the pipeline *between* them.