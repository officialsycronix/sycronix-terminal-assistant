#!/usr/bin/env python3
"""
Sycronix - Intelligent Terminal Assistant
OfC SYCRONIX

All-in-one AI-powered terminal toolkit for Termux / Linux.
"""

# ─── Bulletproof import path setup ───────────────────────────────────
import sys, os

_sycronix_root = os.path.dirname(os.path.abspath(__file__))
_parent = os.path.dirname(_sycronix_root)
if _parent not in sys.path:
    sys.path.insert(0, _parent)
os.chdir(_sycronix_root)

# Termux fallback
_termux_site = "/data/data/com.termux/files/usr/lib/python3.13/site-packages"
if os.path.isdir(_termux_site) and _termux_site not in sys.path:
    sys.path.insert(0, _termux_site)

# ─── Main cli ────────────────────────────────────────────────────────
def _run():
    import typer
    from rich.console import Console
    from rich.table import Table
    from rich import box
    from ui.theme import color, THEME, styled_panel
    from ui.banner import show_banner, show_help, CREDIT
    from core.config import get_api_key, config_path
    from memory.store import store
    from core.utils import get_system_info

    app = typer.Typer(invoke_without_command=True, add_completion=False)
    console = Console()
    api_status = bool(get_api_key())

    @app.callback(invoke_without_command=True)
    def main(ctx: typer.Context):
        if ctx.invoked_subcommand is None:
            show_help()

    @app.command()
    def ai():
        """AI Chat with OpenRouter"""
        from ai.chat import run_ai_chat
        run_ai_chat()

    @app.command()
    def shell():
        """Smart Shell with AI"""
        from shell.smart_shell import run_smart_shell
        run_smart_shell()

    @app.command()
    def tutor():
        """Linux Tutor & Quiz"""
        from tutor.tutor import run_tutor
        run_tutor()

    @app.command()
    def translate():
        """NL → Command translator"""
        from tools.translator import run_translator
        run_translator()

    @app.command()
    def fix():
        """Error fixer"""
        from tools.error_fixer import run_error_fixer
        run_error_fixer()

    @app.command()
    def notes():
        """Note vault"""
        from tools.note_vault import run_note_vault
        run_note_vault()

    @app.command()
    def dashboard():
        """System dashboard"""
        info = get_system_info()
        from ui.banner import show_dashboard
        from pathlib import Path
        import json
        notes_file = Path.home() / ".sycronix" / "notes.json"
        note_count = len(json.loads(notes_file.read_text())) if notes_file.exists() else 0
        show_dashboard(info, api_status, store.get_count(), note_count, 0)

    @app.command()
    def memory():
        """Memory store statistics"""
        count = store.get_count()
        table = Table(box=box.ROUNDED, border_style=THEME["border"])
        table.add_column("Metric", style=THEME["info"])
        table.add_column("Value", style=THEME["text"])
        table.add_row("Total Memory Entries", str(count))
        table.add_row("Storage", str(config_path()))
        console.print()
        show_banner()
        console.print(styled_panel(table, title="Memory Store"))
        console.print()

    @app.command()
    def workflow():
        """Workflow engine"""
        from workflows.engine import run_workflow_engine
        run_workflow_engine()

    @app.command()
    def version():
        """Version info"""
        console.print()
        console.print(f"""[{THEME['primary']}]Sycronix v2.0[{THEME['text']}]
[{THEME['secondary']}]ofx ~ SYCRONIX[/]
Python: {sys.version.split()[0]}
Platform: {sys.platform}
API Key: {color.success('✓') if api_status else color.error('✗')}[/]""")
        console.print()

    @app.command()
    def settings():
        """Configure API key & settings"""
        console.print()
        console.print(styled_panel(
            color.primary("Settings") + color.muted("\n\nAPI Key: ")
            + (color.success("Configured") if api_status else color.error("Not Configured"))
            + color.muted(f"\nConfig path: {config_path()}")
            + color.muted("\n\nRun: python3 /mnt/sdcard/Opencode/sycronix/setup_api.py")
            + color.muted("\nOr: python3 -m sycronix.setup_api"),
            "Sycronix Settings"
        ))
        console.print()

    @app.command()
    def dev():
        """SYCRONIX DEV AGENT - TUI mode"""
        from tui.app import run
        run()

    app()

if __name__ == "__main__":
    _run()
