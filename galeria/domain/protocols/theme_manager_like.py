# galeria/domain/protocols/theme_manager_like.py
"""Protocolo para gerenciadores de tema reativos."""

from collections.abc import Callable
from typing import Protocol

from galeria.domain.protocols.theme_like import ThemeLike
from galeria.ui.theme.models import (
    AccentColors,
    BaseColors,
    ButtonColors,
    GalleryTheme,
    HeaderTheme,
    ImageTheme,
    LogoTheme,
    Radius,
    Spacing,
    SuperDetailTheme,
    TextColors,
    Theme,
    TimelineColors,
    Typography,
    UIColors,
)


class ThemeManagerLike(Protocol):
    """Contrato consumido por views e componentes tematizáveis."""

    @property
    def theme(self) -> Theme: ...

    @property
    def accent(self) -> AccentColors: ...

    @property
    def gallery(self) -> GalleryTheme: ...

    @property
    def header(self) -> HeaderTheme: ...

    @property
    def image(self) -> ImageTheme: ...

    @property
    def logo(self) -> LogoTheme: ...

    @property
    def super_detail(self) -> SuperDetailTheme: ...

    @property
    def base(self) -> BaseColors: ...

    @property
    def button(self) -> ButtonColors: ...

    @property
    def colors(self) -> ThemeLike: ...

    @property
    def spacing(self) -> Spacing: ...

    @property
    def radius(self) -> Radius: ...

    @property
    def typography(self) -> Typography: ...

    @property
    def text(self) -> TextColors: ...

    @property
    def timeline(self) -> TimelineColors: ...

    @property
    def ui(self) -> UIColors: ...

    def set_theme(self, theme: Theme) -> None: ...

    def set_theme_for_era(self, era_id: str | None) -> None: ...

    def get_theme_for_era(self, era_id: str | None) -> Theme: ...

    def subscribe(self, listener: Callable[[Theme], None]) -> None: ...

    def unsubscribe(self, listener: Callable[[Theme], None]) -> None: ...
