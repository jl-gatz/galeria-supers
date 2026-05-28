# galeria/ui/components/media/themed_image.py
"""Imagem simples que reage a mudanças de tema."""

from typing import Any, override

import flet as ft

from galeria.domain.protocols.theme_manager_like import ThemeManagerLike
from galeria.ui.theme.models import Theme


class ThemedImage(ft.Image):
    """Imagem Flet com aplicação opcional de tint configurado pelo tema."""

    def __init__(
        self,
        src: str,
        theme: ThemeManagerLike,
        apply_tint: bool = False,
        **kwargs: Any,
    ):
        super().__init__(src=src, **kwargs)

        self.theme_manager = theme
        self.apply_tint = apply_tint
        self._mounted = False

        self._apply_theme(self.theme_manager.theme)

    def _apply_theme(self, theme: Theme) -> None:
        """Aplica ou remove tint conforme a configuração do componente."""
        if self.apply_tint:
            self.color = theme.image.portrait_tint
            self.color_blend_mode = theme.image.portrait_blend_mode
            self.opacity = theme.image.portrait_opacity
        else:
            self.color = None
            self.color_blend_mode = None
            self.opacity = 1.0

        if self._mounted and self._has_page():
            self.update()

    def _has_page(self) -> bool:
        """Indica se a imagem já está associada a uma página Flet."""
        try:
            _ = self.page
            return True
        except RuntimeError:
            return False

    @override
    def did_mount(self) -> None:
        """Assina mudanças de tema quando a imagem é montada."""
        self._mounted = True
        self.theme_manager.subscribe(self._apply_theme)
        self._apply_theme(self.theme_manager.theme)

    @override
    def will_unmount(self) -> None:
        """Remove a assinatura de tema antes da desmontagem."""
        self._mounted = False
        self.theme_manager.unsubscribe(self._apply_theme)
