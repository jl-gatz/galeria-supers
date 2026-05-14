from typing import Any

import flet as ft


class ThemedLogo(ft.Image):
    def __init__(
        self,
        src: str,
        theme: Any,
        **kwargs: Any,
    ):
        super().__init__(src=src, **kwargs)

        self.theme_manager = theme
        self._mounted = False

        self._apply_theme(self.theme_manager.theme)

    def _apply_theme(self, theme):
        logo = theme.logo

        if logo.variant == "official":
            self.color = None
            self.color_blend_mode = None
            self.opacity = 1.0
        else:
            self.color = logo.tint
            self.color_blend_mode = logo.blend_mode
            self.opacity = logo.opacity

        if self._mounted and self._has_page():
            self.update()

    def _has_page(self) -> bool:
        try:
            return self.page is not None
        except RuntimeError:
            return False

    def did_mount(self):
        self._mounted = True
        self.theme_manager.subscribe(self._apply_theme)
        self._apply_theme(self.theme_manager.theme)

    def will_unmount(self):
        self._mounted = False
        self.theme_manager.unsubscribe(self._apply_theme)
