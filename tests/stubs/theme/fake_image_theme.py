from typing import override

import flet as ft

from galeria.ui.theme.models import ImageTheme


class FakeImageTheme(ImageTheme):
    def __init__(
        self,
        portrait_tint: str | None = None,
        portrait_blend_mode: ft.BlendMode | None = None,
        portrait_opacity: float = 1.0,
        caption_mask_tint: str = "#00ff00",
        caption_mask_blend_mode: ft.BlendMode = ft.BlendMode.SRC_IN,
        caption_mask_opacity: float = 0.8,
    ) -> None:
        super().__init__(
            portrait_tint=portrait_tint,
            portrait_blend_mode=portrait_blend_mode,
            portrait_opacity=portrait_opacity,
            caption_mask_tint=caption_mask_tint,
            caption_mask_blend_mode=caption_mask_blend_mode,
            caption_mask_opacity=caption_mask_opacity,
        )

    @override
    def __setattr__(self, name: str, value: object) -> None:
        object.__setattr__(self, name, value)
