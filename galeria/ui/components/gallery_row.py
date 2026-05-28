# galeria/ui/components/gallery_row.py
"""Linha horizontal de cards da galeria de superintendentes."""

from collections.abc import Callable, Sequence
from typing import Any, cast

import flet as ft

from galeria.core import SUPER_CAPTION_MASK
from galeria.domain.protocols import SuperLike
from galeria.domain.protocols.theme_manager_like import ThemeManagerLike
from galeria.ui.components.media import ThemedMaskedImage, themed_portrait_src
from galeria.ui.components.super_caption import SuperCaption
from galeria.ui.theme.manager import StaticThemeManager


class GalleryRow(ft.Container):
    """Container com cards navegáveis e tematizados por era."""

    def __init__(
        self,
        supers: Sequence[SuperLike],
        card_width: int,
        spacing: int,
        padding: int,
        on_card_click: Callable[[Any], None],
        theme: ThemeManagerLike,
    ):
        self.supers = supers
        self.card_width = card_width
        self._theme = theme
        self._on_card_click = on_card_click

        cards: list[ft.Control] = [self._build_card(s, on_card_click) for s in supers]

        self.row = ft.Row(
            controls=cards,
            spacing=spacing,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.START,
        )

        super().__init__(
            content=self.row,
            padding=ft.padding.only(bottom=padding),
        )

    def _build_card(
        self, super_data: SuperLike, on_card_click: Callable[[Any], None]
    ) -> ft.Container:
        """Monta um card da galeria, incluindo retrato e legenda quando houver."""
        is_placeholder = getattr(super_data, "is_placeholder", False)
        nome = getattr(super_data, "nome", "")
        card_theme = self._theme.get_theme_for_era(getattr(super_data, "era_id", None))
        card_theme_manager = cast(ThemeManagerLike, StaticThemeManager(card_theme))
        is_real_portrait = (
            super_data.foto is not None
            and super_data.foto != ""
            and nome != "_blank"
            and not is_placeholder
        )
        show_caption = nome != "_blank" and not is_placeholder
        stack_controls: list[ft.Control] = []
        stack_controls.append(
            cast(
                ft.Control,
                ThemedMaskedImage(
                src=themed_portrait_src(super_data.foto),
                mask_src=SUPER_CAPTION_MASK,
                theme=card_theme_manager,
                fit=ft.BoxFit.COVER,
                width=self.card_width,
                height=self._theme.gallery.card_height,
                apply_mask=is_real_portrait,
                ),
            )
        )

        if show_caption:
            stack_controls.append(
                SuperCaption(
                    theme_manager=card_theme_manager,
                    nome=nome,
                    subtitle=self._caption_periodo(super_data),
                    width=self.card_width,
                    single_line_name=True,
                )
            )

        return ft.Container(
            width=self.card_width,
            height=self._theme.gallery.card_height,
            on_click=lambda e: on_card_click(super_data),
            data={"type": "card", "nome": nome},
            border_radius=self._theme.radius.md,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Stack(controls=stack_controls),
        )

    def _caption_periodo(self, super_data: SuperLike) -> str | None:
        """Retorna o período formatado para a legenda do card."""
        periodo = getattr(super_data, "periodo", None)
        if periodo:
            return str(periodo)

        return None
