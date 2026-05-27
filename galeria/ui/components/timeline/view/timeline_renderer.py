# galeria/ui/components/timeline/view/timeline_renderer.py

import flet as ft
import flet.canvas as cv


class TimelineRenderer:
    def __init__(self, style):
        self.style = style

    def render(self, pts, curve, progress, active_idx, point_states=None, points=None):
        if not curve or len(curve) < 2:
            return []

        n = min(len(curve), max(1, int(len(curve) * progress)))
        visible = curve[:n]

        shapes = []
        shapes += self._line(visible)
        shapes += self._points(pts, active_idx, point_states or {})
        shapes += self._years(pts, points or [], active_idx, point_states or {})
        shapes += self._cursor(visible)

        # print("PTS SAMPLE:", pts[:3])
        # print("CURVE SAMPLE:", curve[:3])
        # print("PTS LEN:", len(pts))
        # print("CURVE LEN:", len(curve))

        return shapes

    def _years(self, pts, points, active_idx, point_states):
        shapes = []

        for i, p in enumerate(pts):
            if i >= len(points):
                continue

            year = getattr(points[i], "year", None)
            if year is None:
                continue

            color = self.style.year_color
            weight = ft.FontWeight.NORMAL

            if i == active_idx:
                color = self.style.year_active_color
                weight = ft.FontWeight.BOLD

            state = point_states.get(i)
            if state == "clicked":
                color = self.style.year_visited_color
                weight = ft.FontWeight.W_500

            if state == "selected":
                color = self.style.year_selected_color
                weight = ft.FontWeight.BOLD

            shapes.append(
                cv.Text(
                    x=p[0] + self.style.year_offset_x,
                    y=p[1] + self.style.year_offset_y,
                    value=str(year),
                    style=ft.TextStyle(
                        size=self.style.year_font_size,
                        color=color,
                        weight=weight,
                    ),
                )
            )

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

    def _points(self, pts, active_idx, point_states):
        shapes = []

        for i, p in enumerate(pts):
            color = self.style.point_color
            radius = self.style.point_radius

            if i == active_idx:
                color = self.style.point_active_color

            state = point_states.get(i)
            if state == "clicked":
                color = self.style.point_clicked_color
                radius = self.style.point_clicked_radius

            if state == "selected":
                color = self.style.point_selected_color
                radius = self.style.point_selected_radius

            shapes.append(
                cv.Circle(
                    x=p[0],
                    y=p[1],
                    radius=radius,
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
