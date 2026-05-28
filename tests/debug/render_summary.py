from collections import Counter

from rich.console import Console
from rich.table import Table

console = Console()


def render_summary(nodes: list[object]) -> None:

    types = [node.__class__.__name__ for node in nodes]

    counts = Counter(types)

    table = Table(title="Control Summary")

    table.add_column("Control")
    table.add_column("Count", justify="right")

    for name, count in sorted(counts.items()):
        table.add_row(name, str(count))

    console.print(table)
