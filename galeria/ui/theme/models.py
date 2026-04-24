# galeria/ui/theme/models.py

from dataclasses import dataclass


@dataclass
class Theme:
    title: str
    background: str
    primary: str
    text: str
