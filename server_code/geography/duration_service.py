# from geopy.geocoders import Nominatim
from geopy import distance
import openrouteservice
from openrouteservice import distance_matrix


# geo_locator = Nominatim(user_agent="bernacki3")
ORS_CLIENT = openrouteservice.Client(key='5b3ce3597851110001cf62485381e55ad54747b7bf1c25343a66d01d')


def calculate_distance_miles(a: tuple[float, float], b: tuple[float, float]) -> int:
    return round(distance.distance(a, b).miles)


# i think ORS wants (Long, Lat)
def get_durations(coordinates: list[tuple]) -> list[list[float, float]]:
    return distance_matrix.distance_matrix(ORS_CLIENT, locations=coordinates)['durations']