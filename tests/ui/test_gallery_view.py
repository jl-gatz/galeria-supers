import pytest

from galeria.ui.components.gallery_row import GalleryRow
from galeria.ui.views.gallery_view import GalleryView
from tests.harness.flet_harness import FletTestHarness


@pytest.mark.asyncio
async def test_gallery_view_structure(harness: FletTestHarness, gallery_view: GalleryView):
    """
    Testa se o layout básico de GalleryView foi montado
    """
    await harness.mount(gallery_view)

    harness.print_tree()

    rows = harness.find(GalleryRow)

    assert len(rows) > 0


@pytest.mark.asyncio
async def test_gallery_renders_all_supers(harness: FletTestHarness, gallery_view: GalleryView):
    """
    Testa se todos os supers foram renderizados corretamente
    """
    await harness.mount(gallery_view)

    rows = harness.find(GalleryRow)

    gallery_row = rows[0]

    images = list(gallery_row.controls)

    assert len(rows) == 1
    assert len(rows[0].controls) == 12
    assert len(images) == 12


# @pytest.mark.asyncio
# async def test_gallery_contains_super_names(harness: FletTestHarness, gallery_view: GalleryView):
#     """
#     Teste de conteúdo por nome do super
#     """
#     await harness.mount(gallery_view)

#     control = harness.find("Super 3")

#     assert control is not None


@pytest.mark.asyncio
async def test_gallery_rows_distribution(harness: FletTestHarness, gallery_view: GalleryView):
    """
    Teste de layout; verifica se foi criada uma gallery row
    """
    await harness.mount(gallery_view)

    rows = harness.find(GalleryRow)

    assert len(rows) >= 1


@pytest.mark.asyncio
async def test_gallery_tree_snapshot(harness: FletTestHarness, gallery_view: GalleryView):
    """
    Função para salvar a saída da árvore de componentes
    """
    await harness.mount(gallery_view)

    harness.print_tree()
