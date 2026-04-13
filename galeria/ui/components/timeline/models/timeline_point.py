# galeria/ui/components/timeline/models/timeline_point.py

from dataclasses import dataclass


@dataclass
class TimelinePoint:
    year: int
    label: str
    x: float  # 0..1
    y: float  # 0..1
