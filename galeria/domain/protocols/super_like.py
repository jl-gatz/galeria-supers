# domain/protocols/super_like.py
from collections.abc import Sequence
from typing import Any, Protocol


class SuperLike(Protocol):
    id: str
    nome: str
    image_path: str
    timeline_path: str
    periodo: str | None
    historias: Any
    timeline_points: Sequence[Any] | None
