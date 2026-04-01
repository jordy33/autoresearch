# Implementation Plan: Gaming Clips Automation (PoC)

## Phase 1: Preparation & Setup
- [ ] Create directory structure `projects/gaming_clips/poc/`.
- [ ] Install required system dependencies (e.g., `ffmpeg`).
- [ ] Setup virtual environment and install Python libraries (`faster-whisper`, `elevenlabs`, `pydub`, `opencv-python`, etc.).
- [ ] Obtain required assets:
  - Long gameplay video (`.mp4`).
  - Cloned ElevenLabs voice ID.
  - Royalty-free background music (`.mp3`).

## Phase 2: PoC Script Implementation (`demo.py`)
- [ ] **Step 1: Configuration & Setup**
  - Define all hardcoded constants (`HYPE_THRESHOLD`, `CLIP_DURATION`, `VOICE_ID`, etc.).
  - Initialize `WhisperModel` and `ElevenLabs` clients.
- [ ] **Step 2: Hype Detection**
  - Implement `detect_hype_segments()` to transcribe audio and find the moment with the highest energy or specific keywords (e.g., "epico", "kill", "insano").
- [ ] **Step 3: Video Cutting**
  - Use `subprocess` to call `ffmpeg` to extract a 30s vertical segment (1080x1920) centered around the hype moment.
- [ ] **Step 4: AI Voiceover Generation**
  - Create a dynamic prompt based on the detected action.
  - Call ElevenLabs API to synthesize speech and save to `voiceover.mp3`.
- [ ] **Step 5: Audio Mixing**
  - Use `pydub` to overlay original audio, AI voiceover, and background music.
  - Export `final_audio.mp3`.
- [ ] **Step 6: Final Assembly & Output**
  - Use `ffmpeg` to merge the vertical video segment with the newly mixed audio track into `final_demo.mp4`.
  - Generate and print the formatted caption string to the console.

## Phase 3: Execution & Validation
- [ ] Run `python demo.py` and verify successful execution.
- [ ] Review the generated `final_demo.mp4` for correct cutting, voiceover quality, and audio balance.
- [ ] Manually publish the clip to TikTok and YouTube Shorts.
- [ ] Track views and affiliate link clicks over the next 48 hours.
