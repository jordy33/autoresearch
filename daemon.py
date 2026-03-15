import os
import json
import time
import subprocess

PROJECTS_DIR = "projects"
CHECK_INTERVAL_SECONDS = 60

def run_daemon():
    print(f"Starting auto-research daemon. Checking '{PROJECTS_DIR}' every {CHECK_INTERVAL_SECONDS} seconds.")
    print("Press Ctrl+C to stop.")
    
    while True:
        if not os.path.exists(PROJECTS_DIR):
            print(f"Warning: {PROJECTS_DIR} directory not found.")
            time.sleep(CHECK_INTERVAL_SECONDS)
            continue

        for p in os.listdir(PROJECTS_DIR):
            p_path = os.path.join(PROJECTS_DIR, p)
            if not os.path.isdir(p_path):
                continue

            config_path = os.path.join(p_path, "config.json")
            if not os.path.exists(config_path):
                continue

            lock_file = os.path.join(p_path, ".lock")
            if os.path.exists(lock_file):
                # We can silently skip to avoid spamming the logs
                continue

            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
            except Exception as e:
                print(f"[{p}] Error reading config.json: {e}")
                continue

            experiment = config.get("experiment", {})
            interval_hours = experiment.get("loop_interval_hours", 0)
            interval_minutes = experiment.get("loop_interval_minutes", 0)
            
            interval_seconds = (interval_hours * 3600) + (interval_minutes * 60)
            if interval_seconds == 0:
                # Default to 1 hour if nothing is configured
                interval_seconds = 3600

            last_run_file = os.path.join(p_path, ".last_run")
            last_run_time = 0
            if os.path.exists(last_run_file):
                try:
                    with open(last_run_file, "r") as f:
                        last_run_time = float(f.read().strip())
                except:
                    pass

            now = time.time()
            if now - last_run_time >= interval_seconds:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Spawning orchestrator for: {p}")
                try:
                    subprocess.Popen(["/home/ubuntu/.local/bin/uv", "run", "core/orchestrator.py", p_path])
                except Exception as e:
                    print(f"[{p}] Failed to start orchestrator: {e}")
                    
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    try:
        run_daemon()
    except KeyboardInterrupt:
        print("\nDaemon stopped.")
