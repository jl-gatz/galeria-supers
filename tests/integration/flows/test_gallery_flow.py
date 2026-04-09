from unittest.mock import Mock, patch

from galeria.ui.views import GalleryView


def test_sequencia_abrir_fechar_abrir_outro(fake_page, fake_service, fake_root):
    fake_service.pode_abrir = Mock(return_value=True)
    fake_service.build_image_path = Mock(return_value="img.png")
    fake_service.build_timeline_path = Mock(return_value="timeline.json")

    view = GalleryView(page=fake_page, service=fake_service, root_layout=fake_root)

    super_1 = Mock(name="super_1")
    super_2 = Mock(name="super_2")

    detail_1 = Mock(name="detail_1")
    detail_2 = Mock(name="detail_2")

    with patch(
        "galeria.ui.views.gallery_view.SuperDetail", side_effect=[detail_1, detail_2]
    ) as SuperDetailMock:
        # === 1. abre o primeiro ===
        view.abrir_super(super_1)

        assert fake_root.overlay_shown == detail_1

        # captura callback do primeiro
        _, kwargs_1 = SuperDetailMock.call_args_list[0]
        close_1 = kwargs_1["on_request_close"]

        # === 2. fecha o primeiro ===
        close_1()

        assert fake_root.overlay_hidden == detail_1

        # === 3. abre o segundo ===
        view.abrir_super(super_2)

        assert fake_root.overlay_shown == detail_2


def test_fechar_antigo_nao_afeta_novo(fake_page, fake_service, fake_root):
    fake_service.pode_abrir = Mock(return_value=True)
    fake_service.build_image_path = Mock(return_value="img.png")
    fake_service.build_timeline_path = Mock(return_value="timeline.json")

    view = GalleryView(page=fake_page, service=fake_service, root_layout=fake_root)

    super_1 = Mock()
    super_2 = Mock()

    detail_1 = Mock(name="detail_1")
    detail_2 = Mock(name="detail_2")

    with patch(
        "galeria.ui.views.gallery_view.SuperDetail", side_effect=[detail_1, detail_2]
    ) as SuperDetailMock:
        view.abrir_super(super_1)
        _, kwargs_1 = SuperDetailMock.call_args_list[0]
        close_1 = kwargs_1["on_request_close"]

        view.abrir_super(super_2)

        # 👇 agora fecha o antigo (fora de ordem)
        close_1()

        # ainda deve ter fechado o detail_1 corretamente
        assert fake_root.overlay_hidden == detail_1

        # e o atual continua sendo o segundo
        assert fake_root.overlay_shown == detail_2
