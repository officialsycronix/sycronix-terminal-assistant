import sys, os
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

TRANSLATE_SYSTEM_PROMPT = """Convert the user's natural language request into a Linux command.
Return ONLY the command, no explanation. If unsure, return the safest approximation."""

prompt_style = Style([("prompt", "bold #60a5fa")])
psession = PromptSession()

def run_translator():
    console = Console()
    provider = AIProvider()

    if not provider.api_key:
        console.print()
        console.print(styled_panel(
            color.error("API key required for translation.\n")
            + color.muted("Run: python3 /mnt/sdcard/Opencode/sycronix/setup_api.py"),
            "Configuration Required"
        ))
        console.print()
        return

    console.print()
    console.print(styled_panel(
        color.primary("Natural Language → Command Translator")
        + color.muted("\nDescribe what you want to do in plain English.")
        + color.muted("\nExample: 'show me all files ending with .txt'")
        + color.muted("\nType /exit to quit."),
        "Translator"
    ))
    console.print()

    while True:
        try:
            text = psession.prompt("translate> ", style=prompt_style)
        except (KeyboardInterrupt, EOFError):
            break

        if not text.strip():
            continue
        if text.strip() == "/exit":
            break

        ok, response = provider.chat([{"role": "user", "content": text}], TRANSLATE_SYSTEM_PROMPT)
        if ok:
            command = response.strip().strip("`").strip("$").strip()
            console.print()
            console.print(styled_panel(color.success(command), "Command"))
            console.print()
        else:
            console.print(color.error(f"Error: {response}"))

    console.print(styled_panel(color.muted("Translator closed"), "Goodbye"))
