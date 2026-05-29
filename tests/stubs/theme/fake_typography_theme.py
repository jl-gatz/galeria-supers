from typing import override

import flet as ft

from galeria.ui.theme.models import Typography


class FakeTypographyTheme(Typography):
    def __init__(
        self,
        font_family: str = "Montserrat",
        display: int = 48,
        h1: int = 32,
        h2: int = 24,
        body: int = 16,
        small: int = 12,
        weight_regular: ft.FontWeight = ft.FontWeight.W_400,
        weight_medium: ft.FontWeight = ft.FontWeight.W_500,
        weight_bold: ft.FontWeight = ft.FontWeight.W_700,
    ) -> None:
        super().__init__(
            font_family=font_family,
            display=display,
            h1=h1,
            h2=h2,
            body=body,
            small=small,
            weight_regular=weight_regular,
            weight_medium=weight_medium,
            weight_bold=weight_bold,
        )

    @override
    def __setattr__(self, name: str, value: object) -> None:
        object.__setattr__(self, name, value)
