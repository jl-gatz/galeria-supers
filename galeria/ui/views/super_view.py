from collections.abc import Callable
from pathlib import Path
from typing import override

import flet as ft

from galeria.core.config import (
    ANIMATE_OPACITY,
    AUTO_TIME_VIEW_BACK,
)
from galeria.domain.models import Super
from galeria.ui.components.responsive_timeline import ResponsiveTimeline
from galeria.ui.components.super_header import SuperHeader
from galeria.ui.controllers.auto_time_controller import AutoTimeoutController
from galeria.ui.controllers.slide_controller import SlideController


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

        # Desliga scroll no componente
        self.scroll = ft.ScrollMode.HIDDEN
        self.expand = True

        # Controller dos slides
        self.slides = SlideController(self._super.historias)  # Ajuste o nome do campo

        # Cabeçalho com imagem, título e texto rolável
        self.header = SuperHeader(
            image_src=str(self._image_path),
            nome=self._super.nome,
            texto_inicial=self.slides.current,  # string
            expand=True,
        )

        # Linha do tempo interativa
        self.timeline = ResponsiveTimeline(
            image_src=str(self._timeline_path),
            points=self._super.timeline_points or [],
            on_select=self._goto_slide,
        )

        # Timeout para retorno automático
        self.timeout = AutoTimeoutController(
            seconds=AUTO_TIME_VIEW_BACK,
            on_timeout=self._timeout_close,
        )

        self.timeout.start()

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
        self.timeout.start()

    # -------------------------
    # Animações
    # -------------------------
    def fade_in(self) -> None:
        self.opacity = 0
        self.update()

        self.opacity = 1
        self.update()
        # Inicia depois do fade -->
        self.timeout.start()

    def fade_out(self) -> None:
        # Cancela antes da aplicação do fade_out
        self.timeout.cancel()

        self.opacity = 0
        self.update()

    def _refresh_slide(self):
        """Atualiza o texto do slide atual."""
        if not getattr(self, "_mounted", False):
            return
        self.header.update_text(self.slides.current)

    def next(self, e=None):
        if self.slides.next():
            self._refresh_slide()

    def prev(self, e=None):
        if self.slides.prev():
            self._refresh_slide()

    def _goto_slide(self, index: int):
        self._handle_user_activity()
        if self.slides.goto(index):
            self._refresh_slide()

    def _handle_voltar(self, e):
        self._on_request_close()

    def _handle_user_activity(self, e=None):
        self.timeout.restart()

    def _timeout_close(self):
        self._on_request_close()

    @override
    def did_mount(self):
        self._mounted = True
