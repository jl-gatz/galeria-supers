# galeria/ui/components/timeline/utils/timeline_mapper.py
"""Conversores entre dados narrativos e coordenadas de canvas."""

import math
from collections.abc import Mapping, Sequence
from typing import Any, cast

from ..models.timeline_point import TimelinePoint


def extract_points_from_super(raw_points: Sequence[Any]) -> list[TimelinePoint]:
    """Converte pontos crus do controller em instâncias de TimelinePoint."""

    points: list[TimelinePoint] = []

    for item in raw_points:
        # adapte conforme seu formato real
        if isinstance(item, Mapping):
            data = cast(Mapping[str, Any], item)
            x = float(data.get("x", 0))
            y = float(data.get("y", 0.5))
            point_id = data.get("id")
            year = data.get("year")
            points.append(
                TimelinePoint(
                    x,
                    y,
                    data=dict(data),
                    id=str(point_id) if point_id is not None else None,
                    year=int(year) if year is not None else None,
                    label=str(data.get("label", "")),
                    text=str(data.get("text", "")),
                )
            )

        elif isinstance(item, tuple):
            pair = cast(tuple[Any, ...], item)
            if len(pair) < 2:
                continue
            points.append(TimelinePoint(float(pair[0]), float(pair[1])))

        elif isinstance(item, TimelinePoint):
            # fallback defensivo
            points.append(item)

    return points


def map_indexed_points_to_canvas(
    points: Sequence[TimelinePoint], width: float, height: float
) -> list[tuple[int, float, float]]:
    """Mapeia pontos normalizados para coordenadas de canvas com índice."""
    mapped: list[tuple[int, float, float]] = []

    for index, point in enumerate(points):
        try:
            x = float(point.x) * width
            y = float(point.y) * height

            if not (math.isfinite(x) and math.isfinite(y)):
                continue

            mapped.append((index, x, y))
        except Exception:
            continue

    return mapped


def map_points_to_canvas(
    points: Sequence[TimelinePoint], width: float, height: float
) -> list[tuple[float, float]]:
    """Mapeia pontos normalizados para coordenadas de canvas."""
    return [(x, y) for _, x, y in map_indexed_points_to_canvas(points, width, height)]
