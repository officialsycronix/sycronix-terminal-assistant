#!/usr/bin/env python3
import os
from pathlib import Path

SYCRONIX_DIR = Path.home() / ".sycronix"
SYCRONIX_DIR.mkdir(parents=True, exist_ok=True)
ENV_FILE = SYCRONIX_DIR / ".env"

def main():
    current_key = ""
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            if line.startswith("OPENROUTER_API_KEY="):
                current_key = line.split("=", 1)[1]
                break

    print()
    print("╭──────────────────────────────────────────────╮")
    print("│        Sycronix API Key Setup               │")
    print("│        OfC SYCRONIX                         │")
    print("╰──────────────────────────────────────────────╯")
    print()

    if current_key:
        masked = current_key[:8] + "*" * 16 + current_key[-4:]
        print(f"Current API Key: {masked}")
        choice = input("Replace? (y/N): ").strip().lower()
        if choice != "y":
            print("Keeping existing key.")
            return

    key = input("Enter OpenRouter API Key: ").strip()
    if not key:
        print("No key provided. Aborting.")
        return

    ENV_FILE.write_text(f"OPENROUTER_API_KEY={key}\n")
    print()
    print(f"Key saved to {ENV_FILE}")
    print()
    print("You can now run: python3 main.py ai")
    print()

if __name__ == "__main__":
    main()
