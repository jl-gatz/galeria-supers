# galeria/ui/components/timeline/utils/timeline_mapper.py


from ..models.timeline_point import TimelinePoint


def extract_points_from_super(raw_points) -> list[TimelinePoint]:
    """
    Recebe lista crua (do controller) e converte em TimelinePoint
    """

    points = []

    for item in raw_points:
        # adapte conforme seu formato real
        if isinstance(item, dict):
            x = item.get("x", 0)
            y = item.get("y", 0.5)
            points.append(TimelinePoint(x, y, data=item))

        elif isinstance(item, tuple):
            points.append(TimelinePoint(*item))

        else:
            # fallback defensivo
            points.append(item)

    return points
