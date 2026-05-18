from typing import Any

import flet as ft

from galeria.ui.theme.manager import ThemeManager


class SuperCaption(ft.Container):
    def __init__(
        self,
        theme_manager: ThemeManager,
        nome: str,
        subtitle: str | None = None,
        width: float | None = None,
        compact: bool = False,
        single_line_name: bool = False,
        **kwargs: Any,
    ):
        self.theme_manager = theme_manager
        self.nome = nome
        self.subtitle = subtitle
        self.compact = compact
        self.single_line_name = single_line_name
        self._mounted = False

        self.name_text = ft.Text(
            nome,
            max_lines=1 if single_line_name else 2,
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        self.subtitle_text = (
            ft.Text(
                subtitle,
                max_lines=1,
                overflow=ft.TextOverflow.ELLIPSIS,
            )
            if subtitle
            else None
        )

        controls: list[ft.Control] = [self.name_text]
        if self.subtitle_text is not None:
            controls.append(self.subtitle_text)

        self.text_column = ft.Column(
            spacing=2 if compact else 4,
            tight=True,
            controls=controls,
        )

        super().__init__(
            content=self.text_column,
            width=width,
            left=0,
            right=0,
            bottom=0,
            alignment=ft.Alignment.BOTTOM_LEFT,
            **kwargs,
        )

        if self.theme_manager:
            self._apply_theme(self.theme_manager.theme)

    def apply_theme(self, theme):
        self._apply_theme(theme)

        if self._mounted and self._has_page():
            self.update()

    def _apply_theme(self, theme):
        if theme is None:
            return

        typography = getattr(theme, "typography", None)
        spacing = getattr(theme, "spacing", None)
        text = getattr(theme, "text", None)

        # TODO: mover estes tokens locais para theme/styles.py ou theme/typography.py
        # quando houver um contrato explícito para captions sobre retratos.
        horizontal_padding = self._theme_token(spacing, ["md"], 16)
        vertical_padding = self._theme_token(spacing, ["sm"], 8)
        name_size = self._theme_token(
            typography,
            ["super_caption_name_size", "caption_name_size"],
            self._theme_token(typography, ["body"], 16),
        )
        subtitle_size = self._theme_token(
            typography,
            ["super_caption_subtitle_size", "caption_subtitle_size"],
            self._theme_token(typography, ["small"], 12),
        )
        line_height = self._theme_token(
            typography,
            ["super_caption_line_height", "caption_line_height"],
            1.05,
        )

        if self.compact:
            vertical_padding = max(4, int(vertical_padding * 0.75))
            name_size = max(12, int(name_size * 0.8))
            subtitle_size = max(10, int(subtitle_size * 0.9))

        if self.single_line_name:
            name_size = self._theme_token(
                typography,
                ["super_caption_single_line_name_size", "caption_single_line_name_size"],
                max(12, int(name_size * 0.72)),
            )

        self.padding = ft.padding.symmetric(
            horizontal=horizontal_padding,
            vertical=vertical_padding,
        )

        self.name_text.color = self._theme_token(text, ["inverse", "primary"], "#FFFFFF")
        self.name_text.size = name_size
        self.name_text.weight = self._theme_token(
            typography,
            ["weight_bold", "weight_medium"],
            ft.FontWeight.BOLD,
        )
        self.name_text.font_family = self._theme_token(typography, ["font_family"], None)
        self.name_text.style = ft.TextStyle(height=line_height)

        if self.subtitle_text is not None:
            self.subtitle_text.color = self._theme_token(
                text,
                ["inverse", "secondary"],
                "#FFFFFF",
            )
            self.subtitle_text.size = subtitle_size
            self.subtitle_text.weight = self._theme_token(
                typography,
                ["weight_medium", "weight_regular"],
                ft.FontWeight.W_500,
            )
            self.subtitle_text.font_family = self._theme_token(
                typography,
                ["font_family"],
                None,
            )
            self.subtitle_text.style = ft.TextStyle(height=line_height)

    def _theme_token(self, source, names: list[str], fallback=None):
        if source is None:
            return fallback

        for name in names:
            value = getattr(source, name, None)
            if value is not None:
                return value

        return fallback

    def _has_page(self) -> bool:
        try:
            return self.page is not None
        except RuntimeError:
            return False

    def did_mount(self):
        self._mounted = True
        if self.theme_manager:
            self.theme_manager.subscribe(self.apply_theme)
            self.apply_theme(self.theme_manager.theme)

    def will_unmount(self):
        self._mounted = False
        if self.theme_manager:
            self.theme_manager.unsubscribe(self.apply_theme)
