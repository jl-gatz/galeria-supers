from typing import override

from galeria.ui.theme.models import SuperDetailTheme


class FakeSuperDetailTheme(SuperDetailTheme):
    def __init__(
        self,
        content_width: int = 1000,
        image_height: int = 420,
        background: str = "#111111",
        overlay: str = "#00ff0011",
        title_size: int = 34,
        body_size: int = 18,
        timeline_color: str = "#00ff00",
        highlight: str = "#00ff99",
    ) -> None:
        super().__init__(
            content_width=content_width,
            image_height=image_height,
            background=background,
            overlay=overlay,
            title_size=title_size,
            body_size=body_size,
            timeline_color=timeline_color,
            highlight=highlight,
        )

    @override
    def __setattr__(self, name: str, value: object) -> None:
        object.__setattr__(self, name, value)
