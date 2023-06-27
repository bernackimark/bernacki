import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class KnownPoint:
    known_point_id: str = field(init=False)
    known_collection_id: int
    name: str
    lat_long: tuple
    # extras: dict = field(default_factory={})  # this can soak up: city, state, zip, etc.
    # HAVING A PROBLEM W EXTRAS!!!

    def __post_init__(self):
        self.known_point_id = str(uuid.uuid4())


@dataclass
class KnownCollection:
    known_collection_id: int
    collection_name: str
    email: str
    known_points: list[KnownPoint]
    created_ts: datetime = datetime.now()


@anvil.server.callable
def create_known_points(p_list: list[dict], collection_id: int) -> list[KnownPoint]:
    return [KnownPoint(known_collection_id=collection_id, name=p['name'], lat_long=p['lat_long']) for p in p_list]


@anvil.server.callable
def create_known_collection_and_points(coll_name: str, email: str, points: list[dict]) -> None:
    kc = KnownCollection(known_collection_id=get_next_known_collection_id(), collection_name=coll_name, email=email,
                         known_points=known_points)
    app_tables.geo_known_collections.add_row(collection_name=coll_name, created_ts=datetime.now(), email=email, known_collection_id=get_next_known_collection_id())
    known_points = create_known_points(points, get_row_count_known_collection())
    for p in known_points:
      app_tables.geo_known_points.add_row(known_point_id=p.known_point_id, known_collection_id=p.known_collection_id, name=p.name, lat_long=p.lat_long)


# anvil-specific
@anvil.server.callable
def get_user_known_collections(email: str = 'bernackimark@gmail.com') -> list[tuple[str, int]]:
    return [(r['collection_name'], r['known_collection_id']) for r in app_tables.geo_known_collections.search() if r['email'] in [email, 'all']]


# anvil-specific
@anvil.server.callable
def get_known_points(known_collection_id) -> list[dict]:
    return [{'name': r['name'], 'lat_long': r['lat_long']} for r in app_tables.geo_known_points.search(known_collection_id=known_collection_id)]
      

# anvil-specific
def get_next_known_collection_id() -> int:
    return max([r['known_collection_id'] for r in app_tables.geo_known_collections.search()]) + 1

# anvil-specific
def get_row_count_known_collection() -> int:
    return len(app_tables.geo_known_collections.search())
