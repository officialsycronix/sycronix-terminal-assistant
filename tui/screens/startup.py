import asyncio
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual.containers import Vertical


BOOT_SEQUENCE = [
    "[#6b7280]Initializing kernel modules...[/]",
    "[#34d399]✓[/] [#6b7280]CPU cores detected: 4[/]",
    "[#34d399]✓[/] [#6b7280]Memory subsystem online[/]",
    "[#34d399]✓[/] [#6b7280]AI model router initialized[/]",
    "[#34d399]✓[/] [#6b7280]Agent workspace ready[/]",
    "[#34d399]✓[/] [#6b7280]System armed and operational[/]",
]

STARTUP_LINES = [
    "[bold #00d4ff]   ███████  ██   ██  ██████  ██████   ██████  ███    ██  ██  ██   ██ [/]",
    "[bold #00d4ff]   ██       ██   ██  ██       ██   ██  ██      ████   ██  ██  ██   ██ [/]",
    "[bold #00d4ff]   ███████  ███████  ██   ███ ██████   ██      ██ ██  ██  ██  ███████ [/]",
    "[bold #00d4ff]        ██  ██   ██  ██    ██ ██   ██  ██      ██  ██ ██  ██  ██   ██ [/]",
    "[bold #00d4ff]   ███████  ██   ██  ██████  ██   ██   ██████  ██   ████  ██  ██   ██ [/]",
]


class StartupScreen(Screen):
    AUTO_FOCUS = None

    def compose(self) -> ComposeResult:
        with Vertical(id="startup-container"):
            yield Static("", id="startup-title")
            yield Static("[#6b7280]AUTONOMOUS AI DEVELOPER TERMINAL[/]", id="startup-subtitle")
            yield Static("", id="startup-loading")
            yield Static("", id="startup-status")
            yield Static("[#334155]v2.0 • built by ofx ~ SYCRONIX[/]", id="startup-version")

    async def on_mount(self):
        title = self.query_one("#startup-title", Static)
        loading = self.query_one("#startup-loading", Static)
        status = self.query_one("#startup-status", Static)

        rendered = ""
        for line in STARTUP_LINES:
            rendered = rendered + "\n" + line if rendered else line
            title.update(rendered)
            await asyncio.sleep(0.03)

        await asyncio.sleep(0.3)

        spinner_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        frame_idx = 0
        boot_idx = 0
        status_text = ""

        while boot_idx < len(BOOT_SEQUENCE):
            loading.update(f"[#00d4ff]{spinner_frames[frame_idx % len(spinner_frames)]} Booting...[/]")
            if frame_idx % 3 == 0 and boot_idx < len(BOOT_SEQUENCE):
                status_text += BOOT_SEQUENCE[boot_idx] + "\n"
                status.update(status_text)
                boot_idx += 1
            frame_idx += 1
            await asyncio.sleep(0.08)

        loading.update(f"[#34d399]● System Ready[/]")
        await asyncio.sleep(0.5)

        self.app.switch_screen("main")
