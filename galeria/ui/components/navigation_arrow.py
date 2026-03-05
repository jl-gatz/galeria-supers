import flet as ft


def right_arrow(on_click: ft.Control):
    return ft.Container(
        expand=True,
        alignment=ft.Alignment.BOTTOM_RIGHT,
        content=ft.IconButton(
            icon=ft.Icons.ARROW_FORWARD,
            icon_size=48,
            on_click=on_click,
        ),
    )
