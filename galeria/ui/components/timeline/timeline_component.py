# galeria/ui/components/timeline/timeline_component.py

from typing import Any

from .controller.timeline_controller import TimelineController
from .models.timeline_point import TimelinePoint
from .view.timeline_view import TimelineView


class TimelineComponent:
    def __init__(self, timeline_data):
        self.view = TimelineView()
        self.controller = TimelineController(self.view)

        # 🔥 suporte a dict OU lista
        if isinstance(timeline_data, list):
            # veio direto como timeline_points
            points_data = timeline_data
            self._image_src = None

        elif isinstance(timeline_data, dict):
            points_data = timeline_data.get("points", [])
            self._image_src = timeline_data.get("image_src")

        else:
            points_data = []
            self._image_src = None

        # print("RAW DATA:", timeline_data)
        # print("POINTS DATA:", points_data)

        points = self._parse_points(points_data)

        print("POINTS PARSED:", len(points))  # 🔥 debug

        self.controller.set_points(points)

    def _parse_points(self, data: list[dict[str, Any]]) -> list[TimelinePoint]:
        return [
            TimelinePoint(
                year=p["year"],
                label=p["label"],
                x=p["x"],
                y=p["y"],
            )
            for p in data
        ]

    def build(self):
        return self.view.build()

    def animate(self) -> None:
        self.controller.start()
