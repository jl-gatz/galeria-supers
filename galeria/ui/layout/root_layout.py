# ui/layout/root_layout.py

import asyncio

import flet as ft

from galeria.core.config import FADE_OUT_ASYNC_SLEEP
from galeria.debug.debug_panel import ThemeDebugPanel
from galeria.ui.theme.manager import ThemeManager


class RootLayout(ft.Container):
    def __init__(self, gallery_view: ft.Control, theme_manager: ThemeManager):
        self.gallery = gallery_view
        self.theme_manager = theme_manager
        self._current_detail = None

        # 🎭 Backdrop (overlay escuro)
        self.backdrop = ft.Container(
            bgcolor=self.theme_manager.theme.overlay,
            opacity=0,
            animate_opacity=300,
            expand=True,
            ignore_interactions=True,
        )

        # 🛠 Debug
        self.debug_panel = ThemeDebugPanel(self.theme_manager)

        # 🧱 Stack de camadas
        self.stack = ft.Stack(
            expand=True,
            controls=[
                self.gallery,  # base
                self.backdrop,  # overlay
                self.debug_panel,  # debug
            ],
        )

        # 🎨 subscribe theme
        self.theme_manager.subscribe(self.apply_theme)

        # 🧩 Container raiz (SUPERFÍCIE GLOBAL)
        super().__init__(
            expand=True,
            bgcolor=self.theme_manager.theme.base.background,
            content=self.stack,
        )

    # =========================================================
    # 🎨 THEME
    # =========================================================

    def apply_theme(self, theme=None):
        theme = theme or self.theme_manager.theme

        # 🎯 Fundo do layout
        self.bgcolor = theme.base.background

        # 🎯 Fundo do page
        if self.page:
            self.page.bgcolor = theme.base.background

        # 🎯 Backdrop (overlay)
        self.backdrop.bgcolor = theme.overlay

        if self.page:
            self.update()

    def did_mount(self):
        self.apply_theme()

        if self.page:
            self.page.bgcolor = self.theme_manager.theme.base.background

        self.page.on_keyboard_event = self._handle_key

    def will_unmount(self):
        self.theme_manager.unsubscribe(self.apply_theme)

    # =========================================================
    # 🎹 INPUT
    # =========================================================

    def _handle_key(self, e: ft.KeyboardEvent):
        if e.key == "D":
            self.debug_panel.visible = not self.debug_panel.visible
            self.update()

    # =========================================================
    # 🎭 OVERLAY CONTROL
    # =========================================================

    def show_overlay(self, detail: ft.Control):
        self._current_detail = detail

        # ativa backdrop
        self.backdrop.opacity = 1
        self.backdrop.ignore_interactions = False

        # adiciona overlay no topo
        self.stack.controls.append(detail)

        self.update()

    def hide_overlay(self, detail: ft.Control = None):
        detail = detail or self._current_detail

        if not detail:
            return

        detail.disabled = True

        # desativa backdrop
        self.backdrop.opacity = 0
        self.backdrop.ignore_interactions = True

        # fade out
        detail.opacity = 0
        self.update()

        async def remove():
            await asyncio.sleep(FADE_OUT_ASYNC_SLEEP)

            if detail in self.stack.controls:
                self.stack.controls.remove(detail)

            if self._current_detail is detail:
                self._current_detail = None

            self.update()

        self.page.run_task(remove)
