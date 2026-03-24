import pytest

from galeria.ui.views.gallery_view import GalleryView
from tests.harness.flet_harness import FletTestHarness
from tests.utils.snapshot import assert_tree_snapshot


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


def test_gallery_snapshot(snapshot, fake_page, fake_root, fake_service):
    view = GalleryView(
        page=fake_page,
        service=fake_service,
        root_layout=fake_root,
        logo_detic="detic.png",
        logo_unicamp="unicamp.png",
    )

    assert_tree_snapshot(view, snapshot)
