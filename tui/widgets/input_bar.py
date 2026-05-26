from textual.widgets import Input, Static
from textual.widget import Widget
from textual.message import Message


COMMANDS = [
    "sycronix create flask-app",
    "sycronix create fastapi backend",
    "sycronix build portfolio",
    "sycronix fix errors",
    "sycronix explain code",
    "sycronix run project",
    "sycronix debug app",
    "sycronix agent mode",
    "sycronix help",
    "sycronix status",
    "sycronix clear",
    "sycronix memory",
    "sycronix settings",
]


class InputBar(Widget):
    DEFAULT_CSS = """
    InputBar {
        dock: bottom;
        height: 5;
        background: #111827;
        border-top: solid #1e293b;
        layout: vertical;
    }
    """

    class CommandSubmitted(Message):
        def __init__(self, command: str) -> None:
            self.command = command
            super().__init__()

    def compose(self):
        yield Input(
            id="command-input",
            placeholder="> sycronix create flask-app  (Ctrl+P palette, Ctrl+C clear, Ctrl+D exit)",
        )
        yield Static(
            "[#6b7280]Tab ↹ suggestions  •  ↑↓ history  •  Esc clear  •  / commands[/]",
            id="input-hint",
        )

    async def on_mount(self):
        self.query_one("#command-input", Input).focus()

    def on_input_submitted(self, event: Input.Submitted):
        value = event.value.strip()
        if value:
            self.post_message(self.CommandSubmitted(value))
            self.query_one("#command-input", Input).clear()

    def set_suggestions(self, suggestions):
        hint = self.query_one("#input-hint", Static)
        if suggestions:
            display = "  •  ".join(suggestions[:4])
            hint.update(f"[#6b7280]{display}  •  Tab for more[/]")
        else:
            hint.update("[#6b7280]Tab ↹ suggestions  •  ↑↓ history  •  Esc clear  •  / commands[/]")

    def focus_input(self):
        self.query_one("#command-input", Input).focus()
