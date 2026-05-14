# tests/stubs/theme/fake_base_theme.py

from dataclasses import dataclass


@dataclass
class FakeSpacingTheme:
    xs: int = 4
    sm: int = 8
    md: int = 16
    lg: int = 24
    xl: int = 32
