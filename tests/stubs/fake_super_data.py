from collections.abc import Sequence
from typing import Any


class FakeSuperData:
    def __init__(
        self,
        *,
        id: str = "test-hero-1",
        nome: str = "Test Hero",
        image_path: str = "tests/assets/test_image.png",
        timeline_path: str = "tests/assets/test_timeline.png",
        timeline_points: Sequence[Any] | None = None,
        historias: Any = "várias",
    ):
        self.id = id
        self.nome = nome
        self.image_path = image_path
        self.timeline_path = timeline_path
        self.timeline_points = timeline_points or []
        self.historias = historias
