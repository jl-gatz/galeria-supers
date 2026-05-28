# tests/debug/rich_node.py

from rich.panel import Panel
from rich.pretty import Pretty

from .console import console


def render_node(node: object) -> None:

    panel = Panel(
        Pretty(node),
        title=node.__class__.__name__,
        border_style="green",
    )

    console.print(panel)
