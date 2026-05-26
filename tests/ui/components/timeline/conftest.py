# tests/ui/components/timeline/conftest.py

import pytest

from galeria.ui.components.timeline.models import TimelineModel, TimelinePoint
from galeria.ui.components.timeline.utils import PathBuilder
from galeria.ui.components.timeline.view import TimelineRenderer, TimelineStyle


@pytest.fixture
def timeline_points():
    return [
        TimelinePoint(
            0.10,
            0.80,
            id="ingresso-1967",
            year=1967,
            label="ingresso",
            text="Entrada na superintendência.",
        ),
        TimelinePoint(
            0.50,
            0.20,
            id="destaque-1968",
            year=1968,
            label="destaque",
            text="Marco de destaque.",
        ),
        TimelinePoint(
            0.90,
            0.60,
            id="saida-1969",
            year=1969,
            label="saída",
            text="Encerramento do ciclo.",
        ),
    ]


@pytest.fixture
def timeline_model(timeline_points: list[TimelinePoint]):
    return TimelineModel(points=timeline_points)


@pytest.fixture
def path_builder():
    return PathBuilder(mode="linear")


@pytest.fixture
def smooth_path_builder():
    return PathBuilder(mode="smooth")


@pytest.fixture
def infinity_path_builder():
    return PathBuilder(mode="infinity")


@pytest.fixture
def timeline_style():
    return TimelineStyle()


@pytest.fixture
def timeline_renderer(timeline_style: TimelineStyle):
    return TimelineRenderer(timeline_style)
