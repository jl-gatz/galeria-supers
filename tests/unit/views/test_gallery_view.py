# tests/unit/views/test_gallery_view.py

from unittest.mock import Mock, patch

import flet as ft

from galeria.domain import Super
from galeria.domain.protocols.gallery_service_like import GalleryServiceLike
from galeria.ui.layout import RootLayout
from galeria.ui.views import GalleryView
from tests.stubs.fake_page import FakePage
from tests.stubs.fake_theme_manager import FakeThemeManager

# ================================
# ❌ NÃO ABRE QUANDO INVÁLIDO
# ================================


def test_nao_abre_super_quando_pode_abrir_false(
    fake_page: FakePage,
    fake_service: GalleryServiceLike,
    fake_root: RootLayout,
    fake_theme_manager: FakeThemeManager,
):
    fake_service.pode_abrir = Mock(return_value=False)

    view = GalleryView(
        page=fake_page, service=fake_service, root_layout=fake_root, theme=fake_theme_manager
    )
    super_data = Mock()

    with patch("galeria.ui.views.gallery_view.SuperDetail") as SuperDetailMock:
        view._abrir_super(super_data)

        SuperDetailMock.assert_not_called()

        # Assert baseado no estado do fake_root
        assert fake_root.overlay_shown is None


# ================================
# ✅ ABRE SUPER (FLUXO FELIZ)
# ================================


def test_abre_super_com_sucesso(
    fake_page: FakePage,
    fake_service: GalleryServiceLike,
    fake_root: RootLayout,
    fake_theme_manager: FakeThemeManager,
):
    fake_service.pode_abrir = Mock(return_value=True)
    fake_service.build_image_path = Mock(return_value="img.png")
    fake_service.build_timeline_path = Mock(return_value="timeline.json")

    view = GalleryView(
        page=fake_page, service=fake_service, root_layout=fake_root, theme=fake_theme_manager
    )
    super_data = Mock()

    detail_mock = Mock()

    with patch("galeria.ui.views.gallery_view.SuperDetail", return_value=detail_mock):
        view._abrir_super(super_data)

        # 👇 valida efeito real
        assert fake_root.overlay_shown == detail_mock


# ================================
# 🔗 CALLBACK DE FECHAMENTO
# ================================


def test_on_request_close_fecha_overlay(
    fake_page: FakePage,
    fake_service: GalleryServiceLike,
    fake_root: RootLayout,
    fake_theme_manager: FakeThemeManager,
):
    fake_service.pode_abrir = Mock(return_value=True)
    fake_service.build_image_path = Mock(return_value="img.png")
    fake_service.build_timeline_path = Mock(return_value="timeline.json")

    view = GalleryView(
        page=fake_page, service=fake_service, root_layout=fake_root, theme=fake_theme_manager
    )
    super_data = Mock()

    detail_mock = Mock()

    with patch(
        "galeria.ui.views.gallery_view.SuperDetail", return_value=detail_mock
    ) as SuperDetailMock:
        view._abrir_super(super_data)

        _, kwargs = SuperDetailMock.call_args
        on_request_close = kwargs["on_request_close"]

        on_request_close()

        # 👇 valida efeito
        assert fake_root.overlay_hidden == detail_mock


# ================================
# 🔍 GARANTE USO DO SERVICE
# ================================
def test_abre_super_quando_permitido(
    fake_page: ft.Page,
    fake_service: GalleryServiceLike,
    fake_root: RootLayout,
    fake_theme_manager: FakeThemeManager,
) -> None:
    fake_service.pode_abrir = Mock(return_value=True)

    view = GalleryView(
        page=fake_page,
        service=fake_service,
        root_layout=fake_root,
        theme=fake_theme_manager,
    )

    super_data: Super = Mock()

    with patch("galeria.ui.views.gallery_view.SuperDetail") as mock_detail:
        view._abrir_super(super_data)

        fake_service.pode_abrir.assert_called_once_with(super_data)
        mock_detail.assert_called_once()

        detail_instance = mock_detail.return_value
        assert fake_root.overlay_shown == detail_instance
