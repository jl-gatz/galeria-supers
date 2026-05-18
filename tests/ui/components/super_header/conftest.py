import pytest

from galeria.ui.components.super_header import SuperHeader
from tests.stubs.fake_theme import FakeTheme
from tests.stubs.fake_theme_manager import FakeThemeManager


@pytest.fixture
def super_header_theme():
    theme = FakeTheme()
    theme.text.primary = "#101010"
    theme.text.secondary = "#505050"
    theme.accent.primary = "#ff0000"

    theme.typography.super_header_title_size = 34
    theme.typography.super_header_body_size = 18
    theme.typography.super_header_title_font_family = "TitleFont"
    theme.typography.super_header_body_font_family = "BodyFont"
    theme.typography.super_header_body_line_height = 1.45

    return theme


@pytest.fixture
def super_header_manager(super_header_theme):
    return FakeThemeManager(super_header_theme)


@pytest.fixture
def super_header(super_header_manager):
    return SuperHeader(
        theme_manager=super_header_manager,
        image_src="tests/assets/test_image.png",
        nome="Ada",
        texto_inicial="Primeiro parágrafo.\n\nSegundo parágrafo.",
    )
