import requests

from aiohttp import ClientSession
from shellrecharge import Api, LocationEmptyError, LocationValidationError

API_URL = "https://data.stad.gent/api/explore/v2.1/catalog/datasets/bezetting-parkeergarages-real-time/records?limit=20"
parking_station_ids = {
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-savaanstraat": [
        "BELOC003065"
    ],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-vrijdagmarkt": [
        "BELOC003061",
    ],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-reep": [
        "BELOC003063",
    ],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-sint-pietersplein": [
        "BELOC003067",
    ],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-ramen": [
        "BELOC003062",
    ],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-tolhuis": [
        "BELOC003066",
    ],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-sint-michiels": [
        "BELOC003064",
    ],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-ledeberg": [
        "BELOC003068"
    ],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-het-getouw": [
        "BELOC003069"
    ],
    "https://www.belgiantrain.be/nl/station-information/car-or-bike-at-station/b-parking/my-b-parking/gent-dampoort": [
        "BELOC002376",
    ],
    "https://be.parkindigo.com/nl/car-park/parking-dok-noord": ["10954"],
    "https://stad.gent/nl/loop/mobiliteit-loop#Parkeerterreinen_Stad_Gent": [],
    "https://www.belgiantrain.be/nl/station-information/car-or-bike-at-station/b-parking/my-b-parking/gentstpieters": [
        "BELOC002367",
    ],
}


class RateLimitException(Exception):
    pass


async def get_charging_status(parking_id):
    stations = parking_station_ids.get(parking_id, list())
    async with ClientSession() as session:
        api = Api(session)
        total_connectors = 0
        available_connectors = 0
        for station_id in stations:
            location = await api.location_by_id(station_id)
            if not location:
                raise RateLimitException()
            for evse in location.evses:
                total_connectors += 1
                if evse.status.lower() == "available":
                    available_connectors += 1
        return available_connectors, total_connectors


def fetch_parking_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        raise Exception("Failed to fetch data from API")
