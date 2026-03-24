# tests/utils/renderers/json_renderer.py

import json


def render_json(tree) -> str:
    return json.dumps(
        tree,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
    )
