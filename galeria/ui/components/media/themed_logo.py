from typing import Any

import flet as ft

from galeria.core import LOGOS_DIR


def resolve_logo_src(
    theme_id: str | None,
    filename: str,
    logos_dir=None,
) -> str:
    logos_dir = logos_dir or LOGOS_DIR
    logo_filename = filename.split("/")[-1].split("\\")[-1]
    fallback_path = logos_dir / logo_filename

    if theme_id:
        themed_path = logos_dir / theme_id / logo_filename

        if themed_path.exists():
            return f"images/logos/{theme_id}/{logo_filename}"

    return f"images/logos/{fallback_path.name}"


def _theme_id(theme) -> str | None:
    return getattr(theme, "id", None)


class ThemedLogo(ft.Image):
    def __init__(
        self,
        filename: str | None = None,
        theme_manager: Any | None = None,
        src: str | None = None,
        theme: Any | None = None,
        **kwargs: Any,
    ):
        self.theme_manager = theme_manager or theme
        self._filename = filename or src or ""
        self._mounted = False

        super().__init__(
            src=self._resolve_src(self.theme_manager.theme),
            **kwargs,
        )

        self._apply_theme(self.theme_manager.theme)

    def _apply_theme(self, theme):
        self.src = self._resolve_src(theme)
        self.color = None
        self.color_blend_mode = None
        self.opacity = 1.0

        if self._mounted and self._has_page():
            self.update()

    def _resolve_src(self, theme):
        return resolve_logo_src(_theme_id(theme), self._filename)

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
