import flet as ft

from galeria.ui.theme.colors import GRAY


def right_fade():
    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER_RIGHT,
        content=ft.Container(
            width=20,
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.Alignment.CENTER_LEFT,
                end=ft.Alignment.CENTER_RIGHT,
                colors=[ft.Colors.TRANSPARENT, GRAY],
            ),
        ),
        # ignore_pointer=True,
    )
