# tests/debug/rich_tree.py

from rich.text import Text
from rich.tree import Tree

from .console import console

ATTRIBUTES = [
    "src",
    "value",
    "text",
    "width",
    "height",
]


def _collect_attrs(node):

    attrs = []

    for attr in ATTRIBUTES:
        if hasattr(node, attr):
            value = getattr(node, attr)

            if value:
                attrs.append(f"{attr}={value}")

    return attrs


def _format_label(node):

    typename = node.__class__.__name__

    label = Text(typename, style="bold cyan")

    attrs = _collect_attrs(node)

    if attrs:
        label.append(" ")
        label.append("(" + ", ".join(attrs) + ")", style="dim")

    return label


def render_tree(root, inspector):
    """
    Renderiza árvore de componentes com atributos
    """

    def build(node, branch):

        label = _format_label(node)

        child_branch = branch.add(label)

        for child in inspector.children(node):
            build(child, child_branch)

    root_label = Text(root.__class__.__name__, style="bold yellow")

    tree = Tree(root_label)

    for child in inspector.children(root):
        build(child, tree)

    console.print(tree)
