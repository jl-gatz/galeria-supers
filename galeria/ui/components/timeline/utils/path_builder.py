# galeria/ui/components/timeline/utils/path_builder.py
"""Construção de caminhos visuais a partir de pontos da timeline."""


import math
from collections.abc import Sequence

Coord = tuple[float, float]


class PathBuilder:
    """Gera curvas lineares, suaves ou decorativas para o renderer."""

    def __init__(self, mode: str = "smooth", tension: float = 0.5):
        self.mode = mode
        self.tension = tension

    # =========================================================
    # 🛡️ PROTEÇÕES
    # =========================================================

    def _is_valid(self, x: float | None, y: float | None) -> bool:
        """Valida coordenadas antes de incluí-las em uma curva."""
        return (
            x is not None
            and y is not None
            and not math.isnan(x)
            and not math.isnan(y)
            and math.isfinite(x)
            and math.isfinite(y)
        )

    def _sanitize_points(self, points: Sequence[Coord]) -> list[Coord]:
        """Remove pontos com coordenadas inválidas."""
        return [p for p in points if self._is_valid(p[0], p[1])]

    # =========================================================
    # 🎯 ENTRYPOINT
    # =========================================================

    def build_path(self, points: Sequence[Coord]) -> list[Coord]:
        """Constrói o caminho final conforme o modo configurado."""
        # print("RAW:", points)

        pts = self._sanitize_points(points)

        # print("SANITIZED:", pts)

        if len(pts) < 2:
            return pts

        if self.mode == "linear":
            return pts

        if self.mode == "smooth":
            return self._catmull_rom(pts)

        if self.mode == "infinity":
            return self._infinity_curve(pts)

        return pts

    # =========================================================
    # 🧵 CATMULL-ROM SPLINE (suave)
    # =========================================================

    def _catmull_rom(self, pts: Sequence[Coord], segments: int = 20) -> list[Coord]:
        """Gera uma curva Catmull-Rom suave entre os pontos."""
        curve: list[Coord] = []

        for i in range(len(pts) - 1):
            p0 = pts[i - 1] if i > 0 else pts[i]
            p1 = pts[i]
            p2 = pts[i + 1]
            p3 = pts[i + 2] if i + 2 < len(pts) else pts[i + 1]

            for t in range(segments):
                t /= segments
                t2 = t * t
                t3 = t2 * t

                x = 0.5 * (
                    (2 * p1[0])
                    + (-p0[0] + p2[0]) * t
                    + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                    + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3
                )

                y = 0.5 * (
                    (2 * p1[1])
                    + (-p0[1] + p2[1]) * t
                    + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                    + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3
                )

                if self._is_valid(x, y):
                    curve.append((x, y))

        curve.append(pts[-1])
        return curve

    # =========================================================
    # ♾️ CURVA INFINITA (estética)
    # =========================================================

    def _infinity_curve(self, pts: Sequence[Coord], segments: int = 40) -> list[Coord]:
        """Gera uma curva decorativa com oscilação entre os pontos."""
        curve: list[Coord] = []

        for i in range(len(pts) - 1):
            x1, y1 = pts[i]
            x2, y2 = pts[i + 1]

            for t in range(segments):
                alpha = t / segments

                x = x1 + (x2 - x1) * alpha

                # 🔥 assinatura visual
                amplitude = min(40, abs(x2 - x1) * 0.3)

                y = y1 + (y2 - y1) * alpha + math.sin(alpha * math.pi * 2) * amplitude

                if self._is_valid(x, y):
                    curve.append((x, y))

        curve.append(pts[-1])
        return curve
