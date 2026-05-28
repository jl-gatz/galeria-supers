# tests/utils/snapshot_config.py

from collections.abc import Callable
from dataclasses import dataclass, field

from tests.utils.types import JsonValue, SerializedNode

Normalizer = Callable[[SerializedNode], SerializedNode]
ValueTransformer = Callable[[JsonValue], JsonValue]


def _empty_str_set() -> set[str]:
    return set()


def _empty_transformers() -> dict[str, ValueTransformer]:
    return {}


def _empty_normalizers() -> list[Normalizer]:
    return []


@dataclass(frozen=True)
class SnapshotConfig:
    version: str

    include_props: set[str] | bool | None = None
    exclude_props: set[str] = field(default_factory=_empty_str_set)

    ignore_types: set[str] = field(default_factory=_empty_str_set)

    transform_values: dict[str, ValueTransformer] = field(default_factory=_empty_transformers)
    normalizers: list[Normalizer] = field(default_factory=_empty_normalizers)

    max_depth: int | None = None

    # comportamento legado (se quiser manter compatibilidade com teu formato atual)
    use_legacy_layout: bool = False
