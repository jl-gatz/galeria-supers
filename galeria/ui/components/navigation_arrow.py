import flet as ft


def right_arrow(on_click):
    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER_RIGHT,
        content=ft.IconButton(
            icon=ft.Icons.ARROW_FORWARD,
            icon_size=48,
            on_click=on_click,
        ),
    )
