# galeria/ui/components/timeline/view/timeline_renderer.py

import flet as ft
import flet.canvas as cv


class TimelineRenderer:
    def __init__(self, style):
        self.style = style

    def render(self, pts, curve, progress, active_idx):
        if not curve or len(curve) < 2:
            return []

        n = min(len(curve), max(1, int(len(curve) * progress)))
        visible = curve[:n]

        shapes = []
        shapes += self._line(visible)
        shapes += self._points(pts, active_idx)
        shapes += self._cursor(visible)

        # print("PTS SAMPLE:", pts[:3])
        # print("CURVE SAMPLE:", curve[:3])
        # print("PTS LEN:", len(pts))
        # print("CURVE LEN:", len(curve))

        return shapes

    def _line(self, curve):
        return [
            cv.Path(
                [cv.Path.MoveTo(*curve[0]), *[cv.Path.LineTo(x, y) for x, y in curve[1:]]],
                paint=ft.Paint(
                    color=self.style.line_color,
                    stroke_width=self.style.line_width,
                    style=ft.PaintingStyle.STROKE,
                ),
            )
        ]

    def _points(self, pts, active_idx):
        shapes = []

        for i, p in enumerate(pts):
            color = self.style.point_active_color if i == active_idx else self.style.point_color

            shapes.append(
                cv.Circle(
                    x=p[0],
                    y=p[1],
                    radius=self.style.point_radius,
                    paint=ft.Paint(color=color),
                )
            )

        return shapes

    def _cursor(self, curve):
        if not curve:
            return []

        x, y = curve[-1]

        return [
            cv.Circle(
                x=x,
                y=y,
                radius=self.style.cursor_radius,
                paint=ft.Paint(color=self.style.cursor_color),
            )
        ]
