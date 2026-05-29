from typing import override

from galeria.ui.theme.models import AccentColors


class FakeAccentTheme(AccentColors):
    def __init__(
        self,
        primary: str = "#00ff00",
        secondary: str = "#00ff99",
        contrast: str = "#ffffff",
    ) -> None:
        super().__init__(primary=primary, secondary=secondary, contrast=contrast)

    @override
    def __setattr__(self, name: str, value: object) -> None:
        object.__setattr__(self, name, value)
