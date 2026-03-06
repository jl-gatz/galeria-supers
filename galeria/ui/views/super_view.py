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
from galeria.ui.controllers.auto_time_controller import AutoTimeoutController
from galeria.ui.theme.typography import heading_h2


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

        self.timeout.start()

        content = ft.Column(
            controls=[
                ft.GestureDetector(
                    on_tap_down=self._handle_user_activity,
                    content=ft.Column(
                        controls=[
                            ft.Image(
                                src=str(self._image_path),
                                width=300,
                                border_radius=20,
                            ),
                            heading_h2(
                                self._super.nome,
                            ),
                            self._texto,
                            ft.Row(
                                controls=[
                                    ft.Button(
                                        "Anterior",
                                        on_click=lambda e: (
                                            self._handle_user_activity(),
                                            self._anterior(e),
                                        ),
                                    ),
                                    ft.Button(
                                        "Próximo",
                                        on_click=lambda e: (
                                            self._handle_user_activity(),
                                            self._proximo(e),
                                        ),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.TextButton(
                                "Voltar",
                                on_click=lambda e: (
                                    self._handle_user_activity(),
                                    self._handle_voltar(e),
                                ),
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                    ),
                )
            ],
        )

        super().__init__(
            expand=True,
            alignment=ft.Alignment.CENTER,
            opacity=0,
            animate_opacity=ANIMATE_OPACITY,
            content=ft.GestureDetector(
                on_tap_down=self._handle_user_activity,
                # behavior=ft.HitTestBehavior.TRANSLUCENT,
                content=ft.Container(
                    content=content,  # sua Column interna
                    padding=40,
                    border_radius=20,
                    bgcolor=ft.Colors.WHITE,
                    shadow=ft.BoxShadow(
                        blur_radius=20,
                        spread_radius=2,
                        color=ft.Colors.BLACK_26,
                    ),
                ),
            ),
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

    # -------------------------
    # Fechamento
    # -------------------------

    def _handle_voltar(self, e: ft.ControlEvent) -> None:
        self.page.run_task(self._close_sequence)

    async def _close_sequence(self) -> None:
        self.fade_out()
        await asyncio.sleep(FADE_OUT_ASYNC_SLEEP)  # igual ao animate_opacity (0.3)
        self._on_request_close()

    def _handle_user_activity(self, e=None):
        self.timeout.restart()

    def _timeout_close(self):
        # Executa a sequência de fechamento de forma assíncrona
        self.page.run_task(self._close_sequence)
