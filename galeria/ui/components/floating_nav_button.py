from collections.abc import Callable

import flet as ft

from galeria.ui.theme import PRIMARY_RED


class FloatingNavButton(ft.Container):
    def __init__(
        self,
        icon: str | ft.IconData,
        on_click: Callable[[ft.ControlEvent], None],
        tooltip: str | None = None,
        alignment: ft.Alignment = ft.Alignment.BOTTOM_RIGHT,
        key: str | None = None,
    ):
        super().__init__()

        # self.expand = True
        self.alignment = alignment
        self.padding = 20

        self.content = ft.FloatingActionButton(
            icon=icon,
            tooltip=tooltip,
            bgcolor=PRIMARY_RED,
            foreground_color=ft.Colors.WHITE,
            on_click=on_click,
            key=key,
        )

    # 🔹 especializações semânticas
    @classmethod
    def back(
        cls,
        on_click: Callable[[ft.ControlEvent], None],
        key: str = "nav_back",
    ):
        return cls(
            icon=ft.Icons.ARROW_BACK,
            tooltip="Voltar",
            on_click=on_click,
            key=key,
        )

    @classmethod
    def forward(
        cls,
        on_click: Callable[[ft.ControlEvent], None],
        key: str = "nav_forward",
    ):
        return cls(
            icon=ft.Icons.ARROW_FORWARD,
            tooltip="Avançar",
            on_click=on_click,
            key=key,
        )
