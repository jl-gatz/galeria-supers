import pytest

from galeria.ui.components.gallery_row import GalleryRow
from tests.harness import FletTestHarness
from tests.utils.types import HasControls


@pytest.mark.asyncio
async def test_gallery_images_exist(mounted_gallery: FletTestHarness):
    """
    Verifica se existem imagens dentro da galeria.
    """
    assert mounted_gallery.count("ThemedMaskedImage") > 0


@pytest.mark.asyncio
async def test_gallery_row_contains_supers(mounted_gallery: FletTestHarness):
    """
    Verifica se a row contém todos os supers renderizados.
    """
    row = mounted_gallery.one(GalleryRow)
    assert isinstance(row, GalleryRow)
    assert isinstance(row.content, HasControls)

    assert len(row.content.controls) == 4  # Verificar fixture dos supers_sample
