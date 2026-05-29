# tests/ui/debug_panel/conftest.py

from typing import cast

import pytest

from galeria.debug.debug_panel import ThemeDebugPanel
from galeria.ui.theme.manager import ThemeManager
from tests.stubs.fake_theme_manager import FakeThemeManager


@pytest.fixture
def debug_panel(fake_theme_manager: FakeThemeManager) -> ThemeDebugPanel:
    return ThemeDebugPanel(cast(ThemeManager, fake_theme_manager))
