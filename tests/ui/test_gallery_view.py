import pytest

from galeria.ui.components.gallery_row import GalleryRow
from tests.harness.flet_harness import FletTestHarness


@pytest.mark.asyncio
async def test_gallery_view_structure(mounted_gallery: FletTestHarness):
    """
    Verifica se GalleryRow está contida na árvore da GalleryView
    """

    gallery = mounted_gallery.one("GalleryView")

    rows = mounted_gallery.find_descendants(gallery, "GalleryRow")

    assert len(rows) == 1


# @pytest.mark.asyncio
# async def test_gallery_structure_tree(mounted_gallery: FletTestHarness):
#     """
#     Verifica a estrutura interna da galeria
#     """
#     assert mounted_gallery.count_path(["GalleryRow", "Image"]) == 12


# @pytest.mark.asyncio
# async def test_gallery_renders_all_supers(mounted_gallery: FletTestHarness):
#     """
#     Verifica se todos os supers foram renderizados
#     """
#     mounted_gallery.assert_list_rendered(GalleryRow, 12)
#     assert mounted_gallery.count_select("GalleryRow Image") == 12


@pytest.mark.asyncio
async def test_gallery_row_contains_supers(mounted_gallery: FletTestHarness):
    """
    Verifica se a row contém os supers
    """
    row = mounted_gallery.one(GalleryRow)

    assert len(row.controls) == 12


# @pytest.mark.asyncio
# async def test_selector_engine(mounted_gallery: FletTestHarness):
#     """
#     Testa o engine de seletores
#     """
#     assert mounted_gallery.count_select("GalleryRow") == 1
#     assert mounted_gallery.count_select("GalleryRow Image") == 12


# @pytest.mark.asyncio
# async def test_logos_row(mounted_gallery: FletTestHarness):
#     """
#     Verifica se os logos foram renderizados corretamente
#     """
#     logos = mounted_gallery.find_where(
#         lambda n: n.__class__.__name__ == "Image" and "logo" in n.src
#     )

#     assert len(logos) == 2
