# galeria/ui/components/timeline/view/timeline_view.py


import math

import flet as ft

from galeria.ui.components.timeline.utils import (
    map_indexed_points_to_canvas,
    map_points_to_canvas,
)
from galeria.ui.components.timeline.view.timeline_canvas import TimelineCanvas
from galeria.ui.components.timeline.view.timeline_container import TimelineContainer
from galeria.ui.utils.flet_save import safe_update


class TimelineView:
    def __init__(self, controller, path_builder, renderer):
        self.controller = controller
        self.path_builder = path_builder
        self.renderer = renderer

        self.controller.bind_view(self)

        self.canvas = TimelineCanvas(on_resize=self._on_resize)
        self.hit_size = 32
        self._rendered_points = []
        self.canvas_background = ft.TransparentPointer(
            content=self.canvas.canvas,
            width=self.canvas.width,
            height=self.canvas.height,
        )
        self.canvas_stack = ft.Stack(
            expand=True,
            width=self.canvas.width,
            height=self.canvas.height,
            fit=ft.StackFit.EXPAND,
            controls=[self.canvas_background],
        )

        self._cached_curve = None
        self._last_size = None

        self._control = TimelineContainer(
            view=self,
            content=self.canvas_stack,
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.001, ft.Colors.WHITE),
            # on_click=lambda e: print(
            #     "TIMELINE WRAPPER CLICK:",
            #     f"event_type={type(e).__name__ if e else None}",
            #     f"event_data={getattr(e, 'data', None)}",
            #     f"control_data={getattr(getattr(e, 'control', None), 'data', None)}",
            # ),
        )

    def refresh(self):
        self._draw()

    def _draw(self):
        width = self.canvas.width
        height = self.canvas.height

        if not width or not height:
            return

        if math.isinf(width) or math.isinf(height):
            return

        self._rendered_points = map_indexed_points_to_canvas(
            self.controller.model.points,
            width,
            height,
        )
        pts = [(x, y) for _, x, y in self._rendered_points]

        curve = self._get_curve(pts, width, height)

        shapes = self.renderer.render(
            pts,
            curve,
            self.controller.progress,
            self.controller.active_index,
            self.controller.point_states(),
            points=self.controller.model.points,
        )

        self.canvas.set_shapes(shapes)
        self._rebuild_clickable_points()

        # ✅ ponto único de atualização
        safe_update(self.control)

    def _on_resize(self, e):
        self._cached_curve = None
        self._last_size = None

        if self.canvas.width and self.canvas.height:
            self.refresh()

    def _normalize_points(self, points, width, height):
        return map_points_to_canvas(points, width, height)

    def _rebuild_clickable_points(self):
        self.canvas_stack.width = self.canvas.width
        self.canvas_stack.height = self.canvas.height
        self.canvas_background.width = self.canvas.width
        self.canvas_background.height = self.canvas.height
        # print(
        #     "TIMELINE CLICK LAYER:",
        #     f"canvas=({self.canvas.width}x{self.canvas.height})",
        #     f"points={len(self._rendered_points)}",
        # )
        self.canvas_stack.controls = [
            self.canvas_background,
            *self._build_clickable_points(),
        ]

    def _build_clickable_points(self):
        controls = []
        radius = self.hit_size / 2

        for index, x, y in self._rendered_points:
            point = self.controller.model.points[index]
            left = x - radius
            top = y - radius

            # print(
            #     "TIMELINE CLICK TARGET:",
            #     f"id={point.id}",
            #     f"index={index}",
            #     f"x={x}",
            #     f"y={y}",
            #     f"left={left}",
            #     f"top={top}",
            #     f"size={self.hit_size}",
            # )
            def _on_point_click(e, point_id=point.id):
                # print(
                #     "TIMELINE CLICK EVENT:",
                #     f"id={point_id}",
                #     f"event_type={type(e).__name__ if e else None}",
                #     f"event_data={getattr(e, 'data', None)}",
                #     f"control_data={getattr(getattr(e, 'control', None), 'data', None)}",
                # )
                self._handle_point_click(point_id, e)

            controls.append(
                ft.Container(
                    left=left,
                    top=top,
                    width=self.hit_size,
                    height=self.hit_size,
                    border_radius=radius,
                    bgcolor=ft.Colors.with_opacity(0.001, ft.Colors.WHITE),
                    ink=True,
                    data={"type": "timeline_point", "id": point.id},
                    on_click=_on_point_click,
                    # on_hover=lambda e, point_id=point.id: print(
                    #     "TIMELINE HOVER TARGET:",
                    #     point_id,
                    #     getattr(e, "data", None),
                    # ),
                )
            )

        return controls

    def _handle_point_click(self, point_id: str, e=None):
        # print(
        #     "TIMELINE HANDLE CLICK:",
        #     f"id={point_id}",
        #     f"event_type={type(e).__name__ if e else None}",
        # )
        _point = self.controller.select_point(point_id)
        # print(
        #     "TIMELINE SELECT RESULT:",
        #     f"point_found={_point is not None}",
        #     f"selected={self.controller.selected_point_id}",
        #     f"clicked={sorted(self.controller.clicked_point_ids)}",
        # )
        self._rebuild()

    def _rebuild(self):
        self.refresh()

    def _get_curve(self, pts, width, height):
        size = (width, height)

        if self._cached_curve is None or size != self._last_size:
            self._cached_curve = self.path_builder.build_path(pts)
            self._last_size = size

        return self._cached_curve

    @property
    def control(self):
        return self._control
