# tests/harness/selector_engine.py

from .tree_inspector import TreeInspector


class SelectorEngine:
    def __init__(self, root):

        self.root = root
        self.inspector = TreeInspector(root)

    def _match(self, node, name):

        return node.__class__.__name__ == name

    def _descendants(self, node):

        inspector = TreeInspector(node)

        # skip root
        first = True

        for n in inspector.walk():
            if first:
                first = False
                continue

            yield n

    def select(self, selector):

        tokens = selector.split()

        # primeiro token busca na árvore inteira
        current = [n for n in self.inspector.walk() if self._match(n, tokens[0])]

        # tokens seguintes buscam descendentes
        for token in tokens[1:]:
            next_nodes = []

            for node in current:
                for child in self._descendants(node):
                    if self._match(child, token):
                        next_nodes.append(child)

            current = next_nodes

        return current
