import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# from fake_front_end import incoming_data
from geography.geocoding import get_lat_long
from geography.point import Point
from geography import duration_service as ds
from geography.segment import Segment
from geography.route import Route
from itertools import permutations


# STEP 1: GET DATA FROM FRONT END & CREATE A LIST OF POINTS
def create_points(data: list[dict], ll: list[tuple[float, float]]) -> list[Point]:
    # right now, i'm getting a name (text), orig, dest ... not a structured request (name, city, state, zip, country...)
    return [Point(id=idx, name=p['name'], lat_long=ll[idx],
                  orig=p['orig'], dest=p['dest']) for idx, p in enumerate(data)]


# STEP 2: CREATE THE SEGMENTS
def generate_segments(points: list[Point]) -> list[Segment]:
    # example: if you have points [1, 2, 3, 4], the orig is 1, the end is 4, the only seven legit segments are:
    # (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 2), (3, 4)
    # i suppose if there is no orig and destination declared, then you'd have 12 legit segments
    created_segments = []
    for b_idx, b in enumerate(points):
        if not b.dest:
            for e_idx, e in enumerate(points):
                if not e.orig:
                    if b_idx != e_idx:
                        created_segments.append(Segment(id=len(created_segments), start=b, end=e))
    return created_segments


# STEP 3: CALL THE DISTANCE SERVICE TO GET THE DISTANCES
def generate_distance_matrix(list_of_points: list[Point]) -> list[list[float]]:
    return ds.get_durations([p.long_lat for p in list_of_points])  # ORS takes long_lat
    # return [[0.0, 1134.51, 392.74, 1319.48],
    #         [1141.72, 0.0, 1033.58, 1564.67],
    #         [374.17, 1067.07, 0.0, 1312.37],
    #         [1249.03, 1607.08, 1303.54, 0.0]]


# STEP 4: APPEND THE DISTANCES TO THE SEGMENTS
def append_distances_to_segments(segments_list: list[Segment], distances_list: list[list[float]]) -> list[Segment]:
    segments_w_distances = []
    for s in segments_list:
        for o_idx, p in enumerate(distances_list):
            for e_idx, value in enumerate(p):
                if s.start.id == o_idx and s.end.id == e_idx:
                    segments_w_distances.append(Segment(id=s.id, start=s.start, end=s.end, duration_seconds=value))
    return segments_w_distances


# STEP 5: CREATE THE ROUTES
# NOTE: THIS PRESENTLY ONLY SUPPORTS THE ORIG & DESTINATION BEING DIFFERENT ... NO ROUND-TRIPS !!!
def create_routes(segments_list: list[Segment], count_of_points: int) -> list[Route]:
    # for points [0, 1, 2, 3], orig = 0 & destination = 3, there are only two valid routes:
    # [(0, 1), (1, 2), (2, 3)], [(0, 2), (2, 1), (1, 3)]

    # generate every permutation possible of length count_of_points - 1, probably not very performant !!!
    segment_cnt = count_of_points - 1
    all_perms: list[tuple[Segment]] = list(permutations(segments_list, segment_cnt))
    valid_routes: list[tuple[Segment]] = get_valid_routes(all_perms, segment_cnt)
    return [Route(segments=vr) for vr in valid_routes]


def get_valid_routes(all_possible_route_perms: list[tuple[Segment]], segment_cnt: int) -> list[tuple[Segment]]:
    # rule #1: the start of the first segment must be the orig & the end of the last segment must be the destination
    routes_tmp_1 = [r for r in all_possible_route_perms if r[0].start.orig and r[segment_cnt - 1].end.dest]
    # rule #2: a segment's end must be the next segment's begin
    routes_tmp_2 = []
    for r in routes_tmp_1:
        is_route_invalid = False
        for idx, s in enumerate(r):
            if idx <= segment_cnt - 2:
                if r[idx].end.id != r[idx+1].start.id:
                    is_route_invalid = True
        if not is_route_invalid:
            routes_tmp_2.append(r)
    return routes_tmp_2


def run_geography(data: list[dict]) -> list[dict]:
    lat_longs: list[tuple[float, float]] = get_lat_long([(p['name'], p['lat_long']) for p in data])
    # lat_longs: list[tuple[float, float]] = [(41.6616108, -72.7967357), (41.52602295, -72.75613792979621), (41.6485533, -72.77513066618887), (41.7689809, -72.6733028)]
    points: list[Point] = create_points(data, lat_longs)
    segments_no_distances: list[Segment] = generate_segments(points)
    distances: list[list[float]] = generate_distance_matrix(points)
    # distances: list[list[float]] = [[0.0, 1134.51, 392.74, 1319.48], [1141.72, 0.0, 1033.58, 1564.67], [374.17, 1067.07, 0.0, 1312.37], [1249.03, 1607.08, 1303.54, 0.0]]
    segments: list[Segment] = append_distances_to_segments(segments_no_distances, distances)
    routes: list[Route] = create_routes(segments, len(points))
    return [{'points_string': r.points_string, 'duration': r.duration_hour_minutes, 'lat_longs': lat_longs} for r in routes]


def run_geography_no_api_calls(data: list[dict]) -> list[dict]:
    # lat_longs: list[tuple[float, float]] = get_lat_long([(p['name'], p['lat_long']) for p in data])
    lat_longs: list[tuple[float, float]] = [(41.6616108, -72.7967357), (41.52602295, -72.75613792979621), (41.6485533, -72.77513066618887), (41.7689809, -72.6733028)]
    points: list[Point] = create_points(data, lat_longs)
    segments_no_distances: list[Segment] = generate_segments(points)
    # distances: list[list[float]] = generate_distance_matrix(points)
    distances: list[list[float]] = [[0.0, 1134.51, 392.74, 1319.48], [1141.72, 0.0, 1033.58, 1564.67], [374.17, 1067.07, 0.0, 1312.37], [1249.03, 1607.08, 1303.54, 0.0]]
    segments: list[Segment] = append_distances_to_segments(segments_no_distances, distances)
    routes: list[Route] = create_routes(segments, len(points))
    return [{'points_string': r.points_string, 'duration': r.duration_hour_minutes, 'lat_longs': lat_longs} for r in routes]
