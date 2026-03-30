import flet as ft

from galeria.ui.theme import RED_55, RED_DARK, spacing


def right_arrow(on_click: ft.Control):
    return ft.Container(
        expand=True,
        alignment=ft.Alignment.BOTTOM_RIGHT,
        content=ft.IconButton(
            icon=ft.Icons.ARROW_FORWARD,
            icon_size=spacing.XXL,
            style=ft.ButtonStyle(
                color=RED_DARK,  # TODO verificar cor na seta
                bgcolor={
                    ft.ControlState.HOVERED: RED_55,
                },
            ),
            on_click=on_click,
        ),
    )
