from collections.abc import Callable
from pathlib import Path
from typing import override

import flet as ft

from galeria.core import (
    ANIMATE_OPACITY,
    AUTO_TIME_VIEW_BACK,
)
from galeria.domain import Super
from galeria.ui.behaviors.auto_close_behavior import AutoCloseBehavior
from galeria.ui.components import ResponsiveTimeline, SuperHeader
from galeria.ui.controllers.super_detail_controller import SuperDetailController


class SuperDetail(ft.Container):
    def __init__(
        self,
        super_data: Super,
        image_path: Path,
        timeline_path: Path,
        on_request_close: Callable[[], None],
    ):
        self._super = super_data
        self._image_path = image_path
        self._timeline_path = timeline_path
        self._on_request_close = on_request_close

        # 🧠 Controller
        self.controller = SuperDetailController(self._super)

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

        # Cabeçalho
        self.header = SuperHeader(
            image_src=str(self._image_path),
            nome=self._super.nome,
            texto_inicial=self.controller.current,
            expand=True,
        )

        # Timeline
        self.timeline = ResponsiveTimeline(
            image_src=str(self._timeline_path),
            points=self._super.timeline_points or [],
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
                    self.timeline,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=40,
                        controls=[
                            ft.Button("Anterior", on_click=self.prev),
                            ft.Button("Próximo", on_click=self.next),
                        ],
                    ),
                    ft.OutlinedButton(
                        "Voltar",
                        on_click=self._handle_voltar,
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
