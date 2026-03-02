import asyncio
from collections.abc import Callable
from pathlib import Path

import flet as ft
from domain.models import Super

from galeria.core.config import (
    ANIMATE_OPACITY,
    AUTO_TIME_VIEW_BACK,
    FADE_OUT_ASYNC_SLEEP,
)
from galeria.ui.controllers.AutoTimeoutController import AutoTimeoutController


class SuperDetail(ft.Container):
    def __init__(
        self,
        super_data: Super,
        image_path: Path,
        on_request_close: Callable[[], None],
    ):
        self._super = super_data
        self._image_path = image_path
        self._on_request_close = on_request_close
        self.timeout = None

        self._slide_index = 0

        self._texto = ft.Text(
            value=self._super.historias[self._slide_index],
            size=24,
            text_align=ft.TextAlign.CENTER,
            width=800,
        )

        self.timeout = AutoTimeoutController(
            seconds=AUTO_TIME_VIEW_BACK, on_timeout=self._timeout_close
        )

        content = ft.Column(
            controls=[
                ft.Image(
                    src=str(self._image_path),
                    width=300,
                    border_radius=20,
                ),
                ft.Text(
                    self._super.nome,
                    size=32,
                    weight=ft.FontWeight.BOLD,
                ),
                self._texto,
                ft.Row(
                    controls=[
                        ft.Button("Anterior", on_click=self._anterior),
                        ft.Button("Próximo", on_click=self._proximo),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.TextButton("Voltar", on_click=self._handle_voltar),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

        super().__init__(
            content=content,
            padding=40,
            border_radius=20,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                blur_radius=20,
                spread_radius=2,
                color=ft.Colors.BLACK_26,
            ),
            opacity=0,
            animate_opacity=ANIMATE_OPACITY,
            expand=True,
            alignment=ft.Alignment.CENTER,
        )

    # -------------------------
    # Navegação interna
    # -------------------------

    def _proximo(self, e: ft.ControlEvent) -> None:
        if self._slide_index < len(self._super.historias) - 1:
            self._slide_index += 1
            self._texto.value = self._super.historias[self._slide_index]
            self.update()

    def _anterior(self, e: ft.ControlEvent) -> None:
        if self._slide_index > 0:
            self._slide_index -= 1
            self._texto.value = self._super.historias[self._slide_index]
            self.update()

    # -------------------------
    # Animações
    # -------------------------

    def fade_in(self) -> None:
        self.timeout.start()
        self.opacity = 0
        self.update()

        self.opacity = 1
        self.update()

    def fade_out(self) -> None:
        self.timeout.cancel()

        self.opacity = 0
        self.update()

    # -------------------------
    # Fechamento
    # -------------------------

    def _handle_voltar(self, e: ft.ControlEvent) -> None:
        self.page.run_task(self._close_sequence)

    async def _close_sequence(self) -> None:
        self.fade_out()
        await asyncio.sleep(FADE_OUT_ASYNC_SLEEP)  # igual ao animate_opacity (0.3)
        self._on_request_close()

    def _wrap_interaction(self, handler):
        def wrapped(e):
            self.timeout.restart()
            return handler(e)

        return wrapped

    def _timeout_close(self):
        # Executa a sequência de fechamento de forma assíncrona
        self.page.run_task(self._close_sequence)
