# galeria/ui/components/timeline/controller/timeline_controller.py

import time

from ..models.timeline_point import TimelinePoint
from ..utils.curve_generator import catmull_rom_to_segments
from ..utils.path_builder import build_partial_path
from ..view.timeline_view import TimelineView


class TimelineController:
    WIDTH = 800
    HEIGHT = 300

    def __init__(self, view: "TimelineView"):
        self.view = view
        self.points: list[TimelinePoint] = []
        self.segments = []
        self.progress: float = 0.0
        self.is_animating: bool = False

    # ===============================
    # 🔹 Setup
    # ===============================

    def set_points(self, points: list[TimelinePoint]) -> None:
        if len(points) < 2:
            self.points = []
            self.segments = []
            return

        valid_points = []

        for p in points:
            if (
                isinstance(p.x, (int, float))
                and isinstance(p.y, (int, float))
                and 0.0 <= p.x <= 1.0
                and 0.0 <= p.y <= 1.0
            ):
                # 🔥 ESCALA AQUI
                scaled = TimelinePoint(
                    year=p.year,
                    label=p.label,
                    x=p.x * self.WIDTH,
                    y=p.y * self.HEIGHT,
                )
                valid_points.append(scaled)

        if len(valid_points) < 2:
            self.points = []
            self.segments = []
            return

        self.points = sorted(valid_points, key=lambda p: p.year)

        self.segments = catmull_rom_to_segments(self.points)

    # ===============================
    # 🎬 Animation
    # ===============================

    def start(self, duration: float = 1.5) -> None:
        if not self.segments:
            return

        self.is_animating = True

        steps = 60
        delay = duration / steps

        for i in range(steps + 1):
            if not self.is_animating:
                break

            # 🔹 progresso normalizado
            t = i / steps
            t = max(0.0, min(1.0, t))

            # 🔹 ease-in-out
            progress = t * t * (3 - 2 * t)
            progress = max(0.0, min(1.0, progress))

            self.progress = progress

            # 🔹 gera path seguro
            path = build_partial_path(self.segments, progress)

            # 🔹 atualiza view
            self.view.update_path(path)

            time.sleep(delay)

    def stop(self) -> None:
        self.is_animating = False
