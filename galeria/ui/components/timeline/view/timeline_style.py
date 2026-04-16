# galeria/ui/components/timeline/view/timeline_style.py

import flet as ft


class TimelineStyle:
    def __init__(self):
        self.line_color = ft.Colors.RED_400
        self.glow_color = ft.Colors.WHITE
        self.cursor_color = ft.Colors.BLUE_400

        self.line_width = 8
        self.glow_width = 1

        self.point_radius = 6
        self.cursor_radius = 10
