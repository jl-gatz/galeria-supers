# galeria/ui/components/media/themed_logo.py
"""Logo institucional que troca o asset conforme o tema ativo."""

from pathlib import Path
from typing import Any, override

import flet as ft

from galeria.core import LOGOS_DIR
from galeria.domain.protocols.theme_manager_like import ThemeManagerLike
from galeria.ui.theme.models import Theme


def resolve_logo_src(
    theme_id: str | None,
    filename: str,
    logos_dir: Path | None = None,
) -> str:
    """Resolve o caminho público do logo, priorizando a pasta do tema."""
    logos_dir = logos_dir or LOGOS_DIR
    logo_filename = filename.split("/")[-1].split("\\")[-1]
    fallback_path = logos_dir / logo_filename

    if theme_id:
        themed_path = logos_dir / theme_id / logo_filename

        if themed_path.exists():
            return f"images/logos/{theme_id}/{logo_filename}"

    return f"images/logos/{fallback_path.name}"


def _theme_id(theme: Theme) -> str | None:
    """Extrai o identificador de tema usado para buscar logos específicos."""
    return getattr(theme, "id", None)


class ThemedLogo(ft.Image):
    """Imagem de logo que acompanha mudanças de tema."""

    def __init__(
        self,
        filename: str | None = None,
        theme_manager: ThemeManagerLike | None = None,
        src: str | None = None,
        theme: ThemeManagerLike | None = None,
        **kwargs: Any,
    ):
        manager = theme_manager or theme
        if manager is None:
            raise ValueError("ThemedLogo requer theme_manager ou theme.")
        self.theme_manager = manager
        self._filename = filename or src or ""
        self._mounted = False

        super().__init__(
            src=self._resolve_src(self.theme_manager.theme),
            **kwargs,
        )

        self._apply_theme(self.theme_manager.theme)

    def _apply_theme(self, theme: Theme) -> None:
        """Atualiza a origem do logo e remove efeitos de cor."""
        self.src = self._resolve_src(theme)
        self.color = None
        self.color_blend_mode = None
        self.opacity = 1.0

        if self._mounted and self._has_page():
            self.update()

    def _resolve_src(self, theme: Theme) -> str:
        """Resolve o asset de logo para o tema informado."""
        return resolve_logo_src(_theme_id(theme), self._filename)

    def _has_page(self) -> bool:
        """Indica se o logo já está associado a uma página Flet."""
        try:
            _ = self.page
            return True
        except RuntimeError:
            return False

    @override
    def did_mount(self) -> None:
        """Assina mudanças de tema quando o logo é montado."""
        self._mounted = True
        self.theme_manager.subscribe(self._apply_theme)
        self._apply_theme(self.theme_manager.theme)

    @override
    def will_unmount(self) -> None:
        """Remove a assinatura de tema antes da desmontagem."""
        self._mounted = False
        self.theme_manager.unsubscribe(self._apply_theme)
