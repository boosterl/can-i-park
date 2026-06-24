import requests

from aiohttp import ClientSession
from can_i_park.api import get_station, StationNotFoundError

API_URL = "https://data.stad.gent/api/explore/v2.1/catalog/datasets/bezetting-parkeergarages-real-time/records?limit=20"

# Map each parking page URL to a list of EnBW numeric station IDs.
# Replace the empty lists with the correct EnBW station IDs for each parking.
parking_station_ids = {
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-savaan": ["470331"],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-vrijdagmarkt": ["470338", "1245207"],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-reep": ["470333", "470332", "1981322"],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-sint-pietersplein": ["470335", "2047189"],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-ramen": ["470340", "470339", "2046496"],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-tolhuis": ["2041154", "470334"],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-sint-michiels": ["470337", "2104082"],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-ledeberg": ["470329"],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-het-getouw": ["470336"],
    "https://www.belgiantrain.be/nl/station-information/car-or-bike-at-station/b-parking/my-b-parking/gent-dampoort": ["470502"],
    "https://be.parkindigo.com/nl/car-park/parking-dok-noord": ["198905", "1042722"],
    "https://stad.gent/nl/loop/mobiliteit-loop#Parkeerterreinen_Stad_Gent": [],
    "https://www.belgiantrain.be/nl/station-information/car-or-bike-at-station/b-parking/my-b-parking/gentstpieters": ["470351", "470828", "823338"],
}


async def get_charging_status(parking_id, api_key):
    stations = parking_station_ids.get(parking_id, list())
    async with ClientSession() as session:
        total_charge_points = 0
        available_charge_points = 0
        for station_id in stations:
            station = await get_station(session, api_key, station_id)
            total_charge_points += station["numberOfChargePoints"]
            available_charge_points += station["availableChargePoints"]
        return available_charge_points, total_charge_points


def fetch_parking_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        raise Exception("Failed to fetch data from API")
