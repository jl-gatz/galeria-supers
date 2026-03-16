import pytest

from galeria.ui.views.super_view import SuperDetail
from tests.harness import FletTestHarness


@pytest.mark.asyncio
async def test_superdetail_tree_snapshot(
    harness: FletTestHarness,
    super_detail: SuperDetail,
):
    """
    Snapshot da árvore completa do SuperDetail.
    """

    await harness.mount(super_detail)

    harness.assert_tree_snapshot("superdetail_tree")
