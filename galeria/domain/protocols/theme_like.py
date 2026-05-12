from typing import Any, Protocol


class ThemeLike(Protocol):
    base: Any
    gallery: Any
    header: Any
    super_detail: Any

    colors: Any
    spacing: Any
    radius: Any
    typography: Any
    text: Any
