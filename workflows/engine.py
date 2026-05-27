import json, sys, os, subprocess
from pathlib import Path
from datetime import datetime
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
core.config import SYCRONIX_DIR, WORKFLOWS_DIR
ui.theme import color, THEME, styled_panel
memory.store import store

prompt_style = Style([("prompt", "bold #ff6b9d")])
psession = PromptSession()

WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_WORKFLOW = {
    "name": "System Update",
    "steps": [
        {"type": "cmd", "command": "pkg update -y"},
        {"type": "cmd", "command": "pkg upgrade -y"},
        {"type": "msg", "message": "System updated successfully!"},
    ]
}

def run_workflow_engine():
    console = Console()

    console.print()
    ui.banner import show_banner
    show_banner()
    console.print(styled_panel(
        color.primary("Workflow Automation Engine")
        + color.muted(f"\n\n{color.bold('Commands:')}")
        + color.muted(f"\n  {color.info('list')}         — {color.text('Show saved workflows')}")
        + color.muted(f"\n  {color.info('create')}      — {color.text('Create a new workflow')}")
        + color.muted(f"\n  {color.info('run <name>')}  — {color.text('Execute a workflow')}")
        + color.muted(f"\n  {color.info('delete <name>')} — {color.text('Delete a workflow')}")
        + color.muted(f"\n  {color.info('/exit')}       — {color.text('Exit workflow engine')}")
        + color.muted(f"\n\n{color.text('Each step can be:')} {color.info('cmd:<command>')} {color.muted('or')} {color.success('msg:<message>')}"),
        "Workflow"
    ))
    console.print()

    while True:
        try:
            text = psession.prompt("wf> ", style=prompt_style).strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not text:
            continue
        if text == "/exit":
            break

        if text == "list":
            _list_workflows(console)

        elif text == "create":
            _create_workflow(console)

        elif text.startswith("run "):
            name = text[4:].strip()
            _run_workflow(console, name)

        elif text.startswith("delete "):
            name = text[7:].strip()
            _delete_workflow(console, name)

        else:
            console.print(color.muted("Commands: list, run <name>, create, delete <name>, /exit"))

def _list_workflows(console):
    files = list(WORKFLOWS_DIR.glob("*.json"))
    if not files:
        console.print(color.muted("No workflows. Create one with 'create' or run sample."))
        return

    table = Table(box=box.ROUNDED, border_style=THEME["border"])
    table.add_column("Name", style=THEME["primary"])
    table.add_column("Steps", style=THEME["text"])
    table.add_column("Created", style=THEME["muted"])

    for f in files:
        try:
            wf = json.loads(f.read_text())
            table.add_row(
                wf.get("name", f.stem),
                str(len(wf.get("steps", []))),
                datetime.fromtimestamp(f.stat().st_ctime).strftime("%Y-%m-%d"),
            )
        except:
            pass

    console.print(styled_panel(table, "Workflows"))

def _create_workflow(console):
    console.print(color.muted("Creating new workflow. Enter steps (end with . on empty line):"))
    console.print(color.muted("  Step format: cmd:command or msg:message"))

    steps = []
    while True:
        try:
            line = psession.prompt("  step> ", style=prompt_style).strip()
        except (KeyboardInterrupt, EOFError):
            break
        if not line or line == ".":
            break
        if line.startswith("cmd:"):
            steps.append({"type": "cmd", "command": line[4:]})
            console.print(color.muted(f"  Added command: {line[4:]}"))
        elif line.startswith("msg:"):
            steps.append({"type": "msg", "message": line[4:]})
            console.print(color.muted(f"  Added message: {line[4:]}"))
        else:
            console.print(color.error("Invalid format. Use cmd:<command> or msg:<message>"))

    if not steps:
        return

    name = psession.prompt("  Workflow name: ", style=prompt_style).strip()
    if not name:
        name = f"workflow_{len(list(WORKFLOWS_DIR.glob('*.json'))) + 1}"

    wf = {"name": name, "steps": steps, "created": str(datetime.now())[:19]}
    (WORKFLOWS_DIR / f"{name}.json").write_text(json.dumps(wf, indent=2))
    store.remember(f"workflow:{name}", wf, category="workflow")
    console.print(color.success(f"Workflow '{name}' created with {len(steps)} steps"))

def _run_workflow(console, name):
    wf_file = WORKFLOWS_DIR / f"{name}.json"
    if not wf_file.exists():
        if name == "sample":
            wf = SAMPLE_WORKFLOW
        else:
            console.print(color.error(f"Workflow '{name}' not found"))
            return
    else:
        try:
            wf = json.loads(wf_file.read_text())
        except:
            console.print(color.error(f"Failed to load '{name}'"))
            return

    console.print(styled_panel(color.primary(f"Running: {wf['name']}"), "Workflow"))

    for i, step in enumerate(wf["steps"], 1):
        console.print(color.muted(f"[{i}/{len(wf['steps'])}] "), end="")
        if step["type"] == "cmd":
            cmd = step["command"]
            console.print(color.info(f"$ {cmd}"))
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
                if result.stdout:
                    console.print(result.stdout[:500])
                if result.stderr:
                    console.print(color.error(result.stderr[:200]))
            except subprocess.TimeoutExpired:
                console.print(color.error("Timed out"))
            except Exception as e:
                console.print(color.error(str(e)))
        elif step["type"] == "msg":
            console.print(color.success(step["message"]))

    console.print(styled_panel(color.success("Workflow completed"), "Done"))

def _delete_workflow(console, name):
    wf_file = WORKFLOWS_DIR / f"{name}.json"
    if wf_file.exists():
        wf_file.unlink()
        store.forget(f"workflow:{name}")
        console.print(color.success(f"Deleted '{name}'"))
    else:
        console.print(color.error(f"Workflow '{name}' not found"))
