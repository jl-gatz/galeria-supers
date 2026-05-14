from typing import Any, Protocol


class ThemeLike(Protocol):
    accent: Any
    base: Any
    button: Any
    gallery: Any
    header: Any
    super_detail: Any
    timeline: Any
    ui: Any

    colors: Any
    spacing: Any
    radius: Any
    typography: Any
    text: Any
