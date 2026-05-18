import flet as ft

from galeria.ui.components.super_caption import SuperCaption
from tests.stubs.fake_theme import FakeTheme
from tests.stubs.fake_theme_manager import FakeThemeManager


def test_super_caption_renders_name():
    manager = FakeThemeManager(FakeTheme())

    caption = SuperCaption(theme_manager=manager, nome="Ada Lovelace")

    assert caption.name_text.value == "Ada Lovelace"
    assert caption.text_column.controls == [caption.name_text]


def test_super_caption_renders_subtitle_when_provided():
    manager = FakeThemeManager(FakeTheme())

    caption = SuperCaption(
        theme_manager=manager,
        nome="Ada Lovelace",
        subtitle="Diretora",
    )

    assert caption.subtitle_text is not None
    assert caption.subtitle_text.value == "Diretora"
    assert caption.text_column.controls == [caption.name_text, caption.subtitle_text]


def test_super_caption_does_not_render_subtitle_when_none():
    manager = FakeThemeManager(FakeTheme())

    caption = SuperCaption(theme_manager=manager, nome="Ada Lovelace", subtitle=None)

    assert caption.subtitle_text is None
    assert caption.text_column.controls == [caption.name_text]


def test_super_caption_applies_theme_and_reacts_to_theme_change():
    theme = FakeTheme()
    theme.text.inverse = "#fafafa"
    theme.typography.super_caption_name_size = 22
    theme.typography.super_caption_subtitle_size = 14
    theme.typography.super_caption_line_height = 1.2
    manager = FakeThemeManager(theme)
    caption = SuperCaption(
        theme_manager=manager,
        nome="Ada Lovelace",
        subtitle="Diretora",
    )

    caption.did_mount()

    assert caption.name_text.color == "#fafafa"
    assert caption.name_text.size == 22
    assert caption.name_text.style.height == 1.2
    assert caption.subtitle_text is not None
    assert caption.subtitle_text.size == 14

    next_theme = FakeTheme()
    next_theme.text.inverse = "#111111"
    next_theme.typography.super_caption_name_size = 24

    manager.set_theme(next_theme)

    assert caption.name_text.color == "#111111"
    assert caption.name_text.size == 24
    assert caption.name_text.weight == next_theme.typography.weight_bold

    caption.will_unmount()
    assert caption.apply_theme not in manager._listeners


def test_super_caption_uses_text_controls_only():
    manager = FakeThemeManager(FakeTheme())

    caption = SuperCaption(theme_manager=manager, nome="Ada Lovelace")

    assert isinstance(caption.name_text, ft.Text)
    assert all(isinstance(control, ft.Text) for control in caption.text_column.controls)


def test_super_caption_single_line_name_uses_smaller_size():
    theme = FakeTheme()
    manager = FakeThemeManager(theme)

    caption = SuperCaption(
        theme_manager=manager,
        nome="Alfredo Fernandes de Almeida",
        single_line_name=True,
    )

    assert caption.name_text.max_lines == 1
    assert caption.name_text.size == max(12, int(theme.typography.body * 0.72))
