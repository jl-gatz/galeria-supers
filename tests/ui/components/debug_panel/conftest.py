# tests/ui/debug_panel/conftest.py

import pytest

from galeria.debug.debug_panel import ThemeDebugPanel
from tests.stubs.fake_theme_manager import FakeThemeManager


@pytest.fixture
def debug_panel(fake_theme_manager: FakeThemeManager) -> ThemeDebugPanel:
    return ThemeDebugPanel(fake_theme_manager)
