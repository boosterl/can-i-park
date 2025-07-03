from aiohttp import ClientSession
from can_i_park.utils import fetch_parking_data, get_charging_status
from prometheus_client import Gauge

import time

# Create Prometheus metrics
total_capacity = Gauge(
    "cip_total_capacity",
    "Total capacity of the parking",
    ["name", "latitude", "longtitude"],
)
available_capacity = Gauge(
    "cip_available_capacity",
    "Available capacity of the parking",
    ["name", "latitude", "longtitude"],
)
occupation = Gauge(
    "cip_occupation",
    "Occupation percentage of the parking",
    ["name", "latitude", "longtitude"],
)
is_open = Gauge(
    "cip_is_open", "Whether the parking is open", ["name", "latitude", "longtitude"]
)
in_lez = Gauge(
    "cip_in_lez",
    "Whether the parking is located inside the LEZ",
    ["name", "latitude", "longtitude"],
)
total_charging_stalls = Gauge(
    "cip_total_charging_stalls",
    "Total amount of charging stalls in parking",
    ["name", "latitude", "longtitude"],
)
available_charging_stalls = Gauge(
    "cip_available_charging_stalls",
    "Available amount of charging stalls in parking",
    ["name", "latitude", "longtitude"],
)


def set_metrics(
    parking, available_charging_stalls_amount, total_charging_stalls_amount
):
    location = parking.get("location")
    total_capacity.labels(
        name=parking.get("name"),
        latitude=location.get("lat"),
        longtitude=location.get("lon"),
    ).set(parking.get("totalcapacity"))
    available_capacity.labels(
        name=parking.get("name"),
        latitude=location.get("lat"),
        longtitude=location.get("lon"),
    ).set(parking.get("availablecapacity"))
    occupation.labels(
        name=parking.get("name"),
        latitude=location.get("lat"),
        longtitude=location.get("lon"),
    ).set(parking.get("occupation"))
    is_open.labels(
        name=parking.get("name"),
        latitude=location.get("lat"),
        longtitude=location.get("lon"),
    ).set(parking.get("isopennow"))
    in_lez.labels(
        name=parking.get("name"),
        latitude=location.get("lat"),
        longtitude=location.get("lon"),
    ).set("in lez" in parking.get("categorie").lower())
    total_charging_stalls.labels(
        name=parking.get("name"),
        latitude=location.get("lat"),
        longtitude=location.get("lon"),
    ).set(total_charging_stalls_amount)
    available_charging_stalls.labels(
        name=parking.get("name"),
        latitude=location.get("lat"),
        longtitude=location.get("lon"),
    ).set(available_charging_stalls_amount)


async def run_metrics_loop(interval):
    async with ClientSession() as session:
        while True:
            for parking in fetch_parking_data():
                available_charging_stalls, total_charging_stalls = (
                    await get_charging_status(parking.get("id"))
                )
                set_metrics(parking, available_charging_stalls, total_charging_stalls)
            time.sleep(interval)
