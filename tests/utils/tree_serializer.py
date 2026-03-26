# tests/utils/tree_serializer.py

from typing import Any

import flet as ft

from tests.utils.tree_helpers import get_children, walk

from .snapshot_config import SnapshotConfig

# ==========================================
# ENTRYPOINT
# ==========================================
print(get_children)
print(walk)


def serialize_tree(view, config: SnapshotConfig) -> Any:
    root = getattr(view, "content", None)

    if root is None:
        return "Gallery"

    # modo legado (teu formato atual em texto)
    if config.use_legacy_layout:
        return _serialize_legacy(root)

    return _serialize_node(root, config, depth=0)


# ==========================================
# CORE SERIALIZER (NOVO)
# ==========================================


def _serialize_node(node, config: SnapshotConfig, depth: int) -> dict | None:
    if config.max_depth is not None and depth > config.max_depth:
        return None

    node_type = type(node).__name__

    if node_type in config.ignore_types:
        return None

    props = _extract_props(node)

    # filtro de props
    if config.include_props:
        props = {k: v for k, v in props.items() if k in config.include_props}
    else:
        props = {k: v for k, v in props.items() if k not in config.exclude_props}

    # transformações simples
    for key, transform in config.transform_values.items():
        if key in props:
            props[key] = transform(props[key])

    result = {"type": node_type, "props": props, "children": []}

    # normalizers
    for normalizer in config.normalizers:
        result = normalizer(result)

    # filhos
    for child in get_children(node):
        serialized = _serialize_node(child, config, depth + 1)
        if serialized:
            result["children"].append(serialized)

    return result


# ==========================================
# EXTRAÇÃO DE PROPS
# ==========================================


def _extract_props(node) -> dict[str, Any]:
    props = {}

    # heurística simples (segura)
    for attr in dir(node):
        if attr.startswith("_"):
            continue

        try:
            value = getattr(node, attr)
        except Exception:
            continue

        # evita métodos / objetos complexos
        if callable(value):
            continue

        if isinstance(value, (str, int, float, bool)):
            props[attr] = value

    return props


# ==========================================
# LEGACY MODE (SERIALIZER ATUAL)
# ==========================================


def _serialize_legacy(root) -> str:
    nodes = list(walk(root))
    lines = ["Gallery"]

    # TITLE
    title = next((c.value for c in nodes if isinstance(c, ft.Text)), None)
    if title:
        lines.append(f"├── Title('{title}')")

    # CARDS
    cards = extract_cards(nodes)
    if cards:
        lines.append("├── Cards")
        for i, card in enumerate(cards):
            prefix = "│   ├──" if i < len(cards) - 1 else "│   └──"
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


# ==========================================
# HELPERS
# ==========================================


def extract_cards(nodes):
    cards = []

    for c in nodes:
        if hasattr(c, "super_data"):
            nome = getattr(c.super_data, "nome", None)
            if nome:
                cards.append(nome)

        elif hasattr(c, "src") and c.src:
            filename = c.src.split("/")[-1]
            nome = filename.split(".")[0]

            if nome not in ("detic", "unicamp"):
                cards.append(nome.capitalize())

    return cards


def extract_logos(nodes):
    logos = []

    for c in nodes:
        if hasattr(c, "src") and c.src:
            filename = c.src.split("/")[-1]
            nome = filename.split(".")[0]

            if nome in ("detic", "unicamp"):
                logos.append(nome)

    return logos if len(logos) == 2 else None


def has_placeholders(nodes):
    empty = [c for c in nodes if isinstance(c, ft.Container) and not get_children(c)]
    return len(empty) >= 2


# # ==========================================
# # TREE WALK
# # ==========================================


# def walk(control):
#     yield control
#     for child in get_children(control):
#         yield from walk(child)


# def get_children(control):
#     children = []

#     if hasattr(control, "content") and control.content:
#         children.append(control.content)

#     if hasattr(control, "controls") and control.controls:
#         children.extend(control.controls)

#     if hasattr(control, "items") and control.items:
#         children.extend(control.items)

#     return children
