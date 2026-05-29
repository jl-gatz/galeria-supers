from typing import override

from galeria.ui.theme.models import HeaderTheme


class FakeHeaderTheme(HeaderTheme):
    def __init__(
        self,
        height: int = 120,
        title_size: int = 32,
        subtitle_size: int = 16,
        background: str = "#111111",
        text_color: str = "#ffffff",
        accent: str = "#00ff00",
    ) -> None:
        super().__init__(
            height=height,
            title_size=title_size,
            subtitle_size=subtitle_size,
            background=background,
            text_color=text_color,
            accent=accent,
        )

    @override
    def __setattr__(self, name: str, value: object) -> None:
        object.__setattr__(self, name, value)
