from typing import Any

import flet as ft


class ThemedMaskedImage(ft.Stack):
    def __init__(
        self,
        src: str | None,
        mask_src: str,
        theme: Any,
        width: int | None = None,
        height: int | None = None,
        fit: ft.BoxFit = ft.BoxFit.CONTAIN,
        apply_mask: bool = True,
        **kwargs: Any,
    ):
        self.theme_manager = theme
        self.apply_mask = apply_mask
        self._mounted = False

        self.base_image = ft.Image(
            src=src,
            width=width,
            height=height,
            fit=fit,
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

    def _apply_theme(self, theme):
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
        try:
            return self.page is not None
        except RuntimeError:
            return False

    def did_mount(self):
        self._mounted = True
        self.theme_manager.subscribe(self._apply_theme)
        self._apply_theme(self.theme_manager.theme)

    def will_unmount(self):
        self._mounted = False
        self.theme_manager.unsubscribe(self._apply_theme)
