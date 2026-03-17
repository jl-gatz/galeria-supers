# tests/ui/conftest.py


import flet as ft
import pytest
import pytest_asyncio

from galeria.ui.views.gallery_view import GalleryView
from tests.factories import SuperDetailFactory, SuperFactory
from tests.fixtures import FakeSuperData
from tests.harness import FletTestHarness


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
def gallery_view(fake_page: ft.Page):

    supers = SuperFactory.batch(12)

    return GalleryView(supers=supers, root_layout=None, page=fake_page)


@pytest_asyncio.fixture
async def mounted_gallery(harness: FletTestHarness, gallery_view: GalleryView) -> FletTestHarness:
    await harness.mount(gallery_view)
    return harness
