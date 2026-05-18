# tests/fakes/builders.py

from pathlib import Path
from typing import Any

from galeria.domain.models import Super


def super_stub_one(
    id: str = "1",
    nome: str = "Ada",
    foto: Path = Path("ada.png"),
    timeline: Path = Path("ada.json"),
    timeline_points: dict[str, Any] | None = None,
    historias: list[str] | None = None,
    periodo: str | None = None,
):
    return Super(
        id=id,
        nome=nome,
        foto=foto,
        timeline=timeline,
        timeline_points=timeline_points,
        historias=historias,
        periodo=periodo,
    )
