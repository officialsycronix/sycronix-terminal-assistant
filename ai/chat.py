import sys, os
if __name__ != "__main__":
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _root not in sys.path:
        sys.path.insert(0, _root)

from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.history import FileHistory
from sycronix.core.config import HISTORY_FILE, SYCRONIX_DIR
from sycronix.ui.theme import color, THEME, styled_panel
from sycronix.memory.store import store
from sycronix.ai.provider import AIProvider

CHAT_SYSTEM_PROMPT = """You are Sycronix AI, an intelligent terminal assistant created by OfC SYCRONIX.
You help users with Linux commands, system administration, programming, and general tech questions.
Keep responses concise, practical, and terminal-friendly."""

prompt_style = Style([("prompt", "bold #00d4ff")])
session = PromptSession(history=FileHistory(str(HISTORY_FILE)))

def run_ai_chat():
    console = Console()
    provider = AIProvider()

    if not provider.api_key:
        console.print()
        console.print(styled_panel(
            color.error("API key not configured!\n")
            + color.muted("Run: python3 /mnt/sdcard/Opencode/sycronix/setup_api.py"),
            "Configuration Required"
        ))
        console.print()
        return

    messages = []
    console.print()
    console.print(styled_panel(
        color.primary("Sycronix AI Chat")
        + color.muted("\nType your questions. Use /clear to reset, /save to save conversation, /exit to quit."),
        "Session Started"
    ))
    console.print()

    while True:
        try:
            user_input = session.prompt("You: ", style=prompt_style)
        except KeyboardInterrupt:
            console.print(color.muted("\nUse /exit to quit"))
            continue
        except EOFError:
            break

        if not user_input.strip():
            continue

        if user_input.strip() == "/exit":
            break
        if user_input.strip() == "/clear":
            messages.clear()
            console.print(color.warning("Conversation cleared"))
            continue
        if user_input.strip() == "/save":
            store.remember("chat_history", messages, category="chat")
            console.print(color.success("Conversation saved to memory"))
            continue

        messages.append({"role": "user", "content": user_input})

        console.print(color.muted("AI: "), end="")
        full_response = ""
        response_ok = False

        try:
            with Live("", console=console, refresh_per_second=10) as live:
                for ok, chunk in provider.stream_chat(messages, CHAT_SYSTEM_PROMPT):
                    if ok:
                        full_response += chunk
                        live.update(color.text(f"[{THEME['text']}]{full_response}[/]")
                                    + color.muted("▌"))
                    else:
                        live.update(color.error(f"Error: {chunk}"))
                        break
                else:
                    response_ok = True
        except Exception as e:
            console.print(color.error(f"Error: {e}"))
            ok, response = provider.chat(messages[-1:], CHAT_SYSTEM_PROMPT)
            if ok:
                full_response = response
                response_ok = True
                console.print(color.text(f"[{THEME['text']}]{response}[/]"))
            else:
                console.print(color.error(response))

        if response_ok and full_response:
            messages.append({"role": "assistant", "content": full_response})
        console.print()

    console.print()
    console.print(styled_panel(color.muted("AI Chat session ended"), "Goodbye"))
    console.print()
