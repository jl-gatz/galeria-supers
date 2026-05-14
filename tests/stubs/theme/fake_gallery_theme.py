# tests/stubs/theme/fake_gallery_theme.py


from dataclasses import dataclass


@dataclass
class FakeGalleryTheme:
    card_width: int = 300
    card_height: int = 420
    visible_cards: int = 5
    padding: int = 16
    max_width: int = 1200

    h_spacing: int = 20
    v_spacing: int = 16

    image_overlay: str = "#00000055"
