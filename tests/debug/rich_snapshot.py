# tests/debug/rich_snapshot.py

import difflib

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def render_snapshot_diff(expected: str, actual: str):
    """
    Renderiza diff entre dois snapshots usando Rich + difflib
    """

    diff = difflib.ndiff(
        expected.splitlines(),
        actual.splitlines(),
    )

    text = Text()

    for line in diff:
        if line.startswith("+ "):
            text.append(line + "\n", style="green")

        elif line.startswith("- "):
            text.append(line + "\n", style="red")

        elif line.startswith("? "):
            text.append(line + "\n", style="yellow")

        else:
            text.append(line + "\n")

    console.print(
        Panel(
            text,
            title="Snapshot Diff",
            border_style="red",
        )
    )
