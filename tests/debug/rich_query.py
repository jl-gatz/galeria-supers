# tests/debug/rich_query.py

from rich.console import Console
from rich.table import Table

console = Console()


def render_query(nodes: list[object], title: str = "Query Result") -> None:
    table = Table(title=title)

    table.add_column("#")
    table.add_column("Control")

    for i, node in enumerate(nodes):
        table.add_row(str(i), repr(node))

    console.print(table)
