import flet as ft

from galeria.debug.debug_panel import ThemeDebugPanel
from tests.stubs.fake_theme import FakeTheme
from tests.stubs.fake_theme_manager import FakeThemeManager


def test_panel_initial_state(debug_panel: ThemeDebugPanel):
    assert debug_panel.visible is False
    assert debug_panel.opacity == 0.95
    assert debug_panel.top == 16
    assert debug_panel.right == 16
    assert debug_panel._mounted is False


def test_apply_theme_updates_visual_state(
    debug_panel: ThemeDebugPanel,
    fake_theme: FakeTheme,
):
    debug_panel.apply_theme(fake_theme)

    assert debug_panel.title_text.value == f"Theme: {fake_theme.title}"

    assert debug_panel.title_text.color == fake_theme.text.primary

    assert debug_panel.subtitle_text.color == fake_theme.text.secondary

    assert "accent:" in debug_panel.subtitle_text.value
    assert "surface:" in debug_panel.subtitle_text.value
    assert "text:" in debug_panel.subtitle_text.value

    assert isinstance(debug_panel.shadow, ft.BoxShadow)

    assert debug_panel.shadow.color == fake_theme.ui.shadow


def test_apply_theme_updates_auto_switch_state(
    debug_panel: ThemeDebugPanel,
    fake_theme_manager: FakeThemeManager,
    fake_theme: FakeTheme,
):
    fake_theme_manager.auto_mode = False

    debug_panel.apply_theme(fake_theme)

    assert debug_panel.auto_theme_switch.value is False
