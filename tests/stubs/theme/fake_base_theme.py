# tests/stubs/theme/fake_base_theme.py


from dataclasses import dataclass


@dataclass
class FakeBaseTheme:
    background = "#000000"
    surface = "#111111"

    primary = "#ff0000"
    secondary = "#00ff00"

    text = "#ffffff"
