# galeria/ui/components/timeline/view/timeline_style.py
"""Tokens visuais usados pelo renderer da timeline."""

import flet as ft

from galeria.ui.theme.models import Theme


class TimelineStyle:
    """Agrupa cores, raios e offsets aplicados ao desenho da timeline."""

    def __init__(self, theme: Theme | None = None):
        self.line_color = ft.Colors.RED_400
        self.glow_color = ft.Colors.WHITE
        self.point_color = ft.Colors.BLUE_400
        self.point_clicked_color = ft.Colors.BLUE_200
        self.point_active_color = ft.Colors.RED_400
        self.point_selected_color = ft.Colors.WHITE
        self.cursor_color = ft.Colors.RED_400

        self.line_width = 8
        self.glow_width = 1

        self.point_radius = 6
        self.point_clicked_radius = 8
        self.point_selected_radius = 12
        self.cursor_radius = 10
        self.year_font_size = 12
        self.year_color = "#FFFFFFB3"
        self.year_active_color = ft.Colors.WHITE
        self.year_visited_color = ft.Colors.BLUE_100
        self.year_selected_color = ft.Colors.WHITE
        self.year_offset_x = 10
        self.year_offset_y = 14

        if theme:
            self.apply_theme(theme)

    def apply_theme(self, theme: Theme) -> None:
        """Atualiza tokens visuais a partir do tema ativo."""
        timeline = getattr(theme, "timeline", None)

        self.line_color = getattr(timeline, "line", theme.accent.primary)
        self.point_color = getattr(timeline, "point", theme.text.secondary)
        self.point_clicked_color = theme.accent.secondary
        self.point_active_color = getattr(timeline, "point_active", theme.accent.primary)
        self.point_selected_color = theme.accent.primary
        self.cursor_color = self.point_active_color
        self.year_color = theme.text.secondary
        self.year_active_color = theme.text.primary
        self.year_visited_color = theme.accent.secondary
        self.year_selected_color = theme.accent.primary
