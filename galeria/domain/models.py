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
    periodo: str | None = None
    era_id: str = ""


@dataclass(frozen=True, slots=True)
class Era:
    id: str
    nome: str
    periodo: str
    ano_inicio: int
    ano_final: int | None
    theme: str
    descricao: str = ""
