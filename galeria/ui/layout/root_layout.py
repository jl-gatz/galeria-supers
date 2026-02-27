import asyncio

import flet as ft


class RootLayout(ft.Stack):
    def __init__(self, gallery_view: ft.Control):
        self.gallery = gallery_view

        self.backdrop = ft.Container(
            bgcolor=ft.Colors.BLACK54,
            opacity=0,
            animate_opacity=300,
            expand=True,
        )

        super().__init__(
            controls=[
                self.gallery,
                self.backdrop,
            ],
            expand=True,
        )

    def show_overlay(self, detail: ft.Control):
        self.backdrop.opacity = 0.6
        self.controls.append(detail)
        self.update()

    def hide_overlay(self, detail: ft.Control):
        detail.opacity = 0
        self.backdrop.opacity = 0
        self.update()

        async def remove():
            await asyncio.sleep(1)
            self.controls.remove(detail)
            self.update()

        self.page.run_task(remove)
