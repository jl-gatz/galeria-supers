from collections.abc import Callable
from typing import cast

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
from galeria.ui.theme.styles import ComponentStyles
from galeria.ui.theme.themes import theme_for_era


class FakeThemeManager:
    auto_mode: bool

    def __init__(self, theme: Theme):
        self.theme = theme
        self._listeners: list[Callable[[Theme], None]] = []
        self.era_requests: list[str | None] = []
        self.auto_mode = True

    @property
    def gallery(self) -> GalleryTheme:
        return self.theme.gallery

    @property
    def accent(self) -> AccentColors:
        return self.theme.accent

    @property
    def button(self) -> ButtonColors:
        return self.theme.button

    @property
    def header(self) -> HeaderTheme:
        return self.theme.header

    @property
    def image(self) -> ImageTheme:
        return self.theme.image

    @property
    def logo(self) -> LogoTheme:
        return self.theme.logo

    @property
    def base(self) -> BaseColors:
        return self.theme.base

    @property
    def super_detail(self) -> SuperDetailTheme:
        return self.theme.super_detail

    @property
    def colors(self) -> ThemeLike:
        return cast(ThemeLike, self.theme)

    @property
    def spacing(self) -> Spacing:
        return self.theme.spacing

    @property
    def styles(self) -> ComponentStyles:
        return self.theme.styles

    @property
    def radius(self) -> Radius:
        return self.theme.radius

    @property
    def typography(self) -> Typography:
        return self.theme.typography

    @property
    def text(self) -> TextColors:
        return self.theme.text

    @property
    def timeline(self) -> TimelineColors:
        return self.theme.timeline

    @property
    def ui(self) -> UIColors:
        return self.theme.ui

    def set_theme(self, theme: Theme) -> None:
        self.theme = theme
        for listener in self._listeners:
            listener(theme)

    def set_theme_for_era(self, era_id: str | None) -> None:
        self.era_requests.append(era_id)
        theme = theme_for_era(era_id, fallback=self.theme)
        if theme is not None:
            self.set_theme(theme)

    def get_theme_for_era(self, era_id: str | None) -> Theme:
        theme = theme_for_era(era_id, fallback=self.theme)
        return theme or self.theme

    def subscribe(self, listener: Callable[[Theme], None]) -> None:
        if listener not in self._listeners:
            self._listeners.append(listener)

    def unsubscribe(self, listener: Callable[[Theme], None]) -> None:
        if listener in self._listeners:
            self._listeners.remove(listener)

    def set_auto_mode(self, enabled: bool) -> None:
        self.auto_mode = enabled
