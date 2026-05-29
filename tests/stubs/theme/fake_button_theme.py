from typing import override

from galeria.ui.theme.models import ButtonColors


class FakeButtonTheme(ButtonColors):
    def __init__(
        self,
        bg: str = "#00ff00",
        fg: str = "#000000",
        hover: str = "#00cc00",
    ) -> None:
        super().__init__(bg=bg, fg=fg, hover=hover)

    @override
    def __setattr__(self, name: str, value: object) -> None:
        object.__setattr__(self, name, value)
