from tests.stubs.fake_theme import FakeTheme


class FakeThemeManager:
    def __init__(self, theme: FakeTheme):
        self.theme = theme

    @property
    def gallery(self):
        return self.theme.gallery

    @property
    def header(self):
        return self.theme.header

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
    def radius(self):
        return self.theme.radius

    @property
    def typography(self):
        return self.theme.typography

    @property
    def text(self):
        return self.theme.text

    def set_theme(self, theme):
        self.theme = theme

    def subscribe(self, listener):
        pass

    def unsubscribe(self, listener):
        pass
