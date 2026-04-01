# Implementation Plan: Gaming Clips Automation

## Phase 1: Tool Evaluation & TDD (Week 1)
- [ ] Create `projects/gaming_clips` directory.
- [ ] Record 1 long gameplay session (1-2 hours) of a favorite game to use as a test fixture.
- [ ] **TDD:** Evaluate Audio-to-Text (Transcription) tools.
    - [ ] Test YouTube auto-transcription via private upload API.
    - [ ] Test Google Ecosystem tools (e.g., Gemini 1.5 Pro audio processing) for highlight detection.
    - [ ] Compare accuracy, speed, and API ease-of-use.
- [ ] **TDD:** Evaluate Text-to-Speech (TTS) tools.
    - [ ] Test ElevenLabs (Free tier).
    - [ ] Test Amazon Text-to-Voice (Free tier).
    - [ ] Test Chatterbox TTS.
    - [ ] Test Google AI Studio Generate Speech.
    - [ ] Select the best tool based on voice quality (hype tone), cost, and API integration.
- [ ] Install FFmpeg locally and write TDD tests for basic video clipping/cropping commands.
- [ ] Finalize tool selection and record decisions.

## Phase 2: Project Scaffolding & Setup (Week 2)
- [ ] Create `config.json` with selected API keys (TTS, Transcription, YouTube, TikTok).
- [ ] Create `program.md` (Agent Instructions) reflecting the chosen tech stack.
- [ ] Create `resource.md` (Experiment Log).
- [ ] Fork or review base repositories (e.g., ShortGPT, AI-Youtube-Shorts-Generator) for reference.

## Phase 3: Core Pipeline & Validation (Week 3)
- [ ] Implement `clip_pipeline.py` using the selected tools (TDD approach).
- [ ] Generate 5 clips manually using the pipeline to verify output quality.
- [ ] Validate Virality Score and engagement manually.

## Phase 4: Automation & Distribution (Week 4)
- [ ] Implement `deploy.py` for automated posting to TikTok and YouTube Shorts.
- [ ] Post first 20 clips automatically.
- [ ] Connect `projects/gaming_clips` to `core/orchestrator.py` or setup daily cron job.
- [ ] Implement Telegram daily morning summary.

## Phase 5: Autoresearch Loop (Week 5+)
- [ ] Implement `strategy.py` with AI tunable parameters.
- [ ] AI agent starts reading `resource.md` to generate hypotheses.
- [ ] Auto-adjust parameters (hype, game focus, duration, etc.) based on feedback.
- [ ] Reach 1k followers -> Contact indie devs on Discord for promos.