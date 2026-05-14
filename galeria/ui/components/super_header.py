from typing import Any

import flet as ft

from galeria.ui.components.media import ThemedImage, themed_portrait_src
from galeria.ui.theme.manager import ThemeManager


class SuperHeader(ft.Container):
    def __init__(
        self,
        theme_manager: ThemeManager,
        image_src: str | None = None,
        nome: str = "",
        texto_inicial: str = "",
        navigation: ft.Control | None = None,
        **kwargs: Any,
    ):
        # 🎨 Theme
        self.theme_manager = theme_manager

        # 🧱 Conteúdo
        self.text_list = ft.ListView(
            height=433,
            spacing=12,
            controls=[],
        )
        self._set_paragraphs(texto_inicial)

        self.image = ThemedImage(
            src=themed_portrait_src(image_src) or "images/placeholder.png",
            theme=self.theme_manager,
            width=380,
            border_radius=20,
            fit=ft.BoxFit.COVER,
            apply_tint=False,
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
            controls=[self.image, text_area],
        )

        super().__init__(content=layout, **kwargs)

        # 🔗 Tema reativo
        if self.theme_manager:
            self.theme_manager.subscribe(self.apply_theme)

        self._mounted = False

    # =========================================================
    # 🎨 THEME
    # =========================================================
    def apply_theme(self, theme):
        if theme is None:
            return

        # Divider
        self.divider.color = theme.accent.primary

        # Textos
        self.title.color = theme.text.primary

        for p in self.text_list.controls:
            p.color = theme.text.secondary

        if self._mounted:
            self.update()

    # =========================================================
    # 🧩 TEXTO
    # =========================================================
    def _set_paragraphs(self, text: str):
        paragraphs = [p for p in text.split("\n\n") if p.strip()]
        self.text_list.controls = [ft.Text(p, size=14) for p in paragraphs]

    def update_text(self, new_text: str):
        self._set_paragraphs(new_text)

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
