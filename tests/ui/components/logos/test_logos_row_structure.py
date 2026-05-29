from pathlib import Path

from galeria.ui.components.logos_row import logos_row
from galeria.ui.components.media import ThemedLogo
from tests.stubs.fake_theme import FakeTheme
from tests.stubs.fake_theme_manager import FakeThemeManager
from tests.utils.types import HasControls


def test_logos_row_contains_two_themed_logos():
    row = logos_row(
        Path("images/logos/logo-detic-4x.png"),
        Path("images/logos/Logo_Unicamp__0.png"),
        theme=FakeThemeManager(FakeTheme()),
    )

    content = row.content
    assert isinstance(content, HasControls)
    controls = content.controls

    assert len(controls) == 2
    assert all(isinstance(control, ThemedLogo) for control in controls)
    first, second = controls
    assert isinstance(first, ThemedLogo)
    assert isinstance(second, ThemedLogo)
    assert first._filename == "logo-detic-4x.png"
    assert second._filename == "Logo_Unicamp__0.png"
