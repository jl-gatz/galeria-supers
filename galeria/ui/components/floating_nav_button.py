from collections.abc import Callable
from typing import Any

import flet as ft


class FloatingNavButton(ft.Container):
    def __init__(
        self,
        icon: str | ft.IconData,
        on_click: Callable[[ft.ControlEvent], None],
        tooltip: str | None = None,
        alignment: ft.Alignment = ft.Alignment.BOTTOM_RIGHT,
        key: str | None = None,
        theme_manager: Any | None = None,
    ):
        super().__init__()

        self.theme_manager = theme_manager
        self._mounted = False

        # self.expand = True
        self.alignment = alignment
        self.padding = 20

        self.button = ft.FloatingActionButton(
            icon=icon,
            tooltip=tooltip,
            on_click=on_click,
            key=key,
        )
        self.content = self.button

        if self.theme_manager:
            self.apply_theme(self.theme_manager.theme)

    def apply_theme(self, theme):
        button_theme = getattr(theme, "button", None)

        self.padding = getattr(theme.spacing, "md", 20)
        self.button.bgcolor = getattr(button_theme, "bg", theme.accent.primary)
        self.button.foreground_color = getattr(button_theme, "fg", theme.text.inverse)

        if self._mounted:
            self.update()

    def did_mount(self):
        self._mounted = True

        if self.theme_manager:
            self.theme_manager.subscribe(self.apply_theme)
            self.apply_theme(self.theme_manager.theme)

    def will_unmount(self):
        self._mounted = False

        if self.theme_manager:
            self.theme_manager.unsubscribe(self.apply_theme)

    # 🔹 especializações semânticas
    @classmethod
    def back(
        cls,
        on_click: Callable[[ft.ControlEvent], None],
        key: str = "nav_back",
        theme_manager: Any | None = None,
    ):
        return cls(
            icon=ft.Icons.ARROW_BACK,
            tooltip="Voltar",
            on_click=on_click,
            key=key,
            theme_manager=theme_manager,
        )

    @classmethod
    def forward(
        cls,
        on_click: Callable[[ft.ControlEvent], None],
        key: str = "nav_forward",
        theme_manager: Any | None = None,
    ):
        return cls(
            icon=ft.Icons.ARROW_FORWARD,
            tooltip="Avançar",
            on_click=on_click,
            key=key,
            theme_manager=theme_manager,
        )
