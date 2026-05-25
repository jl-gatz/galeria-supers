# galeria/ui/theme/manager.py

from collections.abc import Callable

from galeria.ui.theme.themes import theme_for_era


class StaticThemeManager:
    def __init__(self, theme):
        self._theme = theme

    @property
    def theme(self):
        return self._theme

    def subscribe(self, listener: Callable):
        return None

    def unsubscribe(self, listener: Callable):
        return None

    def __getattr__(self, item):
        return getattr(self._theme, item)


class ThemeManager:
    def __init__(self, initial_theme):
        self._theme = initial_theme
        self._listeners: list[Callable] = []

    # ==========================================================
    # 🎨 CURRENT THEME
    # ==========================================================

    @property
    def theme(self):
        return self._theme

    # 👉 Proxy direto (ESSENCIAL)
    @property
    def accent(self):
        return self._theme.accent

    @property
    def gallery(self):
        return self._theme.gallery

    @property
    def header(self):
        return self._theme.header

    @property
    def image(self):
        return self._theme.image

    @property
    def logo(self):
        return self._theme.logo

    @property
    def super_detail(self):
        return self._theme.super_detail

    @property
    def button(self):
        return self._theme.button

    @property
    def colors(self):
        return self._theme.colors

    @property
    def spacing(self):
        return self._theme.spacing

    @property
    def styles(self):
        return self._theme.styles

    @property
    def radius(self):
        return self._theme.radius

    @property
    def typography(self):
        return self._theme.typography

    @property
    def text(self):
        return self._theme.text

    @property
    def timeline(self):
        return self._theme.timeline

    @property
    def ui(self):
        return self._theme.ui

    # ==========================================================
    # 🔄 THEME SWITCH
    # ==========================================================

    def set_theme(self, theme):
        # 🚫 Evita re-render desnecessário
        if theme is self._theme:
            return

        self._theme = theme

        for listener in self._listeners:
            listener(theme)

    def set_theme_for_era(self, era_id: str | None):
        theme = theme_for_era(era_id, fallback=self._theme)
        self.set_theme(theme)

    def get_theme_for_era(self, era_id: str | None):
        return theme_for_era(era_id, fallback=self._theme)

    # ==========================================================
    # 📡 OBSERVERS
    # ==========================================================

    def subscribe(self, listener: Callable):
        if listener not in self._listeners:
            self._listeners.append(listener)

    def unsubscribe(self, listener: Callable):
        if listener in self._listeners:
            self._listeners.remove(listener)

    # 🔥 MÁGICA AQUI
    def __getattr__(self, item):
        return getattr(self._theme, item)
