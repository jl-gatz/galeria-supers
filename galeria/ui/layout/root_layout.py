# ui/layout/root_layout.py

import asyncio

import flet as ft

from galeria.core.config import FADE_OUT_ASYNC_SLEEP


class RootLayout(ft.Stack):
    def __init__(self, gallery_view: ft.Control):
        self.gallery = gallery_view
        self._current_detail = None

        self.backdrop = ft.Container(
            bgcolor=ft.Colors.BLACK54,
            opacity=0,
            animate_opacity=300,
            expand=True,
            ignore_interactions=True,
        )

        super().__init__(
            controls=[
                self.gallery,
                self.backdrop,
            ],
            expand=True,
        )

    def show_overlay(self, detail: ft.Control):
        self._current_detail = detail
        self.backdrop.opacity = 0.6
        self.backdrop.ignore_interactions = False

        # DEBUG
        # print(f"[show_overlay] Adicionando detail ID: {id(detail)}")
        self.controls.append(detail)
        self.update()

    def hide_overlay(self, detail: ft.Control = None):
        # Se não passarem detail, usa o atual
        # detail = self._current_detail
        # DEBUG
        # print(f"[hide_overlay] Hide detail ID: {id(detail)}")

        detail.disabled = True
        self.backdrop.ignore_interactions = True
        self.backdrop.expand = False

        def on_animation_end(e):
            if detail in self.controls:
                self.controls.remove(detail)
                self.update()

        detail.on_animation_end = on_animation_end

        detail.opacity = 0
        self.backdrop.opacity = 0
        self.update()

        async def remove():
            await asyncio.sleep(FADE_OUT_ASYNC_SLEEP)
            if detail in self.controls:
                self.controls.remove(detail)
                if self._current_detail is detail:
                    self._current_detail = None
                self.update()

        self.page.run_task(remove)
