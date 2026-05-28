from typing import override

import flet as ft

from galeria.ui.theme.models import LogoTheme


class FakeLogoTheme(LogoTheme):
    def __init__(
        self,
        variant: str = "official",
        tint: str | None = None,
        blend_mode: ft.BlendMode | None = None,
        opacity: float = 1.0,
    ) -> None:
        super().__init__(
            variant=variant,
            tint=tint,
            blend_mode=blend_mode,
            opacity=opacity,
        )

    @override
    def __setattr__(self, name: str, value: object) -> None:
        object.__setattr__(self, name, value)
