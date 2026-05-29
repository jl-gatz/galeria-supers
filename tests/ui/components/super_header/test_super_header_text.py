from typing import cast

import flet as ft

from galeria.ui.components.super_caption import SuperCaption
from galeria.ui.components.super_header import SuperHeader
from tests.stubs.fake_theme_manager import FakeThemeManager
from tests.ui.components.super_header.conftest import SuperHeaderThemeLike


def _text_controls(super_header: SuperHeader) -> list[ft.Text]:
    controls = list(super_header.text_list.controls)
    assert all(isinstance(control, ft.Text) for control in controls)
    return cast(list[ft.Text], controls)


def test_update_text_applies_theme_to_new_paragraphs(
    super_header: SuperHeader, super_header_theme: SuperHeaderThemeLike
) -> None:
    super_header.did_mount()

    super_header.update_text("Novo texto.\n\nOutro bloco.")

    assert len(super_header.text_list.controls) == 2

    for paragraph in _text_controls(super_header):
        assert paragraph.color == super_header_theme.text.secondary
        assert paragraph.size == super_header_theme.typography.super_header_body_size
        assert paragraph.font_family == super_header_theme.typography.super_header_body_font_family
        assert paragraph.style is not None
        assert paragraph.style.height == super_header_theme.typography.super_header_body_line_height


def test_set_timeline_event_renders_year_label_and_text(
    super_header: SuperHeader, super_header_theme: SuperHeaderThemeLike
) -> None:
    super_header.did_mount()

    super_header.set_timeline_event(
        year=1967,
        label="Ingresso",
        text="Alfredo inicia sua trajetória.\n\nOutro marco.",
    )

    controls = _text_controls(super_header)

    assert [control.value for control in controls] == [
        "1967",
        "Ingresso",
        "Alfredo inicia sua trajetória.",
        "Outro marco.",
    ]
    assert controls[0].data == "timeline_year"
    assert controls[0].color == super_header_theme.accent.primary
    assert controls[1].data == "timeline_label"
    assert controls[1].color == super_header_theme.text.primary


def test_super_header_disables_mask_for_placeholder(
    super_header_manager: FakeThemeManager,
) -> None:
    header = SuperHeader(
        theme_manager=super_header_manager,
        image_src=None,
        nome="Ada",
        texto_inicial="Texto",
    )

    assert header.portrait_image.apply_mask is False
    assert header.portrait_image.mask_image.visible is False


def test_super_header_layers_caption_above_masked_image(
    super_header_manager: FakeThemeManager,
) -> None:
    header = SuperHeader(
        theme_manager=super_header_manager,
        image_src="tests/assets/test_image.png",
        nome="Ada",
        periodo="1967-1969",
        texto_inicial="Texto",
    )

    assert header.portrait_stack.controls[0] is header.portrait_image
    assert header.portrait_stack.controls[1] is header.portrait_caption
    assert isinstance(header.portrait_caption, SuperCaption)
    assert header.portrait_caption.name_text.value == "Ada"
    assert header.portrait_caption.subtitle_text is not None
    assert header.portrait_caption.subtitle_text.value == "1967-1969"
    assert header.portrait_caption.compact is False
