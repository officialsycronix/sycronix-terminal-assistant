from datetime import datetime
from textual.widgets import Static
from textual.reactive import reactive
from textual.containers import Horizontal

class StatusBar(Horizontal):
    DEFAULT_CSS = """
    StatusBar {
        height: 3;
        background: #111827;
        border-bottom: solid #1e293b;
        layout: horizontal;
    }
    """

    agent_status = reactive("idle")
    model_name = reactive("llama-3.3-70b")
    memory_count = reactive(0)
    project_name = reactive("sycronix")

    def compose(self):
        yield Static(f"[bold #00d4ff]◆ SYCRONIX[/]", id="project-name")
        yield Static(f"[#6b7280]│[/]")
        yield Static(f"[#6b7280]model[/] [#00d4ff]{self.model_name}[/]", id="model-display")
        yield Static(f"[#6b7280]│[/]")
        yield Static(self._get_status_display(), id="agent-status-display")
        yield Static(f"[#6b7280]│[/]")
        yield Static(f"[#6b7280]memory[/] [#a78bfa]{self.memory_count}[/]", id="memory-display")
        yield Static(f"[#6b7280]│[/]")
        yield Static(f"[#6b7280]{datetime.now().strftime('%H:%M:%S')}[/]", id="clock")

    def _get_status_display(self):
        colors = {
            "idle": "[#6b7280]● idle[/]",
            "thinking": "[#fbbf24]● thinking[/]",
            "executing": "[#00d4ff]● executing[/]",
            "done": "[#34d399]● done[/]",
            "error": "[#f87171]● error[/]",
            "streaming": "[#a78bfa]● streaming[/]",
        }
        return colors.get(self.agent_status, colors["idle"])

    def watch_agent_status(self, status):
        try:
            self.query_one("#agent-status-display").update(self._get_status_display())
        except Exception:
            pass

    async def on_mount(self):
        self.set_interval(1, self._update_clock)

    def _update_clock(self):
        self.query_one("#clock").update(f"[#6b7280]{datetime.now().strftime('%H:%M:%S')}[/]")
