import logging
import time

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError
from asyncio import CancelledError
from can_i_park.utils import fetch_parking_data, get_charging_status, RateLimitException
from prometheus_client import Gauge
from random import randrange
from requests.exceptions import ConnectionError
from shellrecharge import LocationEmptyError, LocationValidationError


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
            try:
                parkings = fetch_parking_data()
            except ConnectionError:
                logger.error(
                    "Error connecting to Ghent data API, check your connection"
                )
                time.sleep(interval)
                continue
            for parking in parkings:
                try:
                    available_charging_stalls, total_charging_stalls = (
                        await get_charging_status(parking.get("id"))
                    )
                    set_metrics(
                        parking, available_charging_stalls, total_charging_stalls
                    )
                except (
                    CancelledError,
                    ClientError,
                    LocationEmptyError,
                    LocationValidationError,
                    TimeoutError,
                ):
                    logger.error("There was an issue getting charging status")
                    set_metrics(parking)
                except (RateLimitException):
                    cooldown_period = randrange(30,60)
                    logger.error(f"Rate limit of charging API was probably hit, cooling down for {cooldown_period}s")
                    set_metrics(parking)
                    time.sleep(cooldown_period)
