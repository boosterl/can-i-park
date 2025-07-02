import click

from can_i_park.utils import fetch_parking_data, get_charging_status


async def display_parking_data(names, lez, verbose, chargers):
    for parking in fetch_parking_data():
        if names and not any(
            name.lower() in parking.get("name").lower() for name in names
        ):
            continue
        if not lez and "in lez" in parking.get("categorie").lower():
            continue
        click.echo(f"📍 Parking: {parking.get('name')}")
        if parking.get("occupation") < 75:
            click.echo(f"   - Parking is free ✅")
        elif 75 <= parking.get("occupation") < 95:
            click.echo(
                f"   - Parking only has {parking.get('availablecapacity')} places free"
            )
        else:
            click.echo(f"   - Parking is full 🚫")
        display_parking_details(parking, verbose)
        if not chargers:
            continue
        available_connectors, total_connectors = await get_charging_status(
            parking.get("id")
        )
        if total_connectors:
            status_icon = "✅" if available_connectors else "🚫"
            click.echo(
                f"   - {available_connectors}/{total_connectors} connectors are available for charging {status_icon}"
            )
            if verbose > 0:
                click.echo(
                    get_occupation_chart(
                        100 - int(available_connectors / total_connectors * 100)
                    )
                )


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
