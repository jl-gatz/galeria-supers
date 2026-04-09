# tests/utils/tree_helpers.py


def walk(node):
    yield node
    for child in node.get("children", []):
        yield from walk(child)


# def _safe(value: Any):
#     """Ignora métodos e valores inválidos."""
#     if callable(value):
#         return None
#     return value


def get_children(control):
    children = []
    # Tenta obter content (pode ser property ou atributo)
    try:
        content = getattr(control, "content", None)
        if content is not None and not callable(content):
            children.append(content)
        else:
            # Fallback para alguns controles que usam _content internamente
            if hasattr(control, "_content"):
                content = control._content
                if content is not None:
                    children.append(content)
    except Exception as e:
        print(f"Erro ao acessar content de {type(control).__name__}: {e}")

    # Tenta obter controls
    try:
        controls = getattr(control, "controls", None)
        if isinstance(controls, list):
            children.extend(controls)
    except Exception:
        pass

    # Tenta obter items
    try:
        items = getattr(control, "items", None)
        if isinstance(items, list):
            children.extend(items)
    except Exception:
        pass

    return children


def extract_cards(nodes):
    cards = []

    for n in nodes:
        props = n.get("props", {})

        # 🔥 FILTRO para evitar outros tipos (só cards)
        if props.get("type") == "card":
            nome = props.get("nome")
            cards.append(nome)

    return cards


def extract_logos(nodes):
    logos = [n["props"]["nome"] for n in nodes if n.get("props", {}).get("type") == "logo"]

    return logos if len(logos) == 2 else None


def has_placeholders(nodes):
    empty = [n for n in nodes if n["type"] == "Container" and not n.get("children")]

    return len(empty) >= 2


def extract_navigation(nodes):
    nav = []

    for n in nodes:
        if n["type"] == "FloatingActionButton":
            key = n.get("props", {}).get("key")
            nav.append(key or "fab")

    return nav or None
