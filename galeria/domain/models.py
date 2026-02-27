# domain/models.py

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Super:
    id: str
    nome: str
    foto: Path
    historias: str
