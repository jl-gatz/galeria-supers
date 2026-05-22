# galeria/ui/views/gallery_view.py

from pathlib import Path

import flet as ft

from galeria.core import LOGO_DETIC, LOGO_UNICAMP
from galeria.domain.protocols import GalleryServiceLike
from galeria.domain.protocols.theme_manager_like import ThemeManagerLike
from galeria.ui.components import (
    FloatingNavButton,
    GalleryRow,
    logos_row,
    placeholders_row,
)
from galeria.ui.controllers import GalleryScrollController, SuperDetailController
from galeria.ui.layout import RootLayout
from galeria.ui.views.super_view import SuperDetail


class GalleryView(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        service: GalleryServiceLike,
        root_layout: RootLayout,
        theme: ThemeManagerLike,
        logo_detic: Path = Path(LOGO_DETIC),
        logo_unicamp: Path = Path(LOGO_UNICAMP),
        show_placeholder_left: bool = False,
        show_placeholder_right: bool = False,
    ):
        super().__init__(expand=True)

        # 📦 deps
        self._page = page
        self._mounted = False
        self.root = root_layout
        self._service = service
        self._theme = theme
        self._show_placeholder_left = show_placeholder_left
        self._show_placeholder_right = show_placeholder_right

        # 🎨 atalhos
        self.gallery = self._theme.gallery

        # 📦 estado
        self.supers = self._service.listar_supers()

        self.logos = logos_row(
            logo_detic,
            logo_unicamp,
            theme=self._theme,
        )

        self.placeholders = None

        # 📦 estrutura dinâmica
        self.gallery_row = None
        self.scroll_controller = None
        self.title_text = None

        # 🎨 background inicial
        self.bgcolor = self._theme.base.background

        # ✅ build inicial da UI
        self._apply_theme(self._theme.theme)

    # =========================================================
    # 🎨 THEME
    # =========================================================

    def _apply_theme(self, theme=None):
        # g = self._theme.gallery

        # 🎯 background sempre aqui
        self.bgcolor = self._theme.base.background

        if self.gallery_row is not None:
            self._apply_non_structural_theme()

            if self._mounted:
                self.update()
            return

        # 🎯 cria estrutura uma única vez; mudança de tema não deve resetar o scroll
        self.gallery_row = GalleryRow(
            supers=self.supers,
            card_width=self.gallery.card_width,
            spacing=self.gallery.h_spacing,
            padding=self.gallery.v_spacing,
            on_card_click=self._abrir_super,
            theme=self._theme,
        )
        self.placeholders = placeholders_row(
            self._show_placeholder_left,
            self._show_placeholder_right,
            theme=self._theme.theme,
        )

        self.scroll_controller = GalleryScrollController(
            row=self.gallery_row.row,
            visible_cards=self.gallery.visible_cards,
            card_width=self.gallery.card_width,
            spacing=self.gallery.h_spacing,
            padding=self.gallery.padding,
            on_active_index_change=self._set_active_super_index,
        )

        self.content = ft.Container(
            content=self._build_main_column(),
            width=self.gallery.max_width,
            alignment=ft.Alignment.TOP_CENTER,
            padding=self.gallery.padding,
        )

        # ✅ só atualiza se montado
        if self._mounted:
            self.update()

    def _apply_non_structural_theme(self) -> None:
        if self.title_text is None:
            return

        t = self._theme.typography
        self.title_text.size = t.h1
        self.title_text.font_family = t.font_family
        self.title_text.weight = t.weight_bold
        self.title_text.color = self._theme.text.primary

    def _text(self, value: str, variant: str = "body", weight=None, color=None, **kwargs):
        t = self._theme.typography

        return ft.Text(
            value,
            size=getattr(t, variant),
            font_family=t.font_family,
            weight=weight or t.weight_regular or t.weight_medium or t.weight_bold,
            color=color or self._theme.text.primary,
            **kwargs,
        )

    # =========================================================
    # 🧱 BUILDERS
    # =========================================================
    # def _build_static(self, theme=None):
    #     # g = self._theme.gallery

    #     self.gallery_row = GalleryRow(
    #         supers=self.supers,
    #         card_width=self.gallery.card_width,
    #         spacing=self.gallery.h_spacing,
    #         padding=self.gallery.v_spacing,
    #         on_card_click=self._abrir_super,
    #         theme=self._theme,
    #     )

    #     self.scroll_controller = GalleryScrollController(
    #         row=self.gallery_row.row,
    #         visible_cards=self.gallery.visible_cards,
    #         card_width=self.gallery.card_width,
    #         spacing=self.gallery.h_spacing,
    #         padding=self.gallery.padding,
    #     )

    #     self.content = ft.Container(
    #         expand=True,
    #         bgcolor=self._theme.base.background,
    #         content=self._build_main_column(),
    #         width=self.gallery.max_width,
    #         alignment=ft.Alignment.TOP_CENTER,
    #         padding=self.gallery.padding,
    #     )

    def _build_gallery(self):
        # g = self._theme.gallery

        return ft.Container(
            width=self.scroll_controller.group_width(),
            height=self._gallery_height(),
            content=self.gallery_row,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )

    def _build_main_column(self):
        # g = self._theme.gallery
        self.title_text = self._text(
            "Galeria de Superintendentes",
            variant="h1",
            weight=self._theme.typography.weight_bold,
        )

        return ft.Column(
            expand=True,
            controls=[
                self.title_text,
                self._build_gallery(),
                self._build_fab(),
                self.logos,
                self.placeholders,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=self.gallery.v_spacing,
        )

    def _build_fab(self):
        # g = self._theme.gallery

        return ft.Container(
            content=FloatingNavButton.forward(
                on_click=lambda _: self._page.run_task(self.scroll_controller.next),
                key="gallery_next",
                theme_manager=self._theme,
            ),
            width=self.scroll_controller.group_width() + 2 * self.gallery.padding,
            alignment=ft.Alignment.CENTER_RIGHT,
        )

    def _gallery_height(self):
        # g = self._theme.gallery
        return self.gallery.card_height + self.gallery.v_spacing

    def _set_active_super_index(self, index: int) -> None:
        if not self.supers:
            return

        active_super = self.supers[max(0, min(len(self.supers) - 1, index))]
        self._theme.set_theme_for_era(getattr(active_super, "era_id", None))

    # =========================================================
    # 🔁 INTERAÇÕES
    # =========================================================

    def _abrir_super(self, super_data):
        if not self._service.pode_abrir(super_data):
            return

        self._theme.set_theme_for_era(getattr(super_data, "era_id", None))
        controller = SuperDetailController(super_data)
        detail = None

        def handle_close():
            self.root.hide_overlay(detail)

        detail = SuperDetail(
            controller=controller,
            on_request_close=handle_close,
            theme_manager=self._theme,
        )

        self.root.show_overlay(detail)
        detail._fade_in()

    # =========================================================
    # 🔁 LIFECYCLE
    # =========================================================
    def did_mount(self):
        self._mounted = True

        # ✅ ativa reatividade apenas após mount
        self._theme.subscribe(self._apply_theme)
        self._set_active_super_index(0)

    def will_unmount(self):
        self._mounted = False
        self._theme.unsubscribe(self._apply_theme)
