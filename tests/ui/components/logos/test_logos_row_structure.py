from pathlib import Path

from galeria.ui.components.logos_row import logos_row
from galeria.ui.components.media import ThemedLogo
from tests.stubs.fake_theme import FakeTheme
from tests.stubs.fake_theme_manager import FakeThemeManager


def test_logos_row_contains_two_themed_logos():
    row = logos_row(
        Path("images/logos/logo-detic-4x.png"),
        Path("images/logos/Logo_Unicamp__0.png"),
        theme=FakeThemeManager(FakeTheme()),
    )

    controls = row.content.controls

    assert len(controls) == 2
    assert all(isinstance(control, ThemedLogo) for control in controls)
    assert controls[0]._filename == "logo-detic-4x.png"
    assert controls[1]._filename == "Logo_Unicamp__0.png"
