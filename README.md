<div align="center">

# Sycronix

**Intelligent Terminal Assistant**  
*AI-powered terminal toolkit for Termux / Linux*

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Android%20|%20Linux-blueviolet)](https://termux.dev)

---

</div>

## Overview

Sycronix is an all-in-one AI-powered terminal toolkit built for **Termux (Android)** and **Linux**. It combines an AI chat assistant, smart command shell, Linux tutor, error fixer, note vault, workflow engine, and more into a single CLI.

```
python3 main.py --help
```

## Features

| Command | Description |
|---|---|
| `ai` | AI chat with OpenRouter (streaming responses) |
| `shell` | Describe what you want — AI writes & runs the command |
| `tutor` | Interactive Linux tutor with 10 lessons & quizzes |
| `translate` | Convert natural language to Linux commands |
| `fix` | Paste an error — AI explains & fixes it |
| `notes` | Persistent note vault with rich formatting |
| `workflow` | Multi-step automation engine (YAML/JSON) |
| `dashboard` | Real-time system overview |
| `memory` | Persistent key-value store for AI context |
| `settings` | Configure API key and paths |
| `version` | Version and platform info |

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/sycronix.git
cd sycronix

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up your API key
python3 setup_api.py

# 4. Launch
python3 main.py ai
```

> **No API key?** The `tutor`, `notes`, `dashboard`, `memory`, and `version` modes work fully offline.

## Requirements

- Python 3.10+
- [OpenRouter](https://openrouter.ai) API key (free for AI modes)

### Dependencies

```
rich          Terminal formatting & tables
typer         CLI framework
prompt_toolkit  Interactive input
httpx         HTTP client (OpenRouter API)
python-dotenv  Environment management
sqlalchemy    Memory storage
pyyaml        Workflow engine configs
markdown-it-py  Note rendering
pygments      Code highlighting
```

## Project Structure

```
sycronix/
├── main.py              CLI entry point
├── setup_api.py         API key setup script
├── requirements.txt     Python dependencies
├── ai/                  AI chat & provider
│   ├── chat.py          Interactive chat loop
│   └── provider.py      OpenRouter API client
├── shell/               Smart shell (AI → command)
│   └── smart_shell.py
├── tutor/               Linux tutor & quiz engine
│   ├── tutor.py         Interactive quiz loop
│   └── questions.py     2000+ question bank
├── tools/               Utility tools
│   ├── translator.py    NL → command translator
│   ├── error_fixer.py   Error diagnosis & fix
│   └── note_vault.py    Persistent notes
├── ui/                  Terminal UI components
│   ├── banner.py        Splash screen & dashboard
│   └── theme.py         Color theme & panel styling
├── memory/              Persistent storage
│   └── store.py         SQLAlchemy key-value store
├── workflows/           Workflow engine
│   └── engine.py        Multi-step automation
└── core/                Infrastructure
    ├── config.py        Paths & environment
    ├── logging_setup.py Structured logging
    └── utils.py         System info utilities
```

## AI Modes

### AI Chat (`python3 main.py ai`)
Streaming chat with `/clear`, `/save`, `/exit` commands. Maintains conversation context.

### Smart Shell (`python3 main.py shell`)
Say what you need in plain language — AI generates the command, shows it to you, and runs it on approval.

### Command Translator (`python3 main.py translate`)
```
> zip all .txt files into archive.tar.gz
→ tar -czf archive.tar.gz *.txt
```

### Error Fixer (`python3 main.py fix`)
```
> paste: bash: command not found: htop
→ AI explains the cause and suggests: pkg install htop
```

## Tutor Mode

10 progressive Linux lessons covering:

1. Navigation & File Management
2. File Operations (cp, mv, rm)
3. Permissions & Ownership
4. Process Management
5. Text Processing
6. Package Management
7. User Administration
8. Archiving & Compression
9. Networking
10. SSH & Remote Access

Each lesson includes live command examples and a 10-question quiz drawn from a **2000+ question bank**.

## Offline-First

The following modes work **without internet** or API key:

- `tutor` — Full quiz engine & lessons
- `notes` — Local note vault
- `dashboard` — System monitoring
- `memory` — Storage stats
- `version` — Version info
- `settings` — Configuration

## License

MIT — see [LICENSE](LICENSE)

---

<div align="center">

**ofc ~ SYCRONIX**

</div>
