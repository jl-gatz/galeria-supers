# tests/fakes/builders.py

from collections.abc import Sequence

from galeria.domain.models import Super, TimelinePoint

type SuperPath = str | None


def _to_src(value: SuperPath) -> str | None:
    return value


def super_stub_one(
    id: str = "1",
    nome: str = "Ada",
    foto: SuperPath = "ada.png",
    timeline: SuperPath = "ada.json",
    timeline_points: Sequence[TimelinePoint] | None = None,
    historias: list[str] | None = None,
    periodo: str | None = None,
    era_id: str = "",
) -> Super:
    return Super(
        id=id,
        nome=nome,
        foto=_to_src(foto),
        timeline=_to_src(timeline),
        timeline_points=list(timeline_points) if timeline_points is not None else None,
        historias=historias,
        periodo=periodo,
        era_id=era_id,
    )
