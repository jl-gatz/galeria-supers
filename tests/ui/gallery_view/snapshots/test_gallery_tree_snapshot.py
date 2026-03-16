import pytest

from tests.harness.flet_harness import FletTestHarness


@pytest.mark.asyncio
async def test_gallery_tree_snapshot(mounted_gallery: FletTestHarness):
    """
    Snapshot da árvore completa da galeria.
    Detecta regressões estruturais.
    """
    mounted_gallery.assert_tree_snapshot("gallery_tree")
