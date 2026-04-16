# galeria/ui/components/timeline/models/timeline_point.py


# @dataclass
# class TimelinePoint:
#     year: int
#     label: str
#     x: float  # 0..1
#     y: float  # 0..1


class TimelinePoint:
    def __init__(self, x: float, y: float, data=None):
        self.x = x
        self.y = y
        self.data = data  # futuro: label, evento, etc
