from typing import Any

import flet as ft

from galeria.ui.theme.theme import Theme


class Typography:
    def __init__(
        self,
        font_family: str,
        display: int,
        h1: int,
        h2: int,
        body: int,
        small: int,
        weight_regular: ft.FontWeight = ft.FontWeight.W_400,
        weight_medium: ft.FontWeight = ft.FontWeight.W_500,
        weight_bold: ft.FontWeight = ft.FontWeight.W_700,
    ):
        self.font_family = font_family
        self.sizes = {
            "display": display,
            "h1": h1,
            "h2": h2,
            "body": body,
            "small": small,
            "weight_regular": weight_regular,
            "weight_medium": weight_medium,
            "weight_bold": weight_bold,
        }

    # ---- Headings ----

    def h1(self, theme: Theme, text: str, **kwargs: Any):
        return ft.Text(
            text,
            font_family=self.font_family,
            size=self.sizes["h1"],
            weight=self.weights["bold"],
            color=theme.text.primary,
            **kwargs,
        )

    def h2(self, theme: Theme, text: str, **kwargs: Any):
        return ft.Text(
            text,
            font_family=self.font_family,
            size=self.sizes["h2"],
            weight=self.weights["bold"],
            color=theme.text.primary,
            **kwargs,
        )

    # ---- Body ----

    def body(self, theme: Theme, text: str, **kwargs: Any):
        return ft.Text(
            text,
            font_family=self.font_family,
            size=self.sizes["body"],
            weight=self.weights["regular"],
            color=theme.text.primary,
            **kwargs,
        )

    def small(self, theme: Theme, text: str, **kwargs: Any):
        return ft.Text(
            text,
            font_family=self.font_family,
            size=self.sizes["small"],
            weight=self.weights["regular"],
            color=theme.text.secondary,
            **kwargs,
        )
