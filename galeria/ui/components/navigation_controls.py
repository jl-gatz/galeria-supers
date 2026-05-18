from collections.abc import Callable
from typing import Any

import flet as ft


class NavigationControls(ft.Row):
    def __init__(
        self,
        on_prev: Callable[[], None],
        on_next: Callable[[], None],
        alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.END,
        theme_manager: Any | None = None,
    ):
        self.theme_manager = theme_manager
        self._mounted = False

        def _build_button(icon, tooltip, handler):
            return ft.IconButton(
                icon=icon,
                tooltip=tooltip,
                on_click=lambda e: handler(),
            )

        self.prev_button = _build_button(
            ft.Icons.CHEVRON_LEFT,
            "Anterior",
            on_prev,
        )
        self.next_button = _build_button(
            ft.Icons.CHEVRON_RIGHT,
            "Próximo",
            on_next,
        )

        super().__init__(
            alignment=alignment,
            controls=[self.prev_button, self.next_button],
        )

        if self.theme_manager:
            self.apply_theme(self.theme_manager.theme)

    def apply_theme(self, theme):
        button_theme = getattr(theme, "button", None)  # noqa: F841
        hover_color = theme.accent.secondary

        for button in (self.prev_button, self.next_button):
            button.icon_color = theme.text.primary
            button.style = ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=getattr(theme.radius, "sm", 8)),
                bgcolor={
                    ft.ControlState.HOVERED: hover_color,
                    ft.ControlState.PRESSED: theme.accent.secondary,
                },
            )

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
