# tests/ui/conftest.py


from collections.abc import Callable, Sequence
from typing import Protocol, cast

import flet as ft
import pytest
import pytest_asyncio

from galeria.domain import SuperService
from galeria.domain.protocols.theme_manager_like import ThemeManagerLike
from galeria.ui.controllers.super_detail_controller import SuperDetailController
from galeria.ui.theme.models import Theme
from galeria.ui.views.gallery_view import GalleryView
from galeria.ui.views.super_view import SuperDetail
from tests.factories import SuperDetailFactory
from tests.fixtures.super_data import TimelinePointInput
from tests.harness import FletTestHarness
from tests.stubs.fake_page import FakePage
from tests.stubs.fake_super_data import FakeSuperData
from tests.stubs.fake_theme_manager import FakeThemeManager


class SuperDetailBuilder(Protocol):
    def __call__(
        self,
        *,
        id: str = "test-hero-1",
        nome: str = "Test Hero",
        image_path: str = "tests/assets/test_image.png",
        timeline_path: str = "tests/assets/test_timeline.png",
        timeline_points: Sequence[TimelinePointInput] | None = None,
        historias: Sequence[str] | None = None,
        periodo: str | None = None,
        controller: SuperDetailController | None = None,
        theme_manager: ThemeManagerLike | None = None,
        theme: Theme | None = None,
        on_request_close: Callable[[], None] | None = None,
        auto_start: bool = True,
    ) -> SuperDetail: ...


@pytest.fixture
def super_data() -> FakeSuperData:
    return FakeSuperData()


# @pytest.fixture
# def super_detail_controller(fake_super):
#     return SuperDetailController(fake_super)


@pytest.fixture
def close_callback() -> Callable[[], None]:

    def _callback() -> None:
        pass

    return _callback


@pytest.fixture
def image_path() -> str:
    return "tests/assets/test_image.png"


@pytest.fixture
def timeline_path() -> str:
    return "tests/assets/test_timeline.png"


@pytest.fixture
def super_detail() -> SuperDetail:
    return SuperDetailFactory.build(auto_start=False)


@pytest.fixture
def super_detail_with_data() -> SuperDetailBuilder:
    return SuperDetailFactory.build


@pytest.fixture
def gallery_view(
    fake_page: FakePage, service: SuperService, fake_theme_manager: FakeThemeManager
) -> GalleryView:

    # supers = SuperFactory.batch(12)

    return GalleryView(
        service=service,
        root_layout=None,
        page=cast(ft.Page, fake_page),
        theme=fake_theme_manager,
    )


@pytest.fixture
def mounted() -> Callable[[ft.Control], ft.Control]:
    def _mounted(control: ft.Control) -> ft.Control:
        object.__setattr__(control, "_mounted", True)
        return control

    return _mounted


@pytest_asyncio.fixture
async def mounted_gallery(harness: FletTestHarness, gallery_view: GalleryView) -> FletTestHarness:
    await harness.mount(gallery_view)
    return harness
