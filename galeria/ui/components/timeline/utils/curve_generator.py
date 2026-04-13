# galeria/ui/components/timeline/utils/curve_generator.py


from ..models.timeline_point import TimelinePoint

Segment = dict[str, tuple[float, float]]


def catmull_rom_to_segments(points: list[TimelinePoint], tension: float = 1.0) -> list[Segment]:
    segments: list[Segment] = []

    if len(points) < 2:
        return segments

    for i in range(len(points) - 1):
        p0 = points[i - 1] if i > 0 else points[i]
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else p2

        x0, y0 = p0.x, p0.y
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        x3, y3 = p3.x, p3.y

        cp1x = x1 + (x2 - x0) / 6 * tension
        cp1y = y1 + (y2 - y0) / 6 * tension

        cp2x = x2 - (x3 - x1) / 6 * tension
        cp2y = y2 - (y3 - y1) / 6 * tension

        segments.append(
            {
                "start": (x1, y1),
                "cp1": (cp1x, cp1y),
                "cp2": (cp2x, cp2y),
                "end": (x2, y2),
            }
        )

    return segments
