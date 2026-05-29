# tests/fakes/builders.py

from collections.abc import Sequence
from pathlib import Path

from galeria.domain.models import Super, TimelinePoint

type SuperPath = Path | str | None


def _to_path(value: SuperPath) -> Path | None:
    if value is None or isinstance(value, Path):
        return value
    return Path(value)


def super_stub_one(
    id: str = "1",
    nome: str = "Ada",
    foto: SuperPath = Path("ada.png"),
    timeline: SuperPath = Path("ada.json"),
    timeline_points: Sequence[TimelinePoint] | None = None,
    historias: list[str] | None = None,
    periodo: str | None = None,
    era_id: str = "",
) -> Super:
    return Super(
        id=id,
        nome=nome,
        foto=_to_path(foto),
        timeline=_to_path(timeline),
        timeline_points=list(timeline_points) if timeline_points is not None else None,
        historias=historias,
        periodo=periodo,
        era_id=era_id,
    )
