# tests/ui/components/timeline/test_timeline_canvas.py

from galeria.ui.components.timeline.view import TimelineCanvas


def test_timeline_canvas_creates_canvas_with_default_dimensions():
    timeline_canvas = TimelineCanvas()

    assert timeline_canvas.width == 1900
    assert timeline_canvas.height == 300
    assert timeline_canvas.canvas.expand is True
    assert timeline_canvas.canvas.shapes == []


def test_timeline_canvas_accepts_resize_callback():
    def on_resize(_):
        pass

    timeline_canvas = TimelineCanvas(on_resize=on_resize)

    assert timeline_canvas.canvas.on_resize == on_resize


def test_timeline_canvas_sets_shapes():
    timeline_canvas = TimelineCanvas()
    shapes = [object(), object()]

    timeline_canvas.set_shapes(shapes)

    assert timeline_canvas.canvas.shapes == shapes
