# galeria/ui/views/gallery_view.py
"""Tela de galeria que apresenta a lista navegável de superintendentes."""

from pathlib import Path
from typing import Any, cast, override

import flet as ft

from galeria.core import LOGO_DETIC, LOGO_UNICAMP
from galeria.domain import Super
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
    """Visão principal da galeria para listar e abrir detalhes.

    A visão controla a linha de cards, mantém o tema ativo sincronizado com
    o card em foco e delega a apresentação de overlays ao layout raiz.
    """

    def __init__(
        self,
        page: ft.Page,
        service: GalleryServiceLike,
        root_layout: RootLayout | None,
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
        self.root: RootLayout | None = root_layout
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

        # 📦 estrutura dinâmica
        self.gallery_row: GalleryRow | None = None
        self.scroll_controller: GalleryScrollController | None = None
        self.title_text: ft.Text | None = None
        self.placeholders: ft.Container = placeholders_row(
            self._show_placeholder_left,
            self._show_placeholder_right,
            theme=self._theme.theme,
        )

        # 🎨 background inicial
        self.bgcolor = self._theme.base.background

        # ✅ build inicial da UI
        self._apply_theme(self._theme.theme)

    # =========================================================
    # 🎨 THEME
    # =========================================================

    def _apply_theme(self, theme: Any = None) -> None:
        """Aplica o tema atual sem reconstruir estado sensível ao scroll."""
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
        """Atualiza cores e tipografia em controles já existentes."""
        if self.title_text is None:
            return

        t = self._theme.typography
        self.title_text.value = self._theme.gallery.title
        self.title_text.size = t.h1
        self.title_text.font_family = t.font_family
        self.title_text.weight = cast(ft.FontWeight, t.weight_bold)
        self.title_text.color = self._theme.text.primary

    def _text(
        self,
        value: str,
        variant: str = "body",
        weight: str | ft.FontWeight | None = None,
        color: str | None = None,
        **kwargs: Any,
    ) -> ft.Text:
        """Cria texto temático usando a escala tipográfica da visão."""
        t = self._theme.typography

        return ft.Text(
            value,
            size=getattr(t, variant),
            font_family=t.font_family,
            weight=cast(ft.FontWeight, weight or t.weight_regular or t.weight_medium or t.weight_bold),
            color=color or self._theme.text.primary,
            **kwargs,
        )

    # =========================================================
    # 🧱 BUILDERS
    # =========================================================
    def _build_gallery(self) -> ft.Container:
        """Monta a área recortada que contém a galeria horizontal."""
        assert self.scroll_controller is not None
        assert self.gallery_row is not None

        return ft.Container(
            width=self.scroll_controller.group_width(),
            height=self._gallery_height(),
            content=self.gallery_row,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )

    def _build_main_column(self) -> ft.Column:
        """Monta o layout vertical principal da tela de galeria."""
        self.title_text = self._text(
            self._theme.gallery.title,
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

    def _build_fab(self) -> ft.Container:
        """Monta o controle flutuante que avança a galeria."""
        assert self.scroll_controller is not None

        def handle_click(_: ft.ControlEvent) -> None:
            assert self.scroll_controller is not None
            self._page.run_task(self.scroll_controller.next)

        return ft.Container(
            content=FloatingNavButton.forward(
                on_click=handle_click,
                key="gallery_next",
                theme_manager=self._theme,
            ),
            width=self.scroll_controller.group_width() + 2 * self.gallery.padding,
            alignment=ft.Alignment.CENTER_RIGHT,
        )

    def _gallery_height(self) -> int:
        """Retorna a altura fixa da galeria a partir dos tokens de tema."""
        return self.gallery.card_height + self.gallery.v_spacing

    def _set_active_super_index(self, index: int) -> None:
        """Atualiza o tema da aplicação a partir do superintendente em foco."""
        if not self.supers:
            return

        active_super = self.supers[max(0, min(len(self.supers) - 1, index))]
        self._theme.set_theme_for_era(getattr(active_super, "era_id", None))

    # =========================================================
    # 🔁 INTERAÇÕES
    # =========================================================

    def _abrir_super(self, super_data: Super) -> None:
        """Abre o overlay de detalhe de um superintendente quando permitido."""
        if not self._service.pode_abrir(super_data):
            return
        if self.root is None:
            raise RuntimeError("GalleryView requer RootLayout para abrir detalhes.")

        self._theme.set_theme_for_era(getattr(super_data, "era_id", None))
        controller = SuperDetailController(super_data)
        detail: SuperDetail
        root = self.root

        def handle_close() -> None:
            root.hide_overlay(detail)

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
    @override
    def did_mount(self) -> None:
        """Assina mudanças de tema depois que o Flet monta o controle."""
        self._mounted = True

        # ✅ ativa reatividade apenas após mount
        self._theme.subscribe(self._apply_theme)
        assert self.scroll_controller is not None
        self._set_active_super_index(self.scroll_controller.active_index_from_offset(0))

    @override
    def will_unmount(self) -> None:
        """Libera assinaturas de tema antes que o Flet remova o controle."""
        self._mounted = False
        self._theme.unsubscribe(self._apply_theme)
