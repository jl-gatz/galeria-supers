# tests/ui/debug_panel/test_theme_debug_panel_behavior.py


from unittest.mock import MagicMock

from galeria.debug.debug_panel import ThemeDebugPanel
from tests.stubs.fake_theme import FakeTheme
from tests.stubs.fake_theme_manager import FakeThemeManager


def test_toggle_visibility_hides_panel(debug_panel: ThemeDebugPanel):
    debug_panel.visible = True

    debug_panel._toggle_visibility()

    assert debug_panel.visible is False


def test_toggle_visibility_calls_update_when_mounted(
    debug_panel: ThemeDebugPanel,
):
    debug_panel._mounted = True
    debug_panel.update = MagicMock()

    debug_panel._toggle_visibility()

    debug_panel.update.assert_called_once()


def test_toggle_auto_theme_calls_manager(
    debug_panel: ThemeDebugPanel,
    fake_theme_manager: FakeThemeManager,
):
    fake_theme_manager.set_auto_mode = MagicMock()

    event = MagicMock()
    event.control.value = False

    debug_panel._on_toggle_auto_theme(event)

    fake_theme_manager.set_auto_mode.assert_called_once_with(False)


def test_set_theme_disables_auto_mode_and_calls_manager(
    debug_panel: ThemeDebugPanel,
    fake_theme_manager: FakeThemeManager,
    fake_theme: FakeTheme,
):
    fake_theme_manager.set_theme = MagicMock()

    debug_panel._set_theme(fake_theme)

    assert debug_panel.auto_theme_switch.value is False

    fake_theme_manager.set_theme.assert_called_once_with(fake_theme)


def test_did_mount_sets_mounted_and_applies_theme(
    debug_panel: ThemeDebugPanel,
    fake_theme_manager: FakeThemeManager,
):
    debug_panel.apply_theme = MagicMock()

    debug_panel.did_mount()

    assert debug_panel._mounted is True

    debug_panel.apply_theme.assert_called_once_with(fake_theme_manager.theme)


def test_will_unmount_unsubscribes(
    debug_panel: ThemeDebugPanel,
    fake_theme_manager: FakeThemeManager,
):
    fake_theme_manager.unsubscribe = MagicMock()

    debug_panel.will_unmount()

    fake_theme_manager.unsubscribe.assert_called_once_with(debug_panel.apply_theme)
