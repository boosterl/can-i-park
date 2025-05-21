import click
import requests

API_URL = "https://data.stad.gent/api/explore/v2.1/catalog/datasets/bezetting-parkeergarages-real-time/records?limit=20"

def fetch_parking_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        raise Exception("Failed to fetch data from API")

def display_parking_data(names, lez):
    parkings = fetch_parking_data()
    for parking in parkings:
        if names and not any(name.lower() in parking.get('name').lower() for name in names):
            continue
        if not lez and "in lez" in parking.get('categorie').lower():
            continue
        click.echo(f"📍 Parking: {parking.get('name')}")
        if parking.get('occupation') < 30:
            click.echo(f"   - Parking is free ✅")
        elif 75 <= parking.get('occupation') < 95:
            click.echo(f"   - Parking only has {parking.get('availablecapacity')} places free")
        else:
            click.echo(f"   - Parking is full 🚫")
