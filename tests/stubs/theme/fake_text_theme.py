# tests/stubs/theme/fake_base_theme.py

from dataclasses import dataclass


@dataclass
class FakeTextTheme:
    primary: str = "#FFFFFF"
    secondary: str = "#BBBBBB"
    muted: str = "#888888"
    inverse: str = "#000000"
