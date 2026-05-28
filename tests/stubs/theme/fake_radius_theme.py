from typing import override

from galeria.ui.theme.models import Radius


class FakeRadiusTheme(Radius):
    xl: int

    def __init__(self, sm: int = 4, md: int = 8, lg: int = 16, xl: int = 24) -> None:
        super().__init__(sm=sm, md=md, lg=lg)
        self.xl = xl

    @override
    def __setattr__(self, name: str, value: object) -> None:
        object.__setattr__(self, name, value)
