# galeria/ui/theme/manager.py

from collections.abc import Callable

from .models import Theme


class ThemeManager:
    def __init__(self, initial_theme: Theme):
        self._theme = initial_theme
        self._listeners: list[Callable[[Theme], None]] = []

    @property
    def theme(self) -> Theme:
        return self._theme

    def set_theme(self, theme: Theme):
        # print("SET_THEME:", theme.title, id(theme))
        self._theme = theme
        for listener in self._listeners:
            listener(theme)

    def subscribe(self, listener: Callable[[Theme], None]):
        self._listeners.append(listener)
