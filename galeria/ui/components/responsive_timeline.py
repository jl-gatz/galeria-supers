# ui/components/responsive_timeline.py

from typing import override

import flet as ft


class ResponsiveTimeline(ft.Container):
    def __init__(self, image_src, points, on_select, height=260):
        super().__init__(expand=True, height=height)

        self._points = points
        self._on_select = on_select
        self._image_src = image_src

        self.content = ft.Stack(expand=True)

        self._image = ft.Image(
            src=str(image_src) if image_src else "images/placeholder.png",
            fit=ft.BoxFit.CONTAIN,
            expand=True,
        )

        self.content.controls.append(self._image)

    @override
    def did_mount(self):
        self.page.on_resize = self._handle_resize
        self._rebuild()

    def _handle_resize(self, e):
        self._rebuild()

    def _rebuild(self):
        stack = self.content
        stack.controls = [self._image]

        width = self.width or self.page.width
        height = self.height

        for idx, point in enumerate(self._points):
            px = point["x"] * width
            py = point["y"] * height

            stack.controls.append(
                ft.Container(
                    left=px - 20,
                    top=py - 20,
                    width=40,
                    height=40,
                    border_radius=20,
                    bgcolor=ft.Colors.TRANSPARENT,
                    on_click=lambda e, i=idx: self._on_select(i),
                )
            )

        self.update()
