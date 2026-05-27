# tests/ui/components/timeline/test_timeline_view.py

from unittest.mock import Mock

import pytest

from galeria.ui.components.timeline.controller import (
    TimelineController,
)
from galeria.ui.components.timeline.models import TimelineModel, TimelinePoint
from galeria.ui.components.timeline.utils import PathBuilder
from galeria.ui.components.timeline.view import TimelineRenderer, TimelineStyle, TimelineView


@pytest.fixture
def model():
    return TimelineModel(
        points=[
            TimelinePoint(0.0, 1.0, id="ingresso"),
            TimelinePoint(0.5, 0.0, id="destaque"),
            TimelinePoint(1.0, 0.5, id="saida"),
        ]
    )


@pytest.fixture
def controller(model: TimelineModel):
    return TimelineController(model)


@pytest.fixture
def renderer():
    return TimelineRenderer(TimelineStyle())


@pytest.fixture
def path_builder():
    return PathBuilder(mode="linear")


@pytest.fixture
def timeline_view(
    controller: TimelineController, path_builder: PathBuilder, renderer: TimelineRenderer
):
    return TimelineView(
        controller=controller,
        path_builder=path_builder,
        renderer=renderer,
    )


def test_timeline_view_binds_itself_to_controller(
    controller: TimelineController, path_builder: PathBuilder, renderer: TimelineRenderer
):
    view = TimelineView(
        controller=controller,
        path_builder=path_builder,
        renderer=renderer,
    )

    assert controller.view is view


def test_timeline_view_exposes_control(timeline_view: TimelineView):
    assert timeline_view.control is timeline_view._control


def test_timeline_view_creates_canvas(timeline_view: TimelineView):
    assert timeline_view.canvas.width == 1900
    assert timeline_view.canvas.height == 300


def test_timeline_view_normalizes_points_to_canvas_coordinates(timeline_view: TimelineView):
    normalized = timeline_view._normalize_points(
        timeline_view.controller.model.points,
        width=1000,
        height=200,
    )

    assert normalized == [
        (0.0, 200.0),
        (500.0, 0.0),
        (1000.0, 100.0),
    ]


def test_timeline_view_normalize_returns_empty_list_for_empty_points(
    timeline_view: TimelineView,
):
    assert timeline_view._normalize_points([], width=1000, height=200) == []


def test_timeline_view_normalize_ignores_invalid_points(timeline_view: TimelineView):
    points = [
        TimelinePoint(0.1, 0.2),
        TimelinePoint("invalid", 0.5),
        TimelinePoint(0.3, None),
    ]

    normalized = timeline_view._normalize_points(
        points,
        width=1000,
        height=200,
    )

    assert normalized == [(100.0, 40.0)]


def test_timeline_view_get_curve_uses_cache_for_same_size(timeline_view: TimelineView):
    timeline_view.path_builder.build_path = Mock(return_value=[(0, 0), (1, 1)])

    pts = [(0, 0), (1, 1)]

    first = timeline_view._get_curve(pts, width=100, height=100)
    second = timeline_view._get_curve(pts, width=100, height=100)

    assert first == second
    timeline_view.path_builder.build_path.assert_called_once_with(pts)


def test_timeline_view_get_curve_rebuilds_when_size_changes(timeline_view: TimelineView):
    timeline_view.path_builder.build_path = Mock(
        side_effect=[
            [(0, 0), (1, 1)],
            [(0, 0), (2, 2)],
        ]
    )

    pts = [(0, 0), (1, 1)]

    first = timeline_view._get_curve(pts, width=100, height=100)
    second = timeline_view._get_curve(pts, width=200, height=100)

    assert first != second
    assert timeline_view.path_builder.build_path.call_count == 2


def test_timeline_view_on_resize_invalidates_cache_and_refreshes(timeline_view: TimelineView):
    timeline_view.refresh = Mock()
    timeline_view._cached_curve = [(0, 0), (1, 1)]
    timeline_view._last_size = (100, 100)

    timeline_view._on_resize(None)

    assert timeline_view._cached_curve is None
    assert timeline_view._last_size is None
    timeline_view.refresh.assert_called_once()


def test_timeline_view_draw_returns_when_canvas_has_invalid_size(timeline_view: TimelineView):
    timeline_view.canvas.canvas.width = 0
    timeline_view.canvas.canvas.height = 300

    timeline_view._draw()

    assert timeline_view.canvas.canvas.shapes == []


def test_timeline_view_refresh_draws_shapes(monkeypatch, timeline_view: TimelineView):
    safe_update = Mock()
    monkeypatch.setattr(
        "galeria.ui.components.timeline.view.timeline_view.safe_update",
        safe_update,
    )

    timeline_view.refresh()

    assert timeline_view.canvas.canvas.shapes
    safe_update.assert_called_once_with(timeline_view.control)


def test_timeline_view_uses_stack_with_canvas_behind_clickable_points(
    monkeypatch, timeline_view: TimelineView
):
    monkeypatch.setattr(
        "galeria.ui.components.timeline.view.timeline_view.safe_update",
        Mock(),
    )

    timeline_view.refresh()

    assert type(timeline_view.control.content).__name__ == "Stack"
    assert type(timeline_view.control.content.controls[0]).__name__ == "TransparentPointer"
    assert timeline_view.control.content.controls[0].content is timeline_view.canvas.canvas
    assert all(
        type(control).__name__ == "Container"
        for control in timeline_view.control.content.controls[1:]
    )


def test_timeline_view_builds_clickable_points_over_rendered_coordinates(
    monkeypatch, timeline_view: TimelineView
):
    monkeypatch.setattr(
        "galeria.ui.components.timeline.view.timeline_view.safe_update",
        Mock(),
    )

    timeline_view.refresh()
    target = timeline_view.canvas_stack.controls[2]

    assert target.left == 950 - timeline_view.hit_size / 2
    assert target.top == 0 - timeline_view.hit_size / 2
    assert target.width == timeline_view.hit_size
    assert target.height == timeline_view.hit_size
    assert target.data == {"type": "timeline_point", "id": "destaque"}
    assert target.on_click is not None


def test_timeline_view_point_tap_selects_point_and_rebuilds(
    monkeypatch, timeline_view: TimelineView
):
    monkeypatch.setattr(
        "galeria.ui.components.timeline.view.timeline_view.safe_update",
        Mock(),
    )
    timeline_view.controller.select_point = Mock()

    timeline_view.refresh()
    timeline_view._rebuild = Mock()
    target = timeline_view.canvas_stack.controls[2]
    target.on_click(None)

    timeline_view.controller.select_point.assert_called_once_with("destaque")
    timeline_view._rebuild.assert_called_once()
