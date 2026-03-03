import math

import flet as ft

from galeria.core.config import SCROLL_DURATION, SCROLL_RESET_DURATION


class GalleryScrollController:
    def __init__(self, row: ft.Row, visible_cards: int, card_width: int, spacing: int):
        self.row = row
        self.visible_cards = visible_cards
        self.card_width = card_width
        self.spacing = spacing
        self.current_page = 0

        self.row.on_scroll = self._on_scroll

    def group_width(self):
        return self.visible_cards * self.card_width + (self.visible_cards - 1) * self.spacing

    def total_pages(self):
        total_cards = len(self.row.controls)
        return max(0, math.ceil(total_cards / self.visible_cards) - 1)

    async def _on_scroll(self, e: ft.OnScrollEvent):
        pixels = e.pixels
        max_scroll = e.max_scroll_extent

        if pixels >= max_scroll - 5:
            self.current_page = 0
            await self.row.scroll_to(
                offset=0,
                duration=SCROLL_RESET_DURATION,
            )

    async def next(self):
        if self.current_page < self.total_pages():
            self.current_page += 1
        else:
            self.current_page = 0

        offset = self.current_page * self.group_width()

        await self.row.scroll_to(
            offset=offset,
            duration=SCROLL_DURATION,
        )
