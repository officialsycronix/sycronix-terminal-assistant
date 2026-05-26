from textual.widgets import Static
from textual.widget import Widget


class LogLine(Widget):
    DEFAULT_CSS = """
    LogLine {
        height: 1;
        padding: 0 1;
    }
    """


class Sidebar(Widget):
    DEFAULT_CSS = """
    Sidebar {
        width: 28;
        min-width: 20;
        background: #0f172a;
        border-right: solid #1e293b;
        layout: vertical;
    }
    """

    def __init__(self):
        super().__init__()
        self._log_lines = []

    def compose(self):
        yield Static("[bold #00d4ff]EXPLORER[/]", id="sidebar-header")
        with Widget(classes="sidebar-section"):
            yield Static("[bold #6b7280] ACTIVE TASKS[/]", classes="sidebar-section-title")
            yield Static("  [bold #e2e8f0]No active tasks[/]", id="active-tasks", classes="sidebar-content")
        with Widget(classes="sidebar-section"):
            yield Static("[bold #6b7280] WORKFLOW[/]", classes="sidebar-section-title")
            yield Static("  [bold #e2e8f0]Ready[/]", id="workflow-steps", classes="sidebar-content")
        with Widget(classes="sidebar-section"):
            yield Static("[bold #6b7280] LOGS[/]", classes="sidebar-section-title")
            yield Static("  [#6b7280]System initialized[/]", id="logs-content", classes="sidebar-content")

    def update_tasks(self, tasks):
        if tasks:
            text = "\n".join(f"  {'[#fbbf24]●[/]' if t.get('active') else '[#6b7280]○[/]'} [{'#e2e8f0' if not t.get('done') else '#34d399'}]{t['name']}[/]" for t in tasks)
            self.query_one("#active-tasks").update(text)
        else:
            self.query_one("#active-tasks").update("  [bold #e2e8f0]No active tasks[/]")

    def update_workflow(self, steps):
        if steps:
            text = "\n".join(f"  {'[#34d399]✓[/]' if s.get('done') else '[#6b7280]⋯[/]'} [{'#6b7280' if s.get('done') else '#e2e8f0'}]{s['name']}[/]" for s in steps)
            self.query_one("#workflow-steps").update(text)
        else:
            self.query_one("#workflow-steps").update("  [bold #e2e8f0]Ready[/]")

    def add_log(self, message, style="terminal-info"):
        self._log_lines.append(f"  [{style}]{message}[/]")
        if len(self._log_lines) > 50:
            self._log_lines = self._log_lines[-50:]
        self.query_one("#logs-content").update("\n".join(self._log_lines))
