# tests/factories/super_detail_factory.py

from galeria.ui.views.super_view import SuperDetail
from tests.fixtures.super_data import FakeSuperData


class SuperDetailFactory:
    @staticmethod
    def build(
        *,
        id="test-hero-1",
        nome="Test Hero",
        image_path="tests/assets/test_image.png",
        timeline_path="tests/assets/test_timeline.png",
        timeline_points=None,
        historias="várias",
        on_request_close=None,
    ) -> SuperDetail:

        if on_request_close is None:

            def on_request_close():
                pass

        super_data = FakeSuperData(
            id=id,
            nome=nome,
            image_path=image_path,
            timeline_path=timeline_path,
            timeline_points=timeline_points,
            historias=historias,
        )

        return SuperDetail(
            super_data=super_data,
            image_path=image_path,
            timeline_path=timeline_path,
            on_request_close=on_request_close,
        )
