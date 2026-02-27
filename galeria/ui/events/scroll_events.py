# events/scroll_events.py

import flet as ft
from core.config import SCROLL_RESET_DURATION


def criar_scroll_handler(galeria: ft.Row):
    async def on_scroll(e: ft.OnScrollEvent):
        pixels = e.pixels
        max_scroll = e.max_scroll_extent

        if pixels >= max_scroll - 5:
            await galeria.scroll_to(offset=0, duration=SCROLL_RESET_DURATION)

    return on_scroll
