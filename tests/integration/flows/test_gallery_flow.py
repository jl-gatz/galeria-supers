from typing import Protocol, cast
from unittest.mock import Mock, patch

import flet as ft

from galeria.domain.protocols import SuperServiceLike
from galeria.ui.layout import RootLayout
from galeria.ui.views import GalleryView
from tests.stubs.fake_page import FakePage
from tests.stubs.fake_root import FakeRoot
from tests.stubs.fake_theme_manager import FakeThemeManager


class OverlayRoot(Protocol):
    overlay_shown: object | None
    overlay_hidden: object | None


def _gallery_view(
    fake_page: FakePage,
    fake_service: SuperServiceLike,
    fake_root: FakeRoot,
    fake_theme_manager: FakeThemeManager,
) -> GalleryView:
    return GalleryView(
        page=cast(ft.Page, fake_page),
        service=fake_service,
        root_layout=cast(RootLayout, fake_root),
        theme=fake_theme_manager,
    )


def _overlay_shown(fake_root: FakeRoot) -> object | None:
    return cast(OverlayRoot, fake_root).overlay_shown


def _overlay_hidden(fake_root: FakeRoot) -> object | None:
    return cast(OverlayRoot, fake_root).overlay_hidden


def test_sequencia_abrir_fechar_abrir_outro(
    fake_page: FakePage,
    fake_service: SuperServiceLike,
    fake_root: FakeRoot,
    fake_theme_manager: FakeThemeManager,
):
    fake_service.pode_abrir = Mock(return_value=True)
    fake_service.build_image_path = Mock(return_value="img.png")
    fake_service.build_timeline_path = Mock(return_value="timeline.json")

    view = _gallery_view(fake_page, fake_service, fake_root, fake_theme_manager)

    super_1 = Mock(name="super_1")
    super_2 = Mock(name="super_2")

    detail_1 = Mock(name="detail_1")
    detail_2 = Mock(name="detail_2")

    with patch(
        "galeria.ui.views.gallery_view.SuperDetail", side_effect=[detail_1, detail_2]
    ) as SuperDetailMock:
        # === 1. abre o primeiro ===
        view._abrir_super(super_1)

        assert _overlay_shown(fake_root) == detail_1

        # captura callback do primeiro
        _, kwargs_1 = SuperDetailMock.call_args_list[0]
        close_1 = kwargs_1["on_request_close"]

        # === 2. fecha o primeiro ===
        close_1()

        assert _overlay_hidden(fake_root) == detail_1

        # === 3. abre o segundo ===
        view._abrir_super(super_2)

        assert _overlay_shown(fake_root) == detail_2


def test_fechar_antigo_nao_afeta_novo(
    fake_page: FakePage,
    fake_service: SuperServiceLike,
    fake_root: FakeRoot,
    fake_theme_manager: FakeThemeManager,
):
    fake_service.pode_abrir = Mock(return_value=True)
    fake_service.build_image_path = Mock(return_value="img.png")
    fake_service.build_timeline_path = Mock(return_value="timeline.json")

    view = _gallery_view(fake_page, fake_service, fake_root, fake_theme_manager)

    super_1 = Mock()
    super_2 = Mock()

    detail_1 = Mock(name="detail_1")
    detail_2 = Mock(name="detail_2")

    with patch(
        "galeria.ui.views.gallery_view.SuperDetail", side_effect=[detail_1, detail_2]
    ) as SuperDetailMock:
        view._abrir_super(super_1)
        _, kwargs_1 = SuperDetailMock.call_args_list[0]
        close_1 = kwargs_1["on_request_close"]

        view._abrir_super(super_2)

        # 👇 agora fecha o antigo (fora de ordem)
        close_1()

        # ainda deve ter fechado o detail_1 corretamente
        assert _overlay_hidden(fake_root) == detail_1

        # e o atual continua sendo o segundo
        assert _overlay_shown(fake_root) == detail_2
