# domain/models.py

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class Super:
    id: str
    nome: str
    foto: Path
    timeline: Path
    timeline_points: dict[str, Any]
    historias: list[str]
