from dataclasses import dataclass

import flet as ft


@dataclass
class FakeImageTheme:
    portrait_tint: str | None = None
    portrait_blend_mode: ft.BlendMode | None = None
    portrait_opacity: float = 1.0
    caption_mask_tint: str = "#00ff00"
    caption_mask_blend_mode: ft.BlendMode = ft.BlendMode.SRC_IN
    caption_mask_opacity: float = 0.8
