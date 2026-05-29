# tests/fixtures/super_data.py

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from galeria.ui.components.timeline.models import TimelinePoint

type TimelinePointInput = Mapping[str, object] | tuple[float, float] | TimelinePoint
type SuperPath = Path | str | None


@dataclass
class FakeSuperData:
    id: str
    nome: str
    foto: SuperPath
    timeline: SuperPath
    timeline_points: Sequence[TimelinePointInput] | None
    historias: Sequence[str] | None
    periodo: str | None = None
