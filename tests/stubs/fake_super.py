from pathlib import Path
from typing import Self

from galeria.domain.models import TimelinePoint


class FakeSuper:
    def __init__(self, historias: list[str]):
        self.id = "fake-super"
        self.nome = "Fake Super"
        self.foto: Path | str | None = None
        self.timeline: Path | str | None = None
        self.periodo: str | None = None
        self.timeline_points: list[TimelinePoint] | None = None
        self.historias = historias

    def __call__(self) -> Self:
        return self
