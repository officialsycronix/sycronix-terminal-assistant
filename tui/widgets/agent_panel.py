from textual.widgets import Static, RichLog
from textual.widget import Widget


class AgentPanel(Widget):
    DEFAULT_CSS = """
    AgentPanel {
        width: 32;
        min-width: 24;
        background: #0f172a;
        border-left: solid #1e293b;
        layout: vertical;
    }
    """

    def compose(self):
        yield Static("[bold #a78bfa] AGENT[/]", id="agent-header")
        with Widget(classes="agent-section"):
            yield Static("[bold #6b7280] THOUGHTS[/]", classes="agent-section-title")
            yield RichLog(id="agent-thoughts", highlight=True, markup=True, max_lines=100, wrap=True)
        with Widget(classes="agent-section"):
            yield Static("[bold #6b7280] ANALYSIS[/]", classes="agent-section-title")
            yield RichLog(id="agent-analysis", highlight=True, markup=True, max_lines=50, wrap=True)
        with Widget(classes="agent-section"):
            yield Static("[bold #6b7280] MEMORY[/]", classes="agent-section-title")
            yield RichLog(id="agent-memory", highlight=True, markup=True, max_lines=50, wrap=True)

    async def on_mount(self):
        self.write_thought("[#6b7280]Agent initialized. Awaiting commands...[/]")

    def write_thought(self, message):
        thoughts = self.query_one("#agent-thoughts", RichLog)
        thoughts.write(f"[#a78bfa]💭 {message}[/]")

    def write_analysis(self, message):
        analysis = self.query_one("#agent-analysis", RichLog)
        analysis.write(f"[#fbbf24]🔍 {message}[/]")

    def write_memory(self, message):
        memory = self.query_one("#agent-memory", RichLog)
        memory.write(f"[#60a5fa]🧠 {message}[/]")

    def clear_thoughts(self):
        self.query_one("#agent-thoughts", RichLog).clear()

    def clear_analysis(self):
        self.query_one("#agent-analysis", RichLog).clear()

    def clear_memory(self):
        self.query_one("#agent-memory", RichLog).clear()
