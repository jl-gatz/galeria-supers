# tests/utils/snapshot_config.py

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

Normalizer = Callable[[dict], dict]
ValueTransformer = Callable[[Any], Any]


@dataclass(frozen=True)
class SnapshotConfig:
    version: str

    include_props: set[str] | None = None
    exclude_props: set[str] = field(default_factory=set)

    ignore_types: set[str] = field(default_factory=set)

    transform_values: dict[str, ValueTransformer] = field(default_factory=dict)
    normalizers: list[Normalizer] = field(default_factory=list)

    max_depth: int | None = None

    # comportamento legado (se quiser manter compatibilidade com teu formato atual)
    use_legacy_layout: bool = False
