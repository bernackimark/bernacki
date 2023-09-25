import anvil.facebook.auth
from geography.segment import Segment
from dataclasses import dataclass


@dataclass
class Route:
    duration_seconds: float = 0
    segments: tuple[Segment] = ()

    def __post_init__(self):
        self.duration_seconds = sum([s.duration_seconds for s in self.segments])

    @property
    def segment_cnt(self):
        return len(self.segments)

    @property
    def orig(self):
        return self.segments[0].start

    @property
    def destination(self):
        return self.segments[-1].end

    @property
    def duration_hour_minutes(self) -> str:
        total_minutes = round(round(self.duration_seconds) / 60)
        hours = total_minutes // 60
        minutes = str(total_minutes % 60)
        return f'{hours}:{minutes.zfill(2)}'

    @property
    def points_string(self) -> list:
        points_str = ''
        for idx, s in enumerate(self.segments):
            points_str += f'{s.start.name} to '
            if idx == len(self.segments) - 1:
                points_str += s.end.name
        return points_str
