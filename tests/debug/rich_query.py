# tests/debug/rich_query.py

from rich.table import Table

from .console import console


def render_query(nodes, title="Query Results"):

    table = Table(title=title)

    table.add_column("#", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Attributes")

    for i, node in enumerate(nodes):
        attrs = []

        if hasattr(node, "src"):
            attrs.append(f"src={node.src}")

        if hasattr(node, "value"):
            attrs.append(f"value={node.value}")

        if hasattr(node, "text"):
            attrs.append(f"text={node.text}")

        table.add_row(
            str(i),
            node.__class__.__name__,
            ", ".join(attrs),
        )

    console.print(table)
