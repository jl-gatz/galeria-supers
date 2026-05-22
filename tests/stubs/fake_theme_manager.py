from galeria.ui.theme.themes import theme_for_era
from tests.stubs.fake_theme import FakeTheme


class FakeThemeManager:
    def __init__(self, theme: FakeTheme):
        self.theme = theme
        self._listeners = []
        self.era_requests = []

    @property
    def gallery(self):
        return self.theme.gallery

    @property
    def accent(self):
        return self.theme.accent

    @property
    def button(self):
        return getattr(self.theme, "button", None)

    @property
    def header(self):
        return self.theme.header

    @property
    def image(self):
        return self.theme.image

    @property
    def logo(self):
        return self.theme.logo

    @property
    def base(self):
        return self.theme.base

    @property
    def super_detail(self):
        return self.theme.super_detail

    @property
    def colors(self):
        return self.theme.colors

    @property
    def spacing(self):
        return self.theme.spacing

    @property
    def styles(self):
        return self.theme.styles

    @property
    def radius(self):
        return self.theme.radius

    @property
    def typography(self):
        return self.theme.typography

    @property
    def text(self):
        return self.theme.text

    @property
    def timeline(self):
        return getattr(self.theme, "timeline", None)

    @property
    def ui(self):
        return self.theme.ui

    def set_theme(self, theme):
        self.theme = theme
        for listener in self._listeners:
            listener(theme)

    def set_theme_for_era(self, era_id):
        self.era_requests.append(era_id)
        self.set_theme(theme_for_era(era_id, fallback=self.theme))

    def subscribe(self, listener):
        if listener not in self._listeners:
            self._listeners.append(listener)

    def unsubscribe(self, listener):
        if listener in self._listeners:
            self._listeners.remove(listener)
