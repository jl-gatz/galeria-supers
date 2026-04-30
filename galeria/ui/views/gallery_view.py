# galeria/ui/views/gallery_view.py

from pathlib import Path

import flet as ft

from galeria.core import LOGO_DETIC, LOGO_UNICAMP
from galeria.domain.protocols import GalleryServiceLike
from galeria.ui.components import (
    FloatingNavButton,
    GalleryRow,
    logos_row,
    placeholders_row,
)
from galeria.ui.controllers import GalleryScrollController, SuperDetailController
from galeria.ui.layout import RootLayout
from galeria.ui.theme.manager import ThemeManager
from galeria.ui.views.super_view import SuperDetail


class GalleryView(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        service: GalleryServiceLike,
        root_layout: RootLayout,
        theme: ThemeManager,
        logo_detic: Path = Path(LOGO_DETIC),
        logo_unicamp: Path = Path(LOGO_UNICAMP),
        show_placeholder_left: bool = False,
        show_placeholder_right: bool = False,
    ):
        super().__init__(expand=True)

        # 📦 deps
        # self.page = page
        self.root = root_layout
        self._service = service
        self._theme = theme

        # Atalhos para o tema
        self.gallery = self._theme.gallery

        # 📦 estado
        self.supers = self._service.listar_supers()

        self.logos = logos_row(logo_detic, logo_unicamp)
        self.placeholders = placeholders_row(
            show_placeholder_left,
            show_placeholder_right,
        )

        # 📦 placeholders de estrutura (serão preenchidos no apply_theme)
        self.gallery_row = None
        self.scroll_controller = None

        # 🧠 build inicial
        # self._build_static()

        # Background da page
        self.bgcolor = self._theme.base.background

    # =========================================================
    # 🎨 THEME
    # =========================================================

    def _apply_theme(self, theme=None):
        # g = self._theme.gallery

        # 🎯 background sempre aqui
        self.bgcolor = self._theme.base.background

        # 🎯 atualiza estrutura dependente de tema
        self.gallery_row = GalleryRow(
            supers=self.supers,
            card_width=self.gallery.card_width,
            spacing=self.gallery.h_spacing,
            padding=self.gallery.v_spacing,
            on_card_click=self._abrir_super,
            theme=self._theme,
        )

        self.scroll_controller = GalleryScrollController(
            row=self.gallery_row.row,
            visible_cards=self.gallery.visible_cards,
            card_width=self.gallery.card_width,
            spacing=self.gallery.h_spacing,
            padding=self.gallery.padding,
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

        return ft.Column(
            expand=True,
            controls=[
                self._text(
                    "Galeria de Superintendentes",
                    variant="h1",
                    weight=self._theme.typography.weight_bold,
                ),
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
                on_click=lambda _: self.page.run_task(self.scroll_controller.next),
                key="gallery_next",
            ),
            width=self.scroll_controller.group_width() + 2 * self.gallery.padding,
            alignment=ft.Alignment.CENTER_RIGHT,
        )

    def _gallery_height(self):
        # g = self._theme.gallery
        return self.gallery.card_height + self.gallery.v_spacing

    # =========================================================
    # 🔁 INTERAÇÕES
    # =========================================================

    def _abrir_super(self, super_data):
        if not self._service.pode_abrir(super_data):
            return

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

        # ✅ aplica tema agora (seguro)
        self._apply_theme(self._theme.theme)

        # ✅ só agora começa a ouvir mudanças
        self._theme.subscribe(self._apply_theme)

    def will_unmount(self):
        self._mounted = False
        self._theme.unsubscribe(self._apply_theme)
