# galeria/ui/components/timeline/view/timeline_view.py


import math

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

        self._cached_curve = None
        self._last_size = None

        self._control = TimelineContainer(view=self, content=self.canvas.canvas, expand=True)

    def refresh(self):
        self._draw()

    def _draw(self):
        width = self.canvas.width
        height = self.canvas.height

        if not width or not height:
            return

        if math.isinf(width) or math.isinf(height):
            return

        pts = self._normalize_points(self.controller.model.points, width, height)

        curve = self._get_curve(pts, width, height)

        shapes = self.renderer.render(
            pts, curve, self.controller.progress, self.controller.active_index
        )

        self.canvas.set_shapes(shapes)

        # ✅ ponto único de atualização
        safe_update(self.control)

    def _on_resize(self, e):
        self._cached_curve = None
        self._last_size = None

        if self.canvas.width and self.canvas.height:
            self.refresh()

    def _normalize_points(self, points, width, height):
        """
        Converte pontos normalizados (0-1) para coordenadas do canvas.
        """

        if not points:
            return []

        result = []

        for p in points:
            try:
                x = float(p.x) * width
                y = float(p.y) * height

                if not (math.isfinite(x) and math.isfinite(y)):
                    continue

                result.append((x, y))

            except Exception:
                continue

        return result

    def _get_curve(self, pts, width, height):
        size = (width, height)

        if self._cached_curve is None or size != self._last_size:
            self._cached_curve = self.path_builder.build_path(pts)
            self._last_size = size

        return self._cached_curve

    @property
    def control(self):
        return self._control
