import pytest

from tests.harness import FletTestHarness


@pytest.mark.debug
@pytest.mark.asyncio
async def test_debug_gallery_tree(mounted_gallery: FletTestHarness):
    """
    Mostra a árvore completa de controles.
    """
    mounted_gallery.rich_tree()


@pytest.mark.debug
@pytest.mark.asyncio
async def test_debug_gallery_images_query(mounted_gallery: FletTestHarness):
    """
    Mostra todas as imagens dentro da GalleryRow.
    """
    mounted_gallery.rich_query("GalleryRow Image")
