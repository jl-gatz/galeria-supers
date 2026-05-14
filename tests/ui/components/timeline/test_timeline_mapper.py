# tests/ui/components/timeline/test_timeline_mapper.py

from galeria.ui.components.timeline.models import TimelinePoint
from galeria.ui.components.timeline.utils import (
    extract_points_from_super,
)


def test_mapper_converts_dicts_to_timeline_points():
    raw_points = [
        {"x": 0.1, "y": 0.8, "year": 1967, "label": "ingresso"},
        {"x": 0.5, "y": 0.2, "year": 1968, "label": "destaque"},
    ]

    points = extract_points_from_super(raw_points)

    assert len(points) == 2
    assert all(isinstance(point, TimelinePoint) for point in points)

    assert points[0].x == 0.1
    assert points[0].y == 0.8
    assert points[0].data == raw_points[0]


def test_mapper_uses_default_values_for_missing_dict_coordinates():
    raw_points = [
        {"label": "sem coordenadas"},
    ]

    points = extract_points_from_super(raw_points)

    assert points[0].x == 0
    assert points[0].y == 0.5
    assert points[0].data == raw_points[0]


def test_mapper_converts_tuples_to_timeline_points():
    raw_points = [
        (0.1, 0.8),
        (0.5, 0.2),
    ]

    points = extract_points_from_super(raw_points)

    assert [(point.x, point.y) for point in points] == raw_points


def test_mapper_keeps_unknown_items_as_defensive_fallback():
    existing_point = TimelinePoint(0.2, 0.3)
    raw_points = [existing_point]

    points = extract_points_from_super(raw_points)

    assert points == [existing_point]
