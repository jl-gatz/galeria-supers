# tests/factories/super_detail_factory.py

from collections.abc import Callable, Sequence
from typing import Any, Optional

from galeria.ui.controllers.super_detail_controller import SuperDetailController
from galeria.ui.views.super_view import SuperDetail
from tests.fixtures.super_data import FakeSuperData

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
        timeline_points: Sequence[Any] | None = None,
        historias: Sequence[str] | None = None,
        controller: Optional["SuperDetailController"] = None,
        on_request_close: Callable[[], None] | None = None,
        auto_start: bool = True,
    ) -> "SuperDetail":

        # 🧼 Defaults seguros
        if historias is None:
            historias = ["História 1", "História 2"]

        if timeline_points is None:
            timeline_points = []

        if on_request_close is None:

            def on_request_close():
                pass

        # 🧪 Fake data
        super_data = FakeSuperData(
            id=id,
            nome=nome,
            foto=image_path,
            timeline=timeline_path,
            timeline_points=timeline_points,
            historias=historias,
        )

        # ⚙️ Controller (permite override!)
        if controller is None:
            controller = SuperDetailController(super_data)

        # 🎨 View
        view = SuperDetail(
            controller=controller,
            on_request_close=on_request_close,
        )

        if not auto_start:
            view.auto_close.stop()

        return view
