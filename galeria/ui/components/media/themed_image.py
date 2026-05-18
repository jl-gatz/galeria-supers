from typing import Any

import flet as ft


class ThemedImage(ft.Image):
    def __init__(
        self,
        src: str,
        theme: Any,
        apply_tint: bool = False,
        **kwargs: Any,
    ):
        super().__init__(src=src, **kwargs)

        self.theme_manager = theme
        self.apply_tint = apply_tint
        self._mounted = False

        self._apply_theme(self.theme_manager.theme)

    def _apply_theme(self, theme):
        if self.apply_tint:
            self.color = theme.image.portrait_tint
            self.color_blend_mode = theme.image.portrait_blend_mode
            self.opacity = theme.image.portrait_opacity
        else:
            self.color = None
            self.color_blend_mode = None
            self.opacity = 1.0

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
