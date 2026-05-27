import sys, os, subprocess, shlex
if __name__ != "__main__":
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _root not in sys.path:
        sys.path.insert(0, _root)

from rich.console import Console
from rich.panel import Panel
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
ai.provider import AIProvider
ui.theme import color, styled_panel

FIX_SYSTEM_PROMPT = """You are a Linux error diagnosis expert. Given an error message:
1. Explain what went wrong in simple terms
2. Provide the exact command(s) to fix it
Keep it concise. Be practical."""

prompt_style = Style([("prompt", "bold #f87171")])
psession = PromptSession()

def run_error_fixer():
    console = Console()
    provider = AIProvider()

    console.print()
    console.print(styled_panel(
        color.primary("Error Fixer")
        + color.muted("\nPaste an error message, describe what broke, or type a command that failed.")
        + color.muted("\nType /exit to quit."),
        "Fixer"
    ))
    console.print()

    while True:
        try:
            text = psession.prompt("error> ", style=prompt_style)
        except (KeyboardInterrupt, EOFError):
            break

        if not text.strip():
            continue
        if text.strip() == "/exit":
            break

        if text.strip().startswith("/run "):
            cmd = text.strip()[5:]
            console.print(color.muted(f"$ {cmd}"))
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
                if result.stdout:
                    console.print(result.stdout)
                if result.stderr:
                    console.print(color.error(result.stderr))
            except Exception as e:
                console.print(color.error(str(e)))
            continue

        if not provider.api_key:
            console.print(color.warning("No API key. Try: /run <command> to test locally."))
            console.print(color.muted("Or setup API key: python3 /mnt/sdcard/Opencode/sycronix/setup_api.py"))
            continue

        ok, response = provider.chat([{"role": "user", "content": text}], FIX_SYSTEM_PROMPT)
        if ok:
            console.print()
            console.print(styled_panel(
                color.text(f"[{''.join(['#e2e8f0'])}]{response}[/]"),
                "Solution"
            ))
            console.print()
        else:
            console.print(color.error(f"Error: {response}"))

    console.print(styled_panel(color.muted("Fixer closed"), "Goodbye"))
