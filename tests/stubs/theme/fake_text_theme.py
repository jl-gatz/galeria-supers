from typing import override

from galeria.ui.theme.models import TextColors


class FakeTextTheme(TextColors):
    muted: str

    def __init__(
        self,
        primary: str = "#FFFFFF",
        secondary: str = "#BBBBBB",
        inverse: str = "#000000",
        muted: str = "#888888",
    ) -> None:
        super().__init__(primary=primary, secondary=secondary, inverse=inverse)
        self.muted = muted

    @override
    def __setattr__(self, name: str, value: object) -> None:
        object.__setattr__(self, name, value)
