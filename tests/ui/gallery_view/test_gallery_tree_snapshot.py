from collections.abc import Callable
from pathlib import Path
from typing import cast

import flet as ft
import pytest

from galeria.ui.layout import RootLayout
from galeria.ui.views.gallery_view import GalleryView
from tests.harness.flet_harness import FletTestHarness
from tests.stubs import FakePage
from tests.stubs.fake_root import FakeRoot
from tests.stubs.fake_super_service import FakeSuperService
from tests.stubs.fake_theme_manager import FakeThemeManager
from tests.utils.snapshot import assert_tree_snapshot
from tests.utils.types import SnapshotLike


@pytest.mark.asyncio
async def test_gallery_tree_snapshot(mounted_gallery: FletTestHarness):
    """
    Snapshot da árvore completa da galeria.
    Detecta regressões estruturais.
    """
    mounted_gallery.assert_tree_snapshot("gallery_tree")


# ==========================================
# SNAPSHOT TEST
# ==========================================


def test_gallery_snapshot(
    snapshot: SnapshotLike,
    fake_page: FakePage,
    fake_root: FakeRoot,
    fake_service: FakeSuperService,
    fake_theme_manager: FakeThemeManager,
    mounted: Callable[[ft.Control], ft.Control],
) -> None:
    view = GalleryView(
        page=cast(ft.Page, fake_page),
        service=fake_service,
        root_layout=cast(RootLayout, fake_root),
        theme=fake_theme_manager,
        logo_detic=Path("detic.png"),
        logo_unicamp=Path("unicamp.png"),
    )

    mounted(view)

    assert_tree_snapshot(view, snapshot)
