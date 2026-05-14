import flet as ft

from galeria.ui.components.media import ThemedImage, ThemedLogo, themed_portrait_src
from tests.stubs.fake_theme import FakeTheme
from tests.stubs.fake_theme_manager import FakeThemeManager


def test_themed_image_applies_theme_after_mount():
    theme = FakeTheme()
    theme.image.portrait_tint = "#00ff00"
    theme.image.portrait_blend_mode = ft.BlendMode.COLOR
    theme.image.portrait_opacity = 0.8
    manager = FakeThemeManager(theme)

    image = ThemedImage(src="image.png", theme=manager, apply_tint=True)
    image.did_mount()

    assert image.color == theme.image.portrait_tint
    assert image.color_blend_mode == theme.image.portrait_blend_mode
    assert image.opacity == theme.image.portrait_opacity


def test_themed_image_does_not_apply_tint_when_disabled():
    manager = FakeThemeManager(FakeTheme())

    image = ThemedImage(src="image.png", theme=manager, apply_tint=False)
    image.did_mount()

    assert image.color is None
    assert image.color_blend_mode is None
    assert image.opacity == 1.0


def test_themed_image_reacts_to_theme_change():
    manager = FakeThemeManager(FakeTheme())
    image = ThemedImage(src="image.png", theme=manager, apply_tint=True)
    image.did_mount()

    next_theme = FakeTheme()
    next_theme.image.portrait_tint = "#0000ff"
    next_theme.image.portrait_blend_mode = ft.BlendMode.MULTIPLY
    next_theme.image.portrait_opacity = 0.4

    manager.set_theme(next_theme)

    assert image.color == "#0000ff"
    assert image.color_blend_mode == ft.BlendMode.MULTIPLY
    assert image.opacity == 0.4


def test_themed_image_does_not_update_before_mount():
    manager = FakeThemeManager(FakeTheme())
    image = ThemedImage(src="image.png", theme=manager)

    def fail_update():
        raise AssertionError("update should not be called before mount")

    image.update = fail_update

    image._apply_theme(manager.theme)

    assert image.color is None


def test_themed_logo_preserves_official_variant():
    theme = FakeTheme()
    theme.logo.variant = "official"
    theme.logo.tint = "#ff0000"
    theme.logo.blend_mode = ft.BlendMode.COLOR
    theme.logo.opacity = 0.2
    manager = FakeThemeManager(theme)

    logo = ThemedLogo(src="logo.png", theme=manager)
    logo.did_mount()

    assert logo.color is None
    assert logo.color_blend_mode is None
    assert logo.opacity == 1.0


def test_themed_portrait_src_uses_grayscale_variant_for_transparent_assets():
    assert (
        themed_portrait_src("images/supers/01-prof-alfredo__transp.png")
        == "images/supers/grayscale/01-prof-alfredo__gray.png"
    )


def test_themed_portrait_src_preserves_non_transparent_assets():
    assert themed_portrait_src("ada.png") == "ada.png"


def test_themed_portrait_src_normalizes_windows_paths():
    assert (
        themed_portrait_src(r"images\supers\01-prof-alfredo__transp.png")
        == "images/supers/grayscale/01-prof-alfredo__gray.png"
    )
