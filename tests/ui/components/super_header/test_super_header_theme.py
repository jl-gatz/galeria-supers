from typing import cast

import flet as ft

from galeria.ui.components.super_header import SuperHeader
from tests.stubs.fake_theme import FakeTheme
from tests.stubs.fake_theme_manager import FakeThemeManager
from tests.ui.components.super_header.conftest import SuperHeaderThemeLike


def _text_controls(super_header: SuperHeader) -> list[ft.Text]:
    controls = list(super_header.text_list.controls)
    assert all(isinstance(control, ft.Text) for control in controls)
    return cast(list[ft.Text], controls)


def test_super_header_applies_title_paragraph_and_divider_theme(
    super_header: SuperHeader, super_header_theme: SuperHeaderThemeLike
) -> None:
    super_header.did_mount()

    assert super_header.title.color == super_header_theme.text.primary
    assert super_header.divider.color == super_header_theme.accent.primary

    for paragraph in _text_controls(super_header):
        assert paragraph.color == super_header_theme.text.secondary


def test_super_header_applies_typography_tokens(
    super_header: SuperHeader, super_header_theme: SuperHeaderThemeLike
) -> None:
    super_header.did_mount()

    assert super_header.title.size == super_header_theme.typography.super_header_title_size
    assert (
        super_header.title.font_family
        == super_header_theme.typography.super_header_title_font_family
    )

    for paragraph in _text_controls(super_header):
        assert paragraph.size == super_header_theme.typography.super_header_body_size
        assert (
            paragraph.font_family
            == super_header_theme.typography.super_header_body_font_family
        )
        assert paragraph.style is not None
        assert paragraph.style.height == super_header_theme.typography.super_header_body_line_height


def test_super_header_falls_back_when_specific_typography_tokens_are_missing() -> None:
    theme = FakeTheme()
    manager = FakeThemeManager(theme)
    header = SuperHeader(
        theme_manager=manager,
        image_src=None,
        nome="Ada",
        texto_inicial="Texto",
    )

    header.did_mount()

    assert header.title.size == theme.typography.h2
    assert header.title.font_family == theme.typography.font_family
    first_paragraph = header.text_list.controls[0]
    assert isinstance(first_paragraph, ft.Text)
    assert first_paragraph.size == theme.typography.body
    assert first_paragraph.font_family == theme.typography.font_family


def test_super_header_does_not_update_before_mount(super_header: SuperHeader) -> None:
    def fail_update():
        raise AssertionError("update should not be called before mount")

    super_header.update = fail_update

    super_header.apply_theme(super_header.theme_manager.theme)

    assert super_header.title.color == super_header.theme_manager.theme.text.primary
