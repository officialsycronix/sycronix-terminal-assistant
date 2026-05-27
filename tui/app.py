import sys
import os

_sycronix_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _sycronix_root not in sys.path:
    sys.path.insert(0, _sycronix_root)

from textual.app import App
from textual.binding import Binding
from textual.reactive import reactive

from pathlib import Path
from tui.screens.startup import StartupScreen
from tui.screens.main_screen import MainScreen


CSS_DIR = Path(__file__).parent / "css"


class SycronixApp(App):
    TITLE = "SYCRONIX DEV AGENT"
    SUB_TITLE = "Autonomous AI Developer Terminal"
    CSS_PATH = str(CSS_DIR / "app.css")
    SCREENS = {
        "startup": StartupScreen,
        "main": MainScreen,
    }

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("ctrl+p", "command_palette", "Palette", priority=True),
    ]

    def on_mount(self):
        self.push_screen("startup")


def run():
    app = SycronixApp()
    app.run()


if __name__ == "__main__":
    run()
