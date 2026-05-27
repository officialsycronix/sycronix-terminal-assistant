import json, datetime, sys, os
if __name__ != "__main__":
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _root not in sys.path:
        sys.path.insert(0, _root)

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from core.config import NOTES_FILE
from ui.theme import color, THEME, styled_panel

prompt_style = Style([("prompt", "bold #fbbf24")])
psession = PromptSession()

def run_note_vault():
    console = Console()
    notes = _load_notes()

    console.print()
    from ui.banner import show_banner
    show_banner()
    console.print(styled_panel(
        color.primary("Note Vault")
        + color.muted(f"\n\n{color.bold('Commands:')}")
        + color.muted(f"\n  {color.info('add')}      — {color.text('Add a new note')}")
        + color.muted(f"\n  {color.info('list')}     — {color.text('Show recent notes')}")
        + color.muted(f"\n  {color.info('del <id>')} — {color.text('Delete a note by ID')}")
        + color.muted(f"\n  {color.info('search')}   — {color.text('Search notes by text')}")
        + color.muted(f"\n  {color.info('/exit')}    — {color.text('Save & exit')}"),
        "Notes"
    ))
    console.print()

    while True:
        try:
            text = psession.prompt("notes> ", style=prompt_style).strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not text:
            continue
        if text == "/exit":
            break

        if text == "add":
            console.print(color.muted("Enter note (end with . on empty line):"))
            lines = []
            while True:
                try:
                    line = psession.prompt("  ", style=prompt_style)
                    if line.strip() == ".":
                        break
                    lines.append(line)
                except (KeyboardInterrupt, EOFError):
                    break
            if lines:
                note = "\n".join(lines)
                notes.append({
                    "id": len(notes) + 1,
                    "content": note,
                    "time": str(datetime.datetime.now())[:19],
                })
                _save_notes(notes)
                console.print(color.success("Note saved!"))

        elif text == "list":
            if not notes:
                console.print(color.muted("No notes yet. Use 'add' to create one."))
                continue
            table = Table(box=box.ROUNDED, border_style=THEME["border"])
            table.add_column("ID", style=THEME["primary"])
            table.add_column("Content", style=THEME["text"])
            table.add_column("Time", style=THEME["muted"])
            for n in notes[-10:]:
                content = n["content"][:60] + ("..." if len(n["content"]) > 60 else "")
                table.add_row(str(n["id"]), content, n["time"])
            console.print(styled_panel(table, f"Notes ({len(notes)})"))

        elif text.startswith("del "):
            try:
                nid = int(text[4:])
                notes = [n for n in notes if n["id"] != nid]
                _save_notes(notes)
                console.print(color.success(f"Deleted note #{nid}"))
            except ValueError:
                console.print(color.error("Usage: del <id>"))

        elif text.startswith("search "):
            query = text[7:].lower()
            found = [n for n in notes if query in n["content"].lower()]
            if found:
                table = Table(box=box.ROUNDED, border_style=THEME["border"])
                table.add_column("ID", style=THEME["primary"])
                table.add_column("Content", style=THEME["text"])
                for n in found:
                    content = n["content"][:60] + ("..." if len(n["content"]) > 60 else "")
                    table.add_row(str(n["id"]), content)
                console.print(styled_panel(table, f"Found {len(found)} notes"))
            else:
                console.print(color.muted("No matching notes."))

        else:
            console.print(color.muted("Commands: add, list, del <id>, search <text>, /exit"))

    console.print(styled_panel(color.muted("Notes saved"), "Goodbye"))

def _load_notes():
    try:
        if NOTES_FILE.exists():
            with open(NOTES_FILE) as f:
                return json.load(f)
    except:
        pass
    return []

def _save_notes(notes):
    try:
        NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(NOTES_FILE, "w") as f:
            json.dump(notes, f, indent=2)
    except:
        pass
