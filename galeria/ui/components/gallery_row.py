from collections.abc import Callable
from typing import Any

import flet as ft

from galeria.core import SUPER_CAPTION_MASK
from galeria.ui.components.media import ThemedMaskedImage, themed_portrait_src
from galeria.ui.components.super_caption import SuperCaption


class GalleryRow(ft.Container):
    def __init__(
        self,
        supers: Any,
        card_width: int,
        spacing: int,
        padding: int,
        on_card_click: Callable[[], None],
        theme: Any,
    ):
        self.supers = supers
        self.card_width = card_width
        self._theme = theme
        self._on_card_click = on_card_click

        cards = [self._build_card(s, on_card_click) for s in supers]

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

    def _build_card(self, super_data, on_card_click):
        is_placeholder = getattr(super_data, "is_placeholder", False)
        nome = getattr(super_data, "nome", "")
        is_real_portrait = (
            super_data.foto is not None
            and super_data.foto != ""
            and nome != "_blank"
            and not is_placeholder
        )
        show_caption = nome != "_blank" and not is_placeholder
        stack_controls: list[ft.Control] = [
            ThemedMaskedImage(
                src=themed_portrait_src(super_data.foto),
                mask_src=SUPER_CAPTION_MASK,
                theme=self._theme,
                fit=ft.BoxFit.COVER,
                width=self.card_width,
                height=self._theme.gallery.card_height,
                apply_mask=is_real_portrait,
            )
        ]

        if show_caption:
            stack_controls.append(
                SuperCaption(
                    theme_manager=self._theme,
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

    def _caption_periodo(self, super_data) -> str | None:
        periodo = getattr(super_data, "periodo", None)
        if periodo:
            return str(periodo)

        return None
