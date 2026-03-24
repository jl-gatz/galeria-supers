# tests/utils/tree_render_registry.py

from collections.abc import Callable
from typing import Any

Renderer = Callable[[Any], str]


class TreeRenderRegistry:
    def __init__(self):
        self._renderers: dict[str, Renderer] = {}

    def register(self, name: str, renderer: Renderer):
        self._renderers[name] = renderer

    def get(self, name: str) -> Renderer:
        if name not in self._renderers:
            raise ValueError(f"Renderer '{name}' not registered")
        return self._renderers[name]

    def render(self, name: str, tree: Any) -> str:
        renderer = self.get(name)
        return renderer(tree)


# singleton global (simples e suficiente)
registry = TreeRenderRegistry()
