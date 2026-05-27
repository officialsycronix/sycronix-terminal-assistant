import subprocess, shlex, sys, os
if __name__ != "__main__":
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _root not in sys.path:
        sys.path.insert(0, _root)

from rich.console import Console
from rich.panel import Panel
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.history import FileHistory
from core.config import HISTORY_FILE
from ui.theme import color, THEME, styled_panel
from ai.provider import AIProvider

SHELL_SYSTEM_PROMPT = """You are a smart terminal assistant. The user wants to execute a command.
Analyze their natural language request and provide the appropriate Linux command.
Return ONLY the command to execute, nothing else. If the request is unsafe or unclear, explain why."""

prompt_style = Style([("prompt", "bold #34d399")])
psession = PromptSession(history=FileHistory(str(HISTORY_FILE)))

def run_smart_shell():
    console = Console()
    provider = AIProvider()

    if not provider.api_key:
        console.print()
        console.print(styled_panel(
            color.error("API key required for smart shell.\n")
            + color.muted("Run: python3 /mnt/sdcard/Opencode/sycronix/setup_api.py"),
            "Configuration Required"
        ))
        console.print()
        return

    console.print()
    console.print(styled_panel(
        color.primary("Smart Shell") + color.muted("\nDescribe what you want to do in natural language.")
        + color.muted("\nCommands: /run <cmd> - execute directly, /exit to quit."),
        "Ready"
    ))
    console.print()

    while True:
        try:
            user_input = psession.prompt("sh> ", style=prompt_style)
        except (KeyboardInterrupt, EOFError):
            break

        if not user_input.strip():
            continue
        if user_input.strip() == "/exit":
            break

        if user_input.strip().startswith("/run "):
            cmd = user_input.strip()[5:]
            _run_command(console, cmd)
            continue

        ok, response = provider.chat(
            [{"role": "user", "content": user_input}],
            SHELL_SYSTEM_PROMPT
        )

        if ok:
            command = response.strip().strip("`").strip("$").strip()
            console.print(color.info(f"Suggested: {command}"))
            try:
                execute = psession.prompt("Execute? (Y/n): ", style=prompt_style)
            except (KeyboardInterrupt, EOFError):
                break
            if execute.lower() in ("y", "yes", ""):
                _run_command(console, command)
        else:
            console.print(color.error(f"Error: {response}"))

    console.print(styled_panel(color.muted("Smart Shell ended"), "Goodbye"))

def _run_command(console, command):
    console.print(color.muted(f"$ {command}"))
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=60
        )
        if result.stdout:
            console.print(result.stdout)
        if result.stderr:
            console.print(color.error(result.stderr))
        if result.returncode != 0:
            console.print(color.warning(f"Exit code: {result.returncode}"))
    except subprocess.TimeoutExpired:
        console.print(color.error("Command timed out"))
    except Exception as e:
        console.print(color.error(f"Error: {e}"))
