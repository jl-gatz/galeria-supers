# tests/utils/tree_helpers.py
from typing import Any


def walk(control):
    yield control
    for child in get_children(control):
        yield from walk(child)


def _safe(value: Any):
    """Ignora métodos e valores inválidos."""
    if callable(value):
        return None
    return value


def get_children(control):
    children = []

    # 🔹 content (filho único)
    content = _safe(getattr(control, "content", None))
    if content is not None:
        children.append(content)

    # 🔹 controls (lista)
    controls = _safe(getattr(control, "controls", None))
    if isinstance(controls, list):
        children.extend(controls)

    # 🔹 items (alguns widgets usam isso)
    items = _safe(getattr(control, "items", None))
    if isinstance(items, list):
        children.extend(items)

    # 🔹 fallback interno (Flet às vezes usa)
    _controls = _safe(getattr(control, "_controls", None))
    if isinstance(_controls, list):
        children.extend(_controls)

    return children


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
    import flet as ft

    empty = [c for c in nodes if isinstance(c, ft.Container) and not get_children(c)]
    return len(empty) >= 2
