# tests/unit/views/test_gallery_view.py

from unittest.mock import Mock, patch

from galeria.ui.views import GalleryView

# ================================
# ❌ NÃO ABRE QUANDO INVÁLIDO
# ================================


def test_nao_abre_super_quando_pode_abrir_false(fake_page, fake_service, fake_root):
    fake_service.pode_abrir = Mock(return_value=False)

    view = GalleryView(page=fake_page, service=fake_service, root_layout=fake_root)
    super_data = Mock()

    with patch("galeria.ui.views.gallery_view.SuperDetail") as SuperDetailMock:
        view.abrir_super(super_data)

        SuperDetailMock.assert_not_called()

        # Assert baseado no estado do fake_root
        assert fake_root.overlay_shown is None


# ================================
# ✅ ABRE SUPER (FLUXO FELIZ)
# ================================


def test_abre_super_com_sucesso(fake_page, fake_service, fake_root):
    fake_service.pode_abrir = Mock(return_value=True)
    fake_service.build_image_path = Mock(return_value="img.png")
    fake_service.build_timeline_path = Mock(return_value="timeline.json")

    view = GalleryView(page=fake_page, service=fake_service, root_layout=fake_root)
    super_data = Mock()

    detail_mock = Mock()

    with patch("galeria.ui.views.gallery_view.SuperDetail", return_value=detail_mock):
        view.abrir_super(super_data)

        # 👇 valida efeito
        assert fake_root.overlay_shown == detail_mock

        detail_mock.fade_in.assert_called_once()


# ================================
# 🔗 CALLBACK DE FECHAMENTO
# ================================


def test_on_request_close_fecha_overlay(fake_page, fake_service, fake_root):
    fake_service.pode_abrir = Mock(return_value=True)
    fake_service.build_image_path = Mock(return_value="img.png")
    fake_service.build_timeline_path = Mock(return_value="timeline.json")

    view = GalleryView(page=fake_page, service=fake_service, root_layout=fake_root)
    super_data = Mock()

    detail_mock = Mock()

    with patch(
        "galeria.ui.views.gallery_view.SuperDetail", return_value=detail_mock
    ) as SuperDetailMock:
        view.abrir_super(super_data)

        _, kwargs = SuperDetailMock.call_args
        on_request_close = kwargs["on_request_close"]

        on_request_close()

        # 👇 valida efeito
        assert fake_root.overlay_hidden == detail_mock


# ================================
# 🔍 GARANTE USO DO SERVICE
# ================================


def test_usa_service_para_paths(fake_page, fake_service, fake_root):
    fake_service.pode_abrir = Mock(return_value=True)
    fake_service.build_image_path = Mock(return_value="img.png")
    fake_service.build_timeline_path = Mock(return_value="timeline.json")

    view = GalleryView(page=fake_page, service=fake_service, root_layout=fake_root)
    super_data = Mock()

    with patch("galeria.ui.views.gallery_view.SuperDetail"):
        view.abrir_super(super_data)

        fake_service.build_image_path.assert_called_once_with(super_data)
        fake_service.build_timeline_path.assert_called_once_with(super_data)
