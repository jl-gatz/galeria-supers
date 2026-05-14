# tests/ui/conftest.py


import flet as ft
import pytest
import pytest_asyncio

from galeria.domain import SuperService
from galeria.ui.views.gallery_view import GalleryView
from tests.factories import SuperDetailFactory
from tests.harness import FletTestHarness
from tests.stubs.fake_super_data import FakeSuperData
from tests.stubs.fake_theme_manager import FakeThemeManager


@pytest.fixture
def super_data():
    return FakeSuperData()


# @pytest.fixture
# def super_detail_controller(fake_super):
#     return SuperDetailController(fake_super)


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
    return SuperDetailFactory.build(auto_start=False)


@pytest.fixture
def super_detail_with_data():
    return lambda **kwargs: SuperDetailFactory.build(**kwargs)


@pytest.fixture
def gallery_view(
    fake_page: ft.Page, service: SuperService, fake_theme_manager: FakeThemeManager
) -> GalleryView:

    # supers = SuperFactory.batch(12)

    return GalleryView(service=service, root_layout=None, page=fake_page, theme=fake_theme_manager)


@pytest.fixture
def mounted():
    def _mounted(control):
        control._mounted = True
        return control

    return _mounted


@pytest_asyncio.fixture
async def mounted_gallery(harness: FletTestHarness, gallery_view: GalleryView) -> FletTestHarness:
    await harness.mount(gallery_view)
    return harness
