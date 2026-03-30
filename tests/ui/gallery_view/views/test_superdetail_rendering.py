import pytest

# from app.components.timeline import ResponsiveTimeline
from galeria.ui.components.super_header import SuperHeader
from galeria.ui.views.super_view import SuperDetail
from tests.harness import FletTestHarness


@pytest.mark.asyncio
async def test_superdetail_renders_header(
    harness: FletTestHarness,
    super_detail: SuperDetail,
):
    """
    Verifica se o header foi renderizado.
    """

    await harness.mount(super_detail)

    assert harness.count(SuperHeader) == 1


# @pytest.mark.asyncio
# async def test_superdetail_renders_timeline(
#     harness: FletTestHarness,
#     super_detail: SuperDetail,
# ):
#     """
#     Verifica se a timeline foi renderizada.
#     """

#     await harness.mount(super_detail)

#     assert harness.count(ResponsiveTimeline) == 1


@pytest.mark.asyncio
async def test_superdetail_has_navigation_buttons(
    harness: FletTestHarness,
    super_detail: SuperDetail,
):
    """
    Verifica se existem botões de navegação.
    """

    await harness.mount(super_detail)

    assert harness.count("IconButton") >= 2
