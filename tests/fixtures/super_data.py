# tests/fixtures/super_data.py

from dataclasses import dataclass
from pathlib import Path


@dataclass
class FakeSuperData:
    id: str
    nome: str
    foto: Path
    timeline: Path
    timeline_points: list[dict[str, float]] | None
    historias: list[str]
