import logging
import time

from aiohttp.client_exceptions import ClientError
from asyncio import CancelledError
from can_i_park.api import StationNotFoundError
from can_i_park.utils import fetch_parking_data, get_charging_status
from prometheus_client import Gauge
from requests.exceptions import ConnectionError


total_capacity = Gauge(
    "cip_total_capacity",
    "Total capacity of the parking",
    ["name", "latitude", "longitude"],
)
available_capacity = Gauge(
    "cip_available_capacity",
    "Available capacity of the parking",
    ["name", "latitude", "longitude"],
)
occupation = Gauge(
    "cip_occupation",
    "Occupation percentage of the parking",
    ["name", "latitude", "longitude"],
)
is_open = Gauge(
    "cip_is_open", "Whether the parking is open", ["name", "latitude", "longitude"]
)
in_lez = Gauge(
    "cip_in_lez",
    "Whether the parking is located inside the LEZ",
    ["name", "latitude", "longitude"],
)
total_charging_stalls = Gauge(
    "cip_total_charging_stalls",
    "Total amount of charging stalls in parking",
    ["name", "latitude", "longitude"],
)
available_charging_stalls = Gauge(
    "cip_available_charging_stalls",
    "Available amount of charging stalls in parking",
    ["name", "latitude", "longitude"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)


def set_metrics(
    parking, available_charging_stalls_amount=0, total_charging_stalls_amount=0
):
    location = parking.get("location")
    total_capacity.labels(
        name=parking.get("name"),
        latitude=location.get("lat"),
        longitude=location.get("lon"),
    ).set(parking.get("totalcapacity"))
    available_capacity.labels(
        name=parking.get("name"),
        latitude=location.get("lat"),
        longitude=location.get("lon"),
    ).set(parking.get("availablecapacity"))
    occupation.labels(
        name=parking.get("name"),
        latitude=location.get("lat"),
        longitude=location.get("lon"),
    ).set(parking.get("occupation"))
    is_open.labels(
        name=parking.get("name"),
        latitude=location.get("lat"),
        longitude=location.get("lon"),
    ).set(parking.get("isopennow"))
    in_lez.labels(
        name=parking.get("name"),
        latitude=location.get("lat"),
        longitude=location.get("lon"),
    ).set("in lez" in parking.get("categorie").lower())
    total_charging_stalls.labels(
        name=parking.get("name"),
        latitude=location.get("lat"),
        longitude=location.get("lon"),
    ).set(total_charging_stalls_amount)
    available_charging_stalls.labels(
        name=parking.get("name"),
        latitude=location.get("lat"),
        longitude=location.get("lon"),
    ).set(available_charging_stalls_amount)


async def run_metrics_loop(interval, api_key):
    while True:
        try:
            parkings = fetch_parking_data()
        except ConnectionError:
            logger.error(
                "Error connecting to Ghent data API, check your connection"
            )
            time.sleep(interval)
            continue
        for parking in parkings:
            if not api_key:
                set_metrics(parking)
                continue
            try:
                available_amount, total_amount = await get_charging_status(
                    parking.get("id"), api_key
                )
                set_metrics(parking, available_amount, total_amount)
            except (
                CancelledError,
                ClientError,
                StationNotFoundError,
                TimeoutError,
            ):
                logger.error("There was an issue getting charging status")
                set_metrics(parking)
        time.sleep(interval)
