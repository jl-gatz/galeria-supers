# tests/harness/tree_inspector.py


class TreeInspector:
    def __init__(self, root):
        self.root = root

    # -------------------------
    # child extraction
    # -------------------------

    def _children(self, control):

        kids = []

        if hasattr(control, "controls") and control.controls:
            kids.extend(control.controls)

        if hasattr(control, "content") and control.content:
            kids.append(control.content)

        if hasattr(control, "items") and control.items:
            kids.extend(control.items)

        if hasattr(control, "tabs") and control.tabs:
            kids.extend(control.tabs)

        if hasattr(control, "actions") and control.actions:
            kids.extend(control.actions)

        return [k for k in kids if k is not None]

    # -------------------------
    # traversal
    # -------------------------

    def walk(self, control=None):

        if control is None:
            control = self.root

        yield control

        for child in self._children(control):
            yield from self.walk(child)

    # -------------------------
    # queries
    # -------------------------

    def find(self, cls):

        return [node for node in self.walk() if isinstance(node, cls)]

    def one(self, cls):

        matches = self.find(cls)

        if len(matches) != 1:
            raise AssertionError(f"Expected exactly 1 {cls.__name__}, found {len(matches)}")

        return matches[0]

    def count(self, cls):

        return len(self.find(cls))

    # -------------------------
    # debug
    # -------------------------

    def print_tree(self):

        def _print(node, depth=0):

            indent = "  " * depth
            print(f"{indent}{node.__class__.__name__}")

            for child in self._children(node):
                _print(child, depth + 1)

        _print(self.root)
