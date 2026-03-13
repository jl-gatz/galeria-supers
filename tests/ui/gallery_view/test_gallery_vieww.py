import pytest

from tests.harness.flet_harness import FletTestHarness


@pytest.mark.asyncio
async def test_gallery_view_mounts(
    mounted_gallery: FletTestHarness,
):
    """Testa se GalleryView monta corretamente."""

    assert mounted_gallery.count("GalleryView") == 1


@pytest.mark.asyncio
async def test_gallery_row_exists(
    mounted_gallery: FletTestHarness,
):
    """Testa se a GalleryRow está presente na árvore."""

    assert mounted_gallery.count("GalleryRow") == 1


@pytest.mark.asyncio
async def test_gallery_row_is_descendant_of_gallery_view(
    mounted_gallery: FletTestHarness,
):
    """Testa se GalleryRow pertence à árvore de GalleryView."""

    gallery = mounted_gallery.one("GalleryView")
    rows = mounted_gallery.find_descendants(gallery, "GalleryRow")

    assert len(rows) == 1


@pytest.mark.asyncio
async def test_gallery_images_exist(
    mounted_gallery: FletTestHarness,
):
    """Testa se existem imagens dentro da galeria."""

    assert mounted_gallery.count("Image") > 0


@pytest.mark.asyncio
async def test_gallery_tree_snapshot(mounted_gallery: FletTestHarness):
    mounted_gallery.assert_tree_snapshot("gallery_tree")
