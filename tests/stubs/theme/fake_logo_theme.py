from dataclasses import dataclass

import flet as ft


@dataclass
class FakeLogoTheme:
    variant: str = "official"
    tint: str | None = None
    blend_mode: ft.BlendMode | None = None
    opacity: float = 1.0
