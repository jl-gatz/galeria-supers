# tests/utils/renderers/json_renderer.py

import json

from tests.utils.types import SerializedTree


def render_json(tree: SerializedTree) -> str:
    return json.dumps(
        tree,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
    )
