# domain/models.py

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class TimelinePoint:
    x: float
    y: float


@dataclass(frozen=True, slots=True)
class Super:
    id: str
    nome: str
    foto: Path | None
    timeline: Path | None
    timeline_points: list[TimelinePoint] | None
    historias: list[str] | None
