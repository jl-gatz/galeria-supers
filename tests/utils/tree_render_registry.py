# tests/utils/tree_render_registry.py

from collections.abc import Callable

from tests.utils.types import SerializedTree

Renderer = Callable[[SerializedTree], str]


class TreeRenderRegistry:
    def __init__(self) -> None:
        self._renderers: dict[str, Renderer] = {}

    def register(self, name: str, renderer: Renderer) -> None:
        self._renderers[name] = renderer

    def get(self, name: str) -> Renderer:
        if name not in self._renderers:
            raise ValueError(f"Renderer '{name}' not registered")
        return self._renderers[name]

    def render(self, name: str, tree: SerializedTree) -> str:
        renderer = self.get(name)
        return renderer(tree)


# singleton global (simples e suficiente)
registry = TreeRenderRegistry()
