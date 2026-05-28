# tests/stubs/fake_theme.py

from typing import cast, override

from galeria.domain.protocols.theme_like import ThemeLike
from galeria.ui.theme.models import Theme
from galeria.ui.theme.styles import default_component_styles
from tests.stubs.theme import (
    FakeBaseTheme,
    FakeButtonTheme,
    FakeColorsTheme,
    FakeGalleryTheme,
    FakeHeaderTheme,
    FakeImageTheme,
    FakeLogoTheme,
    FakeRadiusTheme,
    FakeSpacingTheme,
    FakeSuperDetailTheme,
    FakeTextTheme,
    FakeTimelineTheme,
    FakeTypographyTheme,
    FakeUITheme,
)
from tests.stubs.theme.fake_accent_theme import FakeAccentTheme


class FakeTheme(Theme):
    _colors: FakeColorsTheme

    def __init__(self) -> None:
        super().__init__(
            id="fake",
            title="Fake Theme",
            base=FakeBaseTheme(),
            overlay="rgba(0,0,0,0.4)",
            text=FakeTextTheme(),
            accent=FakeAccentTheme(),
            ui=FakeUITheme(),
            button=FakeButtonTheme(),
            timeline=FakeTimelineTheme(),
            image=FakeImageTheme(),
            logo=FakeLogoTheme(),
            typography=FakeTypographyTheme(),
            spacing=FakeSpacingTheme(),
            radius=FakeRadiusTheme(),
            styles=default_component_styles(),
            gallery=FakeGalleryTheme(),
            header=FakeHeaderTheme(),
            super_detail=FakeSuperDetailTheme(),
        )
        self._colors = FakeColorsTheme()

    @property
    def colors(self) -> ThemeLike:
        return cast(ThemeLike, self._colors)

    @override
    def __setattr__(self, name: str, value: object) -> None:
        object.__setattr__(self, name, value)
