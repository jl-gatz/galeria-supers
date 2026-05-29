# tests/factories/super_detail_factory.py

from collections.abc import Callable, Sequence

from galeria.domain.protocols.theme_manager_like import ThemeManagerLike
from galeria.ui.controllers.super_detail_controller import SuperDetailController
from galeria.ui.theme.manager import StaticThemeManager
from galeria.ui.theme.models import Theme
from galeria.ui.theme.themes import CCUEC_THEME
from galeria.ui.views.super_view import SuperDetail
from tests.fixtures.super_data import FakeSuperData, TimelinePointInput

# from tests.fakes.fake_super_data import FakeSuperData
# from ui.controllers.super_detail_controller import SuperDetailController
# from ui.views.super_detail import SuperDetail


class SuperDetailFactory:
    @staticmethod
    def build(
        *,
        id: str = "test-hero-1",
        nome: str = "Test Hero",
        image_path: str = "tests/assets/test_image.png",
        timeline_path: str = "tests/assets/test_timeline.png",
        timeline_points: Sequence[TimelinePointInput] | None = None,
        historias: Sequence[str] | None = None,
        periodo: str | None = None,
        controller: SuperDetailController | None = None,
        theme_manager: ThemeManagerLike | None = None,
        theme: Theme | None = None,
        on_request_close: Callable[[], None] | None = None,
        auto_start: bool = True,
    ) -> "SuperDetail":

        if historias is None:
            historias = ["História 1", "História 2"]

        selected_timeline_points = timeline_points or []

        if theme is None:
            theme = CCUEC_THEME

        if theme_manager is None:
            theme_manager = StaticThemeManager(theme)

        if on_request_close is None:

            def noop_request_close() -> None:
                pass

            selected_on_request_close = noop_request_close
        else:
            selected_on_request_close = on_request_close

        super_data = FakeSuperData(
            id=id,
            nome=nome,
            foto=image_path,
            timeline=timeline_path,
            timeline_points=selected_timeline_points,
            historias=historias,
            periodo=periodo,
        )

        if controller is None:
            controller = SuperDetailController(super_data)

        view = SuperDetail(
            controller=controller,
            on_request_close=selected_on_request_close,
            theme_manager=theme_manager,
        )

        if not auto_start:
            view.auto_close.stop()

        return view
