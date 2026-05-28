from typing import override

from galeria.ui.theme.models import BaseColors


class FakeBaseTheme(BaseColors):
    primary: str
    secondary: str
    text: str

    def __init__(
        self,
        background: str = "#000000",
        surface: str = "#111111",
        surface_variant: str = "#222222",
        primary: str = "#ff0000",
        secondary: str = "#00ff00",
        text: str = "#ffffff",
    ) -> None:
        super().__init__(
            background=background,
            surface=surface,
            surface_variant=surface_variant,
        )
        self.primary = primary
        self.secondary = secondary
        self.text = text

    @override
    def __setattr__(self, name: str, value: object) -> None:
        object.__setattr__(self, name, value)
