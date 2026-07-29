# tests/unit/views/test_gallery_view.py

from typing import Protocol, cast
from unittest.mock import Mock, patch

import flet as ft

from galeria.domain import Super
from galeria.domain.protocols.gallery_service_like import GalleryServiceLike
from galeria.ui.components.gallery_row import GalleryRow
from galeria.ui.components.media import ThemedMaskedImage
from galeria.ui.components.super_caption import SuperCaption
from galeria.ui.layout import RootLayout
from galeria.ui.theme.themes import CCUEC_THEME, DETIC_THEME
from galeria.ui.views import GalleryView
from tests.stubs.fake_page import FakePage
from tests.stubs.fake_root import FakeRoot
from tests.stubs.fake_super_service import FakeSuperService
from tests.stubs.fake_theme_manager import FakeThemeManager
from tests.utils.types import HasContent, HasControls


class OverlayRoot(Protocol):
    overlay_shown: object | None
    overlay_hidden: object | None


def _gallery_view(
    fake_page: FakePage,
    service: GalleryServiceLike,
    fake_root: FakeRoot,
    fake_theme_manager: FakeThemeManager,
) -> GalleryView:
    return GalleryView(
        page=cast(ft.Page, fake_page),
        service=service,
        root_layout=cast(RootLayout, fake_root),
        theme=fake_theme_manager,
    )


def _overlay_shown(fake_root: FakeRoot) -> object | None:
    return cast(OverlayRoot, fake_root).overlay_shown


def _overlay_hidden(fake_root: FakeRoot) -> object | None:
    return cast(OverlayRoot, fake_root).overlay_hidden

# ================================
# ❌ NÃO ABRE QUANDO INVÁLIDO
# ================================


def test_nao_abre_super_quando_pode_abrir_false(
    fake_page: FakePage,
    fake_service: GalleryServiceLike,
    fake_root: FakeRoot,
    fake_theme_manager: FakeThemeManager,
):
    fake_service.pode_abrir = Mock(return_value=False)

    view = _gallery_view(fake_page, fake_service, fake_root, fake_theme_manager)
    super_data = Mock()

    with patch("galeria.ui.views.gallery_view.SuperDetail") as SuperDetailMock:
        view._abrir_super(super_data)

        SuperDetailMock.assert_not_called()

        # Assert baseado no estado do fake_root
        assert _overlay_shown(fake_root) is None


# ================================
# ✅ ABRE SUPER (FLUXO FELIZ)
# ================================


def test_abre_super_com_sucesso(
    fake_page: FakePage,
    fake_service: GalleryServiceLike,
    fake_root: FakeRoot,
    fake_theme_manager: FakeThemeManager,
):
    fake_service.pode_abrir = Mock(return_value=True)
    fake_service.build_image_path = Mock(return_value="img.png")
    fake_service.build_timeline_path = Mock(return_value="timeline.json")

    view = _gallery_view(fake_page, fake_service, fake_root, fake_theme_manager)
    super_data = Mock()

    detail_mock = Mock()

    with patch("galeria.ui.views.gallery_view.SuperDetail", return_value=detail_mock):
        view._abrir_super(super_data)

        # 👇 valida efeito real
        assert _overlay_shown(fake_root) == detail_mock


# ================================
# 🔗 CALLBACK DE FECHAMENTO
# ================================


def test_on_request_close_fecha_overlay(
    fake_page: FakePage,
    fake_service: GalleryServiceLike,
    fake_root: FakeRoot,
    fake_theme_manager: FakeThemeManager,
):
    fake_service.pode_abrir = Mock(return_value=True)
    fake_service.build_image_path = Mock(return_value="img.png")
    fake_service.build_timeline_path = Mock(return_value="timeline.json")

    view = _gallery_view(fake_page, fake_service, fake_root, fake_theme_manager)
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
        assert _overlay_hidden(fake_root) == detail_mock


# ================================
# 🔍 GARANTE USO DO SERVICE
# ================================
def test_abre_super_quando_permitido(
    fake_page: FakePage,
    fake_service: GalleryServiceLike,
    fake_root: FakeRoot,
    fake_theme_manager: FakeThemeManager,
) -> None:
    fake_service.pode_abrir = Mock(return_value=True)

    view = _gallery_view(fake_page, fake_service, fake_root, fake_theme_manager)

    super_data: Super = Mock()

    with patch("galeria.ui.views.gallery_view.SuperDetail") as mock_detail:
        view._abrir_super(super_data)

        fake_service.pode_abrir.assert_called_once_with(super_data)
        mock_detail.assert_called_once()

        detail_instance = mock_detail.return_value
        assert _overlay_shown(fake_root) == detail_instance


def test_gallery_view_mantem_linha_unica_sem_secoes_de_era(
    fake_page: FakePage,
    fake_root: FakeRoot,
    fake_theme_manager: FakeThemeManager,
):
    supers = [
        Super("1", "Ada", None, None, [], ["A"], "1967-1969", "ccuec"),
        Super("2", "Grace", None, None, [], ["A"], "2021-2023", "detic"),
    ]
    service = FakeSuperService(supers=supers)

    view = _gallery_view(fake_page, service, fake_root, fake_theme_manager)

    assert isinstance(view.gallery_row, GalleryRow)
    assert len(view.gallery_row.row.controls) == 2
    assert [super_data.era_id for super_data in view.supers] == ["ccuec", "detic"]


def test_gallery_view_solicita_tema_da_era_do_super_ativo(
    fake_page: FakePage,
    fake_root: FakeRoot,
    fake_theme_manager: FakeThemeManager,
):
    supers = [
        Super("1", "Ada", None, None, [], ["A"], "1967-1969", "ccuec"),
        Super("2", "Grace", None, None, [], ["A"], "2021-2023", "detic"),
    ]
    service = FakeSuperService(supers=supers)

    view = _gallery_view(fake_page, service, fake_root, fake_theme_manager)

    view._set_active_super_index(1)
    view._set_active_super_index(0)

    assert fake_theme_manager.era_requests[-2:] == ["detic", "ccuec"]


def test_gallery_view_nao_recria_linha_ao_trocar_tema_por_era(
    fake_page: FakePage,
    fake_root: FakeRoot,
    fake_theme_manager: FakeThemeManager,
):
    supers = [
        Super("1", "Ada", None, None, [], ["A"], "1967-1969", "ccuec"),
        Super("2", "Grace", None, None, [], ["A"], "2021-2023", "detic"),
    ]
    service = FakeSuperService(supers=supers)
    view = _gallery_view(fake_page, service, fake_root, fake_theme_manager)
    original_row = view.gallery_row
    original_scroll_controller = view.scroll_controller

    view._set_active_super_index(1)

    assert view.gallery_row is original_row
    assert view.scroll_controller is original_scroll_controller


def test_abre_detalhe_com_tema_da_era_do_super(
    fake_page: FakePage,
    fake_root: FakeRoot,
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

    view = _gallery_view(fake_page, service, fake_root, fake_theme_manager)

    with patch("galeria.ui.views.gallery_view.SuperDetail") as mock_detail:
        view._abrir_super(super_data)

        mock_detail.assert_called_once()
        assert fake_theme_manager.era_requests[-1] == "detic"
        assert fake_theme_manager.theme.id == "detic_era"


def test_gallery_background_theme_changes_without_retheming_visible_cards(
    fake_page: FakePage,
    fake_root: FakeRoot,
    fake_theme_manager: FakeThemeManager,
):
    supers = [
        Super("1", "Ada", "ada.png", None, [], ["A"], "1967-1969", "ccuec"),
        Super("2", "Grace", "grace.png", None, [], ["A"], "2021-2023", "detic"),
    ]
    service = FakeSuperService(supers=supers)
    view = _gallery_view(fake_page, service, fake_root, fake_theme_manager)
    assert isinstance(view.gallery_row, GalleryRow)
    ccuec_card = view.gallery_row.row.controls[0]
    assert isinstance(ccuec_card, HasContent)
    ccuec_stack = ccuec_card.content
    assert isinstance(ccuec_stack, HasControls)
    ccuec_image = ccuec_stack.controls[0]
    ccuec_caption = ccuec_stack.controls[1]
    assert isinstance(ccuec_image, ThemedMaskedImage)
    assert isinstance(ccuec_caption, SuperCaption)

    view._set_active_super_index(1)
    view._apply_theme(fake_theme_manager.theme)

    assert view.bgcolor == DETIC_THEME.base.background
    assert ccuec_image.theme_manager.theme.id == CCUEC_THEME.id
    assert ccuec_caption.theme_manager.theme.id == CCUEC_THEME.id


def test_gallery_global_theme_uses_card_closest_to_viewport_center_on_mount(
    fake_page: FakePage,
    fake_root: FakeRoot,
    fake_theme_manager: FakeThemeManager,
):
    supers = [
        Super("1", "Ada", None, None, [], ["A"], "1967-1969", "ccuec"),
        Super("2", "Alan", None, None, [], ["A"], "1969-1972", "ccuec"),
        Super("3", "Grace", None, None, [], ["A"], "2021-2023", "detic"),
    ]
    service = FakeSuperService(supers=supers)
    view = _gallery_view(fake_page, service, fake_root, fake_theme_manager)
    view.update = lambda: None

    view.did_mount()

    assert fake_theme_manager.era_requests[-1] == "detic"
