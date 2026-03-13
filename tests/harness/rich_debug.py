# tests/harness/rich_debug.py

from rich.console import Console
from rich.diff import Diff
from rich.panel import Panel
from rich.pretty import Pretty
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

console = Console()


class RichDebug:
    @staticmethod
    def print_tree(root, inspector):
        """
        Renderiza a árvore de componentes
        """

        def build(node, branch):
            label = f"[bold cyan]{node.__class__.__name__}[/]"

            child_branch = branch.add(label)

            for child in inspector.children(node):
                build(child, child_branch)

        tree = Tree(f"[bold yellow]{root.__class__.__name__}[/]")

        for child in inspector.children(root):
            build(child, tree)

        console.print(tree)

    # -------------------------

    @staticmethod
    def print_query(results):
        """
        Mostra resultado de uma query
        """

        table = Table(title="Query Results")

        table.add_column("#", style="cyan")
        table.add_column("Control")
        table.add_column("Type")

        for i, control in enumerate(results):
            table.add_row(
                str(i),
                str(control),
                control.__class__.__name__,
            )

        console.print(table)

    # -------------------------

    @staticmethod
    def print_node(node):
        """
        Mostra detalhes de um controle
        """

        panel = Panel(
            Pretty(node),
            title=f"{node.__class__.__name__}",
            border_style="green",
        )

        console.print(panel)

    # -------------------------

    @staticmethod
    def print_controls_table(nodes):
        """
        Tabela com controles encontrados
        """

        table = Table(title="Controls")

        table.add_column("Index", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Attributes")

        for i, node in enumerate(nodes):
            attrs = []

            if hasattr(node, "src"):
                attrs.append(f"src={node.src}")

            if hasattr(node, "value"):
                attrs.append(f"value={node.value}")

            table.add_row(
                str(i),
                node.__class__.__name__,
                ", ".join(attrs),
            )

        console.print(table)

    # -------------------------

    @staticmethod
    def print_snapshot_diff(expected, actual):
        """
        Mostra diff entre snapshots
        """

        diff = Diff(expected, actual)

        console.print(Panel(diff, title="Snapshot Diff"))

    # -------------------------

    @staticmethod
    def highlight_selector(selector):
        """
        Destaque visual do selector
        """

        text = Text(selector, style="bold magenta")

        console.print(Panel(text, title="Selector"))
