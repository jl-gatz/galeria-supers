import flet as ft

from galeria.ui.components.media import ThemedMaskedImage
from tests.stubs.fake_theme import FakeTheme
from tests.stubs.fake_theme_manager import FakeThemeManager


def test_masked_image_does_not_tint_base_image():
    manager = FakeThemeManager(FakeTheme())

    component = ThemedMaskedImage(
        src="portrait.png",
        mask_src="mask.png",
        theme=manager,
    )
    component.did_mount()

    assert component.base_image.color is None
    assert component.base_image.color_blend_mode is None


def test_masked_image_applies_theme_to_mask_after_mount():
    theme = FakeTheme()
    manager = FakeThemeManager(theme)

    component = ThemedMaskedImage(
        src="portrait.png",
        mask_src="mask.png",
        theme=manager,
    )
    component.did_mount()

    assert component.mask_image.color == theme.image.caption_mask_tint
    assert component.mask_image.color_blend_mode == theme.image.caption_mask_blend_mode
    assert component.mask_image.opacity == theme.image.caption_mask_opacity


def test_masked_image_reacts_to_theme_change():
    manager = FakeThemeManager(FakeTheme())
    component = ThemedMaskedImage(
        src="portrait.png",
        mask_src="mask.png",
        theme=manager,
    )
    component.did_mount()

    next_theme = FakeTheme()
    next_theme.image.caption_mask_tint = "#0000ff"
    next_theme.image.caption_mask_blend_mode = ft.BlendMode.MULTIPLY
    next_theme.image.caption_mask_opacity = 0.4

    manager.set_theme(next_theme)

    assert component.mask_image.color == "#0000ff"
    assert component.mask_image.color_blend_mode == ft.BlendMode.MULTIPLY
    assert component.mask_image.opacity == 0.4


def test_masked_image_can_disable_mask():
    manager = FakeThemeManager(FakeTheme())

    component = ThemedMaskedImage(
        src="portrait.png",
        mask_src="mask.png",
        theme=manager,
        apply_mask=False,
    )
    component.did_mount()

    assert component.mask_image.visible is False
    assert component.mask_image.color is None
    assert component.mask_image.color_blend_mode is None


def test_masked_image_does_not_update_before_mount():
    manager = FakeThemeManager(FakeTheme())
    component = ThemedMaskedImage(
        src="portrait.png",
        mask_src="mask.png",
        theme=manager,
    )

    def fail_update():
        raise AssertionError("update should not be called before mount")

    component.update = fail_update

    component._apply_theme(manager.theme)

    assert component.mask_image.color == manager.theme.image.caption_mask_tint
