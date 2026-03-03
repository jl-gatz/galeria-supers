import flet as ft
from ui.theme.colors import BLACK


def heading_h1(text: str):
    return ft.Text(
        text,
        font_family="Montserrat",
        size=72,
        weight=ft.FontWeight.BOLD,
        color=BLACK,
    )


def body(text: str):
    return ft.Text(
        text,
        font_family="Montserrat",
        size=22,
        color=BLACK,
    )
