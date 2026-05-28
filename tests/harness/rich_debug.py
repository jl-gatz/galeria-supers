# tests/harness/rich_debug.py

from difflib import unified_diff

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from tests.utils.types import HasSrc, HasValue, InspectorLike

console = Console()


class RichDebug:
    # -------------------------

    @staticmethod
    def _tree_to_lines(root: object, inspector: InspectorLike) -> list[str]:
        """
        Converte árvore de controles em linhas de texto.
        """

        lines: list[str] = []

        def walk(node: object, depth: int = 0) -> None:
            indent = "  " * depth
            lines.append(f"{indent}{node.__class__.__name__}")

            for child in inspector.children(node):
                walk(child, depth + 1)

        walk(root)

        return lines

    # -------------------------

    @staticmethod
    def print_tree(root: object, inspector: InspectorLike) -> None:
        """
        Renderiza árvore de controles.
        """

        def build(node: object, branch: Tree) -> None:

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
    def print_query(results: list[object]) -> None:
        """
        Mostra resultado de query.
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
    def print_node(node: object) -> None:
        """
        Mostra detalhes de um controle.
        """

        panel = Panel(
            Pretty(node),
            title=node.__class__.__name__,
            border_style="green",
        )

        console.print(panel)

    # -------------------------

    @staticmethod
    def print_controls_table(nodes: list[object]) -> None:
        """
        Tabela com controles encontrados.
        """

        table = Table(title="Controls")

        table.add_column("Index", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Attributes")

        for i, node in enumerate(nodes):
            attrs: list[str] = []

            if isinstance(node, HasSrc):
                attrs.append(f"src={node.src}")

            if isinstance(node, HasValue):
                attrs.append(f"value={node.value}")

            table.add_row(
                str(i),
                node.__class__.__name__,
                ", ".join(attrs),
            )

        console.print(table)

    # -------------------------

    @staticmethod
    def print_snapshot_diff(
        expected_root: object, actual_root: object, inspector: InspectorLike
    ) -> None:
        """
        Mostra diff entre duas árvores.
        """

        expected_lines = RichDebug._tree_to_lines(expected_root, inspector)
        actual_lines = RichDebug._tree_to_lines(actual_root, inspector)

        # painel lado a lado
        expected_panel = Panel(
            "\n".join(expected_lines),
            title="Expected Tree",
            border_style="green",
        )

        actual_panel = Panel(
            "\n".join(actual_lines),
            title="Actual Tree",
            border_style="red",
        )

        console.print(Columns([expected_panel, actual_panel]))

        # diff textual
        diff = unified_diff(
            expected_lines, actual_lines, fromfile="expected", tofile="actual", lineterm=""
        )

        diff_text = "\n".join(diff)

        if diff_text:
            console.print(
                Panel(
                    Syntax(diff_text, "diff"),
                    title="Tree Diff",
                    border_style="yellow",
                )
            )
        else:
            console.print(
                Panel(
                    "Trees are identical",
                    title="Tree Diff",
                    border_style="green",
                )
            )

    # -------------------------

    @staticmethod
    def highlight_selector(selector: str) -> None:
        """
        Destaque visual de selector.
        """

        text = Text(selector, style="bold magenta")

        console.print(Panel(text, title="Selector"))
