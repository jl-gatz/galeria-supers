from typing import override

from galeria.ui.theme.models import GalleryTheme


class FakeGalleryTheme(GalleryTheme):
    def __init__(
        self,
        title: str = "Galeria de Superintendentes",
        card_width: int = 300,
        card_height: int = 420,
        visible_cards: int = 5,
        h_spacing: int = 20,
        v_spacing: int = 16,
        padding: int = 16,
        max_width: int = 1200,
        image_overlay: str = "#00000055",
        hover_overlay: str = "#00ff0022",
    ) -> None:
        super().__init__(
            card_width=card_width,
            card_height=card_height,
            visible_cards=visible_cards,
            h_spacing=h_spacing,
            v_spacing=v_spacing,
            padding=padding,
            max_width=max_width,
            image_overlay=image_overlay,
            hover_overlay=hover_overlay,
            title=title,
        )

    @override
    def __setattr__(self, name: str, value: object) -> None:
        object.__setattr__(self, name, value)
