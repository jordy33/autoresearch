# Universal Auto-Research Framework

This repository provides a framework for autonomous AI-driven research and optimization. It allows AI agents to continuously experiment and improve code across multiple projects simultaneously, using a scientific method of harvesting past results, generating hypotheses, and deploying changes.

## Repository Structure

```
autoresearch/
├── core/
│   └── orchestrator.py       # Universal agent that executes the scientific loop for each project
├── projects/
│   └── karpathy_model/       # Example project: LLM training optimizer
│       ├── config.json       # Project settings (metrics, target files, test commands)
│       ├── program.md        # Instructions/prompt for the AI agent
│       ├── resource.md       # Log of past experiments and results
│       ├── train.py          # Code being optimized
│       ├── prepare.py        # Data preparation script
│       └── analysis.ipynb    # Jupyter notebook for analysis
├── archive/                  # Paused/disabled projects
├── daemon.py                 # Background service that schedules project runs
├── pyproject.toml            # Project dependencies and configuration
├── test_gemini.py            # Test script for Gemini integration
├── install-gemini.md         # Installation guide for Gemini CLI
├── install-gemini-es.md      # Spanish version of Gemini installation guide
└── README.md                 # This file
```

## How It Works

### The Daemon
- `daemon.py` runs continuously in the background, checking the `projects/` directory every minute.
- It spawns `orchestrator.py` for each active project based on their configured intervals.
- Uses a lock file system to prevent overlapping runs.

### The Scientific Loop
For each project, the orchestrator performs:
1. **Harvest:** Reads `resource.md` to learn from past experiments.
2. **Generate:** Uses `program.md` and current code to create a new hypothesis.
3. **Deploy:** Applies changes, runs tests, and logs results to `resource.md`.

## Managing Projects

### Creating a New Project
1. Create a folder in `projects/` (e.g., `projects/my_project/`).
2. Add the target code file (e.g., `script.py`).
3. Create `program.md` with agent instructions.
4. Add `config.json` with settings like:
   ```json
   {
     "project_name": "My Project",
     "metric": {
       "name": "accuracy",
       "goal": "maximize",
       "feedback_signal": "Accuracy"
     },
     "experiment": {
       "target_file": "script.py",
       "test_method": "python test.py",
       "duration_minutes": 5
     },
     "agent_settings": {
       "model": "gemini-2.5-pro",
       "temperature": 0.7
     }
   }
   ```

### Pausing a Project
Move the project folder to `archive/`:
```bash
mv projects/my_project archive/
```

## Quick Start (Karpathy Model Example)

**Requirements:** NVIDIA GPU, Python 3.10+, uv package manager.

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Prepare data (one-time setup for the Karpathy project)
uv run projects/karpathy_model/prepare.py
```

### Note on `prepare.py` (Specific to this example)
The `prepare.py` script is **exclusive to the Karpathy LLM project**; you do not need a script like this for general projects (like trading bots or web scrapers) unless your project specifically requires complex data preprocessing. 

For the LLM example, it performs the following critical setup:
1. **Downloads Data:** Connects to Hugging Face and downloads shards of the climbmix-400b-shuffle dataset. 
2. **Trains a BPE Tokenizer:** Trains a custom Byte Pair Encoding tokenizer from scratch using the downloaded data so the model can learn a vocabulary of 8192 tokens.
3. **Prepares the BPB (Bits Per Byte) Metric:** Creates a byte-size lookup table (`token_bytes.pt`). This is fundamental for the agent to calculate its success metric (`val_bpb`). Without it, the agent wouldn't know if its changes actually improved the model.
4. **Intelligent Caching:** Saves everything in `~/.cache/autoresearch/` so the data and tokenizer remain ready even if you reset the project code.

Without running this script, `train.py` would have no data and no vocabulary, leaving the agent unable to train or measure its progress.

```bash
# Set API key and start daemon
export GOOGLE_API_KEY="your-key-here"
uv run daemon.py
```

The daemon will optimize the LLM training code in `projects/karpathy_model/train.py` autonomously.

## Running 24/7 in Production (Supervisor)

If you close your terminal, `uv run daemon.py` will stop. To keep the framework running perpetually in the background, it's highly recommended to use **Supervisor**.

1. **Install Supervisor:**
   ```bash
   sudo apt update
   sudo apt install supervisor
   ```

2. **Configure the Daemon:**
   We have included a template file named `autoresearch.conf`. Edit this file to add your real `GOOGLE_API_KEY` (and ensure the paths match your user setup).

3. **Link and Start:**
   Copy or symlink the config to Supervisor's directory, then update the process list:
   ```bash
   sudo cp autoresearch.conf /etc/supervisor/conf.d/
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start autoresearch
   ```

Now the orchestrator will run 24/7, even if you disconnect from your server. You can check the logs anytime at `daemon.out.log` and `daemon.err.log` or view the status using `sudo supervisorctl status`.

## License

MIT