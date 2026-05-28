from dataclasses import dataclass
from pathlib import Path

from galeria.domain.models import TimelinePoint

type SuperPath = Path | str | None


@dataclass
class SuperStub:
    id: str
    nome: str
    foto: SuperPath
    timeline: SuperPath
    timeline_points: list[TimelinePoint] | None
    historias: list[str] | None
    periodo: str | None = None
