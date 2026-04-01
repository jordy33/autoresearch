# Product Specification: Gaming Clips Automation (PoC)

## 1. Objective
Develop a Proof of Concept (PoC) for an automated gaming clip generation pipeline. The script will take a long gameplay video, automatically detect an "epic" moment, and generate a short, ready-to-publish clip featuring AI-generated hype voiceover, background music, and a caption.

## 2. Scope & Constraints
- **Fully Automated Editing:** No manual video editing allowed. The script handles cutting, audio mixing, and caption generation.
- **Fixed Parameters:** The PoC will use hardcoded parameters (hype threshold, voice style, etc.) without an optimization loop.
- **Manual Publishing:** The final video output will be uploaded manually to TikTok and YouTube Shorts. API integration is out of scope for the PoC.
- **Monetization Goal:** Achieve the first $1 via affiliate links (e.g., Epic Games Creator Code or Roblox equivalents).

## 3. System Architecture & Flow
1. **Input:** Long `.mp4` gameplay recording (OBS).
2. **Analysis:** `faster-whisper` transcribes audio to detect "hype" moments based on keywords and audio energy levels.
3. **Video Processing:** `ffmpeg` cuts the video to a 30-second vertical format (1080x1920) centered on the hype moment.
4. **Voiceover:** `elevenlabs` API generates a custom voiceover based on the detected highlight description.
5. **Audio Mixing:** `pydub` layers the original audio (diminished), the AI voiceover, and royalty-free music.
6. **Output:** The final video with mixed audio and a dynamically generated caption text ready for upload.

## 4. Technical Requirements
- **Language:** Python 3.10+
- **External Dependencies:** FFmpeg
- **Libraries:** `faster-whisper`, `elevenlabs`, `pydub`, `requests`, `opencv-python`, `yt-dlp`

## 5. Fixed Configuration (PoC)
- `HYPE_THRESHOLD`: 0.75
- `CLIP_DURATION`: ~30 seconds (15-45 range)
- `VOICE_STYLE`: Energetic, hype gamer voice.
- `MUSIC_VOLUME`: 0.25 (25% of main volume)
