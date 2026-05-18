# galeria/ui/components/timeline/view/timeline_style.py

import flet as ft


class TimelineStyle:
    def __init__(self, theme=None):
        self.line_color = ft.Colors.RED_400
        self.glow_color = ft.Colors.WHITE
        self.point_color = ft.Colors.BLUE_400
        self.point_active_color = ft.Colors.RED_400
        self.cursor_color = ft.Colors.RED_400

        self.line_width = 8
        self.glow_width = 1

        self.point_radius = 6
        self.cursor_radius = 10

        if theme:
            self.apply_theme(theme)

    def apply_theme(self, theme):
        timeline = getattr(theme, "timeline", None)

        self.line_color = getattr(timeline, "line", theme.accent.primary)
        self.point_color = getattr(timeline, "point", theme.text.secondary)
        self.point_active_color = getattr(timeline, "point_active", theme.accent.primary)
        self.cursor_color = self.point_active_color
