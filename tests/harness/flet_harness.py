# tests/harness/flet_harness.py

import asyncio

from .tree_inspector import TreeInspector


class FletTestHarness:
    def __init__(self, page):

        self.page = page
        self.root = None
        self.inspector = None

    # -------------------------
    # mount component
    # -------------------------

    async def mount(self, control):

        self.root = control

        self.page.add(control)

        # simula lifecycle
        if hasattr(control, "did_mount"):
            control.did_mount()

        await self.flush()

        self.inspector = TreeInspector(control)

    # -------------------------
    # async flush
    # -------------------------

    async def flush(self):

        await asyncio.sleep(0)

    # -------------------------
    # query helpers
    # -------------------------

    def find(self, cls):

        return self.inspector.find(cls)

    def count(self, cls):

        return self.inspector.count(cls)

    def one(self, cls):

        return self.inspector.one(cls)

    # -------------------------
    # debug
    # -------------------------

    def print_tree(self):

        self.inspector.print_tree()
