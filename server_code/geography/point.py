import anvil.email
import anvil.secrets
from dataclasses import dataclass, field


@dataclass
class Point:
    id: int
    # known_place_id: int = field(init=False)
    name: str
    # city: str
    # state: str
    # zip: str
    lat_long: tuple
    orig: bool
    dest: bool

    @property
    def long_lat(self) -> tuple:
        return self.lat_long[1], self.lat_long[0]

    def __str__(self):
        return self.name