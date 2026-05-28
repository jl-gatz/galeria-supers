from typing import override

from galeria.ui.theme.models import TimelineColors


class FakeTimelineTheme(TimelineColors):
    def __init__(
        self,
        line: str = "#00ff00",
        point: str = "#00ff99",
        point_active: str = "#ffffff",
    ) -> None:
        super().__init__(line=line, point=point, point_active=point_active)

    @override
    def __setattr__(self, name: str, value: object) -> None:
        object.__setattr__(self, name, value)
