import flet as ft

from galeria.ui.theme.theme import ThemeManager
from galeria.ui.theme.themes import CCUEC_THEME, DETIC_THEME


class ThemeDebugPanel(ft.Container):
    def __init__(self, theme_manager: ThemeManager):
        super().__init__()

        self.theme_manager = theme_manager

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
                ft.Row([self.btn_ccuec, self.btn_detic], spacing=6),
                ft.Divider(height=10),
                self.btn_toggle,
            ],
            spacing=6,
            tight=True,
        )

        # -------------------------
        # Estilo
        # -------------------------
        self.padding = 12
        self.border_radius = 10
        self.shadow = ft.BoxShadow(
            blur_radius=12,
            spread_radius=1,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
        )

        # cor inicial (segura)
        self.bgcolor = ft.Colors.with_opacity(0.85, ft.Colors.BLACK)

        # -------------------------
        # Binding
        # -------------------------
        self.theme_manager.subscribe(self.on_theme_change)

        # estado inicial
        self.apply_theme(self.theme_manager.theme)

    # =========================================================
    # 🎛️ AÇÕES
    # =========================================================

    def _toggle_visibility(self, e=None):
        self.visible = False
        self.update()

    def _on_toggle_auto_theme(self, e):
        value = e.control.value
        if hasattr(self.theme_manager, "set_auto_mode"):
            self.theme_manager.set_auto_mode(value)

    def _set_theme(self, theme_name: str):
        if hasattr(self.theme_manager, "set_theme"):
            self.auto_theme_switch.value = False  # desliga o auto mode
            self.theme_manager.set_theme(theme_name)

    # =========================================================
    # 🎨 THEME
    # =========================================================

    def on_theme_change(self, theme):
        self.apply_theme(theme)
        self.update()

    def apply_theme(self, theme):
        # fundo semi-transparente baseado no tema
        try:
            self.bgcolor = ft.Colors.with_opacity(0.9, theme.primary)
        except Exception:
            self.bgcolor = ft.Colors.with_opacity(0.85, ft.Colors.BLACK)

        # textos
        self.title_text.value = f"Theme: {getattr(theme, 'title', 'unknown')}"
        self.title_text.color = theme.text

        self.subtitle_text.value = (
            f"primary: {getattr(theme, 'primary', '-')}\ntext: {getattr(theme, 'text', '-')}"
        )
        self.subtitle_text.color = theme.text

        # estado do switch (se existir no manager)
        if hasattr(self.theme_manager, "auto_mode"):
            self.auto_theme_switch.value = self.theme_manager.auto_mode
