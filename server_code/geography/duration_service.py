import anvil.secrets
# from geopy.geocoders import Nominatim
from geopy import distance
import openrouteservice
from openrouteservice import distance_matrix

# geo_locator = Nominatim(user_agent=anvil.secrets.get_secret("NOMINATIM_USER_KEY"))

def calculate_distance_miles(a: tuple[float, float], b: tuple[float, float]) -> int:
    return round(distance.distance(a, b).miles)


# i think ORS wants (Long, Lat)
def get_durations(coordinates: list[tuple]) -> list[list[float, float]]:
    ors_client = openrouteservice.Client(key=anvil.secrets.get_secret("ORS_KEY"))
    return distance_matrix.distance_matrix(ors_client, locations=coordinates)['durations']