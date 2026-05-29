from typing import Protocol, cast

import pytest

from galeria.ui.components.super_header import SuperHeader
from galeria.ui.theme.models import AccentColors, TextColors, Theme
from tests.stubs.fake_theme import FakeTheme
from tests.stubs.fake_theme_manager import FakeThemeManager
from tests.stubs.theme import FakeAccentTheme, FakeTextTheme, FakeTypographyTheme


class SuperHeaderTypographyLike(Protocol):
    font_family: str
    h2: int
    body: int
    super_header_title_size: int
    super_header_body_size: int
    super_header_title_font_family: str
    super_header_body_font_family: str
    super_header_body_line_height: float


class SuperHeaderThemeLike(Protocol):
    text: TextColors
    accent: AccentColors
    typography: SuperHeaderTypographyLike


@pytest.fixture
def super_header_theme() -> SuperHeaderThemeLike:
    theme = FakeTheme()
    typography = FakeTypographyTheme()
    object.__setattr__(theme, "text", FakeTextTheme(primary="#101010", secondary="#505050"))
    object.__setattr__(theme, "accent", FakeAccentTheme(primary="#ff0000"))
    object.__setattr__(typography, "super_header_title_size", 34)
    object.__setattr__(typography, "super_header_body_size", 18)
    object.__setattr__(typography, "super_header_title_font_family", "TitleFont")
    object.__setattr__(typography, "super_header_body_font_family", "BodyFont")
    object.__setattr__(typography, "super_header_body_line_height", 1.45)
    object.__setattr__(theme, "typography", typography)

    return cast(SuperHeaderThemeLike, theme)


@pytest.fixture
def super_header_manager(super_header_theme: SuperHeaderThemeLike) -> FakeThemeManager:
    return FakeThemeManager(cast(Theme, super_header_theme))


@pytest.fixture
def super_header(super_header_manager: FakeThemeManager) -> SuperHeader:
    return SuperHeader(
        theme_manager=super_header_manager,
        image_src="tests/assets/test_image.png",
        nome="Ada",
        texto_inicial="Primeiro parágrafo.\n\nSegundo parágrafo.",
    )
