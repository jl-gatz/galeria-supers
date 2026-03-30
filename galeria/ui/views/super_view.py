from collections.abc import Callable
from typing import override

import flet as ft

from galeria.core import (
    ANIMATE_OPACITY,
    AUTO_TIME_VIEW_BACK,
)
from galeria.ui.behaviors.auto_close_behavior import AutoCloseBehavior
from galeria.ui.components import ResponsiveTimeline, SuperHeader
from galeria.ui.components.navigation_controls import NavigationControls
from galeria.ui.controllers.super_detail_controller import SuperDetailController
from galeria.ui.theme import PRIMARY_RED
from galeria.ui.theme.colors import RED_55


class SuperDetail(ft.Container):
    def __init__(
        self,
        controller: SuperDetailController,
        on_request_close: Callable[[], None],
    ):
        self._on_request_close = on_request_close

        # 🧠 Controller
        self.controller = controller

        # ⏱️ Timeout
        self.auto_close = AutoCloseBehavior(
            seconds=AUTO_TIME_VIEW_BACK,
            on_timeout=self._timeout_close,
        )

        # ⚠️ Mantido por compatibilidade (vamos remover depois)
        self.slides = self.controller._slides

        # Design scroll no componente
        self.scroll = ft.ScrollMode.HIDDEN
        self.expand = True

        # Timeline
        self.timeline = self.controller.timeline

        # Cabeçalho
        self.header = SuperHeader(
            image_src=self.controller.image_src,
            nome=self.controller.nome,
            texto_inicial=self.controller.current,
            expand=True,
        )

        # Navigation Row (setas à direita, abaixo do texto)
        self.navigation = NavigationControls(on_prev=self.prev, on_next=self.next)

        # Timeline view
        self.timeline_view = ResponsiveTimeline(
            image_src=self.timeline["image_src"],
            points=self.timeline["points"],
            on_select=self._goto_slide,
        )

        # Layout principal
        layout = ft.Container(
            padding=60,
            border_radius=20,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                blur_radius=20,
                spread_radius=2,
                color=ft.Colors.BLACK_26,
            ),
            content=ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=40,
                controls=[
                    self.header,
                    self.navigation,
                    # 👇 área da timeline com overlay
                    ft.Container(
                        expand=True,
                        content=ft.Stack(
                            expand=True,
                            controls=[
                                self.timeline_view,
                                ft.Container(
                                    content=ft.OutlinedButton(
                                        "Voltar",
                                        style=ft.ButtonStyle(
                                            color=PRIMARY_RED,
                                            bgcolor={
                                                ft.ControlState.HOVERED: RED_55,
                                            },
                                        ),
                                        on_click=self._handle_voltar,
                                    ),
                                    alignment=ft.Alignment.BOTTOM_RIGHT,
                                    padding=16,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

        super().__init__(
            expand=True,
            alignment=ft.Alignment.CENTER,
            opacity=0,
            animate_opacity=ANIMATE_OPACITY,
            content=ft.GestureDetector(
                on_tap_down=self._handle_user_activity,
                content=layout,
            ),
        )

        # 🔥 Mantém comportamento atual
        self.auto_close.start()

    # -------------------------
    # 🎬 Animações (mantidas)
    # -------------------------
    def fade_in(self) -> None:
        self.opacity = 0
        self.update()

        self.opacity = 1
        self.update()

        self.auto_close.start()

    def fade_out(self) -> None:
        self.auto_close.stop()
        self.opacity = 0
        self.update()

    # -------------------------
    # 🔄 Atualização de slide
    # -------------------------
    def _refresh_slide(self):
        if not getattr(self, "_mounted", False):
            return

        self.header.update_text(self.controller.current)

    # -------------------------
    # 🎯 Navegação
    # -------------------------
    def next(self, e=None):
        if self.controller.next():
            self._refresh_slide()

    def prev(self, e=None):
        if self.controller.prev():
            self._refresh_slide()

    def _goto_slide(self, index: int):
        self._handle_user_activity(None)
        if self.controller.goto(index):
            self._refresh_slide()

    # -------------------------
    # 🔙 Ações externas
    # -------------------------
    def _handle_voltar(self, e):
        self._on_request_close()

    def _handle_user_activity(self, e=None):
        self.auto_close.reset()

    def _timeout_close(self):
        self._on_request_close()

    # -------------------------
    # 🔁 Lifecycle
    # -------------------------
    @override
    def did_mount(self):
        self._mounted = True
