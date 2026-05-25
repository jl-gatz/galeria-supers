from types import SimpleNamespace

import flet as ft

from galeria.ui.components.gallery_row import GalleryRow
from galeria.ui.components.media import ThemedMaskedImage
from galeria.ui.components.super_caption import SuperCaption
from galeria.ui.theme.themes import CCUEC_THEME, DETIC_THEME
from tests.stubs.fake_theme import FakeTheme
from tests.stubs.fake_theme_manager import FakeThemeManager


def _row_for(super_data, manager=None):
    manager = manager or FakeThemeManager(FakeTheme())
    supers = super_data if isinstance(super_data, list) else [super_data]
    return GalleryRow(
        supers=supers,
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


def test_gallery_cards_resolve_theme_from_super_era_id():
    row = _row_for(
        [
            SimpleNamespace(
                nome="Ada Lovelace",
                foto="ada.png",
                periodo="1967-1969",
                era_id="ccuec",
                is_placeholder=False,
            ),
            SimpleNamespace(
                nome="Grace Hopper",
                foto="grace.png",
                periodo="2021-2023",
                era_id="detic",
                is_placeholder=False,
            ),
        ]
    )

    ccuec_stack = row.row.controls[0].content
    detic_stack = row.row.controls[1].content

    assert ccuec_stack.controls[0].theme_manager.theme.id == CCUEC_THEME.id
    assert ccuec_stack.controls[1].theme_manager.theme.id == CCUEC_THEME.id
    assert detic_stack.controls[0].theme_manager.theme.id == DETIC_THEME.id
    assert detic_stack.controls[1].theme_manager.theme.id == DETIC_THEME.id


def test_gallery_card_keeps_own_era_theme_when_global_theme_changes():
    manager = FakeThemeManager(FakeTheme())
    row = _row_for(
        SimpleNamespace(
            nome="Ada Lovelace",
            foto="ada.png",
            periodo="1967-1969",
            era_id="ccuec",
            is_placeholder=False,
        ),
        manager=manager,
    )
    stack = row.row.controls[0].content
    image = stack.controls[0]
    caption = stack.controls[1]

    manager.set_theme_for_era("detic")

    assert manager.theme.id == DETIC_THEME.id
    assert image.theme_manager.theme.id == CCUEC_THEME.id
    assert caption.theme_manager.theme.id == CCUEC_THEME.id
    assert image.mask_image.color == CCUEC_THEME.image.caption_mask_tint
