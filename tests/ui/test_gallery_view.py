import pytest

from galeria.ui.components.gallery_row import GalleryRow
from galeria.ui.views.gallery_view import GalleryView
from tests.harness.flet_harness import FletTestHarness


@pytest.mark.asyncio
async def test_gallery_view_structure(harness: FletTestHarness, gallery_view: GalleryView):

    await harness.mount(gallery_view)

    harness.debug_tree()

    rows = harness.find(GalleryRow)

    assert len(rows) > 0
