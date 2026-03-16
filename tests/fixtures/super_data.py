# tests/fixtures/super_data.py

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class FakeSuperData:
    id: str
    nome: str
    image_path: Path
    timeline_path: Path
    timeline_points: dict[str, Any]
    historias: list[str]
