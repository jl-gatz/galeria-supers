import flet as ft

from galeria.ui.theme import spacing


def right_arrow(on_click: ft.Control):
    return ft.Container(
        expand=True,
        alignment=ft.Alignment.BOTTOM_RIGHT,
        content=ft.IconButton(
            icon=ft.Icons.ARROW_FORWARD,
            icon_size=spacing.XXL,
            on_click=on_click,
        ),
    )
