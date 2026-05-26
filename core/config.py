import os
from pathlib import Path
from dotenv import load_dotenv

SYCRONIX_DIR = Path.home() / ".sycronix"
SYCRONIX_DIR.mkdir(parents=True, exist_ok=True)
ENV_FILE = SYCRONIX_DIR / ".env"
HISTORY_FILE = SYCRONIX_DIR / "history.txt"
MEMORY_FILE = SYCRONIX_DIR / "memory.db"
NOTES_FILE = SYCRONIX_DIR / "notes.json"
WORKFLOWS_DIR = SYCRONIX_DIR / "workflows"
PROGRESS_FILE = SYCRONIX_DIR / "progress.json"
LEADERBOARD_FILE = SYCRONIX_DIR / "leaderboard.json"

load_dotenv(ENV_FILE)

def get_api_key():
    key = os.getenv("OPENROUTER_API_KEY") or os.getenv("API_KEY")
    return key

def set_api_key(key):
    with open(ENV_FILE, "w") as f:
        f.write(f"OPENROUTER_API_KEY={key}\n")

def clear_api_key():
    if ENV_FILE.exists():
        ENV_FILE.unlink()

def config_path():
    return str(SYCRONIX_DIR)
