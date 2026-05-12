# tests/stubs/theme/fake_radius_theme.py

from dataclasses import dataclass


@dataclass
class FakeRadiusTheme:
    sm: int = 4
    md: int = 8
    lg: int = 16
    xl: int = 24
