# tests/stubs/theme/fake_base_theme.py

from dataclasses import dataclass

import flet as ft


@dataclass
class FakeTypographyTheme:
    font_family: str = "Montserrat"

    display: int = 48
    h1: int = 32
    h2: int = 24
    body: int = 16
    small: int = 12

    weight_regular: ft.FontWeight = ft.FontWeight.W_400
    weight_medium: ft.FontWeight = ft.FontWeight.W_500
    weight_bold: ft.FontWeight = ft.FontWeight.W_700
