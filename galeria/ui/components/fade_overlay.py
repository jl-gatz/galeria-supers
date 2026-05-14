import flet as ft


def right_fade(theme=None):
    fade_color = theme.base.background if theme else ft.Colors.GRAY

    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER_RIGHT,
        content=ft.Container(
            width=20,
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.Alignment.CENTER_LEFT,
                end=ft.Alignment.CENTER_RIGHT,
                colors=[ft.Colors.TRANSPARENT, fade_color],
            ),
        ),
        # ignore_pointer=True,
    )
