from typing import cast

import flet as ft
import pytest

from galeria.domain import SuperService
from galeria.ui.theme.manager import ThemeManager
from galeria.ui.theme.themes import CCUEC_THEME, DETIC_THEME
from galeria.ui.views.gallery_view import GalleryView
from tests.harness import FletTestHarness
from tests.stubs.fake_page import FakePage


@pytest.mark.asyncio
async def test_gallery_view_mounts(mounted_gallery: FletTestHarness):
    """
    Testa se GalleryView monta corretamente.
    """
    assert mounted_gallery.count("GalleryView") == 1


@pytest.mark.asyncio
async def test_gallery_row_exists(mounted_gallery: FletTestHarness):
    """
    Verifica se a GalleryRow existe na árvore.
    """
    assert mounted_gallery.count("GalleryRow") == 1


@pytest.mark.asyncio
async def test_gallery_row_is_descendant_of_gallery_view(
    mounted_gallery: FletTestHarness,
):
    """
    Verifica se GalleryRow pertence à árvore da GalleryView.
    """
    gallery = mounted_gallery.one("GalleryView")

    rows = mounted_gallery.find_descendants(
        gallery,
        "GalleryRow",
    )

    assert len(rows) == 1


def test_gallery_title_updates_when_theme_changes(
    fake_page: FakePage, service: SuperService
) -> None:
    theme_manager = ThemeManager(CCUEC_THEME)
    gallery = GalleryView(
        service=service,
        root_layout=None,
        page=cast(ft.Page, fake_page),
        theme=theme_manager,
    )

    assert gallery.title_text is not None
    assert gallery.title_text.value == CCUEC_THEME.gallery.title

    theme_manager.set_theme_for_era("detic")
    gallery._apply_theme(theme_manager.theme)

    assert gallery.title_text.value == DETIC_THEME.gallery.title
