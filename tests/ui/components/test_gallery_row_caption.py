from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import flet as ft

from galeria.domain.models import TimelinePoint
from galeria.domain.protocols.super_like import SuperLike
from galeria.ui.components.gallery_row import GalleryRow
from galeria.ui.components.media import ThemedMaskedImage
from galeria.ui.components.super_caption import SuperCaption
from galeria.ui.theme.themes import CCUEC_THEME, DETIC_THEME
from tests.stubs.fake_theme import FakeTheme
from tests.stubs.fake_theme_manager import FakeThemeManager
from tests.utils.types import HasContent


@dataclass
class GallerySuper:
    nome: str
    foto: Path | str | None
    id: str = "super"
    timeline: Path | str | None = None
    periodo: str | None = None
    historias: Sequence[str] | None = None
    timeline_points: Sequence[TimelinePoint] | None = None
    era_id: str | None = None
    is_placeholder: bool = False


def _row_for(
    super_data: SuperLike | list[SuperLike],
    manager: FakeThemeManager | None = None,
) -> GalleryRow:
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


def _card_stack(row: GalleryRow, index: int = 0) -> ft.Stack:
    card = row.row.controls[index]
    assert isinstance(card, HasContent)
    assert isinstance(card.content, ft.Stack)
    return card.content


def test_gallery_card_stacks_masked_image_before_caption():
    super_data = GallerySuper(
        nome="Ada Lovelace",
        foto="ada.png",
        is_placeholder=False,
    )

    row = _row_for(super_data)
    stack = _card_stack(row)
    assert isinstance(stack.controls[0], ThemedMaskedImage)
    assert isinstance(stack.controls[1], SuperCaption)
    image = stack.controls[0]
    caption = stack.controls[1]
    assert caption.name_text.value == "Ada Lovelace"
    assert caption.name_text.max_lines == 1
    assert caption.single_line_name is True
    assert image.apply_mask is True


def test_gallery_caption_is_separate_from_image():
    super_data = GallerySuper(
        nome="Ada Lovelace",
        foto="ada.png",
        is_placeholder=False,
    )

    row = _row_for(super_data)
    stack = _card_stack(row)
    image = stack.controls[0]
    caption = stack.controls[1]
    assert isinstance(image, ThemedMaskedImage)
    assert isinstance(caption, SuperCaption)

    assert caption not in image.controls
    assert caption.name_text.value == super_data.nome


def test_gallery_card_without_photo_keeps_caption_but_disables_mask():
    super_data = GallerySuper(
        nome="Ada Lovelace",
        foto=None,
        is_placeholder=False,
    )

    row = _row_for(super_data)
    stack = _card_stack(row)
    image = stack.controls[0]
    caption = stack.controls[1]
    assert isinstance(image, ThemedMaskedImage)
    assert isinstance(caption, SuperCaption)

    assert image.apply_mask is False
    assert image.base_image.visible is False
    assert image.mask_image.visible is False
    assert caption.name_text.value == "Ada Lovelace"


def test_gallery_placeholder_does_not_receive_mask_or_caption():
    super_data = GallerySuper(
        nome="_blank",
        foto=None,
        is_placeholder=True,
    )

    row = _row_for(super_data)
    stack = _card_stack(row)
    image = stack.controls[0]
    assert isinstance(image, ThemedMaskedImage)

    assert image.apply_mask is False
    assert image.base_image.visible is False
    assert image.mask_image.visible is False
    assert len(stack.controls) == 1


def test_gallery_caption_uses_periodo_field():
    super_data = GallerySuper(
        nome="Ada Lovelace",
        foto="ada.png",
        periodo="1967-1969",
        is_placeholder=False,
    )

    row = _row_for(super_data)
    stack = _card_stack(row)
    caption = stack.controls[1]
    assert isinstance(caption, SuperCaption)

    assert caption.subtitle_text is not None
    assert caption.subtitle_text.value == "1967-1969"


def test_gallery_cards_resolve_theme_from_super_era_id():
    row = _row_for(
        [
            GallerySuper(
                nome="Ada Lovelace",
                foto="ada.png",
                periodo="1967-1969",
                era_id="ccuec",
                is_placeholder=False,
            ),
            GallerySuper(
                nome="Grace Hopper",
                foto="grace.png",
                periodo="2021-2023",
                era_id="detic",
                is_placeholder=False,
            ),
        ]
    )

    ccuec_stack = _card_stack(row, 0)
    detic_stack = _card_stack(row, 1)
    ccuec_image = ccuec_stack.controls[0]
    ccuec_caption = ccuec_stack.controls[1]
    detic_image = detic_stack.controls[0]
    detic_caption = detic_stack.controls[1]
    assert isinstance(ccuec_image, ThemedMaskedImage)
    assert isinstance(ccuec_caption, SuperCaption)
    assert isinstance(detic_image, ThemedMaskedImage)
    assert isinstance(detic_caption, SuperCaption)

    assert ccuec_image.theme_manager.theme.id == CCUEC_THEME.id
    assert ccuec_caption.theme_manager.theme.id == CCUEC_THEME.id
    assert detic_image.theme_manager.theme.id == DETIC_THEME.id
    assert detic_caption.theme_manager.theme.id == DETIC_THEME.id


def test_gallery_card_keeps_own_era_theme_when_global_theme_changes():
    manager = FakeThemeManager(FakeTheme())
    row = _row_for(
        GallerySuper(
            nome="Ada Lovelace",
            foto="ada.png",
            periodo="1967-1969",
            era_id="ccuec",
            is_placeholder=False,
        ),
        manager=manager,
    )
    stack = _card_stack(row)
    image = stack.controls[0]
    caption = stack.controls[1]
    assert isinstance(image, ThemedMaskedImage)
    assert isinstance(caption, SuperCaption)

    manager.set_theme_for_era("detic")

    assert manager.theme.id == DETIC_THEME.id
    assert image.theme_manager.theme.id == CCUEC_THEME.id
    assert caption.theme_manager.theme.id == CCUEC_THEME.id
    assert image.mask_image.color == CCUEC_THEME.image.caption_mask_tint
