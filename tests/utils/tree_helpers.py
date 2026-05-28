from collections.abc import Iterator, Sequence

from tests.utils.types import HasContent, HasControls, HasItems, HasPrivateContent, SerializedNode


def walk(node: SerializedNode) -> Iterator[SerializedNode]:
    yield node
    for child in node.get("children", []):
        yield from walk(child)


def get_children(control: object) -> list[object]:
    children: list[object] = []
    # Tenta obter content (pode ser property ou atributo)
    try:
        content = control.content if isinstance(control, HasContent) else None
        if content is not None and not callable(content):
            children.append(content)
        else:
            # Fallback para alguns controles que usam _content internamente
            if isinstance(control, HasPrivateContent):
                content = control._content
                if content is not None:
                    children.append(content)
    except Exception as e:  # pragma: no cover - debug aid for odd Flet controls
        print(f"Erro ao acessar content de {type(control).__name__}: {e}")

    # Tenta obter controls
    try:
        controls = control.controls if isinstance(control, HasControls) else None
        if isinstance(controls, Sequence) and not isinstance(controls, (str, bytes)):
            children.extend(controls)
    except Exception:
        pass

    # Tenta obter items
    try:
        items = control.items if isinstance(control, HasItems) else None
        if isinstance(items, Sequence) and not isinstance(items, (str, bytes)):
            children.extend(items)
    except Exception:
        pass

    return children


def extract_cards(nodes: Sequence[SerializedNode]) -> list[object]:
    cards: list[object] = []

    for n in nodes:
        props = n.get("props", {})

        # 🔥 FILTRO para evitar outros tipos (só cards)
        if props.get("type") == "card":
            nome = props.get("nome")
            cards.append(nome)

    return cards


def extract_logos(nodes: Sequence[SerializedNode]) -> list[str] | None:
    logos = [n["props"]["nome"] for n in nodes if n.get("props", {}).get("type") == "logo"]

    return [str(logo) for logo in logos] if len(logos) == 2 else None


def has_placeholders(nodes: Sequence[SerializedNode]) -> bool:
    empty = [n for n in nodes if n["type"] == "Container" and not n.get("children")]

    return len(empty) >= 2


def extract_navigation(nodes: Sequence[SerializedNode]) -> list[str] | None:
    nav: list[str] = []

    for n in nodes:
        if n["type"] == "FloatingActionButton":
            key = n.get("props", {}).get("key")
            nav.append(str(key) if key else "fab")

    return nav or None
