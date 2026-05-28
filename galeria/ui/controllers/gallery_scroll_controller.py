# galeria/ui/controllers/gallery_scroll_controller.py
"""Controle de rolagem paginada da galeria horizontal."""

import math
from collections.abc import Callable

import flet as ft

from galeria.core.config import SCROLL_DURATION


class GalleryScrollController:
    """Calcula páginas, offsets e card ativo de uma linha horizontal."""

    def __init__(
        self,
        row: ft.Row,
        visible_cards: int,
        card_width: int,
        spacing: int,
        padding: int = 0,
        on_active_index_change: Callable[[int], None] | None = None,
    ):
        self.row = row
        self.visible_cards = visible_cards
        self.card_width = card_width
        self.spacing = spacing
        self.padding = padding
        self.on_active_index_change = on_active_index_change
        self.current_page = 0

        self.row.on_scroll = self._on_scroll

    def group_width(self):
        """Retorna a largura ocupada pelos cards visíveis de uma página."""
        return self.visible_cards * self.card_width + (self.visible_cards - 1) * self.spacing

    def page_width(self):
        """Retorna a distância entre o início de uma página e a próxima."""
        return self.group_width() + self.spacing

    def total_pages(self):
        """Retorna o maior índice de página disponível para a linha."""
        total_cards = len(self.row.controls)
        # Número de páginas baseado nos cards, sem considerar padding
        return max(0, math.ceil(total_cards / self.visible_cards) - 1)

    async def _on_scroll(self, e: ft.OnScrollEvent):
        """Atualiza o índice ativo a partir da posição manual do scroll."""
        pixels = e.pixels
        # max_scroll = e.max_scroll_extent
        self._notify_active_index(self.active_index_from_offset(pixels))

        # DESLIGADO POR ENQUANTO: reset automático ao chegar no final (pode ser confuso se o usuário quiser ir pro final)
        # if pixels >= max_scroll - 5:
        #     self.current_page = 0
        #     await self.row.scroll_to(
        #         offset=0,
        #         duration=SCROLL_RESET_DURATION,
        #     )

    async def next(self):
        """Avança para a próxima página da galeria ou retorna ao começo."""
        if self.current_page < self.total_pages():
            self.current_page += 1
        else:
            self.current_page = 0

        # Offset = padding inicial + (página atual) * (largura de uma página completa)
        offset = self.padding + self.current_page * self.page_width()

        await self.row.scroll_to(
            offset=offset,
            duration=SCROLL_DURATION,
        )
        self._notify_active_index(self.active_index_from_offset(offset))

    def active_index_from_offset(self, offset: float) -> int:
        """Calcula o card central aproximado para um offset de rolagem."""
        total_cards = len(self.row.controls)
        if total_cards == 0:
            return 0

        card_step = self.card_width + self.spacing
        centered_offset = max(0, offset - self.padding) + self.group_width() / 2
        index = round(centered_offset / card_step)
        return max(0, min(total_cards - 1, index))

    def _notify_active_index(self, index: int) -> None:
        """Emite o índice ativo quando há callback registrado."""
        if self.on_active_index_change:
            self.on_active_index_change(index)
