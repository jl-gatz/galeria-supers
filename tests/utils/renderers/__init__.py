# tests/utils/renderers/__init__.py

from tests.utils.tree_render_registry import registry

from .json_renderer import render_json
from .render_simple import render_simple


def register_default_renderers() -> None:
    registry.register("json", render_json)
    registry.register("simple", render_simple)
