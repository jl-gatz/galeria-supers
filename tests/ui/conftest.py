# tests/ui/conftest.py


import pytest

from galeria.ui.views.gallery_view import GalleryView
from tests.factories.super_detail_factory import SuperDetailFactory
from tests.factories.super_factory import SuperFactory
from tests.fixtures.super_data import FakeSuperData


@pytest.fixture
def super_data():

    return FakeSuperData(
        id=1,
        nome="Test Hero",
        foto="tests/assets/test_image.png",
        timeline="tests/assets/test_timeline.png",
        timeline_points=None,
        historias=["None", "Nenhum"],
    )


@pytest.fixture
def close_callback():

    def _callback():
        pass

    return _callback


@pytest.fixture
def image_path():
    return "tests/assets/test_image.png"


@pytest.fixture
def timeline_path():
    return "tests/assets/test_timeline.png"


@pytest.fixture
def super_detail():
    return SuperDetailFactory.build()


@pytest.fixture
def gallery_view():

    supers = SuperFactory.batch(12)

    return GalleryView(supers=supers, on_select=lambda s: None)
