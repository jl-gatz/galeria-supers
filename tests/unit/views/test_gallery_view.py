# tests/unit/views/test_gallery_view.py

from unittest.mock import Mock, patch

import flet as ft

from galeria.domain import Super
from galeria.domain.protocols.gallery_service_like import GalleryServiceLike
from galeria.ui.components.gallery_row import GalleryRow
from galeria.ui.layout import RootLayout
from galeria.ui.views import GalleryView
from tests.stubs.fake_page import FakePage
from tests.stubs.fake_super_service import FakeSuperService
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


def test_gallery_view_mantem_linha_unica_sem_secoes_de_era(
    fake_page: FakePage,
    fake_root: RootLayout,
    fake_theme_manager: FakeThemeManager,
):
    supers = [
        Super("1", "Ada", None, None, [], ["A"], "1967-1969", "ccuec"),
        Super("2", "Grace", None, None, [], ["A"], "2021-2023", "detic"),
    ]
    service = FakeSuperService(supers=supers)

    view = GalleryView(
        page=fake_page,
        service=service,
        root_layout=fake_root,
        theme=fake_theme_manager,
    )

    assert isinstance(view.gallery_row, GalleryRow)
    assert len(view.gallery_row.row.controls) == 2
    assert [super_data.era_id for super_data in view.supers] == ["ccuec", "detic"]


def test_gallery_view_solicita_tema_da_era_do_super_ativo(
    fake_page: FakePage,
    fake_root: RootLayout,
    fake_theme_manager: FakeThemeManager,
):
    supers = [
        Super("1", "Ada", None, None, [], ["A"], "1967-1969", "ccuec"),
        Super("2", "Grace", None, None, [], ["A"], "2021-2023", "detic"),
    ]
    service = FakeSuperService(supers=supers)

    view = GalleryView(
        page=fake_page,
        service=service,
        root_layout=fake_root,
        theme=fake_theme_manager,
    )

    view._set_active_super_index(1)
    view._set_active_super_index(0)

    assert fake_theme_manager.era_requests[-2:] == ["detic", "ccuec"]


def test_gallery_view_nao_recria_linha_ao_trocar_tema_por_era(
    fake_page: FakePage,
    fake_root: RootLayout,
    fake_theme_manager: FakeThemeManager,
):
    supers = [
        Super("1", "Ada", None, None, [], ["A"], "1967-1969", "ccuec"),
        Super("2", "Grace", None, None, [], ["A"], "2021-2023", "detic"),
    ]
    service = FakeSuperService(supers=supers)
    view = GalleryView(
        page=fake_page,
        service=service,
        root_layout=fake_root,
        theme=fake_theme_manager,
    )
    original_row = view.gallery_row
    original_scroll_controller = view.scroll_controller

    view._set_active_super_index(1)

    assert view.gallery_row is original_row
    assert view.scroll_controller is original_scroll_controller


def test_abre_detalhe_com_tema_da_era_do_super(
    fake_page: FakePage,
    fake_root: RootLayout,
    fake_theme_manager: FakeThemeManager,
):
    super_data = Super(
        id="2",
        nome="Grace",
        foto=None,
        timeline=None,
        timeline_points=[],
        historias=["A"],
        periodo="2021-2023",
        era_id="detic",
    )
    service = FakeSuperService(supers=[super_data])

    view = GalleryView(
        page=fake_page,
        service=service,
        root_layout=fake_root,
        theme=fake_theme_manager,
    )

    with patch("galeria.ui.views.gallery_view.SuperDetail") as mock_detail:
        view._abrir_super(super_data)

        mock_detail.assert_called_once()
        assert fake_theme_manager.era_requests[-1] == "detic"
        assert fake_theme_manager.theme.id == "detic_era"
