# tests/stubs/fake_theme.py

from tests.stubs.control.fake_header import FakeHeader
from tests.stubs.theme import (
    FakeBaseTheme,
    FakeColorsTheme,
    FakeGalleryTheme,
    FakeRadiusTheme,
    FakeSpacingTheme,
    FakeTextTheme,
    FakeTypographyTheme,
    FakeUITheme,
)


class FakeTheme:
    def __init__(self):
        self.base = FakeBaseTheme()

        self.gallery = FakeGalleryTheme()

        self.radius = FakeRadiusTheme()
        self.spacing = FakeSpacingTheme()
        self.colors = FakeColorsTheme()
        self.typography = FakeTypographyTheme()
        self.text = FakeTextTheme()

        # placeholders temporários
        self.ui = FakeUITheme()
        self.header = FakeHeader()
        self.super_detail = object()
