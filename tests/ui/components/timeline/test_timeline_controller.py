# tests/ui/components/timeline/test_timeline_controller.py

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from galeria.ui.components.timeline.controller import (
    TimelineController,
)
from galeria.ui.components.timeline.models import TimelineModel, TimelinePoint


class FakePage:
    def __init__(self):
        self.run_task = Mock(return_value="task-id")


def make_model(count=3):
    points = [
        TimelinePoint(0.1, 0.8, id="ingresso", year=1967, label="Ingresso", text="Entrada."),
        TimelinePoint(0.5, 0.2, id="destaque", year=1968, label="Destaque", text="Marco."),
        TimelinePoint(0.9, 0.6, id="saida", year=1969, label="Saída", text="Fim."),
    ][:count]

    return TimelineModel(points=points)


def make_view(page=None):
    return SimpleNamespace(
        refresh=Mock(),
        control=SimpleNamespace(page=page),
    )


def test_controller_initial_state():
    controller = TimelineController(make_model())

    assert controller.progress == 0.0
    assert controller.active_index == 0
    assert controller.view is None


def test_controller_binds_view():
    controller = TimelineController(make_model())
    view = object()

    controller.bind_view(view)

    assert controller.view is view


def test_start_resets_progress_and_marks_running():
    controller = TimelineController(make_model())

    controller.start()

    assert controller.progress == 0.0
    assert controller._running is True
    assert controller._animation_done is False


def test_stop_marks_animation_as_done():
    controller = TimelineController(make_model())

    controller.start()
    controller.stop()

    assert controller._running is False
    assert controller._animation_done is True


def test_reset_restores_initial_state_and_refreshes_view():
    controller = TimelineController(make_model())
    view = SimpleNamespace(refresh=Mock())
    controller.bind_view(view)

    controller.progress = 0.8
    controller.active_index = 2
    controller._running = True
    controller._animation_done = True

    controller.reset()

    assert controller.progress == 0.0
    assert controller.active_index == 0
    assert controller._running is False
    assert controller._animation_done is False
    view.refresh.assert_called_once()


def test_tick_does_nothing_when_not_running():
    controller = TimelineController(make_model())

    controller.tick()

    assert controller.progress == 0.0
    assert controller.active_index == 0


def test_tick_advances_progress_and_refreshes_view():
    controller = TimelineController(make_model())
    view = make_view()

    controller.bind_view(view)
    controller.start()

    controller.tick()

    assert controller.progress == 0.02
    assert controller.active_index == 0
    view.refresh.assert_called_once()


def test_tick_caps_progress_at_one_and_marks_done():
    controller = TimelineController(make_model())
    controller.progress = 0.99
    controller.start()

    controller.progress = 0.99
    controller.tick()

    assert controller.progress == 1.0
    assert controller._animation_done is True


def test_active_index_tracks_progress():
    controller = TimelineController(make_model(count=3))

    controller.progress = 0.0
    controller._update_active_index()
    assert controller.active_index == 0

    controller.progress = 0.5
    controller._update_active_index()
    assert controller.active_index == 1

    controller.progress = 1.0
    controller._update_active_index()
    assert controller.active_index == 2


def test_active_index_is_zero_when_model_has_one_or_no_points():
    controller = TimelineController(make_model(count=1))

    controller.progress = 1.0
    controller._update_active_index()

    assert controller.active_index == 0


@pytest.mark.parametrize(
    ("progress", "expected"),
    [
        (0.0, 0.0),
        (0.25, 0.1464466094),
        (0.5, 0.5),
        (0.75, 0.8535533906),
        (1.0, 1.0),
    ],
)
def test_eased_progress_uses_ease_in_out_formula(progress, expected):
    controller = TimelineController(make_model())

    controller.progress = progress

    assert controller.get_eased_progress() == pytest.approx(expected)


def test_start_schedules_loop_when_view_has_page():
    controller = TimelineController(make_model())
    page = FakePage()
    view = SimpleNamespace(control=SimpleNamespace(page=page))
    controller.bind_view(view)

    controller.start()

    page.run_task.assert_called_once()
    assert controller._task == "task-id"


def test_start_does_not_schedule_loop_without_view():
    controller = TimelineController(make_model())

    controller.start()

    assert controller._task is None


def test_select_point_marks_selected_and_clicked():
    controller = TimelineController(make_model())

    point = controller.select_point("destaque")

    assert point is controller.model.points[1]
    assert controller.selected_point_id == "destaque"
    assert controller.clicked_point_ids == {"destaque"}
    assert controller.active_index == 1


def test_select_point_dispatches_callback():
    callback = Mock()
    controller = TimelineController(make_model(), on_point_selected=callback)

    point = controller.select_point("ingresso")

    callback.assert_called_once_with(point)


def test_select_point_ignores_unknown_id():
    callback = Mock()
    controller = TimelineController(make_model(), on_point_selected=callback)

    assert controller.select_point("desconhecido") is None
    assert controller.selected_point_id is None
    assert controller.clicked_point_ids == set()
    callback.assert_not_called()


def test_point_state_distinguishes_normal_clicked_and_selected():
    controller = TimelineController(make_model())

    controller.select_point("ingresso")
    controller.select_point("destaque")

    assert controller.point_state("saida") == "normal"
    assert controller.point_state("ingresso") == "clicked"
    assert controller.point_state("destaque") == "selected"


def test_point_states_returns_renderer_compatible_state_map():
    controller = TimelineController(make_model())

    controller.select_point("ingresso")
    controller.select_point("destaque")

    assert controller.point_states() == {
        0: "clicked",
        1: "selected",
    }
