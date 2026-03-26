# ui/components/responsive_timeline.py

import flet as ft


class ResponsiveTimeline(ft.Stack):
    def __init__(
        self,
        image_src: str | None,
        points: list[dict],
        on_select: ft.Control,
        width: int = 1200,
        height: int = 260,
    ):
        super().__init__(width=width, height=height)

        self._points = points
        self._on_select = on_select
        self._width = width
        self._height = height

        timeline_img = ft.Image(
            src=str(image_src) if image_src else "images/placeholder.png",
            width=width,
            height=height,
            fit=ft.BoxFit.CONTAIN,
        )

        self.controls = [timeline_img]
        self.controls += self._build_hotspots()

    def _build_hotspots(self):

        hotspots = []

        for idx, point in enumerate(self._points):
            px = point["x"] * self._width
            py = point["y"] * self._height

            hotspots.append(
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

        return hotspots
