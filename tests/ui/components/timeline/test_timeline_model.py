# tests/ui/components/timeline/test_timeline_model.py

from galeria.ui.components.timeline.models import TimelineModel, TimelinePoint


def test_timeline_model_starts_empty_when_no_points_are_given():
    model = TimelineModel()

    assert model.points == []
    assert model.count() == 0
    assert model.is_empty() is True


def test_timeline_model_keeps_initial_points(timeline_points: list[TimelinePoint]):
    model = TimelineModel(points=timeline_points)

    assert model.points == timeline_points
    assert model.count() == 3
    assert model.is_empty() is False


def test_timeline_model_adds_point():
    model = TimelineModel()
    point = TimelinePoint(0.2, 0.4)

    model.add_point(point)

    assert model.points == [point]
    assert model.count() == 1


def test_timeline_model_extends_points(timeline_points: list[TimelinePoint]):
    model = TimelineModel()

    model.extend_points(timeline_points)

    assert model.points == timeline_points
    assert model.count() == 3


def test_timeline_model_clears_points(timeline_points: list[TimelinePoint]):
    model = TimelineModel(points=timeline_points)

    model.clear()

    assert model.points == []
    assert model.is_empty() is True


def test_timeline_model_gets_point_by_index(timeline_points: list[TimelinePoint]):
    model = TimelineModel(points=timeline_points)

    assert model.get(1) == timeline_points[1]


def test_timeline_model_returns_points_as_tuples(timeline_points: list[TimelinePoint]):
    model = TimelineModel(points=timeline_points)

    assert model.as_tuples() == [
        (0.10, 0.80),
        (0.50, 0.20),
        (0.90, 0.60),
    ]
