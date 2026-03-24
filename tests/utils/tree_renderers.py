# tests/utils/tree_renderers.py

import flet as ft

from tests.utils.tree_helpers import (
    extract_cards,
    extract_logos,
    has_placeholders,
    walk,
)


def render_simple_tree(view) -> str:
    root = getattr(view, "content", None)

    if not root:
        return "Gallery"

    nodes = list(walk(root))
    lines = ["Gallery"]

    # TITLE
    title = next((c.value for c in nodes if isinstance(c, ft.Text)), None)
    if title:
        lines.append(f'├── Title("{title}")')

    # CARDS
    cards = extract_cards(nodes)
    if cards:
        lines.append("├── Cards")
        for i, card in enumerate(cards):
            prefix = "│    ├──" if i < len(cards) - 1 else "│    └──"
            lines.append(f"{prefix} Card({card})")

    # ARROW
    if any(isinstance(c, ft.IconButton) for c in nodes):
        lines.append("├── Arrow")

    # LOGOS
    logos = extract_logos(nodes)
    if logos:
        lines.append(f"├── Logos({', '.join(logos)})")

    # PLACEHOLDERS
    if has_placeholders(nodes):
        lines.append("└── Placeholders")

    return "\n".join(lines)
