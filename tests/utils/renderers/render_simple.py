# tests/utils/renderers/simple_renderer.py


from tests.utils.tree_helpers import (
    extract_cards,
    extract_logos,
    has_placeholders,
    walk,
)

# def walk(node):
#     yield node
#     for child in node.get("children", []):
#         yield from walk(child)


def render_simple(tree) -> str:
    nodes = list(walk(tree))
    lines = ["Gallery"]

    # TITLE
    title = next(
        (
            n.get("props", {}).get("value")
            for n in nodes
            if n["type"] == "Text" and n.get("props", {}).get("value")
        ),
        None,
    )
    if title:
        lines.append(f'├── Title("{title}")')

    # CARDS (mantém sua lógica adaptada)
    cards = extract_cards(nodes)
    if cards:
        lines.append("├── Cards")
        for i, card in enumerate(cards):
            prefix = "│    ├──" if i < len(cards) - 1 else "│    └──"
            lines.append(f"{prefix} Card({card})")

    # FAB / ARROW 🔥 (agora funciona)
    if any(n["type"] == "FloatingActionButton" for n in nodes):
        lines.append("├── FAB")

    # LOGOS
    logos = extract_logos(nodes)
    if logos:
        lines.append(f"├── Logos({', '.join(logos)})")

    # PLACEHOLDERS
    if has_placeholders(nodes):
        lines.append("└── Placeholders")

    return "\n".join(lines)
