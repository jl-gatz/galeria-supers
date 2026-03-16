# tests/debug/rich_debug.py

from .rich_node import render_node
from .rich_query import render_query
from .rich_tree import render_tree


class RichDebug:
    @staticmethod
    def tree(root, inspector):

        render_tree(root, inspector)

    @staticmethod
    def query(nodes):

        render_query(nodes)

    @staticmethod
    def node(node):

        render_node(node)

    @staticmethod
    def debug_selector(harness, selector):

        nodes = harness.select(selector)

        render_query(nodes)

        for node in nodes:
            render_node(node)
