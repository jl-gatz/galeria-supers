# tests/harness/flet_harness.py

import asyncio

from .control_query import find_by_id, find_by_text, find_by_type
from .interactions import click
from .tree_inspector import inspect_tree


class FletTestHarness:
    def __init__(self):
        self.root = None

    async def mount(self, component):

        self.root = component
        await asyncio.sleep(0)  # Apenas para tornar o método async
        return component

    def debug_tree(self):

        inspect_tree(self.root)

    def find(self, control_type):
        return find_by_type(self.root, control_type)

    def get_by_id(self, cid):

        control = find_by_id(self.root, cid)

        if control is None:
            raise AssertionError(f"Control id={cid} not found")

        return control

    def get_by_text(self, text):

        controls = find_by_text(self.root, text)

        if not controls:
            raise AssertionError(f"Text '{text}' not found")

        return controls[0]

    def click(self, cid):

        control = self.get_by_id(cid)
        click(control)
