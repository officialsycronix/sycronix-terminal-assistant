import sys, os
if __name__ != "__main__":
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _root not in sys.path:
        sys.path.insert(0, _root)

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from ui.theme import color, THEME, styled_panel

CREDIT = f"[{THEME['secondary']}]ofx ~ SYCRONIX[/]"

def show_banner():
    console = Console()
    console.print()
    _line = f"[{THEME['muted']}]" + "━" * 34 + "[/]"
    console.print(_line)
    console.print(f"[bold {THEME['primary']}]    S Y C R O N I X   B O T[/]")
    console.print(f"  {CREDIT}")
    console.print(_line)
    console.print()

def show_dashboard(system_info, api_key_status, memory_stats, note_count, recent_commands):
    console = Console()

    info_table = Table(box=box.ROUNDED, border_style=THEME["border"])
    info_table.add_column("Metric", style=THEME["info"])
    info_table.add_column("Value", style=THEME["text"])
    for k, v in system_info.items():
        info_table.add_row(k.replace("_", " ").title(), str(v))

    status_table = Table(box=box.ROUNDED, border_style=THEME["border"])
    status_table.add_column("Component", style=THEME["info"])
    status_table.add_column("Status", style=THEME["text"])
    api_status = color.success("Configured") if api_key_status else color.error("Not Configured")
    status_table.add_row("API Key", api_status)
    status_table.add_row("Memory Entries", str(memory_stats))
    status_table.add_row("Saved Notes", str(note_count))
    status_table.add_row("Recent Commands", str(recent_commands))

    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column()
    grid.add_row(
        styled_panel(info_table, "System Information"),
        styled_panel(status_table, "Status Overview"),
    )

    show_banner()
    console.print(styled_panel(grid, "Dashboard"))
    console.print()

def show_help():
    console = Console()
    table = Table(box=box.ROUNDED, border_style=THEME["border"])
    table.add_column("Mode", style=THEME["primary"])
    table.add_column("Description", style=THEME["text"])
    table.add_column("Usage", style=THEME["muted"])

    modes = [
        ("ai", "AI Chat with OpenRouter", "main.py ai"),
        ("shell", "Smart Shell with AI", "main.py shell"),
        ("tutor", "Linux Tutor & Quiz", "main.py tutor"),
        ("translate", "Command Translator", "main.py translate"),
        ("fix", "Error Fixer", "main.py fix"),
        ("notes", "Note Vault", "main.py notes"),
        ("dashboard", "System Dashboard", "main.py dashboard"),
        ("memory", "Memory Statistics", "main.py memory"),
        ("workflow", "Workflow Engine", "main.py workflow"),
        ("version", "Version Info", "main.py version"),
        ("settings", "Settings & API Key", "main.py settings"),
    ]

    for mode, desc, usage in modes:
        table.add_row(mode, desc, usage)

    show_banner()
    console.print(styled_panel(table, "Available Modes"))
    console.print(f"\n  {CREDIT}")
    console.print()

