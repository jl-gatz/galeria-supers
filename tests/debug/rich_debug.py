# tests/debug/rich_debug.py

from tests.utils.types import InspectorLike, SelectHarnessLike

from .rich_node import render_node
from .rich_query import render_query
from .rich_tree import render_tree


class RichDebug:
    @staticmethod
    def tree(root: object, inspector: InspectorLike) -> None:

        render_tree(root, inspector)

    @staticmethod
    def query(nodes: list[object]) -> None:

        render_query(nodes)

    @staticmethod
    def node(node: object) -> None:

        render_node(node)

    @staticmethod
    def debug_selector(harness: SelectHarnessLike, selector: str) -> None:

        nodes = harness.select(selector)

        render_query(nodes)

        for node in nodes:
            render_node(node)
