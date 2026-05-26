# tests/ui/components/timeline/test_timeline_renderer.py

from galeria.ui.components.timeline.view import TimelineRenderer, TimelineStyle


def class_names(shapes):
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

    circles = [shape for shape in shapes if type(shape).__name__ == "Circle"]

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

    circles = [shape for shape in shapes if type(shape).__name__ == "Circle"]

    assert circles[0].radius == timeline_style.point_radius
    assert circles[1].radius == timeline_style.point_clicked_radius
    assert circles[2].radius == timeline_style.point_selected_radius
