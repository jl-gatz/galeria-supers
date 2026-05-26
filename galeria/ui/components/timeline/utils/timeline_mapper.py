import math

from ..models.timeline_point import TimelinePoint


def extract_points_from_super(raw_points: list[dict[str, float]]) -> list[TimelinePoint]:
    """
    Recebe lista crua (do controller) e converte em TimelinePoint
    """

    points = []

    for item in raw_points:
        # adapte conforme seu formato real
        if isinstance(item, dict):
            x = item.get("x", 0)
            y = item.get("y", 0.5)
            points.append(
                TimelinePoint(
                    x,
                    y,
                    data=item,
                    id=item.get("id"),
                    year=item.get("year"),
                    label=item.get("label", ""),
                    text=item.get("text", ""),
                )
            )

        elif isinstance(item, tuple):
            points.append(TimelinePoint(*item))

        else:
            # fallback defensivo
            points.append(item)

    return points


def map_indexed_points_to_canvas(points, width, height):
    mapped = []

    for index, point in enumerate(points):
        try:
            x = float(point.x) * width
            y = float(point.y) * height

            if not (math.isfinite(x) and math.isfinite(y)):
                continue

            mapped.append((index, x, y))
        except Exception:
            continue

    return mapped


def map_points_to_canvas(points, width, height):
    return [(x, y) for _, x, y in map_indexed_points_to_canvas(points, width, height)]
