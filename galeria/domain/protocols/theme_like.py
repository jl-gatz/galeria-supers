from typing import Any, Protocol


class ThemeLike(Protocol):
    id: str

    accent: Any
    base: Any
    button: Any
    gallery: Any
    header: Any
    image: Any
    logo: Any
    super_detail: Any
    timeline: Any
    ui: Any

    colors: Any
    spacing: Any
    radius: Any
    typography: Any
    text: Any
