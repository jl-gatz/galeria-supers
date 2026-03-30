from unittest.mock import PropertyMock, patch

import pytest

from galeria.ui.views.super_view import SuperDetail
from tests.harness import FletTestHarness


@pytest.mark.asyncio
async def test_superdetail_tree_snapshot(
    harness: FletTestHarness,
    super_detail: SuperDetail,
):
    with patch.object(type(super_detail), "page", new_callable=PropertyMock) as mock_page:
        mock_page.return_value = harness.page

        await harness.mount(super_detail)

        # lifecycle
        super_detail.did_mount()

        # visibilidade
        super_detail.opacity = 1

        harness.assert_tree_snapshot("superdetail_tree")
