# tests/utils/tree_serializer.py

from typing import Any

import flet as ft

from tests.utils.tree_helpers import get_children

from .snapshot_config import SnapshotConfig

# ==========================================
# ENTRYPOINT
# ==========================================
# print(get_children)
# print(walk)


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

    # 🔥 CASO ESPECIAL: super_data (Cards)
    if hasattr(node, "super_data"):
        nome = getattr(node.super_data, "nome", None)
        if nome:
            props["nome"] = nome

    if hasattr(node, "data") and isinstance(node.data, dict):
        props.update(node.data)

    # 🔥 CASO ESPECIAL: Image src
    if hasattr(node, "src") and isinstance(node.src, str):
        props["src"] = node.src

    # 🔥 CASO ESPECIAL: Text value
    if hasattr(node, "value") and isinstance(node.value, str):
        props["value"] = node.value

    # 🔥 CASO ESPECIAL: key (importante!)
    if hasattr(node, "key") and isinstance(node.key, str):
        props["key"] = node.key

    # 🔹 fallback genérico (mantém o que você já tem)
    for attr in dir(node):
        if attr.startswith("_"):
            continue

        if attr in props:  # 👈 evita sobrescrever
            continue

        try:
            value = getattr(node, attr)
        except Exception:
            continue

        if callable(value):
            continue

        if isinstance(value, (str, int, float, bool)):
            props[attr] = value

    # print(getattr(node, "src", None))

    return props


# ==========================================
# LEGACY MODE (SERIALIZER ATUAL)
# ==========================================
def _dict_to_simple_text(node: dict, indent: int = 0) -> list[str]:
    """Converte o dicionário do novo serializador no formato textual antigo."""
    lines = []
    prefix = "| " * indent if indent > 0 else ""
    node_type = node.get("type", "Unknown")
    props = node.get("props", {})

    # Título especial (se for Text)
    if node_type == "Text" and "value" in props:
        lines.append(f"{prefix}Title('{props['value']}')")
    elif node_type == "FloatingActionButton":
        lines.append(f"{prefix}FAB")
    elif node_type == "Image" and "src" in props:
        # Extrai nome do arquivo para simular Card (se necessário)
        filename = props["src"].split("/")[-1]
        name = filename.split(".")[0].capitalize()
        lines.append(f"{prefix}Card({name})")
    else:
        # Fallback genérico
        lines.append(f"{prefix}{node_type}")

    # Processa filhos recursivamente
    for child in node.get("children", []):
        lines.extend(_dict_to_simple_text(child, indent + 1))

    return lines


def _serialize_legacy(root) -> str:
    # Usa o novo serializador com uma config padrão
    config = SnapshotConfig(use_legacy_layout=False, max_depth=None, include_props=True)
    tree_dict = _serialize_node(root, config, depth=0)
    if tree_dict is None:
        return "Gallery"
    lines = ["Gallery"]
    lines.extend(_dict_to_simple_text(tree_dict, indent=1))
    return "\n".join(lines)


# ==========================================
# HELPERS
# ==========================================


def extract_cards(nodes):
    print(f"[DEBUG] Nós recebidos: {[type(n).__name__ for n in nodes[:10]]}")
    cards = []
    for c in nodes:
        if hasattr(c, "super_data"):
            name = getattr(c, "super_data", None)
            if name:
                cards.append(name)
        elif hasattr(c, "src") and c.src:
            # Se for Image, extrai nome do arquivo
            filename = c.src.split("/")[-1]  # mais robusto
            name = filename.split(".")[0].capitalize()
            if name not in ("detic", "unicamp"):
                cards.append(name)
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
