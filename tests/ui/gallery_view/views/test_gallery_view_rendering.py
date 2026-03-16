import pytest

from galeria.ui.components.gallery_row import GalleryRow
from tests.harness import FletTestHarness


@pytest.mark.asyncio
async def test_gallery_images_exist(mounted_gallery: FletTestHarness):
    """
    Verifica se existem imagens dentro da galeria.
    """
    assert mounted_gallery.count("Image") > 0


@pytest.mark.asyncio
async def test_gallery_row_contains_supers(mounted_gallery: FletTestHarness):
    """
    Verifica se a row contém todos os supers renderizados.
    """
    row = mounted_gallery.one(GalleryRow)

    assert len(row.controls) == 12
