import click
import requests

API_URL = "https://data.stad.gent/api/explore/v2.1/catalog/datasets/bezetting-parkeergarages-real-time/records?limit=20"

def fetch_parking_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        raise Exception("Failed to fetch data from API")

def display_parking_data(names, lez, verbose):
    parkings = fetch_parking_data()
    for parking in parkings:
        if names and not any(name.lower() in parking.get('name').lower() for name in names):
            continue
        if not lez and "in lez" in parking.get('categorie').lower():
            continue
        click.echo(f"📍 Parking: {parking.get('name')}")
        if parking.get('occupation') < 75:
            click.echo(f"   - Parking is free ✅")
        elif 75 <= parking.get('occupation') < 95:
            click.echo(f"   - Parking only has {parking.get('availablecapacity')} places free")
        else:
            click.echo(f"   - Parking is full 🚫")
        display_parking_details(parking, verbose)

def display_parking_details(parking, verbose):
    if verbose < 1:
        return
    print(f"     Total capacity: {parking.get('totalcapacity')}")
    print(f"     Available capacity: {parking.get('availablecapacity')}")
    print(f"     Parking in LEZ: {'yes' if 'in lez' in parking.get('categorie').lower() else 'no'}")
    print(f"     Occupation: {parking.get('occupation')}%")
    print(print_occupation_chart(parking.get("occupation")))

def print_occupation_chart(occupation):
    return f"     [{'#' * occupation}{' ' * (100 - occupation)}]"
