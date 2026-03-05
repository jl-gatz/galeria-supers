from pathlib import Path

import flet as ft

from galeria.infrastructure.repositories.super_repository import Super, SuperRepository
from galeria.ui.components.gallery_row import GalleryRow
from galeria.ui.components.navigation_arrow import right_arrow
from galeria.ui.components.super_view import SuperDetail
from galeria.ui.controllers.GalleryScrollController import GalleryScrollController
from galeria.ui.layout.root_layout import RootLayout
from galeria.ui.theme.typography import heading_h1


class GalleryView(ft.Container):
    CARD_WIDTH = 275
    CARD_HEIGHT = 360
    VISIBLE_CARDS = 5
    SPACING = 60
    MAX_WIDTH = 1800
    PADDING = 20

    def __init__(
        self,
        page: ft.Page,
        root_layout: RootLayout,
        logo1_src: str = "images/logos/logo-detic-4x.png",
        logo2_src: str = "images/logos/Logo_Unicamp__0.png",
        show_placeholders: bool = False,
    ):
        super().__init__(expand=True)

        self.root = root_layout
        self.repo = SuperRepository()
        self.supers = self.repo.listar()

        # Galeria rolável
        self.gallery_row = GalleryRow(
            supers=self.supers,
            card_width=self.CARD_WIDTH,
            spacing=self.SPACING,
            on_card_click=self.abrir_super,
        )

        self.scroll_controller = GalleryScrollController(
            row=self.gallery_row,
            visible_cards=self.VISIBLE_CARDS,
            card_width=self.CARD_WIDTH,
            spacing=self.SPACING,
            padding=self.PADDING,  # opcional, se o controlador precisar
        )

        # Container que envolve a galeria (sem padding extra por enquanto)
        cards_container = ft.Container(
            width=self._calculate_visible_width(),
            height=self.CARD_HEIGHT,
            content=self.gallery_row,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )

        # Stack para sobrepor o fade
        gallery_stack = ft.Stack(
            [
                cards_container,
                # right_fade(),  # descomente se necessário
            ],
            width=self._calculate_visible_width() + 2 * self.PADDING,
            height=self.CARD_HEIGHT,
        )

        # Seta de navegação (abaixo da galeria)
        arrow_container = ft.Container(
            content=right_arrow(on_click=lambda _: self.page.run_task(self.scroll_controller.next)),
            alignment=ft.Alignment.CENTER,
            margin=ft.margin.only(top=20),
        )

        # Linha com os dois logotipos (alinhados à direita)
        logos_row = ft.Container(
            content=ft.Row(
                [
                    ft.Image(src=logo1_src, height=120, fit=ft.BoxFit.CONTAIN),
                    ft.Image(src=logo2_src, height=120, fit=ft.BoxFit.CONTAIN),
                ],
                alignment=ft.MainAxisAlignment.END,
                spacing=20,
            ),
            margin=ft.margin.only(top=20, bottom=10),
        )

        # Placeholders esquerdo e direito (decorativos, podem ser desligados)
        self.left_placeholder = ft.Container(
            width=80,
            height=80,
            bgcolor=ft.Colors.GREY_300 if show_placeholders else None,
            visible=show_placeholders,
            border_radius=10,
            content=ft.Text("L", color=ft.Colors.GREY_700) if show_placeholders else None,
        )
        self.right_placeholder = ft.Container(
            width=80,
            height=80,
            bgcolor=ft.Colors.GREY_300 if show_placeholders else None,
            visible=show_placeholders,
            border_radius=10,
            content=ft.Text("R", color=ft.Colors.GREY_700) if show_placeholders else None,
        )

        # Linha inferior com placeholders (um à esquerda, um à direita)
        placeholders_row = ft.Container(
            content=ft.Row(
                [
                    self.left_placeholder,
                    ft.Container(expand=True),  # espaçador flexível
                    self.right_placeholder,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            visible=show_placeholders,
            margin=ft.margin.only(top=20),
        )

        # Layout principal (coluna)
        layout = ft.Column(
            [
                heading_h1("Galeria de Superintendentes"),
                gallery_stack,
                arrow_container,
                logos_row,
                placeholders_row,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=60,
        )

        # Container final que define a largura máxima e centraliza tudo
        self.content = ft.Container(
            content=layout,
            width=self.MAX_WIDTH,
            alignment=ft.Alignment.TOP_CENTER,
            padding=self.PADDING,
        )

    def _calculate_visible_width(self):
        return self.VISIBLE_CARDS * self.CARD_WIDTH + (self.VISIBLE_CARDS - 1) * self.SPACING

    def abrir_super(self, super_data: Super):
        detail = SuperDetail(
            super_data=super_data,
            image_path=Path(f"images/supers/{super_data.foto}"),
            on_request_close=lambda: self.root.hide_overlay(detail),
        )
        self.root.show_overlay(detail)
        detail.fade_in()
