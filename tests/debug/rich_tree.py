# tests/debug/rich_tree.py

from rich.text import Text
from rich.tree import Tree

from tests.utils.types import HasSrc, HasText, HasValue, InspectorLike

from .console import console

ATTRIBUTES = [
    "src",
    "value",
    "text",
    "width",
    "height",
]


def _collect_attrs(node: object) -> list[str]:

    attrs: list[str] = []

    for attr in ATTRIBUTES:
        value: object | None = None

        if attr == "src" and isinstance(node, HasSrc):
            value = node.src
        elif attr == "value" and isinstance(node, HasValue):
            value = node.value
        elif attr == "text" and isinstance(node, HasText):
            value = node.text
        elif attr in {"width", "height"}:
            value = getattr(node, attr, None)

        if value:
            attrs.append(f"{attr}={value}")

    return attrs


def _format_label(node: object) -> Text:

    typename = node.__class__.__name__

    label = Text(typename, style="bold cyan")

    attrs = _collect_attrs(node)

    if attrs:
        label.append(" ")
        label.append("(" + ", ".join(attrs) + ")", style="dim")

    return label


def render_tree(root: object, inspector: InspectorLike) -> None:
    """
    Renderiza árvore de componentes com atributos
    """

    def build(node: object, branch: Tree) -> None:

        label = _format_label(node)

        child_branch = branch.add(label)

        for child in inspector.children(node):
            build(child, child_branch)

    root_label = Text(root.__class__.__name__, style="bold yellow")

    tree = Tree(root_label)

    for child in inspector.children(root):
        build(child, tree)

    console.print(tree)
