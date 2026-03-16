import pytest

from galeria.ui.views.super_view import SuperDetail
from tests.harness.flet_harness import FletTestHarness


@pytest.mark.debug
@pytest.mark.asyncio
async def test_debug_superdetail_tree(
    harness: FletTestHarness,
    super_detail: SuperDetail,
):
    """
    Mostra a árvore completa do SuperDetail.
    """

    await harness.mount(super_detail)

    harness.rich_tree()


@pytest.mark.debug
@pytest.mark.asyncio
async def test_debug_superdetail_summary(
    harness: FletTestHarness,
    super_detail: SuperDetail,
):
    """
    Mostra resumo da árvore.
    """

    await harness.mount(super_detail)

    harness.rich_query()
