# tests/ui/components/timeline/test_timeline_renderer.py

from collections.abc import Sequence

import flet as ft
import flet.canvas as cv

from galeria.ui.components.timeline.models import TimelinePoint
from galeria.ui.components.timeline.view import TimelineRenderer, TimelineStyle


def class_names(shapes: Sequence[object]) -> list[str]:
    return [type(shape).__name__ for shape in shapes]


def test_renderer_returns_empty_list_when_curve_is_empty(timeline_renderer: TimelineRenderer):
    shapes = timeline_renderer.render(
        pts=[(10, 10), (20, 20)],
        curve=[],
        progress=1.0,
        active_idx=0,
    )

    assert shapes == []


def test_renderer_returns_empty_list_when_curve_has_less_than_two_points(
    timeline_renderer: TimelineRenderer,
):
    shapes = timeline_renderer.render(
        pts=[(10, 10)],
        curve=[(10, 10)],
        progress=1.0,
        active_idx=0,
    )

    assert shapes == []


def test_renderer_creates_line_points_and_cursor(timeline_renderer: TimelineRenderer):
    pts = [(10, 10), (20, 20), (30, 10)]
    curve = [(10, 10), (20, 20), (30, 10)]

    shapes = timeline_renderer.render(
        pts=pts,
        curve=curve,
        progress=1.0,
        active_idx=1,
    )

    names = class_names(shapes)

    assert names.count("Path") == 1
    assert names.count("Circle") == 4  # 3 pontos + 1 cursor


def test_renderer_partial_progress_limits_visible_curve(timeline_renderer: TimelineRenderer):
    pts = [(10, 10), (20, 20), (30, 10), (40, 20)]
    curve = [(10, 10), (20, 20), (30, 10), (40, 20)]

    shapes = timeline_renderer.render(
        pts=pts,
        curve=curve,
        progress=0.5,
        active_idx=0,
    )

    assert len(shapes) == 6
    assert class_names(shapes).count("Path") == 1
    assert class_names(shapes).count("Circle") == 5  # 4 pontos + cursor


def test_renderer_uses_style_values(timeline_style: TimelineStyle):
    renderer = TimelineRenderer(timeline_style)
    pts = [(10, 10), (20, 20)]
    curve = [(10, 10), (20, 20)]

    shapes = renderer.render(
        pts=pts,
        curve=curve,
        progress=1.0,
        active_idx=0,
    )

    circles = [shape for shape in shapes if isinstance(shape, cv.Circle)]

    assert circles[0].radius == timeline_style.point_radius
    assert circles[-1].radius == timeline_style.cursor_radius


def test_renderer_uses_clicked_and_selected_point_states(timeline_style: TimelineStyle):
    renderer = TimelineRenderer(timeline_style)
    pts = [(10, 10), (20, 20), (30, 10)]
    curve = [(10, 10), (20, 20), (30, 10)]

    shapes = renderer.render(
        pts=pts,
        curve=curve,
        progress=1.0,
        active_idx=0,
        point_states={1: "clicked", 2: "selected"},
    )

    circles = [shape for shape in shapes if isinstance(shape, cv.Circle)]

    assert circles[0].radius == timeline_style.point_radius
    assert circles[1].radius == timeline_style.point_clicked_radius
    assert circles[2].radius == timeline_style.point_selected_radius


def test_renderer_draws_years_for_points_with_year(timeline_style: TimelineStyle):
    renderer = TimelineRenderer(timeline_style)
    pts = [(10, 10), (20, 20), (30, 10)]
    curve = [(10, 10), (20, 20), (30, 10)]
    points = [
        TimelinePoint(0.1, 0.2, year=1967),
        TimelinePoint(0.2, 0.4),
        TimelinePoint(0.3, 0.2, year=1969),
    ]

    shapes = renderer.render(
        pts=pts,
        curve=curve,
        progress=1.0,
        active_idx=0,
        points=points,
    )

    years = [shape for shape in shapes if isinstance(shape, cv.Text)]

    assert [year.value for year in years] == ["1967", "1969"]
    assert years[0].x == 10 + timeline_style.year_offset_x
    assert years[0].y == 10 + timeline_style.year_offset_y


def test_renderer_styles_years_by_point_state(timeline_style: TimelineStyle):
    renderer = TimelineRenderer(timeline_style)
    pts = [(10, 10), (20, 20), (30, 10)]
    curve = [(10, 10), (20, 20), (30, 10)]
    points = [
        TimelinePoint(0.1, 0.2, year=1967),
        TimelinePoint(0.2, 0.4, year=1968),
        TimelinePoint(0.3, 0.2, year=1969),
    ]

    shapes = renderer.render(
        pts=pts,
        curve=curve,
        progress=1.0,
        active_idx=0,
        point_states={1: "clicked", 2: "selected"},
        points=points,
    )

    years = [shape for shape in shapes if isinstance(shape, cv.Text)]

    first_style = years[0].style
    second_style = years[1].style
    third_style = years[2].style
    assert first_style is not None
    assert second_style is not None
    assert third_style is not None
    assert first_style.color == timeline_style.year_active_color
    assert first_style.weight == ft.FontWeight.BOLD
    assert second_style.color == timeline_style.year_visited_color
    assert third_style.color == timeline_style.year_selected_color
    assert third_style.weight == ft.FontWeight.BOLD
