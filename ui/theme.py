from rich.style import Style
from rich.color import Color
from rich.table import Table
from rich.panel import Panel
from rich.console import Console

console = Console()

THEME = {
    "primary": "#00d4ff",
    "secondary": "#ff6b9d",
    "accent": "#a78bfa",
    "success": "#34d399",
    "warning": "#fbbf24",
    "error": "#f87171",
    "info": "#60a5fa",
    "muted": "#6b7280",
    "bg": "#0f172a",
    "surface": "#1e293b",
    "border": "#334155",
    "text": "#e2e8f0",
    "heading": "#f8fafc",
}

def styled_panel(content, title="", border=THEME["primary"]):
    return Panel(content, title=title, border_style=Style(color=border))

def styled_table(header_style=THEME["primary"]):
    table = Table(border_style=Style(color=THEME["border"]))
    return table

class ColorTheme:
    def primary(self, text):
        return f"[{THEME['primary']}]{text}[/]"

    def secondary(self, text):
        return f"[{THEME['secondary']}]{text}[/]"

    def success(self, text):
        return f"[{THEME['success']}]{text}[/]"

    def error(self, text):
        return f"[{THEME['error']}]{text}[/]"

    def warning(self, text):
        return f"[{THEME['warning']}]{text}[/]"

    def info(self, text):
        return f"[{THEME['info']}]{text}[/]"

    def muted(self, text):
        return f"[{THEME['muted']}]{text}[/]"

    def bold(self, text):
        return f"[bold]{text}[/]"

    def heading(self, text):
        return f"[bold {THEME['heading']}]{text}[/]"

    def text(self, text):
        return f"[{THEME['text']}]{text}[/]"

color = ColorTheme()
