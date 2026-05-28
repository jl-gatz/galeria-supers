# galeria/ui/components/super_caption.py
"""Legenda temática exibida sobre retratos de superintendentes."""

from typing import Any, cast, override

import flet as ft

from galeria.domain.protocols.theme_manager_like import ThemeManagerLike
from galeria.ui.theme.models import Theme


class SuperCaption(ft.Container):
    """Bloco de nome e subtítulo aplicado sobre imagens de retrato."""

    def __init__(
        self,
        theme_manager: ThemeManagerLike,
        nome: str,
        subtitle: str | None = None,
        width: float | None = None,
        compact: bool = False,
        single_line_name: bool = False,
        **kwargs: Any,
    ):
        self.theme_manager = theme_manager
        self.nome = nome
        self.subtitle = subtitle
        self.compact = compact
        self.single_line_name = single_line_name
        self._mounted = False

        self.name_text = ft.Text(
            nome,
            max_lines=1 if single_line_name else 2,
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        self.subtitle_text = (
            ft.Text(
                subtitle,
                max_lines=1,
                overflow=ft.TextOverflow.ELLIPSIS,
            )
            if subtitle
            else None
        )

        controls: list[ft.Control] = [self.name_text]
        if self.subtitle_text is not None:
            controls.append(self.subtitle_text)

        self.text_column = ft.Column(
            spacing=2 if compact else 4,
            tight=True,
            controls=controls,
        )

        super().__init__(
            content=self.text_column,
            width=width,
            left=0,
            right=0,
            bottom=0,
            alignment=ft.Alignment.BOTTOM_LEFT,
            **kwargs,
        )

        if self.theme_manager:
            self._apply_theme(self.theme_manager.theme)

    def apply_theme(self, theme: Theme):
        """Aplica o tema e atualiza o controle quando estiver montado."""
        self._apply_theme(theme)

        if self._mounted and self._has_page():
            self.update()

    def _apply_theme(self, theme: Theme) -> None:
        """Atualiza espaçamento, tipografia e cores da legenda."""
        typography = getattr(theme, "typography", None)
        caption_style = self._caption_style(theme)
        text = getattr(theme, "text", None)

        horizontal_padding = caption_style.padding_horizontal
        vertical_padding = caption_style.padding_vertical
        name_size = caption_style.name_size
        subtitle_size = caption_style.subtitle_size

        if self.compact:
            vertical_padding = max(
                4,
                int(vertical_padding * caption_style.compact_padding_scale),
            )
            name_size = max(12, int(name_size * caption_style.compact_scale))
            subtitle_size = max(10, int(subtitle_size * caption_style.compact_scale))

        if self.single_line_name:
            name_size = caption_style.name_single_line_size

        self.padding = ft.padding.symmetric(
            horizontal=horizontal_padding,
            vertical=vertical_padding,
        )

        self.name_text.color = self._theme_token(text, ["inverse", "primary"], "#FFFFFF")
        self.name_text.size = name_size
        self.name_text.weight = cast(ft.FontWeight, caption_style.name_weight)
        self.name_text.font_family = self._theme_token(typography, ["font_family"], None)
        self.name_text.style = ft.TextStyle(height=caption_style.line_height)

        if self.subtitle_text is not None:
            self.subtitle_text.color = self._theme_token(
                text,
                ["inverse", "secondary"],
                "#FFFFFF",
            )
            self.subtitle_text.size = subtitle_size
            self.subtitle_text.weight = cast(ft.FontWeight, caption_style.subtitle_weight)
            self.subtitle_text.font_family = self._theme_token(
                typography,
                ["font_family"],
                None,
            )
            self.subtitle_text.style = ft.TextStyle(height=caption_style.line_height)

    def _caption_style(self, theme: Theme) -> Any:
        """Obtém o estilo de legenda do tema ou usa o padrão global."""
        styles = getattr(theme, "styles", None)
        caption_style = getattr(styles, "portrait_caption", None)

        if caption_style is not None:
            return caption_style

        from galeria.ui.theme.styles import default_component_styles

        return default_component_styles().portrait_caption

    def _theme_token(self, source: Any, names: list[str], fallback: Any = None) -> Any:
        """Retorna o primeiro token disponível em uma fonte temática."""
        if source is None:
            return fallback

        for name in names:
            value = getattr(source, name, None)
            if value is not None:
                return value

        return fallback

    def _has_page(self) -> bool:
        """Indica se o controle já possui uma página Flet associada."""
        try:
            _ = self.page
            return True
        except RuntimeError:
            return False

    @override
    def did_mount(self) -> None:
        """Assina mudanças de tema depois da montagem."""
        self._mounted = True
        if self.theme_manager:
            self.theme_manager.subscribe(self.apply_theme)
            self.apply_theme(self.theme_manager.theme)

    @override
    def will_unmount(self) -> None:
        """Remove a assinatura de tema antes da desmontagem."""
        self._mounted = False
        if self.theme_manager:
            self.theme_manager.unsubscribe(self.apply_theme)
