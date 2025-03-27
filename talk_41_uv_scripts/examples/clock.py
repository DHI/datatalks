# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "textual",
# ]
# ///
"""
An App to show the current time.

https://gist.githubusercontent.com/ryan-kipawa/31bc2e63f6dc24f03593b7c9e496c18d/raw/cce7556651fddcd5bb30b19a3f5f5670633f1257/clock.py
"""

from datetime import datetime

from textual.app import App, ComposeResult
from textual.widgets import Digits


class ClockApp(App):
    CSS = """
    Screen { align: center middle; }
    Digits { width: auto; }
    """

    def compose(self) -> ComposeResult:
        yield Digits("")

    def on_ready(self) -> None:
        self.update_clock()
        self.set_interval(1, self.update_clock)

    def update_clock(self) -> None:
        clock = datetime.now().time()
        self.query_one(Digits).update(f"{clock:%T}")


if __name__ == "__main__":
    app = ClockApp()
    app.run()