import anvil.email
import anvil.secrets
import requests

BASE_URL_1 = "https://api.geoapify.com/v1/geocode/search?text="
BASE_URL_2 = "&format=json&apiKey="
API_KEY = '8e11b4f1b14242409377a74e14aec790'


def get_lat_long(locations: tuple[str, tuple]) -> list[tuple[float, float]]:
    lat_lon_list: list[tuple[float, float]] = []
    for l in locations:
        if l[1]:
            lat_lon_list.append(l[1])  # if the lat_long is provided, skip the API and append to list
        else:
            url = BASE_URL_1 + l[0] + BASE_URL_2 + API_KEY
            res = requests.get(url).json()['results'][0]
            lat_lon_list.append((res['lat'], res['lon']))
    return lat_lon_list