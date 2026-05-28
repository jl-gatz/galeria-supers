# galeria/ui/components/timeline/models/timeline_model.py
"""Modelo em memória para os pontos da timeline."""

from .timeline_point import TimelinePoint


class TimelineModel:
    """Coleção ordenada de pontos consumida pelo controlador e renderer."""

    def __init__(self, points: list[TimelinePoint] | None = None):
        self._points: list[TimelinePoint] = points or []

    # =========================
    # API pública
    # =========================

    @property
    def points(self) -> list[TimelinePoint]:
        """Retorna a lista de pontos mantida pelo modelo."""
        return self._points

    def add_point(self, point: TimelinePoint) -> None:
        """Adiciona um ponto ao fim da timeline."""
        self._points.append(point)

    def extend_points(self, points: list[TimelinePoint]) -> None:
        """Adiciona vários pontos ao fim da timeline."""
        self._points.extend(points)

    def clear(self) -> None:
        """Remove todos os pontos da timeline."""
        self._points.clear()

    def count(self) -> int:
        """Retorna a quantidade de pontos registrados."""
        return len(self._points)

    def get(self, index: int) -> TimelinePoint:
        """Retorna o ponto na posição informada."""
        return self._points[index]

    def get_point_by_id(self, point_id: str) -> TimelinePoint | None:
        """Busca um ponto pelo identificador narrativo."""
        return next((point for point in self._points if point.id == point_id), None)

    # =========================
    # utilidades de domínio
    # =========================

    def as_tuples(self) -> list[tuple[float, float]]:
        """Retorna pares de coordenadas para renderer e PathBuilder."""
        return [(p.x, p.y) for p in self._points]

    def is_empty(self) -> bool:
        """Indica se o modelo está sem pontos."""
        return len(self._points) == 0
