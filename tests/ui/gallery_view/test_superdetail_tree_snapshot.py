import pytest

from galeria.ui.views.super_view import SuperDetail
from tests.harness import FletTestHarness


@pytest.mark.asyncio
async def test_superdetail_tree_snapshot(
    harness: FletTestHarness,
    super_detail: SuperDetail,
):
    await harness.mount(super_detail)

    # 🔧 garantir lifecycle
    super_detail.did_mount()

    # 🔧 garantir visibilidade
    super_detail.opacity = 1

    harness.assert_tree_snapshot("superdetail_tree")
