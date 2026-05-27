# tests/ui/components/timeline/test_timeline_mapper.py

from galeria.ui.components.timeline.models import TimelinePoint
from galeria.ui.components.timeline.utils import (
    extract_points_from_super,
    map_indexed_points_to_canvas,
    map_points_to_canvas,
)


def test_mapper_converts_dicts_to_timeline_points():
    raw_points = [
        {
            "id": "ingresso-1967",
            "x": 0.1,
            "y": 0.8,
            "year": 1967,
            "label": "ingresso",
            "text": "Entrada.",
        },
        {
            "id": "destaque-1968",
            "x": 0.5,
            "y": 0.2,
            "year": 1968,
            "label": "destaque",
            "text": "Destaque.",
        },
    ]

    points = extract_points_from_super(raw_points)

    assert len(points) == 2
    assert all(isinstance(point, TimelinePoint) for point in points)

    assert points[0].x == 0.1
    assert points[0].y == 0.8
    assert points[0].data == raw_points[0]
    assert points[0].id == "ingresso-1967"
    assert points[0].year == 1967
    assert points[0].label == "ingresso"
    assert points[0].text == "Entrada."


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


def test_mapper_maps_points_to_canvas_coordinates():
    points = [
        TimelinePoint(0.1, 0.2),
        TimelinePoint(0.5, 0.8),
    ]

    assert map_points_to_canvas(points, width=1000, height=200) == [
        (100.0, 40.0),
        (500.0, 160.0),
    ]


def test_mapper_maps_indexed_points_and_skips_invalid_coordinates():
    points = [
        TimelinePoint(0.1, 0.2),
        TimelinePoint("invalid", 0.8),
        TimelinePoint(0.5, 0.6),
    ]

    assert map_indexed_points_to_canvas(points, width=1000, height=200) == [
        (0, 100.0, 40.0),
        (2, 500.0, 120.0),
    ]
