
# Universal Auto-Research Framework

## Product Vision
A universal framework for autonomous AI-driven code research and optimization. The system leverages AI agents to continuously hypothesize, experiment, and deploy code improvements across multiple projects simultaneously, following a scientific loop of harvesting, generating, and deploying.

## Target Audience
- AI Researchers
- Software Engineers optimizing models or algorithms
- Developers building autonomous systems

## Core Features
1. **Scientific Loop Orchestration:** Automates the cycle of hypothesis generation, experimentation, and results logging.
2. **Multi-Project Management:** Runs a background daemon (`daemon.py`) that manages multiple isolated projects with concurrent, lock-protected execution.
3. **Continuous Background Execution:** Supports 24/7 background operation via `uv run daemon.py` or a managed Supervisor process.
4. **Data Preprocessing & Validation:** Includes capabilities to orchestrate data preparation and validation metrics (e.g., training custom tokenizers and measuring BPB for the Karpathy LLM example).