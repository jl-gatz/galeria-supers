from typing import Any

import flet as ft

from galeria.ui.theme.colors import BLACK
from galeria.ui.theme.typography import BODY, FONT, H1, H2


def heading_h1(text: str, **kwargs: Any):
    return ft.Text(
        text,
        font_family=FONT,
        size=H1,
        weight=ft.FontWeight.BOLD,
        color=BLACK,
        **kwargs,
    )


def heading_h2(text: str, **kwargs: Any):
    return ft.Text(
        text,
        font_family=FONT,
        size=H2,
        weight=ft.FontWeight.BOLD,
        color=BLACK,
        **kwargs,
    )


def body(text: str, **kwargs: Any):
    return ft.Text(
        text,
        font_family=FONT,
        size=BODY,
        color=BLACK,
        **kwargs,
    )
