from typing import override

from galeria.ui.theme.models import UIColors


class FakeUITheme(UIColors):
    def __init__(self, border: str = "#333333", shadow: str = "#000000") -> None:
        super().__init__(border=border, shadow=shadow)

    @override
    def __setattr__(self, name: str, value: object) -> None:
        object.__setattr__(self, name, value)
