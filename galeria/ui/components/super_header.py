from typing import Any

import flet as ft

from galeria.core import SUPER_CAPTION_MASK
from galeria.ui.components import ThemedMaskedImage
from galeria.ui.components.media import themed_portrait_src
from galeria.ui.components.super_caption import SuperCaption
from galeria.ui.theme.manager import ThemeManager


class SuperHeader(ft.Container):
    def __init__(
        self,
        theme_manager: ThemeManager,
        image_src: str | None = None,
        nome: str = "",
        periodo: str | None = None,
        texto_inicial: str = "",
        navigation: ft.Control | None = None,
        **kwargs: Any,
    ):
        # 🎨 Theme
        self.theme_manager = theme_manager
        self._mounted = False

        # 🧱 Conteúdo
        self.text_list = ft.ListView(
            height=433,
            spacing=12,
            controls=[],
        )
        self._set_paragraphs(texto_inicial)

        self.portrait_image = ThemedMaskedImage(
            src=themed_portrait_src(image_src) or "images/placeholder.png",
            mask_src=SUPER_CAPTION_MASK,
            theme=self.theme_manager,
            fit=ft.BoxFit.COVER,
            width=380,
            apply_mask=image_src is not None,
        )
        self.portrait_caption = SuperCaption(
            theme_manager=self.theme_manager,
            nome=nome,
            subtitle=periodo,
            width=380,
        )
        self.portrait_stack = ft.Stack(
            width=380,
            controls=[
                self.portrait_image,
                self.portrait_caption,
            ],
        )

        self.title = ft.Text(
            nome,
            size=28,
            weight=ft.FontWeight.BOLD,
        )

        self.divider = ft.Divider(thickness=3)

        text_area = ft.Column(
            expand=True,
            spacing=16,
            controls=[
                self.title,
                self.divider,
                self.text_list,
                navigation or ft.Container(),
            ],
        )

        layout = ft.Row(
            expand=True,
            spacing=32,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[self.portrait_stack, text_area],
        )

        super().__init__(content=layout, **kwargs)

        # 🔗 Tema reativo
        if self.theme_manager:
            self.theme_manager.subscribe(self.apply_theme)

    # =========================================================
    # 🎨 THEME
    # =========================================================
    def apply_theme(self, theme):
        if theme is None:
            return

        self._apply_divider_theme(theme)
        self._apply_title_theme(theme)
        self._apply_paragraphs_theme(theme)

        if self._mounted and self._has_page():
            self.update()

    def _has_page(self) -> bool:
        try:
            return self.page is not None
        except RuntimeError:
            return False

    def _apply_divider_theme(self, theme):
        self.divider.color = theme.accent.primary

    def _apply_title_theme(self, theme):
        self.title.color = theme.text.primary
        self.title.size = self._theme_token(
            theme,
            ["super_header_title_size", "title_size", "h2"],
            fallback=28,
        )
        self.title.font_family = self._theme_token(
            theme,
            ["super_header_title_font_family", "title_font_family"],
            fallback=self._theme_token(theme, ["font_family"], fallback=None),
        )

    def _apply_paragraphs_theme(self, theme):
        for paragraph in self.text_list.controls:
            self._apply_paragraph_theme(paragraph, theme)

    def _apply_paragraph_theme(self, paragraph: ft.Text, theme):
        role = getattr(paragraph, "data", None)
        paragraph.color = theme.accent.primary if role == "timeline_year" else theme.text.secondary
        paragraph.size = self._theme_token(
            theme,
            ["super_header_body_size", "body_size", "body"],
            fallback=14,
        )
        if role == "timeline_year":
            paragraph.size = self._theme_token(
                theme,
                ["super_header_title_size", "title_size", "h2"],
                fallback=28,
            )
        elif role == "timeline_label":
            paragraph.color = theme.text.primary
        paragraph.font_family = self._theme_token(
            theme,
            ["super_header_body_font_family", "body_font_family"],
            fallback=self._theme_token(theme, ["font_family"], fallback=None),
        )
        paragraph.weight = (
            self._theme_token(theme, ["weight_bold"], fallback=ft.FontWeight.BOLD)
            if role in {"timeline_year", "timeline_label"}
            else None
        )

        line_height = self._theme_token(
            theme,
            ["super_header_body_line_height", "body_line_height"],
            fallback=None,
        )

        if line_height is not None:
            paragraph.style = ft.TextStyle(height=line_height)

    def _theme_token(self, theme, names: list[str], fallback=None):
        typography = getattr(theme, "typography", None)

        if typography is None:
            return fallback

        for name in names:
            value = getattr(typography, name, None)

            if value is not None:
                return value

        return fallback

    # =========================================================
    # 🧩 TEXTO
    # =========================================================
    def _set_paragraphs(self, text: str):
        paragraphs = [p for p in text.split("\n\n") if p.strip()]
        self.text_list.controls = [self._create_paragraph_control(p) for p in paragraphs]

    def _create_paragraph_control(self, text: str) -> ft.Text:
        return ft.Text(text, size=14)

    def update_text(self, new_text: str):
        self._set_paragraphs(new_text)

        if hasattr(self.text_list, "_i"):
            self.text_list.scroll_to(offset=0)

        if self.theme_manager:
            self.apply_theme(self.theme_manager.theme)

    def set_timeline_event(self, year: int, label: str, text: str):
        self.text_list.controls = [
            self._create_paragraph_control(str(year)),
            self._create_paragraph_control(label),
            *[self._create_paragraph_control(p) for p in text.split("\n\n") if p.strip()],
        ]
        self.text_list.controls[0].data = "timeline_year"
        self.text_list.controls[1].data = "timeline_label"

        if hasattr(self.text_list, "_i"):
            self.text_list.scroll_to(offset=0)

        if self.theme_manager:
            self.apply_theme(self.theme_manager.theme)

    # =========================================================
    # 🎬 LIFECYCLE
    # =========================================================
    def did_mount(self):
        self._mounted = True
        if self.theme_manager:
            self.apply_theme(self.theme_manager.theme)
