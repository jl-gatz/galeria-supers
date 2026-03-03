import flet as ft


def right_fade(width=160):
    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER_RIGHT,
        content=ft.Container(
            width=width,
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.Alignment.CENTER_LEFT,
                end=ft.Alignment.CENTER_RIGHT,
                colors=["#F4F4F400", "#F4F4F4"],
            ),
        ),
        # ignore_pointer=True,
    )
