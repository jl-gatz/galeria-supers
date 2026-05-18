# tests/stubs/fake_theme.py

from tests.stubs.control.fake_header import FakeHeader
from tests.stubs.theme import (
    FakeBaseTheme,
    FakeColorsTheme,
    FakeGalleryTheme,
    FakeImageTheme,
    FakeLogoTheme,
    FakeRadiusTheme,
    FakeSpacingTheme,
    FakeTextTheme,
    FakeTypographyTheme,
    FakeUITheme,
)
from tests.stubs.theme.fake_accent_theme import FakeAccentTheme
from galeria.ui.theme.styles import default_component_styles


class FakeTheme:
    def __init__(self):
        self.base = FakeBaseTheme()

        self.gallery = FakeGalleryTheme()
        self.image = FakeImageTheme()
        self.logo = FakeLogoTheme()

        self.id = "fake"
        self.title = "Fake Theme"
        self.radius = FakeRadiusTheme()
        self.styles = default_component_styles()
        self.spacing = FakeSpacingTheme()
        self.colors = FakeColorsTheme()
        self.accent = FakeAccentTheme()
        self.typography = FakeTypographyTheme()
        self.text = FakeTextTheme()

        # placeholders temporários
        self.ui = FakeUITheme()
        self.header = FakeHeader()
        self.super_detail = object()
