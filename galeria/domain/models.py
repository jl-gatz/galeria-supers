# galeria/domain/models.py
"""Entidades de domínio usadas pela galeria."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class TimelinePoint:
    """Coordenada normalizada de um ponto da timeline no domínio."""

    x: float
    y: float


@dataclass(frozen=True, slots=True)
class Super:
    """Representa um superintendente e seus dados narrativos."""

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
    """Representa uma era institucional associada a um tema visual."""

    id: str
    nome: str
    periodo: str
    ano_inicio: int
    ano_final: int | None
    theme: str
    descricao: str = ""
