from .timeline_point import TimelinePoint


class TimelineModel:
    def __init__(self, points: list[TimelinePoint] | None = None):
        self._points: list[TimelinePoint] = points or []

    # =========================
    # API pública
    # =========================

    @property
    def points(self) -> list[TimelinePoint]:
        return self._points

    def add_point(self, point: TimelinePoint):
        self._points.append(point)

    def extend_points(self, points: list[TimelinePoint]):
        self._points.extend(points)

    def clear(self):
        self._points.clear()

    def count(self) -> int:
        return len(self._points)

    def get(self, index: int) -> TimelinePoint:
        return self._points[index]

    def get_point_by_id(self, point_id: str) -> TimelinePoint | None:
        return next((point for point in self._points if point.id == point_id), None)

    # =========================
    # utilidades de domínio
    # =========================

    def as_tuples(self):
        """Retorna [(x, y), ...] para uso no renderer/path_builder"""
        return [(p.x, p.y) for p in self._points]

    def is_empty(self) -> bool:
        return len(self._points) == 0
