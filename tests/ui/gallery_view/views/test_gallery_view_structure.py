import pytest

from tests.harness.flet_harness import FletTestHarness


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
