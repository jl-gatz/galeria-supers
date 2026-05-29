# tests/utils/tree_serializer.py

from collections.abc import Mapping
from typing import TypeGuard, cast

import flet as ft

from tests.utils.tree_helpers import get_children
from tests.utils.types import (
    HasControls,
    HasData,
    HasKey,
    HasSrc,
    HasSuperData,
    HasValue,
    JsonValue,
    SerializedNode,
    SerializedTree,
    TreeProps,
)

from .snapshot_config import SnapshotConfig

# ==========================================
# ENTRYPOINT
# ==========================================
# print(get_children)
# print(walk)


def serialize_tree(view: object, config: SnapshotConfig) -> SerializedTree:
    root = getattr(view, "content", None)

    if isinstance(view, HasControls) and view.controls:
        root = view.controls[0]
    else:
        root = getattr(view, "content", None)

    if root is None:
        return {
            "type": "Gallery",
            "props": {},
            "children": [],
        }

    # modo legado (teu formato atual em texto)
    if config.use_legacy_layout:
        return _serialize_legacy(root)

    return _serialize_node(root, config, depth=0) or {
        "type": "Gallery",
        "props": {},
        "children": [],
    }


# ==========================================
# CORE SERIALIZER (NOVO)
# ==========================================


def _serialize_node(node: object, config: SnapshotConfig, depth: int) -> SerializedNode | None:
    if node is None:
        return None

    if config.max_depth is not None and depth > config.max_depth:
        return None

    node_type = type(node).__name__

    if node_type in config.ignore_types:
        return None

    props = _extract_props(node)

    # filtro de props
    if isinstance(config.include_props, set):
        props = {k: v for k, v in props.items() if k in config.include_props}
    elif config.include_props is True:
        props = dict(props)
    else:
        props = {k: v for k, v in props.items() if k not in config.exclude_props}

    # transformações simples
    for key, transform in config.transform_values.items():
        if key in props:
            props[key] = transform(props[key])

    result: SerializedNode = {
        "type": node_type,
        "props": props,
        "children": [],
    }

    # normalizers
    for normalizer in config.normalizers:
        result = normalizer(result)

    # filhos
    children = get_children(node)

    for child in children:
        serialized = _serialize_node(
            child,
            config,
            depth + 1,
        )

        if serialized is not None:
            result.setdefault("children", []).append(serialized)

    return result


# ==========================================
# EXTRAÇÃO DE PROPS
# ==========================================


def _extract_props(node: object) -> TreeProps:
    props: TreeProps = {}

    # 🔥 CASO ESPECIAL: super_data (Cards)
    if isinstance(node, HasSuperData):
        nome = getattr(node.super_data, "nome", None)
        if nome:
            props["nome"] = str(nome)

    if isinstance(node, HasData):
        raw_data: object = node.data
        if isinstance(raw_data, Mapping):
            props.update(_json_props(cast(Mapping[object, object], raw_data)))

    # 🔥 CASO ESPECIAL: Image src
    if isinstance(node, HasSrc) and isinstance(node.src, str):
        props["src"] = node.src

    # 🔥 CASO ESPECIAL: Text value
    if isinstance(node, HasValue) and isinstance(node.value, str):
        props["value"] = node.value

    # 🔥 CASO ESPECIAL: key (importante!)
    if isinstance(node, HasKey) and isinstance(node.key, str):
        props["key"] = node.key

    # 🔹 fallback genérico (mantém o que você já tem)
    for attr in dir(node):
        if attr.startswith("_"):
            continue

        if attr in props:  # 👈 evita sobrescrever
            continue

        try:
            value: object = getattr(node, attr)
        except Exception:
            continue

        if callable(value):
            continue

        if isinstance(value, (str, int, float, bool)):
            props[attr] = value

    # print(getattr(node, "src", None))

    return props


def _json_props(data: Mapping[object, object]) -> TreeProps:
    props: TreeProps = {}
    for key, value in data.items():
        if isinstance(key, str) and _is_json_value(value):
            props[key] = value
    return props


def _is_json_value(value: object) -> TypeGuard[JsonValue]:
    if value is None or isinstance(value, (str, int, float, bool)):
        return True
    if isinstance(value, list):
        list_items = cast(list[object], value)
        return all(_is_json_value(item) for item in list_items)
    if isinstance(value, dict):
        dict_items = cast(dict[object, object], value)
        return all(
            isinstance(key, str) and _is_json_value(item) for key, item in dict_items.items()
        )
    return False


# ==========================================
# LEGACY MODE (SERIALIZER ATUAL)
# ==========================================
def _dict_to_simple_text(node: SerializedNode, indent: int = 0) -> list[str]:
    """Converte o dicionário do novo serializador no formato textual antigo."""
    lines: list[str] = []
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
        src = props["src"]
        filename = str(src).split("/")[-1]
        name = filename.split(".")[0].capitalize()
        lines.append(f"{prefix}Card({name})")
    else:
        # Fallback genérico
        lines.append(f"{prefix}{node_type}")

    # Processa filhos recursivamente
    for child in node.get("children", []):
        lines.extend(_dict_to_simple_text(child, indent + 1))

    return lines


def _serialize_legacy(root: object) -> str:
    # Usa o novo serializador com uma config padrão
    config = SnapshotConfig(
        version="legacy", use_legacy_layout=False, max_depth=None, include_props=True
    )
    tree_dict = _serialize_node(root, config, depth=0)
    if tree_dict is None:
        raise ValueError(f"Could not serialize root node: {root} ({type(root)})")
    lines = ["Gallery"]
    print(f"[DEBUG] Árvore serializada: {tree_dict}")
    lines.extend(_dict_to_simple_text(tree_dict, indent=1))
    return "\n".join(lines)


# ==========================================
# HELPERS
# ==========================================


def extract_cards(nodes: list[object]) -> list[object]:
    print(f"[DEBUG] Nós recebidos: {[type(n).__name__ for n in nodes[:10]]}")
    cards: list[object] = []
    for c in nodes:
        if isinstance(c, HasSuperData):
            name = c.super_data
            if name:
                cards.append(name)
        elif isinstance(c, HasSrc) and isinstance(c.src, str) and c.src:
            # Se for Image, extrai nome do arquivo
            filename = c.src.split("/")[-1]  # mais robusto
            name = filename.split(".")[0].capitalize()
            if name not in ("detic", "unicamp"):
                cards.append(name)
    return cards


def extract_logos(nodes: list[object]) -> list[str] | None:
    logos: list[str] = []

    for c in nodes:
        if isinstance(c, HasSrc) and isinstance(c.src, str) and c.src:
            filename = c.src.split("/")[-1]
            nome = filename.split(".")[0]

            if nome in ("detic", "unicamp"):
                logos.append(nome)

    return logos if len(logos) == 2 else None


def has_placeholders(nodes: list[object]) -> bool:
    empty = [c for c in nodes if isinstance(c, ft.Container) and not get_children(c)]
    return len(empty) >= 2
