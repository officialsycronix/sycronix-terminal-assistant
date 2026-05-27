import asyncio
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal, Vertical
from textual.widgets import Input, Static
from textual.binding import Binding
from textual import work
from textual.reactive import reactive

from tui.widgets.status_bar import StatusBar
from tui.widgets.sidebar import Sidebar
from tui.widgets.terminal_panel import TerminalPanel
from tui.widgets.agent_panel import AgentPanel
from agent.agent import DevAgent
from core.config import get_api_key


class MainScreen(Screen):
    BINDINGS = [
        Binding("ctrl+p", "command_palette", "Commands"),
        Binding("ctrl+c", "clear_terminal", "Clear"),
        Binding("ctrl+d", "exit_app", "Exit"),
        Binding("ctrl+l", "toggle_sidebar", "Sidebar"),
        Binding("ctrl+r", "toggle_agent", "Agent Panel"),
        Binding("escape", "focus_input", "Focus Input"),
    ]

    agent_mode = reactive(False)

    def __init__(self):
        super().__init__()
        self.agent = DevAgent()
        self.api_key = get_api_key()

    def compose(self) -> ComposeResult:
        with Vertical(id="app-container"):
            yield StatusBar()
            with Horizontal(id="main-content"):
                yield Sidebar()
                with Vertical(id="terminal-panel"):
                    yield TerminalPanel()
                yield AgentPanel()
            with Vertical(id="input-container"):
                yield Input(id="command-input", placeholder="/create flask-app  ·  /agent  ·  /help")
                yield Static("[#6b7280]/command  ·  plain text = shell  ·  /agent ON = AI chat[/]", id="input-hint")

    async def on_mount(self):
        terminal = self.query_one(TerminalPanel)
        terminal.write_system("SYCRONIX DEV AGENT v2.0")
        terminal.write("  /agent  — live AI chat mode")
        terminal.write("  /help   — all commands")
        if not self.api_key:
            terminal.write_warning("No API key — AI disabled. Run: python setup_api.py")
        else:
            terminal.write_success("API key ready — /agent to start building")
        self.query_one("#command-input", Input).focus()

    def on_input_submitted(self, event: Input.Submitted):
        cmd = event.value.strip()
        if cmd:
            self.query_one("#command-input", Input).clear()
            self.process_command(cmd)

    @work(exclusive=True)
    async def process_command(self, command: str):
        terminal = self.query_one(TerminalPanel)
        sidebar = self.query_one(Sidebar)
        agent_panel = self.query_one(AgentPanel)
        status_bar = self.query_one(StatusBar)
        terminal.write_prompt(command)

        if command.startswith("/"):
            await self._handle_command(command[1:], terminal, sidebar, agent_panel, status_bar)
        elif self.agent_mode and self.api_key:
            await self._agent_chat(command, terminal, sidebar, agent_panel, status_bar)
        else:
            await self._run_shell(command, terminal, sidebar, agent_panel, status_bar)

    async def _handle_command(self, args, terminal, sidebar, agent_panel, status_bar):
        parts = args.split()
        cmd = parts[0].lower() if parts else ""
        rest = " ".join(parts[1:]) if len(parts) > 1 else ""

        if cmd == "help":
            terminal.write_system("COMMANDS")
            for c, d in [
                ("/agent", "Live AI chat mode — talk & build"),
                ("/create <type>", "Scaffold: flask-app, fastapi-backend, python-cli, html-portfolio"),
                ("/fix", "Auto-detect and fix errors"),
                ("/run <cmd>", "Run a shell command"),
                ("/clear", "Clear terminal"),
                ("/status", "System status"),
                ("/memory", "Memory stats"),
                ("/exit", "Exit"),
            ]:
                terminal.write(f"  [#00d4ff]{c:20}[/] [#6b7280]{d}[/]")
            terminal.write("  [#6b7280]Agent OFF → shell  |  Agent ON → AI chats & builds[/]")
        elif cmd == "clear":
            terminal.clear()
        elif cmd == "exit":
            await self.app.exit()
        elif cmd == "agent":
            self.agent_mode = not self.agent_mode
            self.agent.active = self.agent_mode
            status_bar.agent_status = "idle"
            if self.agent_mode:
                terminal.write_success("Agent mode ON")
                terminal.write_agent("I'm live. Tell me what to build.")
                agent_panel.write_thought("Live mode. Ready.")
                sidebar.update_workflow([{"name": "Chat with user", "done": False}])
            else:
                terminal.write_info("Agent mode OFF")
                self.agent.conversation_active = False
                agent_panel.write_thought("Paused.")
                sidebar.update_workflow([])
        elif cmd == "status":
            terminal.write_system("STATUS")
            terminal.write(f"  [#60a5fa]API:[/] {'[#34d399]✓[/]' if self.api_key else '[#f87171]✗[/]'}")
            terminal.write(f"  [#60a5fa]Agent:[/] {'[#34d399]Live[/]' if self.agent_mode else '[#6b7280]Off[/]'}")
        elif cmd == "memory":
            from memory.store import store
            terminal.write_system("MEMORY")
            terminal.write(f"  [#a78bfa]Entries:[/] [#e2e8f0]{store.get_count()}[/]")
        elif cmd == "create":
            if not rest:
                terminal.write_info("Usage: /create flask-app | fastapi-backend | python-cli | html-portfolio")
            else:
                await self._scaffold_project(rest, terminal, sidebar, agent_panel, status_bar)
        elif cmd == "fix":
            if self.api_key:
                await self._agent_chat("Fix errors in the current project", terminal, sidebar, agent_panel, status_bar)
            else:
                terminal.write_error("API key needed")
        elif cmd == "run":
            if rest:
                await self._run_shell(rest, terminal, sidebar, agent_panel, status_bar)
            else:
                terminal.write_info("Usage: /run <command>")
        else:
            terminal.write_error(f"Unknown: /{cmd}  —  try /help")

    async def _agent_chat(self, text, terminal, sidebar, agent_panel, status_bar):
        status_bar.agent_status = "streaming"
        agent_panel.write_thought(f"Thinking about: {text}")
        file_count = 0

        def on_token(tok, style="stream"):
            terminal.write_stream(tok, style)

        def on_action(action_type, data):
            nonlocal file_count
            if action_type == "create": terminal.write_info(f"Creating: {data}")
            elif action_type == "created":
                file_count += 1; terminal.write_success(f"Saved: {data}"); agent_panel.write_memory(f"Wrote: {data}")
            elif action_type == "run": terminal.write_agent(f"Running: {data}")
            elif action_type == "output":
                for line in data.split("\n"): terminal.write(f"  {line}")
            elif action_type == "error": terminal.write_error(data)
            elif action_type == "done": terminal.write_success(data)

        def on_done(full_response):
            status_bar.agent_status = "done"
            terminal.flush_stream()
            terminal.write("")
            if file_count > 0: terminal.write_success(f"Created {file_count} file(s)")
            sidebar.update_workflow([{"name": f"Chat: {text[:30]}", "done": True}])
            self.query_one("#command-input", Input).focus()

        await self.agent.chat_stream(user_input=text, on_token=on_token, on_action=on_action, on_done=on_done)

    async def _scaffold_project(self, project_type, terminal, sidebar, agent_panel, status_bar):
        from generator.scaffolder import Scaffolder
        s = Scaffolder()
        info = s.get_template_info(project_type)
        if not info:
            terminal.write_error(f"Unknown: {project_type}"); terminal.write_info("Available: flask-app, fastapi-backend, python-cli, html-portfolio")
            return
        terminal.write_system(f"SCAFFOLDING: {info['name']}")
        result = s.scaffold(project_type)
        if result["success"]:
            terminal.write_success(f"Created at: {result['project_dir']}")
            for f in result["files"]: terminal.write(f"  [#34d399]✓[/] [#e2e8f0]{f}[/]")
            if result["post_install"]:
                terminal.write_info(f"Installing: {result['post_install']}")
                await self._run_shell(result["post_install"], terminal, sidebar, agent_panel, status_bar)
            terminal.write_info(f"Run: {result['run_command']}")
        else:
            terminal.write_error(result["error"])

    async def _run_shell(self, command, terminal, sidebar, agent_panel, status_bar):
        status_bar.agent_status = "executing"
        try:
            process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=60)
            if stdout:
                for line in stdout.decode().splitlines(): terminal.write(line)
            if stderr:
                for line in stderr.decode().splitlines(): terminal.write_error(line)
            if process.returncode == 0:
                terminal.write_success(f"Done (exit {process.returncode})"); status_bar.agent_status = "done"
            else:
                terminal.write_error(f"Failed (exit {process.returncode})"); status_bar.agent_status = "error"
                if self.agent_mode and self.api_key:
                    await self.agent.debug_error(stderr.decode() if stderr else "", command=command, on_analysis=lambda a: agent_panel.write_analysis(a), on_fix=lambda f: terminal.write_info(f"Fix: {f}"))
        except asyncio.TimeoutError: terminal.write_error("Timed out"); status_bar.agent_status = "error"
        except Exception as e: terminal.write_error(f"Error: {e}"); status_bar.agent_status = "error"

    def action_command_palette(self):
        terminal = self.query_one(TerminalPanel)
        terminal.write_system("COMMAND PALETTE")
        terminal.write("  [#00d4ff]/agent[/]    [#6b7280]Live AI chat & build[/]")
        terminal.write("  [#00d4ff]/create[/]   [#6b7280]Scaffold project[/]")
        terminal.write("  [#00d4ff]/fix[/]      [#6b7280]Auto-fix errors[/]")
        terminal.write("  [#00d4ff]/run[/]      [#6b7280]Run command[/]")
        terminal.write("  [#00d4ff]/clear[/]    [#6b7280]Clear[/]")
        terminal.write("  [#00d4ff]/status[/]   [#6b7280]Status[/]")
        terminal.write("  [#00d4ff]/exit[/]     [#6b7280]Exit[/]")
        self.query_one("#command-input", Input).focus()

    def action_clear_terminal(self): self.query_one(TerminalPanel).clear()
    def action_exit_app(self):
        async def _q(): await self.app.exit()
        asyncio.create_task(_q())
    def action_toggle_sidebar(self):
        s = self.query_one(Sidebar); s.styles.display = "block" if s.styles.display != "block" else "none"
    def action_toggle_agent(self):
        a = self.query_one(AgentPanel); a.styles.display = "block" if a.styles.display != "block" else "none"
    def action_focus_input(self): self.query_one("#command-input", Input).focus()
