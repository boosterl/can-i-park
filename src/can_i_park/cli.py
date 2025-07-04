import click

from aiohttp.client_exceptions import ClientError
from asyncio import CancelledError
from can_i_park.utils import fetch_parking_data, get_charging_status
from requests.exceptions import ConnectionError
from shellrecharge import LocationEmptyError, LocationValidationError


async def display_charging_stall_data(parking, verbose):
    try:
        available_stalls, total_stalls = await get_charging_status(parking.get("id"))
    except (
        CancelledError,
        ClientError,
        LocationEmptyError,
        LocationValidationError,
        TimeoutError,
    ):
        click.echo(
            f"Something went wrong fetching charging information for {parking.get('name')}",
            err=True,
        )
        return
    if total_stalls:
        status_icon = "✅" if available_stalls else "🚫"
        click.echo(
            f"   - {available_stalls}/{total_stalls} stalls are available for charging {status_icon}"
        )
        if verbose > 0:
            click.echo(
                get_occupation_chart(100 - int(available_stalls / total_stalls * 100))
            )


async def display_parking_data(names, lez, verbose, chargers):
    try:
        parkings = fetch_parking_data()
    except ConnectionError:
        click.echo(
            "Error connecting to Ghent data API, check your connection", err=True
        )
        return
    except Exception:
        click.echo("Something else went wrong while connecting to the API", err=True)
        return
    for parking in parkings:
        if not display_basic_parking_data(parking, names, lez):
            continue
        display_parking_details(parking, verbose)
        if not chargers:
            continue
        await display_charging_stall_data(parking, verbose)


def display_basic_parking_data(parking, names, lez):
    if names and not any(name.lower() in parking.get("name").lower() for name in names):
        return None
    if not lez and "in lez" in parking.get("categorie").lower():
        return None
    click.echo(f"📍 Parking: {parking.get('name')}")
    if parking.get("occupation") < 75:
        click.echo(f"   - Parking is free ✅")
    elif 75 <= parking.get("occupation") < 95:
        click.echo(
            f"   - Parking only has {parking.get('availablecapacity')} places free"
        )
    else:
        click.echo(f"   - Parking is full 🚫")
    return parking


def display_parking_details(parking, verbose):
    if verbose < 1:
        return
    print(f"     Total capacity: {parking.get('totalcapacity')}")
    print(f"     Available capacity: {parking.get('availablecapacity')}")
    print(
        f"     Parking in LEZ: {'yes' if 'in lez' in parking.get('categorie').lower() else 'no'}"
    )
    print(f"     Occupation: {parking.get('occupation')}%")
    print(get_occupation_chart(parking.get("occupation")))


def get_occupation_chart(occupation):
    return f"     [{'#' * occupation}{' ' * (100 - occupation)}]"
