# galeria/ui/components/timeline/models/timeline_point.py
"""Representação de um ponto narrativo da timeline."""

from typing import Any


class TimelinePoint:
    """Ponto normalizado com coordenadas, metadados e texto narrativo."""

    def __init__(
        self,
        x: float,
        y: float,
        data: dict[str, Any] | None = None,
        *,
        id: str | None = None,
        year: int | None = None,
        label: str = "",
        text: str = "",
    ):
        self.x: float = x
        self.y: float = y
        self.data: dict[str, Any] = data or {}

        self.id: str = id or str(self.data.get("id") or self.data.get("label") or "")
        data_year = self.data.get("year")
        self.year: int | None = year if year is not None else (
            int(data_year) if data_year is not None else None
        )
        self.label: str = label or str(self.data.get("label") or "")
        self.text: str = text or str(self.data.get("text") or "")
