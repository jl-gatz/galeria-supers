import pytest

from tests.debug.rich_node import render_node
from tests.debug.rich_query import render_query
from tests.harness import FletTestHarness

pytestmark = pytest.mark.debug


@pytest.mark.asyncio
async def test_debug_tree(mounted_gallery: FletTestHarness) -> None:
    """
    Renderiza a árvore completa da UI.

    Teste usado principalmente para inspeção visual durante
    desenvolvimento.
    """

    mounted_gallery.rich_tree()


@pytest.mark.asyncio
async def test_debug_query_images(mounted_gallery: FletTestHarness) -> None:
    """
    Mostra todas as imagens encontradas na galeria.
    """

    nodes = mounted_gallery.select("ThemedMaskedImage")

    render_query(nodes, title="ThemedMaskedImages in Gallery")

    assert len(nodes) > 0


@pytest.mark.asyncio
async def test_debug_first_gallery_row(mounted_gallery: FletTestHarness) -> None:
    """
    Inspeciona uma GalleryRow específica.
    """

    row = mounted_gallery.one("GalleryRow")

    render_node(row)

    assert row is not None


@pytest.mark.asyncio
async def test_debug_nested_query(mounted_gallery: FletTestHarness) -> None:
    """
    Testa query descendente.
    """

    nodes = mounted_gallery.select("GalleryRow ThemedMaskedImage")

    render_query(nodes, title="ThemedMaskedImages inside GalleryRow")

    assert len(nodes) > 0


@pytest.mark.asyncio
async def test_debug_gallery_structure(mounted_gallery: FletTestHarness) -> None:
    """
    Renderiza árvore e faz verificação mínima estrutural.
    """

    mounted_gallery.rich_tree()

    gallery_rows = mounted_gallery.select("GalleryRow")

    assert len(gallery_rows) >= 1
