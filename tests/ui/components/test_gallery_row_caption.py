from types import SimpleNamespace

import flet as ft

from galeria.ui.components.gallery_row import GalleryRow
from galeria.ui.components.media import ThemedMaskedImage
from galeria.ui.components.super_caption import SuperCaption
from tests.stubs.fake_theme import FakeTheme
from tests.stubs.fake_theme_manager import FakeThemeManager


def _row_for(super_data):
    manager = FakeThemeManager(FakeTheme())
    return GalleryRow(
        supers=[super_data],
        card_width=manager.gallery.card_width,
        spacing=manager.gallery.h_spacing,
        padding=manager.gallery.v_spacing,
        on_card_click=lambda _: None,
        theme=manager,
    )


def test_gallery_card_stacks_masked_image_before_caption():
    super_data = SimpleNamespace(
        nome="Ada Lovelace",
        foto="ada.png",
        is_placeholder=False,
    )

    row = _row_for(super_data)
    card = row.row.controls[0]
    stack = card.content

    assert isinstance(stack, ft.Stack)
    assert isinstance(stack.controls[0], ThemedMaskedImage)
    assert isinstance(stack.controls[1], SuperCaption)
    assert stack.controls[1].name_text.value == "Ada Lovelace"
    assert stack.controls[1].name_text.max_lines == 1
    assert stack.controls[1].single_line_name is True
    assert stack.controls[0].apply_mask is True


def test_gallery_caption_is_separate_from_image():
    super_data = SimpleNamespace(
        nome="Ada Lovelace",
        foto="ada.png",
        is_placeholder=False,
    )

    row = _row_for(super_data)
    image = row.row.controls[0].content.controls[0]
    caption = row.row.controls[0].content.controls[1]

    assert caption not in image.controls
    assert caption.name_text.value == super_data.nome


def test_gallery_card_without_photo_keeps_caption_but_disables_mask():
    super_data = SimpleNamespace(
        nome="Ada Lovelace",
        foto=None,
        is_placeholder=False,
    )

    row = _row_for(super_data)
    stack = row.row.controls[0].content
    image = stack.controls[0]
    caption = stack.controls[1]

    assert image.apply_mask is False
    assert image.base_image.visible is False
    assert image.mask_image.visible is False
    assert caption.name_text.value == "Ada Lovelace"


def test_gallery_placeholder_does_not_receive_mask_or_caption():
    super_data = SimpleNamespace(
        nome="_blank",
        foto=None,
        is_placeholder=True,
    )

    row = _row_for(super_data)
    stack = row.row.controls[0].content
    image = stack.controls[0]

    assert image.apply_mask is False
    assert image.base_image.visible is False
    assert image.mask_image.visible is False
    assert len(stack.controls) == 1


def test_gallery_caption_uses_periodo_field():
    super_data = SimpleNamespace(
        nome="Ada Lovelace",
        foto="ada.png",
        periodo="1967-1969",
        is_placeholder=False,
    )

    row = _row_for(super_data)
    caption = row.row.controls[0].content.controls[1]

    assert caption.subtitle_text is not None
    assert caption.subtitle_text.value == "1967-1969"
