from textual.widgets import Static, RichLog
from textual.widget import Widget


class TerminalPanel(Widget):
    DEFAULT_CSS = """
    TerminalPanel {
        width: 1fr;
        background: #0a0f1a;
        layout: vertical;
    }
    """

    def __init__(self):
        super().__init__()
        self._stream_content = ""

    def compose(self):
        yield Static("[bold #e2e8f0]  TERMINAL[/]", id="terminal-header")
        yield RichLog(id="terminal-output", highlight=True, markup=True, max_lines=1000, wrap=True)
        yield Static("", id="stream-line", classes="terminal-stream")

    async def on_mount(self):
        log = self.query_one("#terminal-output", RichLog)
        log.write("[#6b7280]╭──────────────────────────────────────────────────────────╮[/]")
        log.write("[#6b7280]│[/]  [#00d4ff]SYCRONIX DEV AGENT[/] [#6b7280]v2.0[/]")
        log.write("[#6b7280]│[/]  [#6b7280]/agent  →  /create  →  /help[/]")
        log.write("[#6b7280]╰──────────────────────────────────────────────────────────╯[/]")
        log.write("")

    def write(self, message, style="terminal-stream"):
        self._flush_stream()
        self.query_one("#terminal-output", RichLog).write(f"[{style}]{message}[/]")

    def write_prompt(self, prompt):
        self._flush_stream()
        self.query_one("#terminal-output", RichLog).write(f"[#34d399]>[/] [#e2e8f0]{prompt}[/]")

    def write_system(self, message):
        self._flush_stream()
        self.query_one("#terminal-output", RichLog).write(f"[#6b7280]━━━ {message} ━━━[/]")

    def write_error(self, message):
        self._flush_stream()
        self.query_one("#terminal-output", RichLog).write(f"[#f87171]✗ {message}[/]")

    def write_success(self, message):
        self._flush_stream()
        self.query_one("#terminal-output", RichLog).write(f"[#34d399]✓ {message}[/]")

    def write_info(self, message):
        self._flush_stream()
        self.query_one("#terminal-output", RichLog).write(f"[#60a5fa]ℹ {message}[/]")

    def write_warning(self, message):
        self._flush_stream()
        self.query_one("#terminal-output", RichLog).write(f"[#fbbf24]⚠ {message}[/]")

    def write_agent(self, message):
        self._flush_stream()
        self.query_one("#terminal-output", RichLog).write(f"[#a78bfa]◆ {message}[/]")

    def write_stream(self, token, style="stream"):
        self._stream_content += token
        self.query_one("#stream-line", Static).update(f"[{style}]{self._stream_content}[/]")

    def _flush_stream(self):
        if self._stream_content.strip():
            self.query_one("#terminal-output", RichLog).write(f"[stream]{self._stream_content}[/]")
            self._stream_content = ""
            self.query_one("#stream-line", Static).update("")

    def flush_stream(self):
        self._flush_stream()

    def clear(self):
        self._flush_stream()
        self.query_one("#terminal-output", RichLog).clear()
