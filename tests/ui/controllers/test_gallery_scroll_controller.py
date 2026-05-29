from types import SimpleNamespace
from typing import cast

import flet as ft
import pytest

from galeria.ui.controllers.gallery_scroll_controller import GalleryScrollController


def _row(card_count: int) -> ft.Row:
    return ft.Row(controls=[ft.Container() for _ in range(card_count)])


def test_gallery_scroll_controller_finds_centered_card_index():
    controller = GalleryScrollController(
        row=_row(5),
        visible_cards=1,
        card_width=100,
        spacing=10,
        padding=0,
    )

    assert controller.active_index_from_offset(0) == 0
    assert controller.active_index_from_offset(110) == 1
    assert controller.active_index_from_offset(440) == 4


@pytest.mark.asyncio
async def test_gallery_scroll_controller_notifies_active_index_on_scroll():
    active_indexes: list[int] = []
    controller = GalleryScrollController(
        row=_row(5),
        visible_cards=1,
        card_width=100,
        spacing=10,
        padding=0,
        on_active_index_change=active_indexes.append,
    )

    event = cast(ft.OnScrollEvent, SimpleNamespace(pixels=110, max_scroll_extent=440))
    await controller._on_scroll(event)

    assert active_indexes == [1]
