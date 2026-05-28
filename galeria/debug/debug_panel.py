# galeria/debug/debug_panel.py
"""Painel visual para alternar e inspecionar temas em desenvolvimento."""

from typing import Any, override

import flet as ft

from galeria.ui.theme.models import Theme
from galeria.ui.theme.theme import ThemeManager
from galeria.ui.theme.themes import CCUEC_THEME, DETIC_THEME, GREENISH_THEME


class ThemeDebugPanel(ft.Container):
    """Overlay de debug para troca manual de tema e inspeção de tokens."""

    def __init__(self, theme_manager: ThemeManager):
        """Monta controles de debug e assina mudanças de tema."""
        super().__init__()

        self.theme_manager = theme_manager
        self._mounted = False

        # -------------------------
        # Estado
        # -------------------------
        self.visible = False
        self.top = 16
        self.right = 16
        self.opacity = 0.95

        # -------------------------
        # UI básica
        # -------------------------
        self.title_text = ft.Text(size=16, weight=ft.FontWeight.BOLD)
        self.subtitle_text = ft.Text(size=12)

        # -------------------------
        # Controles
        # -------------------------
        self.auto_theme_switch = ft.Switch(
            label="Auto Theme",
            value=True,
            on_change=self._on_toggle_auto_theme,
        )

        self.btn_ccuec = ft.ElevatedButton(
            "CCUEC",
            on_click=lambda e: self._set_theme(CCUEC_THEME),
        )

        self.btn_detic = ft.ElevatedButton(
            "DETIC",
            on_click=lambda e: self._set_theme(DETIC_THEME),
        )

        self.btn_greenish = ft.ElevatedButton(
            "GREENISH",
            on_click=lambda e: self._set_theme(GREENISH_THEME),
        )

        self.btn_toggle = ft.TextButton(
            "Hide",
            on_click=self._toggle_visibility,
        )

        # -------------------------
        # Layout
        # -------------------------
        self.content = ft.Column(
            [
                self.title_text,
                self.subtitle_text,
                ft.Divider(height=10),
                self.auto_theme_switch,
                ft.Row([self.btn_ccuec, self.btn_detic, self.btn_greenish], spacing=6),
                ft.Divider(height=10),
                self.btn_toggle,
            ],
            spacing=6,
            tight=True,
        )

        # -------------------------
        # Estilo base (neutro)
        # -------------------------
        self.padding = 12
        self.border_radius = 10

        # -------------------------
        # Binding
        # -------------------------
        self.theme_manager.subscribe(self.apply_theme)

    # =========================================================
    # 🎛️ AÇÕES
    # =========================================================

    def _toggle_visibility(self, e: Any = None) -> None:
        """Oculta o painel de debug."""
        self.visible = False
        if self._mounted:
            self.update()

    def _on_toggle_auto_theme(self, e: Any) -> None:
        """Encaminha a preferência de troca automática ao gerenciador."""
        value = e.control.value
        if hasattr(self.theme_manager, "set_auto_mode"):
            self.theme_manager.set_auto_mode(value)

    def _set_theme(self, theme: Theme) -> None:
        """Aplica manualmente um tema e desliga a troca automática."""
        if hasattr(self.theme_manager, "set_theme"):
            print("SET_THEME CALLED:", theme.title, id(theme))
            self.auto_theme_switch.value = False
            self.theme_manager.set_theme(theme)

    # =========================================================
    # 🎨 THEME
    # =========================================================

    def apply_theme(self, theme: Theme | None) -> None:
        """Atualiza textos e superfície do painel para o tema ativo."""
        if theme is None:
            return

        # 🎨 Fundo (surface com leve transparência)
        self.bgcolor = ft.Colors.with_opacity(0.92, theme.base.surface)

        # 🌑 Shadow consistente com o tema
        self.shadow = ft.BoxShadow(
            blur_radius=12,
            spread_radius=1,
            color=theme.ui.shadow,
        )

        # 🧾 Textos
        self.title_text.value = f"Theme: {theme.title}"
        self.title_text.color = theme.text.primary

        self.subtitle_text.value = (
            f"accent: {theme.accent.primary}\n"
            f"surface: {theme.base.surface}\n"
            f"text: {theme.text.primary}"
        )
        self.subtitle_text.color = theme.text.secondary

        # 🔘 Estado do switch
        if hasattr(self.theme_manager, "auto_mode"):
            self.auto_theme_switch.value = self.theme_manager.auto_mode

        if self._mounted:
            self.update()

    # =========================================================
    # 🎬 LIFECYCLE
    # =========================================================

    @override
    def did_mount(self) -> None:
        """Aplica o tema inicial após a montagem do painel."""
        self._mounted = True
        self.apply_theme(self.theme_manager.theme)

    @override
    def will_unmount(self) -> None:
        """Remove a assinatura de tema antes da desmontagem."""
        self.theme_manager.unsubscribe(self.apply_theme)
