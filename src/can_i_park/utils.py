import requests

API_URL = "https://data.stad.gent/api/explore/v2.1/catalog/datasets/bezetting-parkeergarages-real-time/records?limit=20"


def fetch_parking_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        raise Exception("Failed to fetch data from API")
