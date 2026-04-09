from collections.abc import Callable

import flet as ft

from galeria.ui.theme import PRIMARY_RED


def floating_nav_button(
    icon: str | ft.IconData,
    on_click: Callable[[ft.ControlEvent], None],
    tooltip: str | None = None,
    alignment: ft.Alignment = ft.Alignment.BOTTOM_RIGHT,
    key: str | None = None,
):
    return ft.Container(
        expand=True,
        alignment=alignment,
        padding=20,
        content=ft.FloatingActionButton(
            icon=icon,
            tooltip=tooltip,
            bgcolor=PRIMARY_RED,
            foreground_color=ft.Colors.WHITE,
            on_click=on_click,
            key=key,
        ),
    )


def fab_back(on_click: Callable[[ft.ControlEvent], None], key: str = "nav_back"):
    return floating_nav_button(
        icon=ft.Icons.ARROW_BACK, tooltip="Voltar", on_click=on_click, key=key
    )


def fab_forward(on_click: Callable[[ft.ControlEvent], None], key: str = "nav_forward"):
    return floating_nav_button(
        icon=ft.Icons.ARROW_FORWARD, tooltip="Avançar", on_click=on_click, key=key
    )
