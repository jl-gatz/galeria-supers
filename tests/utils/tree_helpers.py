# tests/utils/tree_helpers.py


def walk(control):
    yield control
    for child in get_children(control):
        yield from walk(child)


def get_children(control):
    children = []

    if hasattr(control, "content") and control.content:
        children.append(control.content)

    if hasattr(control, "controls") and control.controls:
        children.extend(control.controls)

    if hasattr(control, "items") and control.items:
        children.extend(control.items)

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
