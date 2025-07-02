import requests

from aiohttp import ClientSession
from shellrecharge import Api, LocationEmptyError, LocationValidationError

API_URL = "https://data.stad.gent/api/explore/v2.1/catalog/datasets/bezetting-parkeergarages-real-time/records?limit=20"
parking_station_ids = {
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-savaanstraat": [
        "BEALLEGO005188"
    ],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-vrijdagmarkt": [
        "BEALLEGO005141",
        "BEALLEGO005138",
    ],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-reep": [
        "BEALLEGO005186",
        "BEALLEGO005146",
        "BEALLEGO005187",
        "BEALLEGO005149",
    ],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-sint-pietersplein": [
        "BEALLEGO005180",
        "BEALLEGO005158",
    ],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-ramen": [
        "BEALLEGO005139",
        "BEALLEGO005135",
    ],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-tolhuis": [
        "BEALLEGO005183",
        "BEALLEGO005142",
    ],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-sint-michiels": [
        "BEALLEGO005151",
        "BEALLEGO005148",
    ],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-ledeberg": [
        "BEALLEGO005136"
    ],
    "https://stad.gent/nl/mobiliteit-openbare-werken/parkeren/parkings-gent/parking-het-getouw": [
        "BEALLEGO005137"
    ],
    "https://www.belgiantrain.be/nl/station-information/car-or-bike-at-station/b-parking/my-b-parking/gent-dampoort": [
        "BEALLEGO004674",
        "BEALLEGO004678",
    ],
    "https://be.parkindigo.com/nl/car-park/parking-dok-noord": ["10954"],
    "https://stad.gent/nl/loop/mobiliteit-loop#Parkeerterreinen_Stad_Gent": [],
    "https://www.belgiantrain.be/nl/station-information/car-or-bike-at-station/b-parking/my-b-parking/gentstpieters": [
        "BEALLEGO004982",
        "BEALLEGO004305",
    ],
}


async def get_charging_status(parking_id):
    stations = parking_station_ids.get(parking_id, list())
    async with ClientSession() as session:
        api = Api(session)
        total_connectors = 0
        available_connectors = 0
        for station_id in stations:
            location = await api.location_by_id(station_id)
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
