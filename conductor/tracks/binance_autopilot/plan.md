# Binance Autopilot - Implementation Plan

## Phase 1: The Promotion Engine
- [ ] Define the exact mathematical criteria for promotion (e.g., minimum win rate, minimum profit percentage over a sliding window of recent experiments in `resource.md`).
- [ ] Create `promote.py`: A script that reads `projects/binance_trading/resource.md` to evaluate the criteria.
- [ ] If criteria are met, `promote.py` automatically copies `strategy.py` to `projects/binance_live_trading/strategy.py`.
- [ ] Send Telegram Alert: "🟢 PROMOTION: Strategy X meets maturity criteria. Deploying to LIVE."

## Phase 2: The Demotion Engine (Circuit Breaker)
- [ ] Create a lightweight monitor `monitor_live.py` that runs alongside the live trader (or integrates into it).
- [ ] If the live account balance drops below the safety threshold (e.g., -5%), `monitor_live.py` kills the live trading process.
- [ ] `monitor_live.py` writes a failure report back into the lab's `resource.md` (e.g., "LIVE TRADING FAILED: Strategy degraded under live conditions. Adjust parameters.") so the AI knows its live strategy failed and why.
- [ ] Send Telegram Alert: "🔴 DEMOTION: Circuit breaker tripped. Live trading paused. Returning to lab."

## Phase 3: Orchestration
- [ ] Integrate `promote.py` and `monitor_live.py` into the main `daemon.py` or a dedicated cron job.
- [ ] Test the full loop in a "paper trading" mode before trusting the automated promotion with real funds.