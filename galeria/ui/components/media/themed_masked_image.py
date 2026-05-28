# galeria/ui/components/media/themed_masked_image.py
"""Imagem composta por retrato e máscara tematizada."""

from typing import Any, override

import flet as ft

from galeria.domain.protocols.theme_manager_like import ThemeManagerLike
from galeria.ui.theme.models import Theme


class ThemedMaskedImage(ft.Stack):
    """Stack que sobrepõe uma máscara visual ao retrato quando necessário."""

    def __init__(
        self,
        src: str | None,
        mask_src: str,
        theme: ThemeManagerLike,
        width: int | None = None,
        height: int | None = None,
        fit: ft.BoxFit = ft.BoxFit.CONTAIN,
        apply_mask: bool = True,
        **kwargs: Any,
    ):
        self.theme_manager = theme
        self.apply_mask = apply_mask
        self._mounted = False
        self._has_src = src is not None

        self.base_image = ft.Image(
            src=src or "",
            width=width,
            height=height,
            fit=fit,
            visible=self._has_src,
        )
        self.mask_image = ft.Image(
            src=mask_src,
            width=width,
            height=height,
            fit=fit,
        )

        super().__init__(
            controls=[
                self.base_image,
                self.mask_image,
            ],
            **kwargs,
        )

        self._apply_theme(self.theme_manager.theme)

    def _apply_theme(self, theme: Theme) -> None:
        """Aplica visibilidade e tint da máscara conforme o tema."""
        self.base_image.visible = self._has_src
        self.base_image.color = None
        self.base_image.color_blend_mode = None

        if self.apply_mask:
            self.mask_image.visible = True
            self.mask_image.color = theme.image.caption_mask_tint
            self.mask_image.color_blend_mode = theme.image.caption_mask_blend_mode
            self.mask_image.opacity = theme.image.caption_mask_opacity
        else:
            self.mask_image.visible = False
            self.mask_image.color = None
            self.mask_image.color_blend_mode = None
            self.mask_image.opacity = 1.0

        if self._mounted and self._has_page():
            self.update()

    def _has_page(self) -> bool:
        """Indica se a imagem composta já está associada a uma página Flet."""
        try:
            _ = self.page
            return True
        except RuntimeError:
            return False

    @override
    def did_mount(self) -> None:
        """Assina mudanças de tema quando a imagem composta é montada."""
        self._mounted = True
        self.theme_manager.subscribe(self._apply_theme)
        self._apply_theme(self.theme_manager.theme)

    @override
    def will_unmount(self) -> None:
        """Remove a assinatura de tema antes da desmontagem."""
        self._mounted = False
        self.theme_manager.unsubscribe(self._apply_theme)
