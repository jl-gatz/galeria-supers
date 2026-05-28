# galeria/ui/components/floating_nav_button.py
"""Botão flutuante temático usado para ações de navegação."""

from collections.abc import Callable
from typing import Any, cast, override

import flet as ft

from galeria.domain.protocols.theme_manager_like import ThemeManagerLike
from galeria.ui.theme.models import Theme


class FloatingNavButton(ft.Container):
    """Container que envolve um FloatingActionButton com tema reativo."""

    def __init__(
        self,
        icon: ft.IconData,
        on_click: Callable[[Any], None],
        tooltip: str | None = None,
        alignment: ft.Alignment = ft.Alignment.BOTTOM_RIGHT,
        key: str | None = None,
        theme_manager: ThemeManagerLike | None = None,
    ):
        super().__init__()

        self.theme_manager = theme_manager
        self._mounted = False

        # self.expand = True
        self.alignment = alignment
        self.padding = 20

        self.button = ft.FloatingActionButton(
            icon=icon,
            tooltip=tooltip,
            on_click=cast(Any, on_click),
            key=key,
        )
        self.content = self.button

        if self.theme_manager:
            self.apply_theme(self.theme_manager.theme)

    def apply_theme(self, theme: Theme) -> None:
        """Atualiza espaçamento e cores do botão a partir do tema."""
        button_theme = getattr(theme, "button", None)

        self.padding = getattr(theme.spacing, "md", 20)
        self.button.bgcolor = getattr(button_theme, "bg", theme.accent.primary)
        self.button.foreground_color = getattr(button_theme, "fg", theme.text.inverse)

        if self._mounted:
            self.update()

    @override
    def did_mount(self) -> None:
        """Assina o gerenciador de tema quando o botão é montado."""
        self._mounted = True

        if self.theme_manager:
            self.theme_manager.subscribe(self.apply_theme)
            self.apply_theme(self.theme_manager.theme)

    @override
    def will_unmount(self) -> None:
        """Remove a assinatura de tema quando o botão é desmontado."""
        self._mounted = False

        if self.theme_manager:
            self.theme_manager.unsubscribe(self.apply_theme)

    # 🔹 especializações semânticas
    @classmethod
    def back(
        cls,
        on_click: Callable[[Any], None],
        key: str = "nav_back",
        theme_manager: ThemeManagerLike | None = None,
    ) -> "FloatingNavButton":
        """Cria um botão semântico de voltar."""
        return cls(
            icon=ft.Icons.ARROW_BACK,
            tooltip="Voltar",
            on_click=on_click,
            key=key,
            theme_manager=theme_manager,
        )

    @classmethod
    def forward(
        cls,
        on_click: Callable[[Any], None],
        key: str = "nav_forward",
        theme_manager: ThemeManagerLike | None = None,
    ) -> "FloatingNavButton":
        """Cria um botão semântico de avançar."""
        return cls(
            icon=ft.Icons.ARROW_FORWARD,
            tooltip="Avançar",
            on_click=on_click,
            key=key,
            theme_manager=theme_manager,
        )
