from typing import override

from galeria.ui.theme.models import Spacing


class FakeSpacingTheme(Spacing):
    def __init__(
        self,
        xs: int = 4,
        sm: int = 8,
        md: int = 16,
        lg: int = 24,
        xl: int = 32,
    ) -> None:
        super().__init__(xs=xs, sm=sm, md=md, lg=lg, xl=xl)

    @override
    def __setattr__(self, name: str, value: object) -> None:
        object.__setattr__(self, name, value)
