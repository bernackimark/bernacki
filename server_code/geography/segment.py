from dataclasses import dataclass
from geography.point import Point


@dataclass
class Segment:
    id: int
    start: Point
    end: Point
    duration_seconds: float = 0
