# galeria/ui/theme/manager.py
"""Gerenciadores de tema com suporte a observadores."""

from collections.abc import Callable
from typing import Any, cast

from galeria.domain.protocols.theme_like import ThemeLike
from galeria.ui.theme.models import Theme
from galeria.ui.theme.themes import theme_for_era


class StaticThemeManager:
    """Gerenciador mínimo para componentes com tema fixo."""

    def __init__(self, theme: Theme):
        """Armazena o tema que será exposto aos componentes."""
        self._theme = theme

    @property
    def theme(self) -> Theme:
        """Retorna o tema atual."""
        return self._theme

    @property
    def accent(self):
        return self._theme.accent

    @property
    def gallery(self):
        return self._theme.gallery

    @property
    def header(self):
        return self._theme.header

    @property
    def image(self):
        return self._theme.image

    @property
    def logo(self):
        return self._theme.logo

    @property
    def super_detail(self):
        return self._theme.super_detail

    @property
    def base(self):
        return self._theme.base

    @property
    def button(self):
        return self._theme.button

    @property
    def colors(self) -> ThemeLike:
        return cast(ThemeLike, self._theme)

    @property
    def spacing(self):
        return self._theme.spacing

    @property
    def radius(self):
        return self._theme.radius

    @property
    def typography(self):
        return self._theme.typography

    @property
    def text(self):
        return self._theme.text

    @property
    def timeline(self):
        return self._theme.timeline

    @property
    def ui(self):
        return self._theme.ui

    def subscribe(self, listener: Callable[[Theme], None]) -> None:
        """Ignora inscrições porque o tema estático não emite mudanças."""
        return None

    def unsubscribe(self, listener: Callable[[Theme], None]) -> None:
        """Ignora remoções porque não há lista de ouvintes."""
        return None

    def set_theme(self, theme: Theme) -> None:
        """Substitui o tema estático."""
        self._theme = theme

    def set_theme_for_era(self, era_id: str | None) -> None:
        """Seleciona um tema por era quando houver mapeamento."""
        theme = theme_for_era(era_id, fallback=self._theme)
        if theme is not None:
            self._theme = theme

    def get_theme_for_era(self, era_id: str | None) -> Theme:
        """Retorna o tema correspondente à era ou o tema atual."""
        theme = theme_for_era(era_id, fallback=self._theme)
        return theme or self._theme

    def __getattr__(self, item: str) -> Any:
        """Delega atributos desconhecidos ao tema armazenado."""
        return getattr(self._theme, item)


class ThemeManager:
    """Gerenciador reativo do tema global da aplicação."""

    def __init__(self, initial_theme: Theme):
        """Inicializa o tema atual e a lista de observadores."""
        self._theme = initial_theme
        self._listeners: list[Callable[[Theme], None]] = []

    # ==========================================================
    # 🎨 CURRENT THEME
    # ==========================================================

    @property
    def theme(self) -> Theme:
        """Retorna o tema ativo."""
        return self._theme

    # 👉 Proxy direto (ESSENCIAL)
    @property
    def accent(self):
        return self._theme.accent

    @property
    def gallery(self):
        return self._theme.gallery

    @property
    def header(self):
        return self._theme.header

    @property
    def image(self):
        return self._theme.image

    @property
    def logo(self):
        return self._theme.logo

    @property
    def super_detail(self):
        return self._theme.super_detail

    @property
    def base(self):
        return self._theme.base

    @property
    def button(self):
        return self._theme.button

    @property
    def colors(self) -> ThemeLike:
        return cast(ThemeLike, self._theme)

    @property
    def spacing(self):
        return self._theme.spacing

    @property
    def styles(self):
        return self._theme.styles

    @property
    def radius(self):
        return self._theme.radius

    @property
    def typography(self):
        return self._theme.typography

    @property
    def text(self):
        return self._theme.text

    @property
    def timeline(self):
        return self._theme.timeline

    @property
    def ui(self):
        return self._theme.ui

    # ==========================================================
    # 🔄 THEME SWITCH
    # ==========================================================

    def set_theme(self, theme: Theme) -> None:
        """Atualiza o tema e notifica observadores quando ele muda."""
        # 🚫 Evita re-render desnecessário
        if theme is self._theme:
            return

        self._theme = theme

        for listener in self._listeners:
            listener(theme)

    def set_theme_for_era(self, era_id: str | None) -> None:
        """Seleciona e aplica o tema associado a uma era."""
        theme = theme_for_era(era_id, fallback=self._theme)
        if theme is None:
            return
        self.set_theme(theme)

    def get_theme_for_era(self, era_id: str | None) -> Theme:
        """Retorna o tema de uma era sem alterar o tema ativo."""
        theme = theme_for_era(era_id, fallback=self._theme)
        return theme or self._theme

    # ==========================================================
    # 📡 OBSERVERS
    # ==========================================================

    def subscribe(self, listener: Callable[[Theme], None]) -> None:
        """Registra um observador de mudanças de tema."""
        if listener not in self._listeners:
            self._listeners.append(listener)

    def unsubscribe(self, listener: Callable[[Theme], None]) -> None:
        """Remove um observador de mudanças de tema."""
        if listener in self._listeners:
            self._listeners.remove(listener)

    # 🔥 MÁGICA AQUI
    def __getattr__(self, item: str) -> Any:
        """Delega atributos desconhecidos ao tema ativo."""
        return getattr(self._theme, item)
