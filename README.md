# Universal Auto-Research Framework

This repository provides a framework for autonomous AI-driven research and optimization. It allows AI agents to continuously experiment and improve code across multiple projects simultaneously, using a scientific method of harvesting past results, generating hypotheses, and deploying changes.

## Repository Structure

```
autoresearch/
├── core/
│   └── orchestrator.py       # Universal agent that executes the scientific loop
├── projects/
│   └── binance_trading/      # CURRENT PROJECT: Autonomous Bitcoin Trading
│       ├── config.json       # Project settings (MCP, Telegram, Metrics)
│       ├── program.md        # Scientific directives for the AI Researcher
│       ├── resource.md       # Long-term memory (Experiment logs)
│       ├── strategy.py       # Trading logic being evolved by the AI
│       └── dry_run.py        # High-speed market simulator (Dry Run)
├── archive/                  # Paused projects (e.g., Karpathy Model)
├── daemon.py                 # Background service scheduler
├── autoresearch.conf         # Supervisor configuration (Production)
└── .env                      # Environment secrets (API Keys, Bot Tokens)
```

## Featured Project: Bitcoin Binance Automated Trading (Auto-Researcher)

This project uses the framework to evolve a Bitcoin trading strategy autonomously using the **Model Context Protocol (MCP)** to interact with live market data.

### Key Features
- **Brain:** Powered by `gemini-2.0-flash-lite` for fast, cost-effective iterations.
- **Data Source:** Uses the **Model Context Protocol (MCP)** as the interface to Binance market feeds (SSE). The SSE endpoint is configurable in `projects/binance_trading/config.json`.
- **Simulation:** Uses `dry_run.py` to test every new code variant against 500 hours of historical data before deployment.
- **Feedback Loop:** The agent reads its own failures (Tracebacks) and successes (Profit/Loss %) from `resource.md` to learn.
- **Reporting:** Sends daily morning summaries (8:00 AM Mexico Time) and critical alerts via **Telegram Bot**.

## When Auto-Research Works
- **Works great for autoresearch:**
  - Fast feedback (hours)
  - Clear metric (reply rate, CIR)
  - API access to change inputs
- **Other potential projects:**
  - Cold email
  - Landing pages
  - Ad copy
- **Example goals:**
  - Complex sales
  - Brand building
  - Relationship selling
- **Not ideal for:**
  - Slow feedback (months)
  - Fuzzy metrics
  - Manual-only changes

## Code & MCP Server
MCP is required as the interface to Binance (SSE) for live trading.

You can implement and run an MCP server using the code from:

**Source Code:** https://github.com/jordy33/binance_mcp

### Technical Stack
- **AI:** Google Gemini (Generative AI).
- **Communication:** Model Context Protocol (MCP) for tool-use.
- **Process Management:** Supervisor (for 24/7 autonomous operation).
- **Environment:** Python with `uv` for lightning-fast dependency management.

## How It Works (The Scientific Loop)

For each project, the orchestrator performs:
1. **Harvest:** Reads `resource.md` to learn from past experiments and results.
2. **Generate:** Uses `program.md` to formulate a new hypothesis and modifies `strategy.py`.
3. **Deploy (Dry Run):** Executes `dry_run.py` to calculate the `profit_loss_pct`.
4. **Learn:** Logs the results and code changes back to `resource.md`.

## Production Setup (Supervisor)

To keep the research loop running 24/7 in the background:

1. **Configure:** Edit `autoresearch.conf` with your `GOOGLE_API_KEY`, `TELEGRAM_BOT_TOKEN`, and `TELEGRAM_CHAT_ID`.
2. **Timezone:** The framework is configured to `America/Mexico_City` for localized reporting.
3. **Start Service:**
   ```bash
   sudo cp autoresearch.conf /etc/supervisor/conf.d/
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl restart autoresearch
   ```

## Monitoring
- **Live Logs:** `sudo tail -f /var/log/autoresearch.out.log`
- **Error Tracking:** `sudo tail -f /var/log/autoresearch.err.log`
- **Memory:** Check `projects/binance_trading/resource.md` to see the AI's evolution.

---
*Inspired by the research automation patterns of Andrej Karpathy and Nick Saraev.*
