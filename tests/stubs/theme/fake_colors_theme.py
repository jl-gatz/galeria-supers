# tests/stubs/theme/fake_base_theme.py

from dataclasses import dataclass


@dataclass
class FakeColorsTheme:
    primary: str = "#FF0000"
    secondary: str = "#00FF00"
    background: str = "#101010"
    text: str = "#FFFFFF"
