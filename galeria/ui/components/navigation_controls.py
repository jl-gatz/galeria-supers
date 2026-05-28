# galeria/ui/components/navigation_controls.py
"""Controles de navegação anterior/próximo com tema reativo."""

from collections.abc import Callable
from typing import Any, override

import flet as ft

from galeria.domain.protocols.theme_manager_like import ThemeManagerLike
from galeria.ui.theme.models import Theme


class NavigationControls(ft.Row):
    """Linha de botões para navegar entre itens de uma visão de detalhe."""

    def __init__(
        self,
        on_prev: Callable[[Any], None],
        on_next: Callable[[Any], None],
        alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.END,
        theme_manager: ThemeManagerLike | None = None,
    ):
        self.theme_manager = theme_manager
        self._mounted = False

        def _build_button(
            icon: ft.IconData,
            tooltip: str,
            handler: Callable[[Any], None],
        ) -> ft.IconButton:
            def handle_click(event: Any) -> None:
                handler(event)

            return ft.IconButton(
                icon=icon,
                tooltip=tooltip,
                on_click=handle_click,
            )

        self.prev_button = _build_button(
            ft.Icons.CHEVRON_LEFT,
            "Anterior",
            on_prev,
        )
        self.next_button = _build_button(
            ft.Icons.CHEVRON_RIGHT,
            "Próximo",
            on_next,
        )

        super().__init__(
            alignment=alignment,
            controls=[self.prev_button, self.next_button],
        )

        if self.theme_manager:
            self.apply_theme(self.theme_manager.theme)

    def apply_theme(self, theme: Theme) -> None:
        """Aplica cores e estados visuais aos botões de navegação."""
        hover_color = theme.accent.secondary

        for button in (self.prev_button, self.next_button):
            button.icon_color = theme.text.primary
            button.style = ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=getattr(theme.radius, "sm", 8)),
                bgcolor={
                    ft.ControlState.HOVERED: hover_color,
                    ft.ControlState.PRESSED: theme.accent.secondary,
                },
            )

        if self._mounted:
            self.update()

    @override
    def did_mount(self) -> None:
        """Assina mudanças de tema quando o controle entra na página."""
        self._mounted = True

        if self.theme_manager:
            self.theme_manager.subscribe(self.apply_theme)
            self.apply_theme(self.theme_manager.theme)

    @override
    def will_unmount(self) -> None:
        """Remove a assinatura de tema antes de desmontar o controle."""
        self._mounted = False

        if self.theme_manager:
            self.theme_manager.unsubscribe(self.apply_theme)
