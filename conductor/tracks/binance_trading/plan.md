# Implementation Plan: Binance Automated Trading

## Phase 1: Project Scaffolding
- [x] Move `karpathy_model` to `archive/`
- [x] Create Conductor track for Binance Trading
- [x] Create `projects/binance_trading` directory
- [x] Create `config.json` with MCP tool configuration.
- [x] Create `program.md` (Agent Instructions) with validated MCP tools.
- [x] Create `resource.md` (Experiment Log/Long-term Memory).

## Phase 2: Core Strategy & Baseline
- [x] Implement initial `strategy.py` (Baseline RSI).
- [ ] Create `backtest.py` / Execution engine.
    - [ ] Must connect to MCP Server (`https://binance.armaddia.lat/sse`).
    - [ ] Must produce a clean numeric output for `profit_loss_pct`.
- [ ] Set up environment variables (`.env`) for Binance and Telegram.
- [ ] Implement Telegram notification logic.
    - [ ] Phase 2A: Experiment-level notifications (Real-time feedback).
    - [ ] Phase 2B: Transition to Daily Morning Summary (Stable phase).

## Phase 3: Loop Integration
- [ ] Connect `projects/binance_trading` to `core/orchestrator.py`.
- [ ] Run first automated experiment iteration.
- [ ] Verify that findings and metrics are correctly logged in `resource.md`.
